import os
import sys

sys.path.append('/home/yuxi/Projects/SelfEvaluation_BeamSearch_MWP/src')
from utils.tool import *
from utils.dataset import jsonlines_load, jsonlines_dump
from execute_and_evaluate.interpret_and_evaluate import check_eq, cal_weight

if __name__ == '__main__':
    N = 40
    T = 1.0
    
    # directory = '/hdd2/yuxi/conf_outputs/gsm8k/test_outputs'
    # directory = '/hdd2/yuxi/conf_outputs/gsm8k_cot/test_outputs'
    # directory = '/hdd2/yuxi/conf_outputs/svamp/test_outputs'
    # directory = '/hdd2/yuxi/conf_outputs/asdiv/test_outputs'
    # directory = '/hdd2/yuxi/conf_outputs/finqa/test_outputs'
    directory = '/hdd2/yuxi/conf_outputs/tabmwp/test_outputs'
    # directory = '/hdd2/yuxi/conf_outputs/csqa/dev_outputs'
    # directory = '/hdd2/yuxi/conf_outputs/strategyqa/test_outputs'
    filenames = [
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.1_n16_s0_e1319_02_24_23_31.jsonl',
        
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_26_23_38.jsonl',
        
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_22_22_40.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_24_11_32.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_24_11_33.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_24_23_09.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_27_21_04.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_03_03_15_58.jsonl',
        
        # 'gsm8k_cot_sebs_rjs_mc_pal_tp0.5_n16_s0_e1319_02_19_14_57.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_tp0.5_n16_s0_e1319_02_22_15_49.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_tp0.5_n16_s0_e1319_02_22_16_00.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_tp0.5_n16_s0_e1319_02_24_16_15.jsonl',
        # 'gsm8k_cot_sebs_rjs_mc_pal_tp0.5_n16_s0_e1319_03_12_09_52.jsonl',
        
        # 'to_discard/gsm8K_sebs_rjs_mc_pal_tp0.5_n16_s0_e1319_01_29_02_19.jsonl', 
        # 'gsm8k_sebs_rjs_mc_pal_tp0.8_n16_s0_e1319_01_31_09_19.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.01_tp0.8_n16_s0_e1319_01_31_20_20.jsonl',
        # 'gsm8K_sebs_rjs_mc_pal_bstp0.05_tp0.5_n16_s0_e1319_01_30_02_54.jsonl',
        # 'gsm8K_sebs_rjs_mc_pal_bstp0.1_tp0.5_n16_s0_e1319_01_29_15_10.jsonl', 
        # 'gsm8K_sebs_rjs_mc_pal_bstp0.2_tp0.5_n16_s0_e1319_01_30_00_28.jsonl',
        # 'gsm8K_sebs_rjs_mc_pal_bstp0.5_tp0.5_n16_s0_e1319_01_29_21_40.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.4_tp0.8_n16_s0_e1319_02_02_03_25.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_02_03_16_55.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_09_16_30.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_11_02_11.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_11_02_14.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_12_12_30.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_12_13_15.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_15_09_25.jsonl', 
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_15_09_36.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e1319_03_15_11_49.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_02_20_47.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_05_14_26.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_06_09_29.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_06_19_20.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_07_13_59.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_08_01_31.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_08_15_21.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_09_08_27.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_14_10_04.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_20_05_34.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_22_03_02.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_22_03_05.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_22_03_07.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_22_17_30.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_24_00_09.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_24_00_10.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_02_24_00_11.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_01_12_29.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_01_20_30.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_01_20_33.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_01_22_27.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_02_12_53.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_03_16_14.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_03_16_17.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_04_20_11.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_04_20_32.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_04_20_33.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1319_03_11_02_10.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_03_11_12.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_17_16_12.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_18_13_46.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_18_13_48.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_18_13_50.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_18_23_15.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_18_23_16.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_18_23_17.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_19_09_00.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_02_22_17_30.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_03_02_13_37.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_03_03_16_17.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_03_04_20_32.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_03_09_13_16.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1319_03_12_05_47.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e1319_02_26_10_44.jsonl',
        
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e1319_03_01_08_49.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e1319_03_02_13_38.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e1319_03_03_16_19.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e1319_03_04_18_16.jsonl',
        # 'gsm8k_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e1319_03_04_18_18.jsonl',
        
        # 'svamp_sebs_rjs_mc_pal_tp0.5_n16_s0_e1000_02_02_00_19.jsonl',
        # 'svamp_sebs_rjs_mc_pal_tp0.8_n16_s0_e1000_02_01_16_31.jsonl',
        # 'svamp_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e1000_02_02_22_00.jsonl',
        # 'svamp_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e1000_02_03_02_26.jsonl',
        
        # 'asdiv_sebs_rjs_mc_pal_tp0.5_n16_s0_e2159_02_04_09_25.jsonl',
        # 'asdiv_sebs_rjs_mc_pal_tp0.8_n16_s0_e2159_02_02_02_04.jsonl',

        'tabmwp_sebs_rjs_mc_pal_tp0.5_n16_s0_e7686_02_04_11_00.jsonl',
        'tabmwp_sebs_rjs_mc_pal_tp0.8_n16_s0_e7686_02_05_14_31.jsonl',
        'tabmwp_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e7686_02_07_13_58.jsonl',
        'tabmwp_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.5_n16_s0_e7686_02_08_22_11.jsonl',
        'tabmwp_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e7686_02_11_16_33.jsonl',
        # 'tabmwp_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.8_n16_s0_e7686_02_14_10_01.jsonl',
        'tabmwp_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp1.0_n16_s0_e7686_03_20_16_47.jsonl',
    
        # 'csqa_sebs_rjs_mc_pal_tp0.8_n16_s0_e1221_02_08_00_36.jsonl',
        # 'csqa_sebs_rjs_mc_pal_tp0.5_n16_s0_e1221_02_08_08_25.jsonl',
        # 'csqa_sebs_rjs_mc_pal_tp0.5_n16_s0_e1221_02_08_17_18.jsonl',
    
        # 'finqa_sebs_rjs_mc_pal_tp0.2_n16_s0_e1147_02_04_23_22.jsonl',
        # 'finqa_sebs_rjs_mc_pal_tp0.4_n16_s0_e1147_02_04_16_03.jsonl',
        # 'finqa_sebs_rjs_mc_pal_tp0.5_n16_s0_e1147_02_05_19_28.jsonl',
        # 'finqa_sebs_rjs_mc_pal_tp0.8_n16_s0_e1147_02_05_16_51.jsonl',
        
        # 'strategyqa_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.1_n16_s0_e2290_02_12_16_10.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e2290_02_12_23_06.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_bstp0.5_decay0.5_tp0.2_n16_s0_e2290_02_25_17_46.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp0.2_n16_s0_e2290_02_11_22_56.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp0.4_n16_s0_e2290_03_11_02_13.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp0.5_n16_s0_e2290_02_09_19_38.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp0.5_n16_s0_e2290_02_10_18_03.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp0.6_n16_s0_e2290_03_11_02_17.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp0.8_n16_s0_e2290_02_11_16_17.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp0.9_n16_s0_e2290_03_14_11_14.jsonl',
        # 'strategyqa_sebs_rjs_mc_pal_tp1.0_n16_s0_e2290_03_14_03_16.jsonl',
    ]
    
    dtname = directory.strip('/').split('/')[-2]
    
    if dtname == 'asdiv':
        real_test = jsonlines_load('/hdd2/yuxi/math_word_problem/nlu-asdiv-dataset/dataset/asdiv.jsonl')
        real_test = [x['input'] for x in real_test]
    
    results = defaultdict(list)
    for fname in tqdm(filenames, desc='   (load results)   '):
        d = jsonlines_load(os.path.join(directory, fname))
        for x in d:
            if 'index' not in x: continue
            results[x['index']].append(x)
    
    to_dump = []

    accu_greedy, accu_ensemble = {}, {}
    for idx, rst in tqdm(results.items(), desc='   (calculate accu)   '):
        if len(rst) < len(filenames): continue
        if 'asdiv' in fname and all(not x.startswith(rst[0]['Body']) for x in real_test): continue
        
        gt_ans = rst[0]['answer']
        
        in_beam = [g for r in rst for g in r['generated']]
        
        predictions, scores = [], []
        for g in in_beam:
            code = '\n'.join(g['generated'])
            predictions.append(g.get('executed', None))
            scores.append(nor_prod(cal_weight(c, p) for c, p in zip(g['conf'], g['prob'])))
        _i = scores.index(max(scores))
        accu_greedy[idx] = check_eq(predictions[_i], gt_ans, dtname=dtname, percent_check=rst[0]['question'])
        
        sampled_predictions, corresponding_codes, selected_generations = [], [], []
        Ns = [N // len(filenames)] * len(filenames)
        for i in range(len(Ns) - 1, -1, -1):
            if sum(Ns) < N: Ns[i] += 1
        Ts = [T] * len(filenames)
        for _r_id, r in enumerate(rst):
            prds, scrs, _prbs, cur_codes, _generations = [], [], [], [], []
            for g in r['generated']:
                prds.append(g.get('executed', None))
                scrs.append(nor_prod(cal_weight(c, p) for c, p in zip(g['conf'], g['prob'])))
                if dtname in ['gsm8k']:
                    scrs[-1] *= (len(g['generated']) - 1) / max(1, len(g['conf']))
                else:
                    scrs[-1] *= len(g['generated']) / max(1, len(g['conf']))
                _prbs.append(nor_prod(p[0] ** (1 / max(1, p[1])) for p in g['prob']))
                cur_codes.append('\n'.join(g['generated']))
                _generations.append({
                    'executed': g.get('executed', None), 'splited': g['generated'], 
                    'probs': g['prob'], 'confs': g['conf'], 'comments': g['conf_comments'],
                })
            _w0 = [math.exp(w / Ts[_r_id]) for w in scrs]
            _w1 = [(1/p) * w for p, w in zip(_prbs, _w0)]
            _w = [w / (sum(_w1) / max(1, len(_w1))) for w in _w0]
            # _w = [w / (sum(_w0) / max(1, len(_w0))) for w in _w0]
            indexes = random.choices(list(range(len(prds))), weights=_w, k=Ns[_r_id])
            sampled_predictions += [prds[i] for i in indexes]
            corresponding_codes += [cur_codes[i] for i in indexes]
            selected_generations += [_generations[i] for i in indexes]
        
        if len(sampled_predictions) and not isinstance(sampled_predictions[0], list):
            result_counter = Counter()
            result_counter.update([x for x in sampled_predictions if x is not None and type(x) not in [dict, set, list]])
            prd = result_counter.most_common(1)[0][0] if len(result_counter) else None
        else:
            result_counter = defaultdict(float)
            for x in sampled_predictions:
                for xx in x:
                    if xx is None: continue
                    result_counter[xx] += 1 / len(x)
            prd = sorted(result_counter.items(), key=lambda x: -x[1])[0][0] if len(result_counter) else None
        accu_ensemble[idx] = check_eq(prd, gt_ans, dtname=dtname, percent_check=rst[0]['question'])

        to_dump.append({
            'index': rst[0]['index'],
            'question': rst[0]['question'], 'answer': rst[0]['answer'],
            'executed': prd, 'generated': selected_generations,
        })
    
    accuracy = sum(accu_ensemble.values()) / len(accu_ensemble) * 100
    M = len(filenames)
    # if accuracy > 85.3:
    # jsonlines_dump(to_dump, f'/hdd2/yuxi/conf_outputs/{dtname}/test_outputs/modified_mv/majority_voting_1.0tp/{dtname}_sc_{M}runs_N{N}_accu{accuracy:.5f}.jsonl')

    print(len(accu_greedy), 'samples')
    print('accu one:', sum(accu_greedy.values()) / len(accu_greedy) * 100)
    print('accu all:', sum(accu_ensemble.values()) / len(accu_ensemble) * 100)
    