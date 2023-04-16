import sys
import csv

sys.path.append('/home/yuxi/Projects/SelfEvaluation_BeamSearch_MWP/src')
from utils.tool import *
from utils.dataset import jsonlines_load, jsonlines_dump


def check_eq(p, g, percent_check='', dtname=None):
    if dtname == 'finqa':
        # return finqa_equal(p, g, include_percentage='percent' in percent_check, is_close=True)
        return finqa_equal(p, g)
    elif dtname == 'csqa':
        ps = list(p)
        return ps.count(g) / max(1, len(ps))
    return p == g


def cal_weight(c, p, s=1):
    if isinstance(p, list) and len(p) == 2 and isinstance(p[0], float):
        p = p[0] ** (1 / p[1])
    return ((c * p) ** 0.5) * (1 + s) / 2


if __name__ == '__main__':
    fname = sys.argv[1]
    data = jsonlines_load(fname)
    
    dtname = fname.strip().split('/')[-3]
    dur = []
    
    to_save = []
    
    sample_id = -1
    for result in tqdm(data):
        sample_id += 1
        if 'index' not in result: continue
        
        predictions = []
        if isinstance(result['generated'], list) and 'finished' in result['generated'][0]:
            result['generated'] = [x for x in result['generated'] if not isinstance(x, dict) or x['finished']] \
                + [x for x in result['generated'] if isinstance(x, dict) and not x['finished']]
        for g_id, g in enumerate(result['generated']):
            if dtname in ['csqa', 'strategyqa', 'sports', 'saycan', 'gsm8k_cot']:
                if isinstance(g, dict):
                    g['generated'] = g['generated'][:-1] \
                        if len(g['generated']) > 2 and (g['generated'][-2].startswith('So the answer is') or 'return result' in g['generated'][-1]) \
                        else g['generated']
            
            if isinstance(g, str):
                code = g
            elif isinstance(g, dict):
                code = '\n'.join(g['generated'])
            else:
                code = g[0]
            
            rst = [x[0].strip('()') for x in regex.finditer(r'\([a-z\s]+\)', code.strip().split('\n')[-1])]
            prd = [x.strip() for r in rst for x in r.split() if regex.match(r'^[a-z]$', x.strip())]
            prd = ';'.join(sorted(tuple(set(prd))))
            
            if not len(prd.strip()) and ' answer is ' in code:
                ans = [x for x in code.strip().split('\n') if x.count(' answer is ')]
                prd = [x.strip() for r in ans[-1:] for x in r.split() if regex.match(r'^[a-z]$', x.strip())]
                prd = ';'.join(sorted(tuple(set(prd))))
            if isinstance(g, dict): g['executed'] = prd
            elif len(g) == 1: result['executed'] = prd
            
            predictions.append(prd)
        
        to_save.append({'id': result['question'], 'answer': predictions[0].upper() if len(predictions) and len(predictions[0]) else 'A;B;C;D'})

        if 'run_time' in result: dur.append(result['run_time'])
        
        if 'all_generated' not in result: continue
        del result['all_generated']
            
    if len(dur): print('avg running time:', sum(dur)/len(dur) if isinstance(dur[0], float) else sum(sum(x) for x in dur)/len(dur))
    
    jsonlines_dump(data, fname)
    
    rows = [list(row.values()) for row in to_save]
    with open(fname.replace('.jsonl', '.csv'), 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(rows)
    
    