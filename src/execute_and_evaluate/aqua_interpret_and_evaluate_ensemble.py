import sys

sys.path.append('/home/yuxi/Projects/SelfEval-Guided-Decoding/src')
from utils.tool import *
from utils.dataset import jsonlines_load, jsonlines_dump
from execute_and_evaluate.aqua_interpret_and_evaluate import check_eq, cal_weight


if __name__ == '__main__':
    directory = '/hdd2/yuxi/conf_outputs/aqua/test_outputs'
    filenames = [
        'aqua_sebs_rjs_mc_pal_tp0.2_n16_s0_e254_02_01_23_01.jsonl',
        # 'aqua_sebs_rjs_mc_pal_nop_tp0.2_n16_s0_e254_02_02_00_41.jsonl',
        # 'aqua_sebs_rjs_mc_pal_nop_tp0.5_n16_s0_e254_02_02_00_49.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.2_n16_s0_e254_02_02_21_58.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.4_n16_s0_e254_02_03_01_21.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.4_n16_s0_e254_02_03_19_24.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.4_n16_s0_e254_02_03_19_25.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.4_n16_s0_e254_02_03_19_26.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.4_n16_s0_e254_02_03_19_27.jsonl',
        # 'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.4_n16_s0_e254_02_03_23_31.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.5_n16_s0_e254_02_03_14_50.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.8_n16_s0_e254_02_03_10_20.jsonl',
        'aqua_sebs_rjs_mc_pal_bstp0.2_decay0.5_tp0.8_n16_s0_e254_02_03_10_24.jsonl',
    ]
    
    N = 30
    T = .5
    
    results = defaultdict(list)
    for fname in tqdm(filenames, desc='   (load results)   '):
        d = jsonlines_load(os.path.join(directory, fname))
        for x in d:
            if 'index' not in x: continue
            results[x['index']].append(x)
    
    accu_one, accu_all = {}, {}
    for idx, rst in tqdm(results.items(), desc='   (calculate accu)   '):
        if len(rst) < len(filenames): continue
        
        exp_rst = rst[0]
        gt_ans = exp_rst['correct'].strip()
        
        predictions, sampled_preds = [], []        
        for r in rst:
            executed_results = r['executed_results']
            preds = []
            for g in r['generated']:
                code = '\n'.join(g['generated'])
                executed = executed_results[code]
                prd, selected = executed['predict'], executed['select']
                if prd == 'None': selected = None
                preds.append((
                    code, prd, selected,
                    nor_prod(cal_weight(c, p) for c, p in zip(g['conf'], g['prob'])),
                ))
            weights = [x[-1] for x in preds]
            try:
                _w = [math.exp(w / T) for w in weights]
            except:
                _w = [w for w in weights]
            _w = [w / sum(_w) for w in _w]
            indexes = random.choices(list(range(len(preds))), weights=_w, k=N//len(filenames))
        
            predictions += preds
            sampled_preds += [preds[_i] for _i in indexes]
        
        weights = [x[-1] for x in predictions]
        try:
            _w = [math.exp(w / .5) for w in weights]
        except:
            _w = [w for w in weights]
        _w = [w / sum(_w) for w in _w]
        indexes = random.choices(list(range(len(predictions))), weights=_w, k=10)
        _predictions = [predictions[_i] for _i in indexes]
        
        result_counter = Counter()
        result_counter.update([x[2] for x in _predictions if x[2] is not None])
        ans = result_counter.most_common(1)[0][0] if len(result_counter) else None
        accu_all[idx] = check_eq(ans, gt_ans)
        
        ans = sorted(predictions, key=lambda x: -x[-1])[0][2]
        accu_one[idx] = check_eq(ans, gt_ans)

    print(len(accu_all), 'samples')
    print('accu one:', sum(accu_one.values()) / len(accu_one))
    print('accu all:', sum(accu_all.values()) / len(accu_all))

