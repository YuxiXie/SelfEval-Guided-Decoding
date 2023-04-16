import os
import regex
import jsonlines
from tqdm import tqdm


def jsonlines_load(fname):
    with jsonlines.open(fname, mode='r') as reader:
        data = [row for row in reader]
    return data

def jsonlines_dump(data, fname):
    with jsonlines.open(fname, mode='w') as writer:
        writer.write_all(data)


def _merge_sub(fn_prefix: str):
    main_data = jsonlines_load(f'{fn_prefix}.jsonl')
    sub_data = jsonlines_load(f'{fn_prefix}_sub.jsonl')
    
    indexes = [d['index'] for d in main_data if 'index' in d]
    for d in sub_data:
        if 'index' not in d: continue
        if d['index'] in indexes: continue
        main_data.append(d)

    main_data = main_data[:1] + sorted(main_data[1:], key=lambda x: x['index'])
    jsonlines_dump(main_data, f'{fn_prefix}.jsonl')

def merge_parallel_results(fn_prefix: str, num: int):
    results, indexes = [], []
    if os.path.exists(f'{fn_prefix}.jsonl'):
        results = jsonlines_load(f'{fn_prefix}.jsonl')
        indexes = [d['index'] for d in results if 'index' in d]
    for i in tqdm(range(num)):
        fname = f'{fn_prefix}_parallel_split{i}.jsonl'
        if os.path.exists(fname):
            results += [x for x in jsonlines_load(fname) if x not in results and ('index' not in x or x['index'] not in indexes)]
    if 'index' in results[-1]:
        if 'index' not in results[0]:
            results = [results[0]] + sorted(results[1:], key=lambda x: x['index'])
        else:
            results.sort(key=lambda x: x['index'])
    with jsonlines.open(f'{fn_prefix}.jsonl', mode='w') as writer:
        writer.write_all(results)
    
    if fn_prefix.endswith('_sub'):
        _merge_sub(fn_prefix[:-4])


def split_parallel_results(fn_prefix: str, num: int):
    results = jsonlines_load(f'{fn_prefix}.jsonl')
    prompt = results[0]
    sid = int(regex.search(r'_s\d+_', fn_prefix).group().strip('s_'))
    eid = int(regex.search(r'_e\d+_', fn_prefix).group().strip('e_'))
    step = (eid - sid + num - 1) // num
    to_dump = [[] for _ in range(num)]
    to_dump[0].append(prompt)
    for rst in results[1:]:
        idx = rst['index']
        fid = idx // step
        to_dump[fid].append(rst)
    for fid, data in enumerate(to_dump):
        if not len(data): continue
        with jsonlines.open(f'{fn_prefix}_parallel_split{fid}.jsonl', mode='w') as writer:
            writer.write_all(data)
            