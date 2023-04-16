# 3-shot
code_prompt = '''
"""
Table: Here is a table where the first line is a header and each subsequent line is a penguin:
name | age | height (cm) | weight (kg)
Louis | 7 | 50 | 11
Bernard | 5 | 80 | 13
Vincent | 9 | 60 | 11
Gwen | 8 | 70 | 15
For example: the age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is 80 cm.

We now add a penguin to the table:
James | 12 | 90 | 12

Question: How many penguins are less than 8 years old?
"""

# solution in Python:


def solution():
    """Table:
    name | age | height (cm) | weight (kg)
    Louis | 7 | 50 | 11
    Bernard | 5 | 80 | 13
    Vincent | 9 | 60 | 11
    Gwen | 8 | 70 | 15
    Add:
    James | 12 | 90 | 12
    Question: How many penguins are less than 8 years old?
    """
    # Put the penguins into a list.
    penguins = []
    penguins.append(('Louis', 7, 50, 11))
    penguins.append(('Bernard', 5, 80, 13))
    penguins.append(('Vincent', 9, 60, 11))
    penguins.append(('Gwen', 8, 70, 15))
    # Add penguin James.
    penguins.append(('James', 12, 90, 12))
    # Find penguins under 8 years old.
    penguins_under_8_years_old = [penguin for penguin in penguins if penguin[1] < 8]
    # Count number of perguins under 8.
    num_penguin_under_8 = len(penguins_under_8_years_old)
    result = num_penguin_under_8
    return result





"""
Table: Here is a table where the first line is a header and each subsequent line is a penguin:
name | age | height (cm) | weight (kg)
Louis | 7 | 50 | 11
Bernard | 5 | 80 | 13
Vincent | 9 | 60 | 11
Gwen | 8 | 70 | 15
For example: the age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is 80 cm.

Question: Which is the youngest penguin?
"""

# solution in Python:


def solution():
    """Table:
    name | age | height (cm) | weight (kg)
    Louis | 7 | 50 | 11
    Bernard | 5 | 80 | 13
    Vincent | 9 | 60 | 11
    Gwen | 8 | 70 | 15
    Question: Which is the youngest penguin?
    """
    # Put the penguins into a list.
    penguins = []
    penguins.append(('Louis', 7, 50, 11))
    penguins.append(('Bernard', 5, 80, 13))
    penguins.append(('Vincent', 9, 60, 11))
    penguins.append(('Gwen', 8, 70, 15))
    # Sort the penguins by age.
    penguins = sorted(penguins, key=lambda x: x[1])
    # Get the youngest penguin's name.
    youngest_penguin_name = penguins[0][0]
    result = youngest_penguin_name
    return result





"""
Table: Here is a table where the first line is a header and each subsequent line is a penguin:
name | age | height (cm) | weight (kg)
Louis | 7 | 50 | 11
Bernard | 5 | 80 | 13
Vincent | 9 | 60 | 11
Gwen | 8 | 70 | 15
For example: the age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is 80 cm.

Question: What is the name of the second penguin sorted by alphabetic order?
"""

# solution in Python:


def solution():
    """Table:
    name | age | height (cm) | weight (kg)
    Louis | 7 | 50 | 11
    Bernard | 5 | 80 | 13
    Vincent | 9 | 60 | 11
    Gwen | 8 | 70 | 15
    Question: What is the name of the second penguin sorted by alphabetic order?
    """
    # Put the penguins into a list.
    penguins = []
    penguins.append(('Louis', 7, 50, 11))
    penguins.append(('Bernard', 5, 80, 13))
    penguins.append(('Vincent', 9, 60, 11))
    penguins.append(('Gwen', 8, 70, 15))
    # Sort penguins by alphabetic order.
    penguins_alphabetic = sorted(penguins, key=lambda x: x[0])
    # Get the second penguin sorted by alphabetic order.
    second_penguin_name = penguins_alphabetic[1][0]
    result = second_penguin_name
    return result
'''

# 
evaluate_prompt = '''
'''

choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']


