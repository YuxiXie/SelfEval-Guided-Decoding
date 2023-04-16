import os
import math
import regex
import random
import string
import jsonlines
import func_timeout
from tqdm import tqdm
from time import time
from sympy import Symbol
from typing import Union
from math import isclose
from pprint import pprint
from copy import deepcopy
from ipdb import set_trace
from sympy import simplify
from functools import reduce
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from sympy.solvers import solve
from collections import defaultdict
from dateutil.relativedelta import relativedelta


prod = lambda l: reduce(lambda x,y:x*y, l, 1)
nor_prod = lambda l: prod(l) ** (1 / max(1, len(list(l))))

ERRORS = ['Rate limit reached for default-code-davinci-002', 'Request timed out']


###===== hyper-parameters =====###
def get_cp_ratio(r=0):
    r = 2 ** r
    ratio = 1 if math.isinf(r) else r / (r + 1)
    return ratio


def aggregate_conf_and_prob(c, p, r=0.5):
    return c**r * p**(1-r)


def get_internal(keys_used, k, cur_time):
    t = 6e2    # TODO: magic number
    if keys_used[k] is not None:
        t = cur_time - keys_used[k]
    return t


def select_key(keys_used, keys, all_keys=None):
    if all_keys is not None and random.random() < 0.1:     # TODO: magic number
        newkeys = [(k, get_internal(keys_used, k, time())) for k in all_keys]
        newkeys = [k[0] for k in newkeys if k[1] > 6e2]    # TODO: magic number
        if len(newkeys):
            keys = list(set(keys + random.sample(newkeys, min(10, len(newkeys)))))    # TODO: magic number
    
    key_and_time = [(k, get_internal(keys_used, k, time())) for k in keys]
    _key = sorted(key_and_time, key=lambda x:-x[1])[0][0]
    keys_used[_key] = time()
    return _key


def split_keys(keys, c_num=4):
    random.shuffle(keys)
    num = len(keys)
    if num < 10: # TODO: magic number
        return (keys, keys)
    c_num = min(c_num, num - 1)
    return (keys[c_num:], keys[:c_num])


###===== Post-Processing =====###
def get_precision(gt_ans: float) -> int:
    precision = 5
    if '.' in str(gt_ans):
        precision = len(str(gt_ans).split('.')[-1])
    return precision


def finqa_equal(prediction: Union[bool, float, str],
                reference: Union[float, str],
                include_percentage: bool = False,
                is_close: float = False) -> bool:
    if prediction is None:
        return False
    elif type(prediction) == bool:
        # bool questions
        if prediction:
            return reference == 'yes'
        else:
            return reference == 'no'
    elif type(reference) == str or type(prediction) == str:
        # string questions
        return prediction == reference
    else:
        # number questions
        if include_percentage:
            gt_result = [reference / 100, reference, reference * 100]
        else:
            gt_result = [reference]
        for item in gt_result:
            try:
                if is_close:
                    if isclose(item, prediction, rel_tol=0.001):
                        return True
                precision = min(get_precision(prediction), get_precision(item))
                if round(prediction, precision) == round(item, precision):
                    return True
            except Exception:
                continue
        return False


def simplify_ans(ans, convert_to_str: bool = True):
    if isinstance(ans, dict):
        rst = ans.get('result', None)
        if rst is None:
            ans = list(ans.values())
        else:
            ans = rst
    elif isinstance(ans, set):
        ans = list(ans)
    
    if 'relational' in str(type(ans)):
        return str(ans)
    elif 'numpy' in str(type(ans)):
        if ans.shape == ():
            ans = float(ans) # scalar value
        else:
            ans = float(ans[0]) # array value
        if convert_to_str:
            return str(ans)
        else:
            return ans
    
    if ans is None: 
        return None
    if type(ans) in [list, tuple]:
        if not len(ans):
            return None
        if 'sympy' in str(type(ans[0])):
            try:
                ans = [float(x) for x in ans]
            except Exception:
                ans = [str(x) for x in ans]
        if len(ans) == 1:
            ans = ans[0]
    elif 'sympy' in str(type(ans)):
        try:
            ans = float(ans)
        except Exception:
            ans = str(ans)
    
    if convert_to_str:
        return str(ans)
    else:
        return ans


def floatify_ans(ans):
    if ans is None:
        return None
    elif type(ans) == dict:
        ans = list(ans.values())[0] if len(ans) else None
    elif type(ans) == bool:
        ans = ans
    elif type(ans) in [list, tuple]:
        if not ans:
            return None
        else:
            try:
                ans = float(ans[0])
            except Exception:
                ans = str(ans[0])
    else:
        try:
            ans = float(ans)
        except Exception:
            ans = str(ans)
    return ans


def solve_it(equation, variable):
    solution = solve(equation, variable, dict=True)
    if not solution:
        if isinstance(variable, list):
            solution = {v: None for v in variable}
        else:
            solution = {variable: None}
        return solution
    else:
        solution = solution[0]
        if isinstance(variable, list) and len(solution) < len(variable):
            idx = len(solution)
            for v in variable[idx:]:
                solution[v] = v
        return solution


def safe_execute(code_string: str, keys=None, use_pot=False, maxtime=5):
    def execute(x):
        try:
            exec(f'from math import *\n{x}')
            locals_ = locals()
            if keys is not None:
                return [locals_.get(k, None) for k in keys]
            # PoT
            if use_pot:
                return locals_.get('ans', None)
            # PAL
            solution = locals_.get('solution', None)
            if solution is not None: 
                return solution()
            else:
                exec('\n'.join([xx[4:] for xx in x.strip().split('\n')[1:-1]]))
                locals_ = locals()
                return locals_.get('result', None)
        except Exception as e:
            return None
    try:
        ans = func_timeout.func_timeout(maxtime, execute, args=(code_string,))
    except func_timeout.FunctionTimedOut:
        ans = None
    
    return ans


def synthesize_program(result: str, prefix: str) -> str:
    program = prefix
    for i, line in enumerate(result.split('\n')):
        if i == 0:
            program += line + '\n'
        else:
            if line.startswith('    '):
                program += line + '\n'
            else:
                break
    program += 'ans = solver()'    
    return program


###===== OpenAI Result Parsing =====###
def get_text_prob(tokens, token_logprobs, normalize_prob=True, use_pot=False, oneline=False):
    end_of_line = [regex.match(r'^[\n]+', t) is not None for t in tokens]
    start_idx = end_of_line.index(True) if True in end_of_line else 0
    logprobs, logprob, cur_line, lines = [], 0, [], []
    for i, t, lp in zip(range(len(tokens)), tokens, token_logprobs):
        if i <= start_idx: continue
        if ''.join(tokens[start_idx + 1: i + 1]).count('\n\n' if use_pot else '\n\n\n'): break    # stop sign
        if ''.join(tokens[start_idx + 1: i + 1]).count('<|endoftext|>'): break    # stop sign
        if oneline and ''.join(tokens[start_idx + 1: i + 1]).count('\n'): break
        if (regex.match(r'\n$', tokens[i - 1]) or regex.match(r'^\n', t)) and logprob and ''.join(cur_line).replace('\n', ''):
            logprobs.append(logprob)
            lines.append(cur_line)
            logprob, cur_line = 0, []
        if regex.match(r'^[\n]+$', t): continue
        if '\n' in t[1:-1]:
            _ts = [_t for _t in t.split('\n') if _t]
            if len(_ts):
                logprobs.append(logprob + lp)
                lines.append(cur_line + [_ts[0]])
                logprob, cur_line = 0, []
                for _t in _ts[1:-1]:
                    logprobs.append(lp)
                    lines.append([_t])
                if len(_ts) > 1: t = _ts[-1]
                else: continue
            else: continue
        logprob += lp
        cur_line.append(t)
    if logprob and ''.join(cur_line).replace('\n', ''): 
        logprobs.append(logprob)
        lines.append(cur_line)
    return [((math.exp(lp), len(line)) if normalize_prob else math.exp(lp)) for lp, line in zip(logprobs, lines)], [''.join(l) for l in lines]


def parse_api_result(result, return_prob=True, normalize_prob=True, use_pot=False, use_chatgpt=False):
    to_return, return_prob = [], (return_prob and not use_chatgpt)
    for idx, g in enumerate(result['choices']):
        text = g['message']['content'] if use_chatgpt else g['text']
        logprob = -1 if use_chatgpt else sum(g['logprobs']['token_logprobs'])
        if return_prob:
            prbs, lines = get_text_prob(g['logprobs']['tokens'], g['logprobs']['token_logprobs'], 
                                        normalize_prob=normalize_prob, use_pot=use_pot)
            text = '\n'.join(lines)
            to_return.append((text, logprob, prbs))
        elif use_chatgpt:
            text = g['message']['content']
            to_return.append((text, logprob, None))
        else:
            to_return.append((text, logprob, None))
    to_return = sorted(to_return, key=lambda tup: tup[1], reverse=True)
    if return_prob:
        return to_return
    return [r[0] for r in to_return]


def parse_api_result_oneline(result):
    to_return = []
    for idx, g in enumerate(result['choices']):
        text = g['text']
        logprob = sum(g['logprobs']['token_logprobs'])
        prbs, lines = get_text_prob(g['logprobs']['tokens'], g['logprobs']['token_logprobs'], 
                                    normalize_prob=True, oneline=True)
        text = '\n'.join(lines)
        to_return.append((text, logprob, prbs))
    return sorted(to_return, key=lambda tup: tup[1], reverse=True)


def extract_confidence_score(result, use_choice=True):
    def _check_eq(x, tokens):
        x = regex.sub(r'[\(\)\s]', ' ', x).strip()
        eq = False
        if any(x == t for t in tokens): eq = True
        elif any(x.lower() == t.lower() for t in tokens): eq = True
        return eq
    
    w_tokens = ['B'] if use_choice else ['wrong', 'incorrect']
    r_tokens = ['A'] if use_choice else ['correct']
    
    scores, comments = [], []
    for i, g in enumerate(result['choices']):
        text, tokens = g['text'], g['logprobs']['tokens']
        top_logprobs = g['logprobs']['top_logprobs']
        confidence = 0
        for t, tlp in zip(tokens, top_logprobs):
            if not _check_eq(t, w_tokens + r_tokens) or t not in text: continue
            tlp = {k: math.exp(v) for k,v in tlp.items()}
            correct = sum(tlp.get(k, 0) for k in tlp if _check_eq(k, r_tokens))
            wrong = sum(tlp.get(k, 0) for k in tlp if _check_eq(k, w_tokens))
            confidence = correct    # / (correct + wrong + 1e-9)
            break
        # if confidence is not None:
        scores.append(confidence)
        comments.append(text)
    
    return scores, comments


def split_code_with_probs(code, prob, normalize_prob=True, use_pot=False, not_code=False):
    if not code.replace('\n', '') or not len(prob):
        return [], []
    normalize_prob = normalize_prob and (type(prob[0]) in [list, tuple])
    def unfinished(content):
        for x in ['"""', "'''"]:
            if content.count(x) == 2:
                content = regex.sub(r'""".*"""', '\n', content) if x[0] == '"' else regex.sub(r"'''.*'''", '\n', content)
                if content.count(x) > 1:
                    i1 = content.index(x)
                    i2 = content[i1 + 1:].index(x) + (i1 + 1) + 3
                    content = f'{content[:i1]}\n{content[i2:]}'
                elif content.count(x): return True
            elif content.count(x) == 1: return True
        if not content.strip(): return True
        return all(
            (not x.strip() or regex.match(r'[\:\(\{\[]', x.strip()[-1]) or (x.strip().startswith('#') and not not_code))
            for x in regex.split(r'[\n]+', content.strip())
        )
    def get_prob(p):
        return (prod(x[0] for x in p), sum(x[1] for x in p)) if normalize_prob \
            else (nor_prod(p) if isinstance(p[0], float) else nor_prod(x[0] for x in p))
    
    lines = regex.split(r'[\n]+', code.rstrip())
    blocks, block = [], ''
    probs, p = [], []
    ans_cnt = 0
    for i, line in enumerate(lines):        
        block += line if not block else f'\n{line}'
        p.append(prob[i])
        
        if unfinished(block): continue
        if not use_pot and len(block.strip().split()) == 3 and block.strip().split()[1].strip() == '=':
            val = block.strip().split()[0].strip()
            if f'result = {val}' in [x.strip() for x in lines] and not ans_cnt:
                ans_cnt += 1
                if any(x.strip().startswith(f'{val} ') for x in lines[i + 1:]): continue
        if use_pot and 'ans' in line and line.strip().split()[0] == 'ans' and i < len(lines) - 1 and not ans_cnt: 
            ans_cnt += 1; continue
        
        blocks.append(block)
        probs.append(get_prob(p))
        block, p = '', []
    
    if block:
        blocks.append(block)
        probs.append(get_prob(p))
    
    return blocks, probs


def get_eval_type(code, use_pot=False):
    if not use_pot and (code.strip().startswith('return ') or len(code.strip().split()) == 1):
        return 'command'
    if any(x in code for x in '+-*/><%&|'):
        return 'calculation'
    if ' = ' in code and len(code.split(' = ')[-1].strip().split()) <= 1:
        return 'value'
    return 'calculation'
