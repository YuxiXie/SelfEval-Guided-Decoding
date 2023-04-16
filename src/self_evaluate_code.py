import os
import argparse
from time import sleep
from concurrent.futures import ProcessPoolExecutor as Pool

from utils.tool import *
from utils.prompt import *
from utils.dataset import jsonlines_load, merge_parallel_results
from utils.self_evaluate import get_line_confidence


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
    parser.add_argument("--input_file", required=True, type=str, help='generated file to check confidence')
    parser.add_argument("--output_dir", required=True, type=str, help='directory to save output results')
    parser.add_argument("--start", default=0, type=int)
    parser.add_argument("--end", default=-1, type=int)
    ##=== prompting hyperparameters ===##
    parser.add_argument("--key", default="OPENAI_KEY", type=str)
    parser.add_argument("--keys", default=[], nargs='+', type=str)
    parser.add_argument("--sleep_time", default=10, type=int)
    parser.add_argument("--max_stuck_time", default=30, type=int)
    ##=== running settings ===##
    parser.add_argument("--use_mini_n", default=False, action='store_true')
    parser.add_argument("--mini_n_samples", default=10, type=int, help='value of n for mini code generation sampling (when token rate is limited)')
    parser.add_argument("--verbal", default=False, action='store_true')
    parser.add_argument("--parallel", default=False, action='store_true')
    parser.add_argument("--n_jobs", default=4, type=int, help='number of jobs in parallel')
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
    
    args.prompts = get_prompts(args.dt_name)
    
    return args


def get_code_confidence(args, example, key=KEYS):
    _, prefix = get_prompt_inputs(args.dt_name, args.prompts, example)
    
    confidence = {k: v for k, v in example.items() if k not in ['generated']}
    confidence['generated'] = {}
    
    # get unique generated codes & probs
    for code, _, probs in example["generated"]:
        if code in confidence['generated']: continue
        confidence['generated'][code] = {'line_probs': probs}
    # get the confidence scores and comments
    code_list_batch, steps, codes = [], [], []
    for code, x in confidence['generated'].items():
        blocks, probs = split_code_with_probs(code, x['line_probs'], not_code=(args.prompts['type'] == 'commonsense'))
        x.update({'splited': blocks, 'probs': probs, 'confs': [], 'comments': []})
        
        code_list_batch += [blocks] * len(blocks)
        steps += list(range(1, len(blocks) + 1))
        codes += [code] * len(blocks)
    
    confs, comments = get_line_confidence(args, prefix, code_list_batch, steps, key, use_batch=True)
    for code, conf, comment in zip(codes, confs, comments):
        confidence['generated'][code]['confs'].append(conf)
        confidence['generated'][code]['comments'].append(comment)
    
    confs = []
    for x in confidence['generated'].values():
        confs.append(nor_prod(x['confs']) if len(x['confs']) else -1)
    
    return confidence, max(confs)


def main(argv):
    args, examples, key, fname, sid = argv
    
    prev_indexes = []
    if os.path.exists(fname):
        processed = jsonlines_load(fname)
        prev_indexes += [x['index'] for x in processed if 'index' in x]
    
    for example in tqdm(examples, desc=f'  - (example {sid} starts) -  '):
        if example['index'] in prev_indexes: continue
        result, _ = get_code_confidence(args, example, key=key)
        with jsonlines.open(fname, mode='a') as writer:
            writer.write(result)
    
    print('Examples {} to {} done.'.format(sid, sid + len(examples)))


if __name__ == "__main__":  
    args = parse_args()
    
    ### ==================== Load Input Data ==================== ###
    results = jsonlines_load(args.input_file)[1:]
    
    ### ==================== Prepare Output Filename ==================== ###
    args.end = len(results) if args.end == -1 else args.end + 1
    results = results[args.start:args.end]
    print('number of examples: ', len(results))
    
    fn_prefix = '.'.join(args.input_file.split('/')[-1].strip().split('.')[:-1])
    filename = f'{fn_prefix}_conf_mc_s{args.start}_e{args.end}'
    
    ### ==================== Run Self-Evaluation ==================== ###
    if args.parallel_on_sub:
        merge_parallel_results(f'{args.output_dir}/{filename}', 100)   # TODO: magic number
        sleep(args.sleep_time)
        if os.path.exists(f'{args.output_dir}/{filename}.jsonl'):
            prev = jsonlines_load(f'{args.output_dir}/{filename}.jsonl')
            _indexes = [x['index'] for x in prev if 'index' in x]
            results = [x for x in results if x['index'] not in _indexes]
            filename += '_sub'
    
    if args.parallel:
        examples_list, fname_list, sid_list, key_list = [], [], [], []
        
        fname1 = f'{args.output_dir}/{filename}_parallel_split0.jsonl'
        if not os.path.exists(fname1):
            with jsonlines.open(fname1, mode='w') as writer:
                writer.write(args.prompts)
        
        interval = (len(results) + args.n_jobs - 1) // args.n_jobs
        k_interval = (len(args.keys) + args.n_jobs - 1) // args.n_jobs
        for i in range(args.n_jobs):
            sid = i * interval
            examples_list.append(results[sid: sid + interval])
            fname_list.append(f'{args.output_dir}/{filename}_parallel_split{i}.jsonl')
            sid_list.append(sid + args.start)
            key_list.append(args.keys[i * k_interval: (i + 1) * k_interval])
        
        with Pool(args.n_jobs) as pool:
            results = pool.map(main, zip([args] * args.n_jobs, examples_list, key_list, fname_list, sid_list))
        
        print('Finished parallel running.')
        sleep(args.sleep_time)
        print('Merging result files...')
        merge_parallel_results(f'{args.output_dir}/{filename}', args.n_jobs)
    else:
        filename = f'{args.output_dir}/{filename}.jsonl'
        prev_indexes = []
        if not os.path.exists(filename):
            with jsonlines.open(filename, mode='w') as writer:
                writer.write(args.prompts)
        else:
            prev = jsonlines_load(filename)
            prev_indexes += [x['index'] for x in prev if 'index' in x]
        
        conf_list = []
        for example in tqdm(results):
            if example['index'] in prev_indexes: continue
            result, conf = get_code_confidence(args, example, key=args.keys)
            with jsonlines.open(filename, mode='a') as writer:
                writer.write(result)
            conf_list.append(conf)
            # print('*** avg conf:', sum(conf_list) / len(conf_list))
            
        print('Done.')
