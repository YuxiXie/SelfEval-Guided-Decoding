import random
import openai
from time import sleep, time
from tenacity import wait_random_exponential, stop_after_attempt, retry

from .tool import select_key, ERRORS


@retry(wait=wait_random_exponential(min=5, max=1000), stop=stop_after_attempt(128))
def _generate_code(args, prompt, max_tokens=256, temperature=0.0, 
                   top_p=1, n=1, logprobs=1, key=[]):
    st = time()
    if args.chatgpt:
        rst = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            api_key=select_key(args.keys_used, key, all_keys=args.keys),
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stop=['\n\n\n'],
            # logprobs=logprobs,
        )
    else:
        rst = openai.Completion.create(
            engine='code-davinci-002',
            prompt=prompt,
            api_key=select_key(args.keys_used, key, all_keys=args.keys),
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stop=['\n\n\n'],
            logprobs=logprobs,
        )
    dur = time() - st
    if args.verbal: print(f'@_generate_code: {dur} seconds')
    return rst


def openai_prompt_once(args, prompt, max_tokens=256, temperature=0.0, top_p=1, n=1, logprobs=1, 
                       key=[], min_to_wait=3, max_to_wait=10):
    start_time = time()
    result, cost = None, args.sleep_time
    
    try:
        result = _generate_code(args, prompt, max_tokens=max_tokens, temperature=temperature, 
                                top_p=top_p, n=n, logprobs=logprobs, key=key)
        cost = time() - start_time
    except Exception as e:
        if args.verbal or all(x not in str(e) for x in ERRORS):
            print(f'***code API error***', str(e))
        sleep(args.sleep_time)
    
    dur = time() - start_time
    to_wait = args.sleep_time
    if to_wait < min_to_wait: to_wait = random.uniform(to_wait, max_to_wait) 
    sleep_time = to_wait - int(dur) if dur < to_wait - min_to_wait \
        else random.uniform(min_to_wait, max(min_to_wait + 1, args.sleep_time))
    if args.verbal: print(f'@generation: {cost} seconds (+ sleep {sleep_time} seconds)')
    sleep(sleep_time)
    
    return result


def prompt_the_result(args, prompt, max_tokens=256, temperature=0.0, 
                      top_p=1, n=1, logprobs=1, key=[]):
    got_result = False
    start_time = time()
    
    while not got_result and not args.use_mini_n:
        if time() - start_time > args.max_stuck_time: break
        result = openai_prompt_once(args, prompt, max_tokens=max_tokens, temperature=temperature, 
                                    top_p=top_p, n=n, logprobs=logprobs, key=key)
        if result is not None: got_result = True
    
    results = []
    if not got_result and args.use_mini_n:
        mini_n_samples = args.mini_n_samples if (max_tokens <= 256 and args.mini_n_samples <= 10) else (args.mini_n_samples // 2)   # TODO: magic number
        n_step = (n + mini_n_samples - 1) // mini_n_samples
        _ns = [mini_n_samples] * (n_step - 1) + [n - mini_n_samples * (n_step - 1)]
        for _n in _ns:
            start_time = time()
            got_result = False
            while not got_result:
                if time() - start_time > args.max_stuck_time: break
                result = openai_prompt_once(args, prompt, max_tokens=max_tokens, temperature=temperature, 
                                            top_p=top_p, n=_n, logprobs=logprobs, key=key)
                if result is not None: got_result = True
            if not got_result:
                for _ in range(_n):
                    got_result = False
                    while not got_result:
                        result = openai_prompt_once(args, prompt, max_tokens=max_tokens, temperature=temperature, 
                                                    top_p=top_p, n=1, logprobs=logprobs, key=key)
                        if result is not None: got_result = True
                    results.append(result)
            else:
                results.append(result)
        result['choices'] = [c for x in results for c in x['choices']]
    elif not got_result:
        for _ in range(n):
            while not got_result:
                result = openai_prompt_once(args, prompt, max_tokens=max_tokens, temperature=temperature, 
                                            top_p=top_p, n=1, logprobs=logprobs, key=key)
                if result is not None: got_result = True
            results.append(result)
        result['choices'] = [c for x in results for c in x['choices']]
    
    return result

