# 4-shot
code_prompt = '''
Q: say java twice and data once, and then repeat all of this three times.

# solution in Python:


def solution():
    """say java twice and data once, and then repeat all of this three times."""
    result_in_list = []
    tmp = ["java", "java", "data"]
    for i in range(3):
        result_in_list.extend(tmp)
    result = " ".join(result_in_list)
    return result





Q: ask a group of insects in what family? four times. after the fourth time say The happy family

# solution in Python:


def solution():
    """ask a group of insects in what family? four times. after the fourth time say The happy family"""
    result_in_list = []
    tmp = []
    for i in range(1, 5):
        tmp.append("a group of insects in what family?")
    tmp.append("The happy family")
    result_in_list.extend(tmp)
    result = " ".join(result_in_list)
    return result





Q: Repeat the word duck four times, but halfway through also say quack

# solution in Python:


def solution():
    """Repeat the word duck four times, but halfway through also say quack"""
    result_in_list = []
    for i in range(1, 5):
        result_in_list.append("duck")
        if i == 2:
            result_in_list.append("quack")
    result = " ".join(result_in_list)
    return result





Q: Print boolean eleven times, but after the 3rd and 8th also say correct

# solution in Python:


def solution():
    """Print boolean eleven times, but after the 3rd and 8th also say correct"""
    result_in_list = []
    for i in range(1, 12):
        result_in_list.append("boolean")
        if i == 3 or i == 8:
            result_in_list.append("correct")
    result = " ".join(result_in_list)
    return result
'''

# 
evaluate_prompt = '''
'''


choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']


