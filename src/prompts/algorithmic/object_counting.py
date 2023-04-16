# 4-shot
code_prompt = '''
Q: I have a drum, a flute, a clarinet, a violin, four accordions, a piano, a trombone, and a trumpet. How many musical instruments do I have?

# solution in Python:


def solution():
    """I have a drum, a flute, a clarinet, a violin, four accordions, a piano, a trombone, and a trumpet. How many musical instruments do I have?"""
    musical_instruments_to_count = {
        'drum': 1,
        'flute': 1,
        'clarinet': 1,
        'violin': 1,
        'accordion': 4,
        'piano': 1,
        'trombone': 1,
        'trumpet': 1
    }
    num_musical_instruments = sum(musical_instruments_to_count.values())
    result = num_instruments
    return result





Q: I have a chair, two ovens, and three tables. How many objects do I have?

# solution in Python:


def solution():
    """I have a chair, two ovens, and three tables. How many objects do I have?
    """
    objects_to_count = {
        'chair': 1,
        'oven': 2,
        'table': 3
    }
    num_objects = sum(objects_to_count.values())
    result = num_objects
    return result





Q: I have a chair, two potatoes, a cauliflower, a lettuce head, two tables, a cabbage, two onions, and three fridges. How many vegetables do I have?

# solution in Python:


def solution():
    """I have a chair, two potatoes, a cauliflower, a lettuce head, two tables, a cabbage, two onions, and three fridges. How many vegetables do I have?
    """
    # note: I'm not counting the chair, tables, or fridges as vegetables
    vegetables_to_count = {
        'potato': 2,
        'cauliflower': 1,
        'lettuce head': 1,
        'cabbage': 1,
        'onion': 2
    }
    num_vegetables = sum(vegetables_to_count.values())
    result = num_vegetables
    return result





Q: I have a raspberry, a cat, a rabbit, a mouse, a pig, two snails, a fish, two cows, a snake, a goat, and a duck. How many animals do I have?

# solution in Python:


def solution():
    """I have a raspberry, a cat, a rabbit, a mouse, a pig, two snails, a fish, two cows, a snake, a goat, and a duck. How many animals do I have?
    """
    # note: I'm not counting the raspberry as an animal
    animals_to_count = {
        'cat': 1,
        'rabbit': 1,
        'mouse': 1,
        'pig': 1,
        'snail': 2,
        'fish': 1,
        'cow': 2,
        'snake': 1,
        'goat': 1,
        'duck': 1
    }
    num_animals = sum(animals_to_count.values())
    result = num_animals
    return result
'''

# 1-shot
evaluate_prompt = '''
Q: I have a peach, an onion, two garlics, a nectarine, a yam, a carrot, a potato, a head of broccoli, a cabbage, a banana, and a stalk of celery. How many vegetables do I have?

# solution in Python:


def solution():
    """I have a peach, an onion, two garlics, a nectarine, a yam, a carrot, a potato, a head of broccoli, a cabbage, a banana, and a stalk of celery. How many vegetables do I have?
    """
    # note: I'm not counting the peach, nectarine, banana, or celery as vegetables
    vegetables_to_count = {
        'onion': 1,
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (A)
        'garlic': 2,
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (A)
        'yam': 1,
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (A)
        'carrot': 1,
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (A)
        'potato': 1,
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (A)
        'broccoli': 1,
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (A)
        'cabbage': 1
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (A)
    }
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because celery should also be counted as vegetables
    num_vegetables = sum(vegetables_to_count.values())
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of vegetables_to_count is incorrect
    result = num_vegetables
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of num_vegetables is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
'''


choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']


