# 6-shot
code_prompt = '''
Q: 2015 is coming in 36 hours. What is the date one week from today in MM/DD/YYYY?

# solution in Python:


def solution():
    """2015 is coming in 36 hours. What is the date one week from today in MM/DD/YYYY?"""
    # If 2015 is coming in 36 hours, then today is 36 hours before.
    today = datetime(2015, 1, 1) - relativedelta(hours=36)
    # One week from today,
    one_week_from_today = today + relativedelta(weeks=1)
    # The answer formatted with %m/%d/%Y is
    result = one_week_from_today.strftime('%m/%d/%Y')
    return result





Q: The first day of 2019 is a Tuesday, and today is the first Monday of 2019. What is the date today in MM/DD/YYYY?

# solution in Python:


def solution():
    """The first day of 2019 is a Tuesday, and today is the first Monday of 2019. What is the date today in MM/DD/YYYY?"""
    # If the first day of 2019 is a Tuesday, and today is the first Monday of 2019, then today is 6 days later.
    today = datetime(2019, 1, 1) + relativedelta(days=6)
    # The answer formatted with %m/%d/%Y is
    result = today.strftime('%m/%d/%Y')
    return result





Q: The concert was scheduled to be on 06/01/1943, but was delayed by one day to today. What is the date 10 days ago in MM/DD/YYYY?

# solution in Python:


def solution():
    """The concert was scheduled to be on 06/01/1943, but was delayed by one day to today. What is the date 10 days ago in MM/DD/YYYY?"""
    # If the concert was scheduled to be on 06/01/1943, but was delayed by one day to today, then today is one day later.
    today = datetime(1943, 6, 1) + relativedelta(days=1)
    # 10 days ago,
    ten_days_ago = today - relativedelta(days=10)
    # The answer formatted with %m/%d/%Y is
    result = ten_days_ago.strftime('%m/%d/%Y')
    return result





Q: It is 4/19/1969 today. What is the date 24 hours later in MM/DD/YYYY?

# solution in Python:


def solution():
    """It is 4/19/1969 today. What is the date 24 hours later in MM/DD/YYYY?"""
    # It is 4/19/1969 today.
    today = datetime(1969, 4, 19)
    # 24 hours later,
    later = today + relativedelta(hours=24)
    # The answer formatted with %m/%d/%Y is
    result = today.strftime('%m/%d/%Y')
    return result





Q: Jane thought today is 3/11/2002, but today is in fact Mar 12, which is 1 day later. What is the date 24 hours later in MM/DD/YYYY?

# solution in Python:


def solution():
    """Jane thought today is 3/11/2002, but today is in fact Mar 12, which is 1 day later. What is the date 24 hours later in MM/DD/YYYY?"""
    # If Jane thought today is 3/11/2002, but today is in fact Mar 12, then today is 3/1/2002.
    today = datetime(2002, 3, 12)
    # 24 hours later,
    later = today + relativedelta(hours=24)
    # The answer formatted with %m/%d/%Y is
    result = later.strftime('%m/%d/%Y')
    return result





Q: Jane was born on the last day of Feburary in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?

# solution in Python:


def solution():
    """Jane was born on the last day of Feburary in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?"""
    # If Jane was born on the last day of Feburary in 2001 and today is her 16-year-old birthday, then today is 16 years later.
    today = datetime(2001, 2, 28) + relativedelta(years=16)
    # Yesterday,
    yesterday = today - relativedelta(days=1)
    # The answer formatted with %m/%d/%Y is
    result = yesterday.strftime('%m/%d/%Y')
    return result
'''


# 3-shot
evaluate_prompt = '''
Q: Yesterday was April 30, 2021. What is the date yesterday in MM/DD/YYYY?

# solution in Python:


def solution():
    """Yesterday was April 30, 2021. What is the date yesterday in MM/DD/YYYY?"""
    # Yesterday was April 30, 2021.
    yesterday = datetime(2021, 4, 30)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    # Yesterday,
    yesterday = yesterday - relativedelta(days=1)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the date of yesterday was already got and this is step is redundant
    # The answer formatted with %m/%d/%Y is
    result = yesterday.strftime('%m/%d/%Y')
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of yesterday is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result if incorrect





Q: Yesterday was April 30, 2021. What is the date tomorrow in MM/DD/YYYY?

# solution in Python:


def solution():
    """Yesterday was April 30, 2021. What is the date tomorrow in MM/DD/YYYY?"""
    # Yesterday was April 30, 2021.
    yesterday = datetime(2021, 4, 30)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    # Tomorrow,
    tomorrow = yesterday + relativedelta(days=1)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because tomorrow is 2 days later than yesterday as there is a today in between
    # The answer formatted with %m/%d/%Y is
    result = tomorrow.strftime('%m/%d/%Y')
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of tomorrow if incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result if incorrect





Q: Tomorrow is 11/12/2019. What is the date 24 hours later in MM/DD/YYYY?

# solution in Python:


def solution():
    """Tomorrow is 11/12/2019. What is the date 24 hours later in MM/DD/YYYY?"""
    # Tomorrow is 11/12/2019.
    tomorrow = datetime(2019, 11, 12)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    # 24 hours later,
    later = tomorrow + relativedelta(hours=24)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), 24 hours later should start from today
    # The answer formatted with %m/%d/%Y is
    result = later.strftime('%m/%d/%Y')
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of later is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result if incorrect
'''


choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']




