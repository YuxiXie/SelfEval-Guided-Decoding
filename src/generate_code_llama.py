import os
import argparse
from time import sleep
from datetime import datetime

import torch
from transformers import GenerationConfig

from utils.tool import *
from utils.prompt import *
from utils.dataset import jsonlines_load

from utils.Beam import Beam


def parse_args():
    '''
        Parse Arguments
    '''
    parser = argparse.ArgumentParser()
    ##=== input data ===##
    parser.add_argument("--model_name", default='meta-llama/Llama-2-70b-hf', type=str)
    parser.add_argument("--auth_token", default="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", type=str)
    parser.add_argument("--dt_name", required=True, type=str,
                        choices=[
                            'gsm8k', 'aqua', 'svamp', 'asdiv', 'mawps', 'tabmwp', 'finqa',
                            'object_counting', 'repeat_copy', 'colored_object', 'penguin',
                            'date_understanding', 'sports', 'csqa', 'saycan', 'strategyqa',
                            'gsm8k_cot',
                        ], 
                        help='the dataset to test')
    parser.add_argument("--input_file", required=True, type=str, help='input data file to generate code')
    parser.add_argument("--output_dir", required=True, type=str, help='directory to save output results')
    parser.add_argument("--start", default=0, type=int)
    parser.add_argument("--end", default=-1, type=int)
    ##=== prompting hyperparameters ===##
    parser.add_argument("--temperature", default=0.5, type=float)
    parser.add_argument("--max_tokens", default=256, type=int)
    parser.add_argument("--top_p", default=1, type=int)
    parser.add_argument("--n_samples", default=16, type=int, help='value of n for code generation sampling')
    parser.add_argument("--logprobs", default=1, type=int)
    parser.add_argument("--mini_n_samples", default=8, type=int, help='value of n for mini code generation sampling (when token rate is limited)')
    parser.add_argument("--mini_n_samples_eval", default=4, type=int, help='value of n for mini batch size for evaluation')
    parser.add_argument("--sleep_time", default=5, type=int)
    parser.add_argument("--max_stuck_time", default=30, type=int)
    ##=== running settings ===##
    parser.add_argument("--eval_13b", default=False, action='store_true')
    parser.add_argument("--reverse", default=False, action='store_true')
    parser.add_argument("--verbal", default=False, action='store_true')
    parser.add_argument("--resume", default=False, action='store_true')
    parser.add_argument("--resume_dt_string", default="", type=str)
    ##=== beam search ===##
    parser.add_argument("--beam_size", default=5, type=int)
    parser.add_argument("--bs_temperature", default=0.0, type=float)
    parser.add_argument("--bs_temperature_decay", default=-1.0, type=float)
    parser.add_argument("--reject_sample", default=False, action='store_true')
    parser.add_argument("--unbiased", default=False, action='store_true')
    parser.add_argument("--bs_min_score", default=0.6, type=float)
    parser.add_argument("--not_use_logprob", default=False, action='store_true')
    parser.add_argument("--not_use_conf", default=False, action='store_true')
    parser.add_argument("--conf_ratio", default=0, type=float)
    parser.add_argument("--beam_search_max_step", default=16, type=int)
    
    args = parser.parse_args()
    
    args.prompts = get_prompts(args.dt_name)
    
    return args


@torch.no_grad()
def get_generations(model, tokenizer, input_ids, attention_mask, generation_config):
    sequences = model.generate(
        input_ids=input_ids.to(model.device),
        attention_mask=attention_mask.to(model.device),
        generation_config=generation_config,
        output_scores=True, 
        return_dict_in_generate=True,
    )
    
    sequences, scores = sequences.sequences.cpu(), sequences.scores
    scores = torch.stack(scores, dim=0).transpose(0, 1).cpu()
    sequences = (
        sequences.contiguous()
        .view(
            input_ids.size(0),
            generation_config.num_return_sequences,
            -1,
        )
        .transpose(0, 1)
    )
    
    if sequences.size(1) == 1:
        texts = tokenizer.batch_decode(sequences[:, 0, input_ids.size(-1):], skip_special_tokens=True)
        sequence_ids = sequences[:, 0, :]
    elif sequences.size(0) == 1:
        texts = tokenizer.batch_decode(sequences[0, :, input_ids.size(-1):], skip_special_tokens=True)
        sequence_ids = sequences[0, :, :]
    
    result = []
    for text, ids, _scores in zip(texts, sequence_ids, scores):
        gen_ids = ids[input_ids.size(-1):]
        tokens = [x.replace('▁', ' ').replace('<0x0A>', '\n') for x in tokenizer.convert_ids_to_tokens(gen_ids)]
        g = {
            'text': text, 
            'logprobs': {
                'tokens': tokens,
                'token_logprobs': gather_log_probabilities(_scores, gen_ids).tolist(),
            }
        }
        if sequences.size(0) == 1:
            g['logprobs']['top_logprobs'] = []
            log_probs = F.log_softmax(_scores.float(), dim=-1)
            for logprobs in log_probs:
                topk_logprobs, topk_ids = logprobs.topk(5)
                topk_tokens = tokenizer.batch_decode(
                    topk_ids.unsqueeze(1), skip_special_tokens=True,
                )
                g['logprobs']['top_logprobs'].append({tok: lp for tok, lp in zip(topk_tokens, topk_logprobs.tolist())})
        result.append(g)
    
    return result


def prompt_the_result(args, prompt, n=1):
    _inputs = args.tokenizer(prompt, return_tensors="pt")
    prompts, attn_masks = _inputs.input_ids, _inputs.attention_mask
    
    results = []
    while len(results) < n:
        results.extend(get_generations(args.model, args.tokenizer, 
                                       prompts, attn_masks, 
                                       args.generation_config))
    return {'choices': results}


def get_confidence(args, prompt):
    _inputs = args.tokenizer(prompt, return_tensors="pt", padding=True)
    prompts, attn_masks = _inputs.input_ids, _inputs.attention_mask
    
    results, idx = [], 0
    mini_n_samples = args.mini_n_samples_eval
    while len(results) < len(prompts):
        torch.cuda.empty_cache()
        prpt = prompts[idx * mini_n_samples: (idx + 1) * mini_n_samples, :]
        attn_msk = attn_masks[idx * mini_n_samples: (idx + 1) * mini_n_samples, :]
        results.extend(get_generations(
            args.eval_model, args.eval_tokenizer, prpt, attn_msk, args.evaluation_config
        ))
        idx += 1
    scores, comments = extract_confidence_score({'choices': results})
    return scores, comments


def get_line_confidence(args, prefix, code_list, step, use_batch=False):
    
    def _generate_prompt(cur_code, i=-1):
        _step = step if (i < 0 and not isinstance(step, list)) else step[i]
        blk = cur_code[_step - 1]
        blk_lastline = regex.split(r'[\n]+', blk.rstrip())[-1]
        indent = ' ' * blk_lastline.index(blk_lastline.strip())
        cur_code[_step - 1] += '\n{}{}'.format(indent, f'\n{indent}'.join(args.prompts['choice_prefix']))
        return prefix + '\n'.join(cur_code[:_step])

    if use_batch:
        prompt = []
        for i, cdl in enumerate(code_list):
            prompt.append(_generate_prompt(deepcopy(cdl), i=i))
    else:
        prompt = _generate_prompt(deepcopy(code_list))
    
    scores, comments = [], []
    while not (len(scores) * len(comments)):
        scores, comments = get_confidence(args, prompt)
    
    return scores, comments


def generate_one_step(_input):
    '''
        Generate one step of beam searching
        [input] 
            - args: arguments
            - init_instance
            - num_of_lines
            - prefix, prompt
            - n
        [output]
            - prd: predicted step
            - prd_p, prd_c: confidence scores
            - ill: is last line? (bool)
            - full_prd
            - cmt
            - raw_results
    '''
    args, init_instance, num_of_lines, prefix, prompt, n = _input
    ins, finished, _ = init_instance
    
    if finished:
        return (
            # preds, pred_probs, pred_confs, is_last_line, full_preds, comments, raw_result
            [None], [(1, 0)], [1], [True], [None], [None], [],
        )
    
    prd, prd_p, prd_c, ill, full_prd, cmt = [], [], [], [], [], []
    ##=== sampling to get the generated codes ===##
    if len(ins) and args.verbal:
        print(' [init code]\n{}'.format('\n'.join(ins)))
    
    unique_result, raw_results = defaultdict(list), []
    while not len(unique_result):
        input_prompt = f'{prompt}' + ('\n'.join(ins) + '\n' if ins else '')
        raw_result = prompt_the_result(args, input_prompt, 
                                       n=max(1, n - len(unique_result)))
        result = parse_api_result(raw_result, llama=True)
        # remove the duplicate code
        for rst in result:
            code, _, _probs = rst
            n_code_steps = len(regex.split(r'[\n]+', code.rstrip()))
            if not (n_code_steps * len(_probs)) or n_code_steps > len(_probs):
                continue
            lines, probs = split_code_with_probs(code, _probs, not_code=(args.prompts['type'] == 'commonsense'))
            if not (len(lines) * len(probs)):
                continue
            raw_results.append((lines, probs))
            if lines[0].strip():
                unique_result[lines[0]].append((lines, probs))
    
    ##=== get ready the predictions ===##
    code_list_batch = [(ins + [k]) for k in unique_result]
    # get the confidence score in a batch
    confs, comments = get_line_confidence(args, prefix, code_list_batch, [num_of_lines] * len(code_list_batch), use_batch=True)
    conf_results = {}
    for k, conf, comment in zip(unique_result.keys(), confs, comments):
        conf_results[k] = (conf, comment)
    
    for k, v in unique_result.items():
        # get the confidence score
        conf, comment = conf_results[k]
        # pack the results
        if args.bs_temperature == 0: random.shuffle(v)
        for l, p in v:
            prd.append(k)
            prd_p.append(p[0])
            
            is_end = not ''.join(l[1:]).strip()
            is_return = is_end or l[1].split('#')[0].rstrip() == '    return result'
            ill.append(is_end or is_return)
            if is_end: l, p = l[:1], p[:1]
                
            prd_c.append(conf)
            cmt.append(comment)
            full_prd.append((l, p, conf, comment, num_of_lines))    # (lines, probs, conf, comment, step)
            # only pick one of the duplicate codes (PS: duplicate version doesn't work -> UPDATE: work when unbiased)
            if args.bs_temperature == 0: break
    
    for i, rst in enumerate(raw_results):
        k = rst[0][0]
        raw_results[i] = raw_results[i] + conf_results.get(k, [])
    
    return (prd, prd_p, prd_c, ill, full_prd, cmt, raw_results,)


def generate_code_beam_search(args, exp):
    '''
        Beam Searching
    '''
    start_time = time()
    
    ### ==================== Prepare Prompt ==================== ###
    prompt, prefix = get_prompt_inputs(args.dt_name, args.prompts, exp)
    if args.prompts['type'] not in ['commonsense']:
        start_of_solution = f'def solution():\n    """{exp["question"]}"""\n'
    else:
        start_of_solution = ''
    prompt, prefix = prompt + start_of_solution, prefix + start_of_solution
    
    ### ==================== Beam Searching ==================== ###
    all_generated_codes = {}
    code_gen_beam = Beam(args.beam_size, args.conf_ratio, 
                         temperature=args.bs_temperature, temperature_decay=args.bs_temperature_decay, 
                         reject_sample=args.reject_sample, min_score=args.bs_min_score, 
                         unbiased=args.unbiased)
    for num_of_lines in range(1, args.beam_search_max_step + 1):
        init_instances = code_gen_beam.get_current_state(return_expl=True)
        if args.verbal:
            print('Beam Search: step {} - {}/{} activate instances'.format(num_of_lines,
                                                                           len([x for x in init_instances if not x[1]]),
                                                                           len(init_instances)))
        
        preds, pred_probs, pred_confs, is_last_line, full_preds, comments = [], [], [], [], [], []
        num_ins = len(init_instances)
        n = args.n_samples if num_ins * args.n_samples > args.beam_size else (args.beam_size * 2 // num_ins)  # TODO: magic number
        
        pred_rst = []
        for init_instance in init_instances:
            pred_rst.append(generate_one_step((
                args, init_instance, num_of_lines, prefix, prompt, n
            )))
        
        all_generated_codes[num_of_lines], _idx_ins = [], 0
        for prd, prd_p, prd_c, ill, full_prd, cmt, raw_rst in pred_rst:
            preds.append(prd)
            pred_probs.append(prd_p)
            pred_confs.append(prd_c)
            is_last_line.append(ill)
            full_preds.append(full_prd)
            comments.append(cmt)
            all_generated_codes[num_of_lines].append({'init': init_instances[_idx_ins][0], 'rest': raw_rst})
            _idx_ins += 1
        
        done = code_gen_beam.advance(preds, pred_probs, pred_confs, 
                                     is_last_line, expl=comments)
        if done: break
    
    ### ==================== Pack the Results ==================== ###
    to_return = []
    instances = code_gen_beam.get_current_state(return_expl=True)
    ins_scores = code_gen_beam.get_step_scores()
    for idx, ins in enumerate(instances):
        ins, finished, cmt = ins
        
        rest_code = []
        if not finished or (not ins[-1].startswith('    return ') and args.prompts['type'] not in ['commonsense']):
            i, j = code_gen_beam.all_traces[-1][idx]
            try:
                rest_code = full_preds[i][j][0][1:]
            except:
                if args.prompts['type'] not in ['commonsense']:
                    rest_code = ['    return result']
        
        length = code_gen_beam.all_length[-1][idx]
        scores = ins_scores[idx]
        to_return.append({
            'finished': finished, 'length': length,
            'score': [s[0] for s in scores], 'conf': [s[1] for s in scores], 'prob': [s[2] for s in scores],
            'generated': ins + rest_code,
            'conf_comments': cmt, 'info': None if finished else full_preds[i][j][1:],
        })
    
    if not to_return:
        print(f'*** None return at index {index}')
    
    dur = time() - start_time
    return to_return, dur, {k:[] for k in all_generated_codes}


if __name__ == "__main__":
    args = parse_args()
    
    ### ==================== Load Input Data ==================== ###
    data_test = jsonlines_load(args.input_file)
    for i, _ in enumerate(data_test):
        data_test[i]['index'] = i

    ### ==================== Prepare Output Filename ==================== ###
    if args.resume:
        dt_string = args.resume_dt_string
    else:
        now = datetime.now()
        dt_string = now.strftime("%m_%d_%H_%M")

    args.end = len(data_test) if args.end == -1 else args.end + 1
    data_test = data_test[args.start:args.end]
    print('Number of Examples: ', len(data_test))
    
    mtype = 'llama2'
    if args.model_name.count('7b'):
        mtype += '-7b'
    elif args.model_name.count('13b'):
        mtype += '-13b'
    elif args.model_name.count('70b'):
        mtype += '-70b'
    else:
        raise ValueError("The specified model does not exist.")
    
    nop = '_nop' if args.not_use_logprob else ''
    noc = '_noc' if args.not_use_conf else ''
    rjsbs = '_rjs' if args.reject_sample else ''
    bs = f'_bs{args.beam_size}' if args.beam_size != 5 else ''
    bstp = f'_bstp{args.bs_temperature}' if args.bs_temperature else ''
    bstp += f'_decay{args.bs_temperature_decay}' if bstp and args.bs_temperature_decay >= 0 else ''
    fn_prefix = f'{args.output_dir}/{args.dt_name}_{mtype}_sebs{rjsbs}_mc_pal{bs}{bstp}{nop}{noc}_tp{args.temperature}_n{args.n_samples}_s{args.start}_e{args.end}_{dt_string}'
    if args.not_use_logprob:
        args.conf_ratio = math.inf
    if args.not_use_conf:
        args.conf_ratio = -math.inf
    assert not (args.not_use_logprob and args.not_use_conf), "cannot discard logprob & confidence scores at the same time"
    
    ### ==================== Run Generation ==================== ###
    if args.eval_13b:
        fn_prefix += '_ev13b'
    if args.reverse:
        filename = f'{fn_prefix}_reverse.jsonl'
    else:
        filename = f'{fn_prefix}.jsonl'
    
    prev_indexes = []
    if not os.path.exists(filename):
        with jsonlines.open(filename, mode='w') as writer:
            writer.write(args.prompts)
    else:
        prev = jsonlines_load(filename)
        prev_indexes += [x['index'] for x in prev if 'index' in x]
    
    inputs = []
    for example in tqdm(data_test):
        index = example['index']
        if index in prev_indexes: continue
        rst = {'index': index}
        rst.update(example)
        
        inputs.append(rst)
    
    args.model, args.tokenizer = load_llama_model_and_tokenizer(args.model_name, args.auth_token)
    if args.eval_13b:
        args.eval_model, args.eval_tokenizer = load_llama_model_and_tokenizer("meta-llama/Llama-2-13b-hf", args.auth_token)
    else:
        args.eval_model, args.eval_tokenizer = args.model, args.tokenizer
    
    args.generation_config = GenerationConfig(
        max_new_tokens=args.max_tokens,
        num_return_sequences=args.mini_n_samples,
        temperature=args.temperature,
        top_p=args.top_p,
        do_sample=args.temperature > 0,
        bos_token_id=args.tokenizer.bos_token_id,
        eos_token_id=args.tokenizer.eos_token_id,
        pad_token_id=args.tokenizer.pad_token_id,
    )
    args.evaluation_config = GenerationConfig(
        max_new_tokens=8,   # TODO: magic number
        num_return_sequences=1,
        temperature=0.0,
        top_p=1.0,
        do_sample=False,
        bos_token_id=args.tokenizer.bos_token_id,
        eos_token_id=args.tokenizer.eos_token_id,
        pad_token_id=args.tokenizer.pad_token_id,
    )
    
    inputs = inputs[::-1] if args.reverse else inputs
    
    for example in tqdm(inputs):
        result, dur, all_candidates = generate_code_beam_search(args, example)
        example.update({
            'generated': result, 'all_generated': all_candidates, 'run_time': dur
        })
        with jsonlines.open(filename, mode='a') as writer:
            writer.write(example)
        torch.cuda.empty_cache()
    
    print('All Done.')
