import sys
import openai
from concurrent.futures import ProcessPoolExecutor as Pool
from tenacity import wait_random_exponential, stop_after_attempt, retry

sys.path.append('/home/yuxi/Projects/SelfEval-Guided-Decoding/src')
from utils.tool import *
from utils.dataset import jsonlines_load, jsonlines_dump
from prompts.aqua import choice_prompt
from execute_and_evaluate.interpret_and_evaluate import cal_weight

from transformers import GenerationConfig


def check_eq(p, g):
    return p == g


def generate_prompt(qu, options, prediction):
    prompt = f'{choice_prompt}\nQuestion: {qu}\nAnswer Choices:\n{options}\nPrediction: {prediction}\nClosest Option:'
    return prompt


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


def llama_make_choice(prompt, model, tokenizer, generation_config):
    _inputs = tokenizer(prompt, return_tensors="pt")
    prompts, attn_masks = _inputs.input_ids, _inputs.attention_mask
    results = get_generations(model, tokenizer, prompts, attn_masks, generation_config)
    return {'choices': results}


def select_option(examples, model=None, tokenizer=None, generation_config=None):    
    exp_id = -1
    for example in tqdm(examples):
        exp_id += 1
        if example.get('executed_results', None) is None or len(example['executed_results']) <= len(example['generated']):
            saved = list(example.get('executed_results', {}).keys())
            candidates = []
            for g_id, g in enumerate(example['generated']):
                if isinstance(g, str):
                    code = g
                elif isinstance(g, list):
                    code = g[0]
                else:
                    if not g['generated'][0].startswith('def solution():\n'):
                        g['generated'][0] = 'def solution():\n' + g['generated'][0]
                    code = '\n'.join(g['generated'])
                if code not in candidates + saved:
                    candidates.append(code)

            candidate_results = {c: {} for c in candidates}
            qu, options = example['question'], '\n'.join(example['options'])
            for code in candidate_results:
                prediction = simplify_ans(safe_execute(code))
                prediction = 'None' if prediction is None else prediction
                
                prompt = generate_prompt(qu, options, prediction)
                rst = llama_make_choice(prompt, model, tokenizer, generation_config)
                selected = rst['choices'][0]['text'].strip().split()[0].strip()
                
                candidate_results[code] = {'predict': prediction, 'select': selected}
            
            if len(saved):
                if len(candidate_results):
                    examples[exp_id]['executed_results'].update(candidate_results)
            else:
                examples[exp_id]['executed_results'] = candidate_results
            
    return examples


if __name__ == '__main__':
    fname = sys.argv[1]
    data = jsonlines_load(fname)
    
    prompts, data = data[0], data[1:]
    
    model, tokenizer = load_llama_model_and_tokenizer("meta-llama/Llama-2-13b-hf", "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")   
    generation_config = GenerationConfig(
        max_new_tokens=8,
        num_return_sequences=1,
        temperature=0.0,
        top_p=1.0,
        do_sample=False,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    ) 
    data = select_option(data, model, tokenizer, generation_config)
    
    accu, accu_all = {}, {}
    
    for d in tqdm(data):
        idx = d['index']
        gt_ans = d['correct'].strip()
        executed_results = d['executed_results']

        if d.get('executed', None) is not None and isinstance(d['generated'][0], list) \
            and isinstance(d['executed'], list) and d['executed'][0] is not None:
            selected = d['executed'][1]
            answers = [selected]
            ans = answers[0]
        else:
            answers, weights, predictions = [], [], []
            candidates = []
            
            for g_id, g in enumerate(d['generated']):
                if isinstance(g, str):
                    code = g
                elif isinstance(g, list):
                    code = g[0]
                else:
                    code = '\n'.join(g['generated'])
                candidates.append(code)
                
                executed = executed_results[code]
                prd, selected = executed['predict'], executed['select']
                
                answers.append(selected)
                predictions.append(prd)
            
            anss, prds = answers, predictions
            
            result_counter = Counter()
            result_counter.update([x for x, y in zip(anss, prds) if y != 'None'])
            ans = result_counter.most_common(1)[0][0] if len(result_counter) else None
            prd = prds[anss.index(ans)] if ans is not None else None
            d['executed'] = (prd, ans)
        
        accu[idx] = check_eq(answers[0], gt_ans)
        accu_all[idx] = check_eq(ans, gt_ans)
    
    print('accu ({}):'.format(len(accu)), sum(accu.values())/len(accu))
    print('accu_all:', sum(accu_all.values())/len(accu_all))
    
    jsonlines_dump([prompts] + data, fname)
    
    