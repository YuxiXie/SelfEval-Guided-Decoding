import regex
import random
import openai
from copy import deepcopy
from time import sleep, time
from tenacity import wait_random_exponential, stop_after_attempt, retry

from .tool import select_key, extract_confidence_score, ERRORS


@retry(wait=wait_random_exponential(min=5, max=1000), stop=stop_after_attempt(128))
def _evaluate_code(args, prefix, suffix=None, max_tokens=64, temperature=0.0, 
                   top_p=1, n=1, logprobs=5, key=[]):
    st = time()
    rst = openai.Completion.create(
        engine='code-davinci-002',
        prompt=prefix,
        api_key=select_key(args.keys_used, key, all_keys=args.keys),
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stop=['\n'],
        logprobs=logprobs,
    )
    dur = time() - st
    if args.verbal: print(f'@self_evaluate_code: {dur} seconds')
    return rst
    

def openai_prompt_eval_once(args, prefix, suffix=None, max_tokens=64, temperature=0.0, top_p=1, n=1, 
                            logprobs=5, key=[], min_to_wait=3, max_to_wait=10):
    start_time = time()
    result, cost = None, args.sleep_time
    
    try:
        result = _evaluate_code(args, prefix, suffix=suffix, max_tokens=max_tokens, temperature=temperature, 
                                top_p=top_p, n=n, logprobs=logprobs, key=key)
        cost = time() - start_time
    except Exception as e:
        if args.verbal or all(x not in str(e) for x in ERRORS):
            print(f'***conf API error***', str(e))
        sleep(args.sleep_time)
    
    dur = time() - start_time
    to_wait = min(args.sleep_time, int(cost * 5 + 1))
    if to_wait < min_to_wait: to_wait = random.uniform(to_wait, max_to_wait)
    sleep_time = to_wait - int(dur) if dur < to_wait - min_to_wait \
        else random.uniform(min_to_wait, max(min_to_wait + 1, args.sleep_time))
    if args.verbal: print(f'@self-evaluation: {cost} seconds (+ sleep {sleep_time} seconds)')
    sleep(sleep_time)
        
    return result


def get_confidence(args, prefix, suffix=None, max_tokens=64, temperature=0.0, 
                   top_p=1, n=1, logprobs=5, key=[]):
    got_result = False
    start_time = time()
    
    while not got_result and not args.use_mini_n:
        if time() - start_time > args.max_stuck_time: break
        result = openai_prompt_eval_once(args, prefix, suffix=suffix, max_tokens=max_tokens, temperature=temperature, 
                                         top_p=top_p, n=n, logprobs=logprobs, key=key)
        if result is not None: got_result = True
    
    results = []
    if not got_result and args.use_mini_n and isinstance(prefix, list):
        mini_n_samples = args.mini_n_samples if args.mini_n_samples <= 32 else (args.mini_n_samples // 2)
        n_step = (len(prefix) + mini_n_samples - 1) // mini_n_samples
        _ns = [mini_n_samples] * (n_step - 1) + [len(prefix) - mini_n_samples * (n_step - 1)]
        for _i in range(len(_ns)):
            sidx, eidx = sum(_ns[:_i]), sum(_ns[:_i + 1])
            start_time = time()
            _got_result = False
            while not _got_result:
                if time() - start_time > args.max_stuck_time: break
                result = openai_prompt_eval_once(args, prefix[sidx:eidx], max_tokens=max_tokens, 
                                                 temperature=temperature, top_p=top_p, n=n, 
                                                 logprobs=logprobs, key=key)
                if result is not None: got_result = True
            if not _got_result:
                for ii in range(sidx, eidx):
                    _got_result = False
                    while not got_result:
                        result = openai_prompt_eval_once(args, prefix[ii], max_tokens=max_tokens, 
                                                         temperature=temperature, top_p=top_p, n=n, 
                                                         logprobs=logprobs, key=key)
                        if result is not None: got_result = True
                    results.append(result)
            else:
                results.append(result)
        result['choices'] = [c for x in results for c in x['choices']]
    elif not got_result:
        prefix = prefix if isinstance(prefix, list) else [prefix]
        for ii in range(len(prefix)):
            _got_result = False
            while not _got_result:
                result = openai_prompt_eval_once(args, prefix[ii], max_tokens=max_tokens, temperature=temperature, 
                                                 top_p=top_p, n=n, logprobs=logprobs, key=key)
                if result is not None: _got_result = True
            results.append(result)
        result['choices'] = [c for x in results for c in x['choices']]
    
    return extract_confidence_score(result)


def get_line_confidence(args, prefix, code_list, step, key, use_batch=False):
    
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
        scores, comments = get_confidence(args, prompt, key=key)
    
    return scores, comments


