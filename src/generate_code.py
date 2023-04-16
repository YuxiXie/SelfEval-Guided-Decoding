import os
import argparse
from time import sleep
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor as Pool

from utils.tool import *
from utils.prompt import *
from utils.generate import prompt_the_result
from utils.self_evaluate import get_line_confidence
from utils.dataset import jsonlines_load, merge_parallel_results

from utils.Beam import Beam


def parse_args():
    parser = argparse.ArgumentParser()
    ##=== input data ===##
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
    parser.add_argument("--key", default="OPENAI_KEY", type=str)
    parser.add_argument("--keys", default=[], nargs='+', type=str)
    parser.add_argument("--temperature", default=0.5, type=float)
    parser.add_argument("--max_tokens", default=256, type=int)
    parser.add_argument("--top_p", default=1, type=int)
    parser.add_argument("--n_samples", default=16, type=int, help='value of n for code generation sampling')
    parser.add_argument("--logprobs", default=1, type=int)
    parser.add_argument("--use_mini_n", default=False, action='store_true')
    parser.add_argument("--mini_n_samples", default=8, type=int, help='value of n for mini code generation sampling (when token rate is limited)')
    parser.add_argument("--sleep_time", default=5, type=int)
    parser.add_argument("--max_stuck_time", default=30, type=int)
    ##=== running settings ===##
    parser.add_argument("--chatgpt", default=False, action='store_true')    # TODO: always False
    parser.add_argument("--verbal", default=False, action='store_true')
    parser.add_argument("--parallel_on_sub", default=False, action='store_true')
    parser.add_argument("--parallel", default=False, action='store_true')
    parser.add_argument("--n_jobs", default=20, type=int, help='number of jobs in parallel')
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
    
    if not len(args.keys):
        args.keys = [args.key]
    num_key = len(args.keys)
    if args.parallel and num_key >= args.n_jobs:
        num_key = args.n_jobs * (num_key // args.n_jobs)
        args.keys = random.sample(args.keys, min(len(args.keys), num_key))
    else:
        args.keys = [args.key]
    print('({} keys in total).'.format(len(args.keys)))
    args.keys_used = {k: None for k in args.keys}
    
    args.prompts = get_prompts(args.dt_name)
    
    assert not args.chatgpt, "chatGPT is not supported for self-evaluation"
    
    return args


def generate_one_step(_input):
    args, init_instance, keys, num_of_lines, prefix, prompt, n = _input
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
        raw_result = prompt_the_result(args, f'{prompt}' + ('\n'.join(ins) + '\n' if ins else ''), 
                                       temperature=args.temperature, n=max(1, n - len(unique_result)), 
                                       max_tokens=args.max_tokens if ((num_of_lines == 1 and args.max_tokens >= 200) or args.max_tokens <= 128) else (args.max_tokens // 2), # not necessary to be too long for a following line
                                       top_p=args.top_p, logprobs=args.logprobs, key=keys[0])
        result = parse_api_result(raw_result)
        # remove the duplicate code
        for rst in result:
            code, _, _probs = rst
            n_code_steps = len(regex.split(r'[\n]+', code.rstrip()))
            if not (n_code_steps * len(_probs)) or n_code_steps > len(_probs):
                if not args.parallel: set_trace()
                continue
            lines, probs = split_code_with_probs(code, _probs, not_code=(args.prompts['type'] == 'commonsense'))
            if not (len(lines) * len(probs)):
                if not args.parallel: set_trace()
                continue
            raw_results.append((lines, probs))
            if lines[0].strip():
                unique_result[lines[0]].append((lines, probs))
    
    ##=== get ready the predictions ===##
    code_list_batch = [(ins + [k]) for k in unique_result]
    # get the confidence score in a batch
    confs, comments = get_line_confidence(args, prefix, code_list_batch, [num_of_lines] * len(code_list_batch), keys[1], use_batch=True)
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


def generate_code_beam_search(args, example, key=KEYS, index=-1):
    start_time = time()
    
    ### ==================== Prepare Prompt ==================== ###
    qu = example["question"]
    prompt, prefix = get_prompt_inputs(args.dt_name, args.prompts, example)
    
    if args.verbal:
        print('====================')
        print(f'Index: {index}\nQuestion: {qu}')
    
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
        # if args.parallel and num_ins > 1 and args.beam_size <= len(key):
        if num_ins > 1 and args.beam_size <= len(key):
            random.shuffle(key)
            key_per_p = len(key) // num_ins
            with Pool(num_ins) as subpool:
                pred_rst = subpool.map(generate_one_step, zip(
                    [args] * num_ins, init_instances,
                    [split_keys(key[i*key_per_p:(i+1)*key_per_p]) for i in range(num_ins)],
                    [num_of_lines] * num_ins, [prefix] * num_ins, [prompt] * num_ins, [n] * num_ins
                ))
        else:
            pred_rst = []
            for init_instance in init_instances:
                pred_rst.append(generate_one_step((
                    args, init_instance, split_keys(key), num_of_lines, prefix, prompt, n
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


def main(argv):
    args, examples, key, fname, sid = argv
    
    prev_indexes = []
    if os.path.exists(fname):
        processed = jsonlines_load(fname)
        prev_indexes += [x['index'] for x in processed if 'index' in x]
    
    idx = sid
    for example in tqdm(examples, desc=f'  - (example {sid} starts) -  '):
        idx = example['index']
        if idx in prev_indexes: continue
        data = {'index': idx}
        data.update(example)
            
        result, dur, all_candidates = generate_code_beam_search(args, example, key=key, index=idx)
        data.update({
            'generated': result, 'all_generated': all_candidates, 'run_time': dur
        })
        with jsonlines.open(fname, mode='a') as writer:
            writer.write(data)
    
    for k in key: args.keys_used[k] = time()
    
    print(f'Examples {sid} to {idx} done.')


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
    
    nop = '_nop' if args.not_use_logprob else ''
    noc = '_noc' if args.not_use_conf else '' 
    rjsbs = '_rjs' if args.reject_sample else ''
    bs = f'_bs{args.beam_size}' if args.beam_size != 5 else ''
    bstp = f'_bstp{args.bs_temperature}' if args.bs_temperature else ''
    bstp += f'_decay{args.bs_temperature_decay}' if bstp and args.bs_temperature_decay >= 0 else ''
    fn_prefix = f'{args.output_dir}/{args.dt_name}_sebs{rjsbs}_mc_pal{bs}{bstp}{nop}{noc}_tp{args.temperature}_n{args.n_samples}_s{args.start}_e{args.end}_{dt_string}'
    if args.not_use_logprob:
        args.conf_ratio = math.inf
    if args.not_use_conf:
        args.conf_ratio = -math.inf
    assert not (args.not_use_logprob and args.not_use_conf), "cannot discard logprob & confidence scores at the same time"
    
    ### ==================== Run Generation ==================== ###
    if args.parallel_on_sub:
        merge_parallel_results(fn_prefix, 100)   # TODO: magic number
        sleep(args.sleep_time)
        if os.path.exists(f'{fn_prefix}.jsonl'):
            prev = jsonlines_load(f'{fn_prefix}.jsonl')
            _indexes = [x['index'] for x in prev if 'index' in x]
            data_test = [x for x in data_test if x['index'] not in _indexes]
            fn_prefix += '_sub'
    
    if args.parallel:
        fname1 = f'{fn_prefix}_parallel_split0.jsonl'
        if not os.path.exists(fname1):
            with jsonlines.open(fname1, mode='w') as writer:
                writer.write(args.prompts)
        
        args_list = [args] * args.n_jobs
        examples_list, fname_list, sid_list, key_list = [], [], [], []
        interval = (len(data_test) + args.n_jobs - 1) // args.n_jobs
        k_interval = len(args.keys) // args.n_jobs
        for i in range(args.n_jobs):
            sid = i * interval
            examples_list.append(data_test[sid: sid + interval])
            fname_list.append(f'{fn_prefix}_parallel_split{i}.jsonl')
            sid_list.append(sid + args.start)
            key_list.append(args.keys[i * k_interval: (i + 1) * k_interval])
        
        with Pool(args.n_jobs) as pool:
            results = pool.map(main, zip(args_list, examples_list, key_list, fname_list, sid_list))

        print('Finished parallel running... {} results in total.'.format(len(list(results))))
        sleep(args.sleep_time)
        print('Merging result files...')
        merge_parallel_results(fn_prefix, args.n_jobs)
    else:
        filename = f'{fn_prefix}.jsonl'
        
        prev_indexes = []
        if not os.path.exists(filename):
            with jsonlines.open(filename, mode='w') as writer:
                writer.write(args.prompts)
        else:
            prev = jsonlines_load(filename)
            prev_indexes += [x['index'] for x in prev if 'index' in x]
        
        highest_s = []
        for example in tqdm(data_test, desc=f'  - (example {args.start} starts) -  '):
            idx = example['index']
            if idx in prev_indexes: continue
            data = {'index': idx}
            data.update(example)
            
            result, dur, all_candidates = generate_code_beam_search(args, example, key=args.keys, index=idx)
            data.update({
                'generated': result, 'all_generated': all_candidates, 'run_time': dur
            })
            with jsonlines.open(filename, mode='a') as writer:
                writer.write(data)
            
            highest_s.append(nor_prod(result[0]['score']))
            print('')
            print('*** Avg Highest Score:', sum(highest_s) / len(highest_s))
            
    print('All Done.')
