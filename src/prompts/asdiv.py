'''
Same as SVAMP
'''


# 7-shot
code_prompt = '''
Passage: James bought 93 red and 10 blue stickers, he used 31 red sticker on his fridge and 7 blue stickers on his laptop.
Question: How many red stickers does James have?

# solution in Python:


def solution():
    """Passage: James bought 93 red and 10 blue stickers, he used 31 red sticker on his fridge and 7 blue stickers on his laptop.
    Question: How many red stickers does James have?
    """
    original_red_stickers = 93
    used_red_stickers = 31
    red_stickers = original_red_stickers - used_red_stickers
    result = red_stickers
    return result





Passage: Allen went to supermarket to buy eggs, each egg costs 80 dollars, if the discount is 29 dollars.
Question: How much do you have to pay to buy for each egg?

# solution in Python:


def solution():
    """Passage: Allen went to supermarket to buy eggs, each egg costs 80 dollars, if the discount is 29 dollars.
    Question: How much do you have to pay to buy for each egg?
    """
    original_egg_price_in_dollars = 80
    discount_dollars = 29
    egg_price = original_egg_price_in_dollars - discount_dollars
    result = egg_price
    return result





Passage: Dianna collects both cases and books. He bought 22 cases and 5 books from the store. Now he has 57 cases and 25 books.
Question: How many books did danny have at first?

# solution in Python:


def solution():
    """Passage: Dianna collects both cases and books. He bought 22 cases and 5 books from the store. Now he has 57 cases and 25 books.
    Question: How many books did danny have at first?
    """
    num_books_bought_at_store = 5
    num_books_now = 25
    num_books_at_first = num_books_now - num_books_bought_at_store
    result = num_books_at_first
    return result





Passage: There were 108 chickens and 20 sheeps at the farm, some of chickens and sheeps were sold. There are 87 chickens and 18 sheeps left now.
Question: How many chickens were sold?

# solution in Python:


def solution():
    """Passage: There were 108 chickens and 20 sheeps at the farm, some of chickens and sheeps were sold. There are 87 chickens and 18 sheeps left now.
    Question: How many chickens were sold?
    """
    num_chicken_before = 108
    num_chicken_now = 87
    num_chicken_sold = num_chicken_before - num_chicken_now
    result = num_chicken_sold
    return result





Passage: Katty scored 2 goals on monday, 8 goals on tuesday and 9 goals on wednesday.
Question: How many did Katty score on monday and wednesday?

# solution in Python:


def solution():
    """Passage: Katty scored 2 goals on monday, 8 goals on tuesday and 9 goals on wednesday.
    Question: How many did Katty score on monday and wednesday?
    """
    num_goals_on_monday = 2
    num_goals_on_wednesday = 9
    num_goals_total = num_goals_on_monday + num_goals_on_wednesday
    result = num_goals_total
    return result





Passage: There are 5 girls and 4 boys in the Masquerade, 12 more girls and 7 more boys joined.
Question: How many more girls than boys are in the Masquerade?

# solution in Python:


def solution():
    """Passage: There are 5 girls and 4 boys in the Masquerade, 12 more girls and 7 more boys joined.
    Question: How many more girls than boys are in the Masquerade?
    """
    num_girls_before = 5
    num_girls_joined = 12
    num_boys_before = 4
    num_boys_joined = 7
    total_girls = num_girls_before + num_girls_joined
    total_boys = num_boys_before + num_boys_joined
    num_more = total_girls - total_boys
    result = num_more
    return result





Passage: Joseph and Getty went to buy ice creams, they together bought 36 ice creams. On the way back, Joseph ate 12 of the ice creasm, and he has 2 ice creams left now.
Question: How much ice creasm did Getty purchase?

# solution in Python:


def solution():
    """Passage: Joseph and Getty went to buy ice creams, they together bought 36 ice creams. On the way back, Joseph ate 12 of the ice creasm, and he has 2 ice creams left now.
    Question: How much ice creasm did Getty purchase?
    """
    num_ice_creams_bought_by_joseph = 2 + 12
    total_ice_creams = 36
    num_ice_creams_bought_by_getty = total_ice_creams - num_ice_creams_bought_by_joseph
    result = num_ice_creams_bought_by_getty
    return result
'''

# 5-shot (T/F)
# (https://www.mathplayground.com/wpdatabase/wpindex.html)
# (https://www.analyzemath.com/middle_school_math/grade_8/problems.html)
evaluate_prompt = '''
Passage: A piece of square paper has a perimeter of 32 centimeters. Nicky's dog, Rocky, tore off 1/4 of the paper.
Question: What is the area of the remaining paper?

# solution in Python:


def solution():
    """Passage: A piece of square paper has a perimeter of 32 centimeters. Nicky's dog, Rocky, tore off 1/4 of the paper.
    Question: What is the area of the remaining paper?
    """
    perimeter = 32
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    side_length = perimeter / 4
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    area = side_length ** 2
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    result = area
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should calculate the remaining area after torn off as result
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Passage: Lavender is making punch for the school dance. She mixes 3 parts lemonade with 5 parts cranberry juice. She wants to fill a 72 cup bowl.
Question: How many more cups of cranberry juice will she need than lemonade?

# solution in Python:


def solution():
    """Passage: Lavender is making punch for the school dance. She mixes 3 parts lemonade with 5 parts cranberry juice. She wants to fill a 72 cup bowl.
    Question: How many more cups of cranberry juice will she need than lemonade?
    """
    num_parts_lemonade = 3
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    num_parts_cranberry_juice = 5
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    num_cups_bowl = 72
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    num_cups_lemonade = num_parts_lemonade * num_cups_bowl
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should convert the parts of lemonade into proportion first
    num_cups_cranberry_juice = num_parts_cranberry_juice * num_cups_bowl
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should convert the parts of cranberry juice into proportion first
    num_more_cups_cranberry_juice = num_cups_cranberry_juice - num_cups_lemonade
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the values of num_cups_cranberry_juice and num_cups_lemonade are incorrect
    result = num_more_cups_cranberry_juice
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of num_more_cups_cranberry_juice is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Passage: Sara bought decorations for her party. She paid $5 for balloons and $18 for tablecloths. She also spent $9 for streamers. She paid the cashier and got $8 back.
Question: How much money did Sara give to the cashier?

# solution in Python:


def solution():
    """Passage: Sara bought decorations for her party. She paid $5 for balloons and $18 for tablecloths. She also spent $9 for streamers. She paid the cashier and got $8 back.
    Question: How much money did Sara give to the cashier?
    """
    balloons_price = 5
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    tablecloths_price = 18
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    streamers_price = 9
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    change = 8
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    total_price = balloons_price + tablecloths_price + streamers_price
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    money_paid = total_price - change
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the money paid to the cashier contains the change
    result = money_paid
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of money_paid is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Passage: Zachary is thinking of a mystery number. If he divides his number by 4 and then multiplies it by 5, the result is 135.
Question: What is Zachary’s mystery number?

# solution in Python:


def solution():
    """Passage: Zachary is thinking of a mystery number. If he divides his number by 4 and then multiplies it by 5, the result is 135.
    Question: What is Zachary’s mystery number?
    """
    result = 135 * 4 / 5
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because it correctly converts division to multiplication in backpropogation
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)





Passage: A box of apples was delivered to Paul's Pies and Cakes. He put half of the apples aside for a pie he would make later. He put 25 of the remaining apples in the refrigerator. That left 6 apples to use in his muffins.
Question: How many apples were in the box at first?

# solution in Python:


def solution():
    """Passage: A box of apples was delivered to Paul's Pies and Cakes. He put half of the apples aside for a pie he would make later. He put 25 of the remaining apples in the refrigerator. That left 6 apples to use in his muffins.
    Question: How many apples were in the box at first?
    """
    num_apples_for_pie = 25
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because half of the apples in the box are put aside for a pie
    num_apples_for_muffins = 6
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    num_apples_in_box = num_apples_for_pie + num_apples_for_muffins
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because there are 25 apples in the refrigerator, and the value of num_apples_for_pie is incorrect
    result = num_apples_in_box
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of num_apples_in_box is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
'''



choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']


