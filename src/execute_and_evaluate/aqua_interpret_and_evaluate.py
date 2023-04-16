import sys
import openai
from concurrent.futures import ProcessPoolExecutor as Pool
from tenacity import wait_random_exponential, stop_after_attempt, retry

sys.path.append('/home/yuxi/Projects/SelfEvaluation_BeamSearch_MWP/src')
from utils.tool import *
from utils.dataset import jsonlines_load, jsonlines_dump
from prompts.aqua import choice_prompt
from execute_and_evaluate.interpret_and_evaluate import cal_weight

USE_CHATGPT = False
KEYS = ["OPENAI_KEY1", "OPENAI_KEY2"]
KEYS_USED = {k:None for k in KEYS}


def check_eq(p, g):
    return p == g


@retry(wait=wait_random_exponential(min=5, max=10000), stop=stop_after_attempt(256))
def make_choice(prompt, keys, chatgpt=False):
    if chatgpt:
        return openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=prompt,
            api_key=select_key(KEYS_USED, keys, all_keys=KEYS),
            max_tokens=8,
            temperature=0.0,
            n=1,
            stop=['\n'],
        )
    else:
        return openai.Completion.create(
            engine='code-davinci-002',
            prompt=prompt,
            api_key=select_key(KEYS_USED, keys, all_keys=KEYS),
            max_tokens=8,
            temperature=0.0,
            n=1,
            stop=['\n'],
        )


def generate_prompt(qu, options, prediction, chatgpt=False):
    if chatgpt:
        chatgpt_choice_prompt = choice_prompt.strip().split('\n\n')
        instr, examples = chatgpt_choice_prompt[0], chatgpt_choice_prompt[1:]
        prompt = [{'role': 'system', 
                   'content': 'You are a helpful assistant that finds {} '.format(' '.join(instr.split()[1:]))}]
        for exp in examples:
            _input, _output = exp.split('\nClosest Option: ')
            prompt += [
                {'role': 'user', 'content': f'Choose the closest answer to the question according the prediction:\n{_input}'},
                {'role': 'assistant', 'content': _output},
            ]
        prompt += [{
            'role': 'user', 
            'content': 'Choose the closest answer to the question according the prediction:\n' \
                + f'Question: {qu}\nAnswer Choices:\n{options}\nPrediction: {prediction}',
        }]
    else:
        prompt = f'{choice_prompt}\nQuestion: {qu}\nAnswer Choices:\n{options}\nPrediction: {prediction}\nClosest Option:'
    return prompt


def select_option(argv):
    examples, keys = argv
    
    exp_id = -1
    for example in tqdm(examples):
        exp_id += 1
        if example.get('executed_results', None) is None or len(example['executed_results']) <= len(example['generated']):
            saved = list(example.get('executed_results', {}).keys())
            candidates = []
            for g_id, g in enumerate(example['generated']):
                if isinstance(g, str):
                    code = g
                elif isinstance(g, list):
                    code = g[0]
                else:
                    code = '\n'.join(g['generated'])
                if code not in candidates + saved:
                    candidates.append(code)

            candidate_results = {c: {} for c in candidates}
            qu, options = example['question'], '\n'.join(example['options'])
            for code in candidate_results:
                prediction = simplify_ans(safe_execute(code))
                prediction = 'None' if prediction is None else prediction
                
                prompt = generate_prompt(qu, options, prediction, chatgpt=USE_CHATGPT)
                rst = make_choice(prompt, keys, chatgpt=USE_CHATGPT)
                selected = rst['choices'][0]['text'].strip()
                
                candidate_results[code] = {'predict': prediction, 'select': selected}
            
            if len(saved):
                if len(candidate_results):
                    examples[exp_id]['executed_results'].update(candidate_results)
            else:
                examples[exp_id]['executed_results'] = candidate_results
            
    return examples


if __name__ == '__main__':
    fname = sys.argv[1]
    data = jsonlines_load(fname)
    n_jobs = 2
    
    prompts, data = data[0], data[1:]
    n_d_per_job = (len(data) + n_jobs - 1) // n_jobs
    n_k_per_job = len(KEYS) // n_jobs
    data_list, keys_list = [], []
    for i in range(n_jobs):
        data_list.append(data[i * n_d_per_job: (i + 1) * n_d_per_job])
        keys_list.append(KEYS[i * n_k_per_job: (i + 1) * n_k_per_job])
    
    with Pool(n_jobs) as pool:
        results = list(pool.map(select_option, zip(data_list, keys_list)))
    data = [example for _set in results for example in _set]
    
    # data = select_option((data, KEYS))
    
    accu, accu_all = {}, {}
    
    for d in tqdm(data):
        idx = d['index']
        gt_ans = d['correct'].strip()
        executed_results = d['executed_results']
        
        if d.get('executed', None) is not None and isinstance(d['generated'][0], list) and d['executed'][0] is not None:
            selected = d['executed'][1]
            answers = [selected]
            ans = answers[0]
        else:
            answers, weights, predictions = [], [], []
            candidates = []
            
            for g_id, g in enumerate(d['generated']):
                if isinstance(g, str):
                    code = g
                elif isinstance(g, list):
                    code = g[0]
                else:
                    code = '\n'.join(g['generated'])
                candidates.append(code)
                
                executed = executed_results[code]
                prd, selected = executed['predict'], executed['select']
                
                answers.append(selected)
                predictions.append(prd)
            
            anss, prds = answers, predictions
            
            result_counter = Counter()
            result_counter.update([x for x, y in zip(anss, prds) if y != 'None'])
            ans = result_counter.most_common(1)[0][0] if len(result_counter) else None
            prd = prds[anss.index(ans)] if ans is not None else None
            d['executed'] = (prd, ans)
        
        accu[idx] = check_eq(answers[0], gt_ans)
        accu_all[idx] = check_eq(ans, gt_ans)
    
    print('accu ({}):'.format(len(accu)), sum(accu.values())/len(accu))
    print('accu_all:', sum(accu_all.values())/len(accu_all))
    
    jsonlines_dump([prompts] + data, fname)
    
    