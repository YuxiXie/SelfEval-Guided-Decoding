import math
import random
import numpy as np
from time import time
from copy import deepcopy
from collections import defaultdict

from .tool import get_cp_ratio, aggregate_conf_and_prob


class Beam:
    '''
        Conduct Step-wise Stochastic Beam Search
    '''
    def __init__(self, size, cp_ratio, min_score=0.6,   # TODO: magic number
                 temperature=0.0, temperature_decay=-1.0, 
                 reject_sample=False, unbiased=False):
        self.size = size
        self._done = False
        
        self.temperature = temperature      # sampling temperature (when > 0, there is randomness in topk results)
        self.dynamic_temperature = temperature_decay >= 0
        if self.dynamic_temperature:
            self.temperature_decay = temperature_decay
        self.reject_sample = reject_sample
        self.unbiased = unbiased
        
        self.scores = []        # normalized scores at the last step
        self.finished = []      # whether finished at the last step
        self.min_score = min_score
        
        self.all_confs = []     # accumulated confs at all steps
        self.all_probs = []     # accumulated probs at all steps
        self.all_scores = []    # accumulated scores at all steps
        
        self.all_traces = []    # selected indexes (i, j) at all steps
        self.all_length = []    # lengths of selected generations at all steps
        
        self.prev_ks = []       # Backpointers at each time step
        self.next_ys = []       # Outputs at each time step
        self.all_expls = []      # confidence explanations at all steps
        
        self.last_candidates = {}      # candidates in the last step
        
        self.update_cp_ratio(r=cp_ratio)

    @property
    def done(self):
        return self._done

    def update_cp_ratio(self, r=0):
        self.r = get_cp_ratio(r=r)

    def cal_score(self, c, p, normalize_prob=True):
        if normalize_prob:
            p = self.normalized_p(p)
        return aggregate_conf_and_prob(c, p, r=self.r)

    def flat(self, lst):
        rst = {}
        for i, l in enumerate(lst):
            for j, x in enumerate(l):
                rst[i, j] = x
        return rst

    def normalized_p(self, p):
        return p[0] ** (1 / max(1, p[1]))

    def softmax(self, scores, step_id=0, normalize_scores=None):
        assert not self.unbiased or normalize_scores is not None, "should provide scores divided by LM probabilities if unbiased is on"
        if self.unbiased:
            # numerators = [math.exp(min(s, 2) / self.calculate_temperature(step_id)) for s in scores]    # TODO: magic number
            numerators = [s ** (1 / self.calculate_temperature(step_id)) for s in scores]
            denominators = [(1 / p) * s for s, p in zip(numerators, normalize_scores)]
            # denominators = [math.exp(min(s, 2) / self.calculate_temperature(step_id)) for s in normalize_scores]    # TODO: magic number
            probs = [p / (sum(denominators) / max(len(denominators), 1)) for p in numerators]
        else:
            # probs = [math.exp(min(s, 2) / self.calculate_temperature(step_id)) for s in scores]    # TODO: magic number
            probs = [s ** (1 / self.calculate_temperature(step_id)) for s in scores]
            probs = [p / sum(probs) for p in probs]
        return probs

    def calculate_temperature(self, step_id):
        if self.dynamic_temperature:
            tp = self.temperature * (self.temperature_decay ** step_id if step_id else 1.0)
        else:
            tp = self.temperature
        return tp
    
    def advance(self, preds, pred_probs, pred_confs, is_last_line, expl=None, normalize_prob=True):
        '''
            preds / pred_probs / pred_confs / is_last_line / expl / normalize_prob: 
            [n_beam, n_sampling]
        '''
        # Label the duplicate predictions
        tmp, duplicate_set = {}, {}
        for i, prds in enumerate(preds):
            for j, prd in enumerate(prds):
                tmp[i, j] = []
                for k, _prd in enumerate(prds):
                    if k == j: continue
                    if _prd != prd: continue
                    tmp[i, j].append((i, k))
        preds_indexes = list(tmp.keys())
        for k, v in tmp.items():
            kk = preds_indexes.index(k)
            duplicate_set[kk] = [preds_indexes.index(vv) for vv in v]
        
        # Accumulate length for those who hasn't finished yet
        if len(self.prev_ks):
            cur_length = deepcopy(self.all_length[-1])
            for idx in range(len(self.next_ys[-1])):
                cur_length[idx] += 0 if self.finished[idx] else 1
                if self.finished[idx]:
                    preds[idx], pred_confs[idx], is_last_line[idx] = [None], [1], [True]
                    pred_probs[idx] = [(1, 0) if normalize_prob else 1]
                    if expl: expl[idx] = [None]
        
        # Sum the previous scores
        if len(self.prev_ks):
            prev_score = self.all_scores[-1]
            now_acc_score = []
            for idx, prb in enumerate(pred_probs):
                acc_score = []
                for j, p in enumerate(prb):
                    acc_cp, c = prev_score[idx], pred_confs[idx][j]
                    cur_acc_c = (self.all_confs[-1][idx] if len(self.all_confs) else 1) * c
                    if normalize_prob:
                        cur_acc_p = self.all_probs[-1][idx] if len(self.all_probs) else [1, 0]
                        cur_acc_p = (cur_acc_p[0] * p[0], cur_acc_p[1] + p[1])
                    else:
                        cur_acc_p = (self.all_probs[-1][idx] if len(self.all_probs) else 1) * p
                    acc_score.append((acc_cp * self.cal_score(c, p, normalize_prob=normalize_prob), 
                                      cur_acc_c, cur_acc_p)) # accumulated (cp, c, p)
                now_acc_score.append(acc_score)
            beam_lk = [[(cp ** (1 / cur_length[idx]), c, p) for cp, c, p in acc_score] \
                for idx, acc_score in enumerate(now_acc_score)]
        else:
            beam_lk = [[(self.cal_score(c, p, normalize_prob=normalize_prob), c, p) \
                for c, p in zip(pred_confs[0], pred_probs[0])]]
        
        # Sample (without replacement) to get unique candidates
        def _sample(flat_beam_lk):
            unique_flat_beam_lk, to_ignore = {}, []
            for _idx, ij in enumerate(flat_beam_lk.keys()):
                if _idx in to_ignore: continue
                to_ignore += [_idx] + duplicate_set[_idx]
                unique_flat_beam_lk[ij] = flat_beam_lk[ij]
            
            if self.calculate_temperature(len(self.prev_ks)) < 5e-3:    # TODO: magic number
                sorted_beam_lk = sorted(unique_flat_beam_lk.items(), key=lambda x: -x[1][0])
                # sorted_beam_lk = sorted(flat_beam_lk.items(), key=lambda x: -x[1][0]/(x[1][2][0] ** (1/x[1][2][1])))
                topk_beam_lk = sorted_beam_lk[:self.size]
            else:
                num_to_sample = min(self.size, len(unique_flat_beam_lk))
                unique_aggregate_scores = [s[0] for s in unique_flat_beam_lk.values()]
                threshold = sorted(unique_aggregate_scores)[::-1][num_to_sample - 1] - 1e-5
                
                aggregate_scores = [s[0] for s in flat_beam_lk.values()]
                latest_scores = [self.cal_score(s[1], s[2], normalize_prob=True) for s in flat_beam_lk.values()]
                normalize_scores = [1 / (s[2][0] ** (1 / max(1, s[2][1]))) for s in flat_beam_lk.values()]
                
                if self.unbiased:
                    probs = self.softmax(aggregate_scores, step_id=len(self.prev_ks), normalize_scores=normalize_scores)
                else:
                    probs = self.softmax(aggregate_scores, step_id=len(self.prev_ks))
                
                if self.reject_sample:
                    indexes, topk_beam_idx, iterate_cnt = list(range(len(probs))), [], 0
                    cur_probs = deepcopy(probs)
                    while len(topk_beam_idx) < num_to_sample and len(indexes) and iterate_cnt < 100:    # TODO: magic number
                        iterate_cnt += 1
                        i = random.choices(list(range(len(indexes))), weights=cur_probs)[0]
                        idx = indexes[i]
                        if random.uniform(0, 1) < latest_scores[idx] and aggregate_scores[idx] > min(self.min_score, threshold):
                            topk_beam_idx.append(idx)
                            for _idx in duplicate_set[idx] + [idx]: 
                                if _idx in indexes: indexes.remove(_idx)
                            if self.unbiased:
                                cur_probs = self.softmax([aggregate_scores[idx] for idx in indexes], 
                                                         step_id=len(self.prev_ks),
                                                         normalize_scores=[normalize_scores[idx] for idx in indexes])
                            else:
                                cur_probs = self.softmax([aggregate_scores[idx] for idx in indexes], step_id=len(self.prev_ks))
                else:
                    topk_beam_idx = list(np.random.choice(list(range(len(probs))), num_to_sample, 
                                                          replace=False, p=probs))
                topk_beam_lk = [list(flat_beam_lk.items())[idx] for idx in topk_beam_idx]
            return topk_beam_lk
        
        flat_beam_lk = self.flat(beam_lk)
        topk_beam_lk = _sample(flat_beam_lk)
        
        next_finished = []
        for idx, _ in topk_beam_lk:
            i, j = idx
            next_finished.append(bool(is_last_line[i][j] or (len(self.finished) and self.finished[i])))
        # End condition is when top-of-beam is EOS.
        if all(next_finished):
            self._done = True
        
        if self._done:
            topk_beam_lk = sorted(flat_beam_lk.items(), key=lambda x: -x[1][0])
        
        # Select and update the topk scores and instances
        self.scores = [s[0] for _, s in topk_beam_lk]   # only this is normalized
        self.all_confs.append([s[1] for _, s in topk_beam_lk])
        self.all_probs.append([s[2] for _, s in topk_beam_lk])
        self.all_traces.append([idx for idx, _ in topk_beam_lk])
        if len(self.prev_ks):
            self.all_length.append([cur_length[idx[0]] for idx, _ in topk_beam_lk])
            self.all_scores.append([now_acc_score[idx[0]][idx[1]][0] for idx, _ in topk_beam_lk])
        else:
            self.all_length.append([1 for _ in range(len(topk_beam_lk))])
            self.all_scores.append(self.scores)
        
        prev_k, next_y, next_finished, cur_expl = [], [], [], []
        for idx, _ in topk_beam_lk:
            i, j = idx
            prev_k.append(i)
            next_y.append(preds[i][j])
            next_finished.append(bool(is_last_line[i][j] or (len(self.finished) and self.finished[i])))
            if expl: cur_expl.append(expl[i][j])
        
        self.prev_ks.append(prev_k)
        self.next_ys.append(next_y)
        self.finished = next_finished
        if expl: self.all_expls.append(cur_expl)
        
        return self._done

    def get_current_state(self, return_expl=False):
        '''
            return the existing states (kept candidate paths) within the beam
        '''
        if len(self.next_ys):
            return_expl = return_expl and len(self.next_ys) == len(self.all_expls)
            instances = [[] for _ in self.next_ys[-1]]
            if return_expl: ins_expls = [[] for _ in self.all_expls[-1]]
            prev_k = list(range(len(self.next_ys[-1])))
            for i in range(len(self.next_ys) - 1, -1, -1):
                next_y = [self.next_ys[i][k] for k in prev_k]
                cur_expl = [self.all_expls[i][k] for k in prev_k]
                for j, y in enumerate(next_y):
                    if y is not None:
                        instances[j].append(y)
                    if return_expl and cur_expl[j] is not None:
                        ins_expls[j].append(cur_expl[j])
                prev_k = [self.prev_ks[i][k] for k in prev_k]
            return [(ins[::-1], flg, expl[::-1]) for ins, flg, expl in zip(instances, self.finished, ins_expls)] if return_expl \
                else [(ins[::-1], flg) for ins, flg in zip(instances, self.finished)]
        return [([], False, []) if return_expl else ([], False)]

    def get_step_scores(self):
        '''
            return the scores of existing states (kept candidate paths) within the beam
        '''
        if not len(self.all_scores): return None

        ins_scores = [[] for _ in self.scores]
        prev_k = list(range(len(self.scores)))
        cur_scores = [(self.all_scores[-1][k], self.all_confs[-1][k], self.all_probs[-1][k]) for k in prev_k]
        normalize_prob = type(cur_scores[0][2]) in [list, tuple]
        for i in range(len(self.all_scores) - 1, -1, -1):
            prev_k = [self.prev_ks[i][k] for k in prev_k]
            if i > 0:
                prev_scores = [(self.all_scores[i - 1][k], self.all_confs[i - 1][k], self.all_probs[i - 1][k]) for k in prev_k]
            else:
                prev_scores = [(1, 1, (1, 0)) if normalize_prob else (1, 1, 1) for _ in prev_k]
            for j, cur_s, prv_s in zip(range(len(ins_scores)), cur_scores, prev_scores):
                ins_scores[j].append(tuple(
                    (sc / max(sp, 1) if isinstance(sc, float) else (sc[0] / max(sp[0], 1), sc[1] - sp[1])) \
                        for sc, sp in zip(cur_s, prv_s)
                ))
            cur_scores = prev_scores
        
        return [ins[::-1][:l] for ins, l in zip(ins_scores, self.all_length[-1])]
