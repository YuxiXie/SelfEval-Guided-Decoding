import os
import argparse
from time import sleep
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor as Pool

from utils.tool import *
from utils.prompt import *
from utils.dataset import jsonlines_load, merge_parallel_results
from utils.generate import prompt_the_result


def parse_args():
    parser = argparse.ArgumentParser()
    ##=== prompting hyperparameters ===##
    parser.add_argument("--key", default='OPENAI_KEY', type=str)
    parser.add_argument("--keys", default=[], nargs='+', type=str)
    parser.add_argument("--temperature", default=0.0, type=float)
    parser.add_argument("--max_tokens", default=600, type=int)
    parser.add_argument("--top_p", default=1, type=int)
    parser.add_argument("--n_samples", default=1, type=int)
    parser.add_argument("--logprobs", default=1, type=int)
    parser.add_argument("--use_mini_n", default=False, action='store_true')
    parser.add_argument("--mini_n_samples", default=4, type=int, help='value of n for mini code generation sampling (when token rate is limited)')
    parser.add_argument("--sleep_time", default=3, type=int)
    parser.add_argument("--max_stuck_time", default=8, type=int)
    ##=== prompt settings ===##
    parser.add_argument("--greedy", default=False, action='store_true')
    parser.add_argument("--chatgpt", default=False, action='store_true')
    ##=== input data ===##
    parser.add_argument("--dt_name", required=True, type=str, 
                        choices=[
                            'gsm8k', 'aqua', 'svamp', 'asdiv', 'mawps', 'tabmwp', 'finqa',
                            'object_counting', 'repeat_copy', 'colored_object', 'penguin',
                            'date_understanding', 'sports', 'csqa', 'saycan', 'strategyqa',
                            'gsm8k_cot',
                        ],
                        help='the dataset to test')
    parser.add_argument("--input_file", required=True, type=str)
    parser.add_argument("--start", default=0, type=int)
    parser.add_argument("--end", default=-1, type=int)
    ##=== others ===##
    parser.add_argument("--output_dir", required=True, type=str)
    parser.add_argument("--verbal", default=False, action='store_true')
    parser.add_argument("--resume", default=False, action='store_true')
    parser.add_argument("--resume_dt_string", default="", type=str)
    parser.add_argument("--parallel", default=False, action='store_true')
    parser.add_argument("--n_jobs", default=2, type=int, help='number of jobs in parallel')
    parser.add_argument("--parallel_on_sub", default=False, action='store_true')
    args = parser.parse_args()
    
    if not len(args.keys):
        args.keys = [args.key]
    num_key = len(args.keys)
    if args.parallel and num_key >= args.n_jobs:
        num_key = args.n_jobs * (num_key // args.n_jobs)
        args.keys = random.sample(args.keys, min(len(args.keys), num_key))
    else:
        args.keys = [args.key]
    print('Using {} keys in total.'.format(len(args.keys)))
    args.keys_used = {k: None for k in args.keys}
    
    args.prompts = get_prompts(args.dt_name, return_eval=False, use_chatgpt=args.chatgpt)
    
    return args


def main(argv):
    args, examples, key, fname, sid = argv
    
    prev_indexes = []
    if os.path.exists(fname):
        processed = jsonlines_load(fname)
        prev_indexes += [x['index'] for x in processed if 'index' in x]
    
    for example in tqdm(examples, desc=f'  - (example {sid} starts) -  '):
        index = example['index']
        if index in prev_indexes: continue
        rst = {'index': index}
        rst.update(example)
        
        full_prompt, _ = get_prompt_inputs(args.dt_name, args.prompts, example, use_chatgpt=args.chatgpt)
        result = prompt_the_result(args, full_prompt, max_tokens=args.max_tokens, 
                                   temperature=args.temperature, top_p=args.top_p, 
                                   n=args.n_samples, logprobs=args.logprobs, key=key)

        # self-consistency decoding or greedy decoding.
        result_counter = Counter()
        codes = parse_api_result(result, use_chatgpt=args.chatgpt)
        if args.prompts['type'] not in ['commonsense'] and args.dt_name not in ['aqua']:
            for r in codes:
                if isinstance(r, tuple):
                    r = r[0]
                if args.dt_name in ['finqa']:
                    r = r.replace('&', '_')
                ans = safe_execute(r)
                ans = floatify_ans(ans)
                if ans is not None:
                    result_counter.update([ans])

        prediction = None
        if len(result_counter) > 0:
            prediction = result_counter.most_common(1)[0][0]

        # check correctness
        rst.update({
            'executed': prediction, 'generated': codes
        })
        with jsonlines.open(fname, mode='a') as writer:
            writer.write(rst)
    
    print('Examples {} to {} done.'.format(sid, index))


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

    correct, wrong = 0, 0

    args.end = len(data_test) if args.end == -1 else args.end + 1
    data_test = data_test[args.start:args.end]
    print('number of examples: ', len(data_test))

    mtype = 'chatgpt' if args.chatgpt else 'pal'
    if args.greedy:
        filename = f'{args.output_dir}/{args.dt_name}_{mtype}_s{args.start}_e{args.end}_{dt_string}.jsonl'
        assert not args.temperature, "In greedy decoding, temperature should be 0.0"
    else:
        filename = f'{args.output_dir}/{args.dt_name}_sc_{mtype}_tp{args.temperature}_s{args.start}_e{args.end}_{dt_string}.jsonl'
    
    if args.parallel_on_sub:
        fn_prefix = filename.replace('.jsonl', '')
        merge_parallel_results(fn_prefix, 100)   # TODO: magic number
        sleep(args.sleep_time)
        if os.path.exists(f'{fn_prefix}.jsonl'):
            prev = jsonlines_load(f'{fn_prefix}.jsonl')
            _indexes = [x['index'] for x in prev if 'index' in x]
            data_test = [x for x in data_test if x['index'] not in _indexes]
            fn_prefix += '_sub'
        filename = f'{fn_prefix}.jsonl'
    
    if args.parallel:
        filename = filename.rstrip('jsonl').rstrip('.')
        examples_list, fname_list, sid_list, key_list = [], [], [], []
        
        fname1 = f'{filename}_parallel_split0.jsonl'
        if not os.path.exists(fname1):
            with jsonlines.open(fname1, mode='w') as writer:
                writer.write(args.prompts)
        
        interval = (len(data_test) + args.n_jobs - 1) // args.n_jobs
        k_interval = (len(args.keys) + args.n_jobs - 1) // args.n_jobs
        for i in range(args.n_jobs):
            sid = i * interval
            examples_list.append(data_test[sid: sid + interval])
            fname_list.append(f'{filename}_parallel_split{i}.jsonl')
            sid_list.append(sid + args.start)
            key_list.append(args.keys[i * k_interval: (i + 1) * k_interval])
        
        with Pool(args.n_jobs) as pool:
            results = pool.map(main, zip([args]*args.n_jobs, examples_list, key_list, fname_list, sid_list))

        print('Finished parallel running.')
        sleep(args.sleep_time)
        print('Merging result files...')
        merge_parallel_results(filename, args.n_jobs)
    else:    
        if os.path.exists(filename):
            prev = jsonlines_load(filename)
            indexes = [x['index'] for x in prev if 'index' in x]
        else:
            indexes = []
            with jsonlines.open(filename, mode='w') as writer:
                writer.write(args.prompts)
        
        for example in tqdm(data_test):
            index = example['index']
            if index in indexes: continue
            rst = {'index': index}
            rst.update(example)
            
            if args.verbal:
                print('======================')
                print(f'Index: {index}\nQuestion: {example["question"]}')
            
            full_prompt, _ = get_prompt_inputs(args.dt_name, args.prompts, example, use_chatgpt=args.chatgpt)
            result = prompt_the_result(args, full_prompt, max_tokens=args.max_tokens, temperature=args.temperature, 
                                       top_p=args.top_p, n=args.n_samples, logprobs=args.logprobs, key=args.keys)

            # self-consistency decoding or greedy decoding.
            result_counter = Counter()
            codes = parse_api_result(result, use_chatgpt=args.chatgpt)
            if args.prompts['type'] not in ['commonsense'] and args.dt_name not in ['aqua']:
                for r in codes:
                    if isinstance(r, tuple):
                        r, _, probs = r
                    else:
                        r, probs = r, []
                    if args.dt_name in ['finqa']:
                        r = r.replace('&', '_')
                    ans = safe_execute(r)
                    ans = floatify_ans(ans)
                    if ans is not None:
                        result_counter.update([ans])

            prediction = None
            if len(result_counter) > 0:
                prediction = result_counter.most_common(1)[0][0]

            # check correctness
            if args.prompts['type'] not in ['commonsense'] and args.dt_name not in ['aqua']:
                gt_ans = example['answer']
                if finqa_equal(prediction, gt_ans, False):
                    correct += 1
                else:
                    wrong += 1
            
            rst.update({
                'executed': prediction, 'generated': codes
            })
            with jsonlines.open(filename, mode='a') as writer:
                writer.write(rst)

        print('======================')
        if args.dt_name not in ['aqua']:
            print(correct / (correct + wrong), '(', correct, '/', correct + wrong, ')')
 