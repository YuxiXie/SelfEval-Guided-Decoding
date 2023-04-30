import sys
import random

sys.path.append('/home/yuxi/Projects/SelfEval-Guided-Decoding/src')
from utils.tool import *
from utils.dataset import jsonlines_load, jsonlines_dump


def check_eq(p, g, percent_check='', dtname=None):
    if dtname == 'finqa':
        # return finqa_equal(p, g, include_percentage='percent' in percent_check, is_close=True)
        return finqa_equal(p, g)
    elif dtname == 'csqa':
        ps = list(p)
        return int(ps.count(g) > 0) / max(1, len(ps))
    return p == g


def cal_weight(c, p, s=1):
    if isinstance(p, list) and len(p) == 2 and isinstance(p[0], float):
        p = p[0] ** (1 / p[1])
    return ((c * p) ** 0.5) * (1 + s) / 2


if __name__ == '__main__':
    fname = sys.argv[1]
    data = jsonlines_load(fname)
    
    dtname = fname.strip().split('/')[-3]
    if dtname == 'asdiv':
        real_test = jsonlines_load('/hdd2/yuxi/math_word_problem/nlu-asdiv-dataset/dataset/asdiv.jsonl')
        real_test = [x['input'] for x in real_test]
    
    accu_greedy = {}
    dur = []
    
    sample_id = -1
    for result in tqdm(data):
        sample_id += 1
        if 'index' not in result: continue
        if dtname == 'asdiv' and all(not x.startswith(result['Body']) for x in real_test): continue
        
        gt_ans = result['answer']
        
        predictions = []
        if isinstance(result['generated'], list) and 'finished' in result['generated'][0]:
            result['generated'] = [x for x in result['generated'] if x['finished']] \
                + [x for x in result['generated'] if not x['finished']]
        for g_id, g in enumerate(result['generated']):
            if dtname in ['csqa', 'strategyqa', 'sports', 'saycan', 'gsm8k_cot']:
                if isinstance(g, dict):
                    g['generated'] = g['generated'][:-1] \
                        if len(g['generated']) > 2 and (g['generated'][-2].startswith('So the answer is') or 'return result' in g['generated'][-1]) \
                        else g['generated']
            
            if isinstance(g, dict):
                code = '\n'.join(g['generated'])
            else:
                code = g[0]
            if dtname == 'finqa': code = code.replace('&', '_')
            
            if isinstance(g, dict) and g.get('executed', None) is not None:# and False:
                prd = g['executed']
            else:
                if dtname in ['csqa']:
                    rst = [x[0].strip('()') for x in regex.finditer(r'\([a-z\s]+\)', code.strip().split('\n')[-1])]
                    prd = [x.strip() for r in rst for x in r.split() if regex.match(r'^[a-z]$', x.strip())]
                    prd = tuple(set(prd))
                    if not len(prd):
                        ans = [x for x in code.strip().split('\n') if x.count(' answer is ')]
                        prd = [x.strip() for r in ans[-1:] for x in r.split() if regex.match(r'^[a-z]$', x.strip())]
                        prd = tuple(set(prd))
                elif dtname in ['strategyqa', 'sports']:
                    ans = [x for x in code.strip().split('\n') if regex.search(r' answer.* is ', x)]
                    if not len(ans): ans = code.strip().split('\n')[-1:]
                    prd = [x.strip(string.punctuation) for r in ans[:1] for x in r.split('answer')[-1].split() if x.strip(string.punctuation) in ['yes', 'no']]
                    if prd.count('yes') and prd.count('no'):
                        if ' neither ' in ans[0]: prd = None
                        else: prd = prd[0]
                    elif prd.count('yes'): prd = 'yes'
                    elif prd.count('no'): prd = 'no'
                    else: prd = None
                elif dtname in ['saycan']:
                    prd = code.strip().split('\n')[2:]
                elif dtname in ['gsm8k_cot']:
                    ans = code.strip().split('\n')[-1].replace('So the answer is ', '')
                    prd = [x[0] for x in regex.finditer(r'[\d\.,]+', ans) if regex.search(r'\d', x[0])]
                    if len(prd) > 2: prd = prd[-1]
                    elif len(prd): prd = prd[0]
                    else: prd = None
                    try: prd = float(prd.replace(',', '').rstrip('.')) if prd else prd
                    except: prd = None
                else:
                    exe_rst = safe_execute(code)
                    prd = floatify_ans(exe_rst)
                    if type(prd) not in [float, int, bool, str, dict, set, list, tuple]:
                        prd = floatify_ans(simplify_ans(exe_rst))
                
                if isinstance(g, dict): g['executed'] = prd
            
            predictions.append(prd)
        
        accu_greedy[result['index']] = check_eq(predictions[0], gt_ans, 
                                                percent_check=result['question'],
                                                dtname=dtname)

        if 'run_time' in result:
            dur.append(result['run_time'])
        
        if 'all_generated' not in result: continue
        del result['all_generated']
        
    print('accu: ({})'.format(len(accu_greedy)), sum(accu_greedy.values()) / len(accu_greedy) * 100)
    if len(dur): print('avg running time:', sum(dur)/len(dur) if isinstance(dur[0], float) else sum(sum(x) for x in dur)/len(dur))
    
    jsonlines_dump(data, fname)
