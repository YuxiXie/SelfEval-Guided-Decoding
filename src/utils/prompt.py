import regex


def import_name(modulename, name):
    """ Import a named object from a module in the context of this function.

    modulename: python filename
    name: variable/function/class name
    """
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except ImportError:
        return None
    
    return vars(module)[name]


def _get_reasoning_type(dt_name):
    if dt_name in ['colored_object', 'date_understanding', 'penguin']:
        reasoning_type = 'symbolic'
    elif dt_name in ['object_counting', 'repeat_copy']:
        reasoning_type = 'algorithmic'
    elif dt_name in ['csqa', 'saycan', 'sports', 'strategyqa', 'gsm8k_cot']:
        reasoning_type = 'commonsense'
    else:
        reasoning_type = 'arithmetic'
    return reasoning_type
    

def _get_request(raw, dt_name):
    reasoning_type = _get_reasoning_type(dt_name)
    instruction, in_context = '', ''
    
    if dt_name in [
        'gsm8k', 'mawps', 'date_understanding', 'colored_object', 'repeat_copy', 'object_counting',
        'strategyqa', 'sports', 'gsm8k_cot',
    ]:
        instruction = 'Answer the following question {}: '.format(
            'via chain-of-thought reasoning' if reasoning_type in ['commonsense'] else 'in Python'
        )
        in_context = raw.strip()[3:].strip() if raw.strip().startswith('Q: ') else raw.strip()
    elif dt_name in ['aqua', 'csqa']:
        instruction = 'Choose the right answer to answer the following question {}:\n'.format(
            'via chain-of-thought reasoning' if reasoning_type in ['commonsense'] else 'in Python'
        )
        in_context = raw.strip()
    elif dt_name in ['svamp', 'asdiv']:
        instruction = 'Given the passage, answer the question {}:\n'.format(
            'via chain-of-thought reasoning' if reasoning_type in ['commonsense'] else 'in Python'
        )
        in_context = raw.strip()
    elif dt_name in ['tabmwp', 'finqa', 'penguin']:
        instruction = 'Given the table, answer the question {}:\n'.format(
            'via chain-of-thought reasoning' if reasoning_type in ['commonsense'] else 'in Python'
        )
        in_context = raw.strip()
    else:
        assert False, f"cannot support dataset {dt_name}"
        
    return instruction, in_context


def _split_ans(ans_prompt, reasoning_type, dt_name):
    if reasoning_type in ['arithmetic', 'symbolic', 'algorithmic']:
        examples = ans_prompt.strip().split('\n\n\n\n\n')
        to_return = [{"role": "system", "content": f"You are a helpful assistant that generates Python code to answer {reasoning_type} questions. "}]
        for example in examples:
            qu, soln = example.split('# solution in Python:')
            instr, qu = _get_request(qu, dt_name)
            soln = soln.strip()
            to_return += [
                {"role": "user", "content": f"{instr}{qu}"}, {"role": "assistant", "content": soln},
            ]
        return to_return
    elif reasoning_type in ['commonsense']:
        examples = ans_prompt.strip().split('\n\n\n\n\n')
        to_return = [{"role": "system", "content": f"You are a helpful assistant that conducts step-by-step reasoning to answer {reasoning_type} questions. "}]
        for example in examples:
            qu, soln = example.split('\n\nA:\n')
            instr, qu = _get_request(qu, dt_name)
            soln = soln.strip()
            to_return += [
                {"role": "user", "content": f"{instr}{qu}"}, {"role": "assistant", "content": soln},
            ]
        return to_return


def get_prompts(dt_name, return_eval=True, use_chatgpt=False):
    reasoning_type = _get_reasoning_type(dt_name)
    if reasoning_type == 'arithmetic':
        path = ['prompts', dt_name]
    else:
        path = ['prompts', reasoning_type, dt_name]
    
    modulename = '.'.join(path)
    
    if reasoning_type in ['commonsense']:
        ans_prompt = import_name(modulename, 'answer_prompt')
    else:
        ans_prompt = import_name(modulename, 'code_prompt')
    evaluate_prompt = import_name(modulename, 'evaluate_prompt') if return_eval else None
    choice_prefix = import_name(modulename, 'choice_prefix') if return_eval else None
    
    return {'ans': _split_ans(ans_prompt, reasoning_type, dt_name) if use_chatgpt else ans_prompt, 
        'type': reasoning_type, 'eval': evaluate_prompt, 'choice_prefix': choice_prefix}


def get_prompt_inputs(dt_name, prompts, example, use_chatgpt=False):
    return_eval = (prompts['eval'] is not None)
    
    qu = example["question"]
    prompt = prompts["ans"] if use_chatgpt else f'{prompts["ans"]}\n\n\n\n\n'
    prefix = f'{prompts["eval"]}\n\n\n\n\n' if (return_eval and not use_chatgpt) else None  # TODO: to implement
    
    if dt_name in ['gsm8k', 'mawps', 'date_understanding', 'colored_object', 'repeat_copy', 'object_counting']:
        if use_chatgpt:
            instr, _ = _get_request(qu, dt_name)
            prompt += [{"role": "user", "content": f"{instr}{qu}"}]
        else:
            prompt += f'Q: {qu}\n\n# solution in Python:\n\n\n'
        if return_eval:
            prefix += f'Q: {qu}\n\n# solution in Python:\n\n\n'
    elif dt_name in ['aqua']:
        options = '\n'.join(example['options'])
        if use_chatgpt:
            instr, _ = _get_request(qu, dt_name)
            prompt += [{"role": "user", "content": f"{instr}Question: {qu}\nAnswer Choices:\n{options}"}]
        else:
            prompt += f'Question: {qu}\nAnswer Choices:\n{options}\n\n# solution in Python:\n\n\n'
        if return_eval:
            prefix += f'Question: {qu}\nAnswer Choices:\n{options}\n\n# solution in Python:\n\n\n'
    elif dt_name in ['svamp', 'asdiv']:
        p, q = example['Body'], example['Question']
        if use_chatgpt:
            instr, _ = _get_request(qu, dt_name)
            prompt += [{"role": "user", "content": f"{instr}Passage: {p}\nQuestion: {q}"}]
        else:
            prompt += f'Passage: {p}\nQuestion: {q}\n\n# solution in Python:\n\n\n'
        if return_eval:
            prefix += f'Passage: {p}\nQuestion: {q}\n\n# solution in Python:\n\n\n'
    elif dt_name in ['tabmwp', 'finqa']:
        if use_chatgpt:
            instr, _ = _get_request(qu, dt_name)
            prompt += [{"role": "user", "content": f"{instr}{example['table']}\nQuestion: {qu}"}]
        else:
            prompt += f'{example["table"]}\nQuestion: {qu}\n\n# solution in Python:\n\n\n'
        if return_eval:
            prefix += f'{example["table"]}\nQuestion: {qu}\n\n# solution in Python:\n\n\n'
    elif dt_name in ['penguin']:
        if use_chatgpt:
            instr, _ = _get_request(qu, dt_name)
            prompt += [{"role": "user", "content": f'{instr}"""\n{example["table"]}\n\nQuestion: {qu}"""'}]
        else:
            prompt += f'"""\n{example["table"]}\n\nQuestion: {qu}"""\n\n# solution in Python:\n\n\n'
        if return_eval:
            prefix += f'"""\n{example["table"]}\n\nQuestion: {qu}"""\n\n# solution in Python:\n\n\n'
    elif dt_name in ['strategyqa', 'sports', 'gsm8k_cot']:
        if use_chatgpt:
            instr, _ = _get_request(qu, dt_name)
            prompt += [{"role": "user", "content": f"{instr}{qu}"}]
        else:
            prompt += f'Q: {qu}\n\nA:\n'
        if return_eval:
            prefix += f'Q: {qu}\n\nA:\n'
    elif dt_name in ['saycan']:
        prompt += f'Human: {qu}\n\n'
        if return_eval:
            prefix += f'Human: {qu}\n\n'
    elif dt_name in ['csqa']:
        options = '\n'.join(example['options'])
        if use_chatgpt:
            instr, _ = _get_request(qu, dt_name)
            prompt += [{"role": "user", "content": f"{instr}Q: {qu}\nAnswer Choices:\n{options}"}]
        else:
            prompt += f'Q: {qu}\nAnswer Choices:\n{options}\n\nA:\n'
        if return_eval:
            prefix += f'Q: {qu}\nAnswer Choices:\n{options}\n\nA:\n'
    
    return prompt, prefix

