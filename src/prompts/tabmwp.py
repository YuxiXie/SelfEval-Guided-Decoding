# 4-shot
code_prompt = '''
Table of "Coin collections":
Name | Number of coins
Braden | 76
Camilla | 94
Rick | 86
Mary | 84
Hector | 80
Devin | 83
Emily | 82
Avery | 87
Question: Some friends discussed the sizes of their coin collections. What is the mean of the numbers?

# solution in Python:


def solution():
    """Table of "Coin collections":
    Name | Number of coins
    Braden | 76
    Camilla | 94
    Rick | 86
    Mary | 84
    Hector | 80
    Devin | 83
    Emily | 82
    Avery | 87
    Question: Some friends discussed the sizes of their coin collections. What is the mean of the numbers?
    """
    number_of_coins_for_different_person = [76, 94, 86, 84, 80, 83, 82, 87]
    mean_of_the_numbers = sum(number_of_coins_for_different_person) / len(number_of_coins_for_different_person)
    result = mean_of_the_numbers
    return result





Table of "":
Price | Quantity demanded | Quantity supplied
$155 | 22,600 | 5,800
$275 | 20,500 | 9,400
$395 | 18,400 | 13,000
$515 | 16,300 | 16,600
$635 | 14,200 | 20,200
Question: Look at the table. Then answer the question. At a price of $155, is there a shortage or a surplus?
Choose from the the options: [shortage, surplus]

# solution in Python:


def solution():
    """Table of :
    Price | Quantity demanded | Quantity supplied
    $155 | 22,600 | 5,800
    $275 | 20,500 | 9,400
    $395 | 18,400 | 13,000
    $515 | 16,300 | 16,600
    $635 | 14,200 | 20,200
    Question: Look at the table. Then answer the question. At a price of $155, is there a shortage or a surplus?
    Choose from the the options: [shortage, surplus]
    """
    quantity_demanded_price_155 = 22600
    quantity_supplied_price_155 = 5800
    if quantity_demanded_price_155 > quantity_supplied_price_155:
        result = 'shortage'
    else:
        result = 'surplus'
    return result





Table of "Cans of food collected":
Samir | 7
Kristen | 4
Dakota | 7
Jamie | 8
Maggie | 9
Question: Samir's class recorded how many cans of food each student collected for their canned food drive. What is the median of the numbers?

# solution in Python:


def solution():
    """Table of "Cans of food collected":
    Samir | 7
    Kristen | 4
    Dakota | 7
    Jamie | 8
    Maggie | 9
    Question: Samir's class recorded how many cans of food each student collected for their canned food drive. What is the median of the numbers?
    """
    cans = [7, 4, 5, 8, 9]
    cans = sorted(cans)
    middle1 = (len(cans) - 1) // 2
    middle2 = len(cans) // 2
    median = (cans[middle1] + cans[middle2]) / 2
    result = median
    return result





Table of "":
toy boat | $5.54
toy guitar | $8.23
set of juggling balls | $5.01
trivia game | $8.18
jigsaw puzzle | $5.30
toy dinosaur | $3.00
Question: Lorenzo has $13.50. Does he have enough to buy a toy guitar and a set of juggling balls?
Choose from the the options: ['yes', 'no']

# solution in Python:


def solution():
    """Table of "":
    toy boat | $5.54
    toy guitar | $8.23
    set of juggling balls | $5.01
    trivia game | $8.18
    jigsaw puzzle | $5.30
    toy dinosaur | $3.00
    Question: Lorenzo has $13.50. Does he have enough to buy a toy guitar and a set of juggling balls?
    Choose from the the options: ['yes', 'no']
    """
    guitar_price = 8.23
    juggling_balls = 5.01
    total_money = 13.5
    if total_money > juggling_balls + guitar_price:
        result = "yes"
    else:
        result = "no"
    return result
'''

# 5-shot
evaluate_prompt = '''
Table of "Roller coasters per amusement park":
Stem | Leaf 
1 | 0, 0, 1, 6, 8, 9
2 | 4, 4, 5, 7, 8, 8
3 | 1, 2, 4, 4, 9, 9
4 | 2, 3, 5, 6, 8, 9, 9
Question: Rodrigo found a list of the number of roller coasters at each amusement park in the state. How many amusement parks have fewer than 40 roller coasters?

# solution in Python:


def solution():
    """Table of "Roller coasters per amusement park":
    Stem | Leaf 
    1 | 0, 0, 1, 6, 8, 9
    2 | 4, 4, 5, 7, 8, 8
    3 | 1, 2, 4, 4, 9, 9
    4 | 2, 3, 5, 6, 8, 9, 9
    Question: Rodrigo found a list of the number of roller coasters at each amusement park in the state. How many amusement parks have fewer than 40 roller coasters?
    """
    number_of_roller_coasters_per_amusement_park = [10, 14, 14, 15, 16, 18, 19, 20, 24, 25, 26, 28, 29, 29, 29, 30, 34, 35, 36, 39, 40, 40, 40, 41, 42, 43, 44, 44, 45, 45, 46, 46, 47, 48, 48, 49, 49, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55, 56, 56, 57, 57, 58, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 65, 66, 66, 67, 67, 68, 68, 69, 69, 70, 70, 71, 71, 72, 72, 73, 73, 74, 74, 75, 75, 76, 76, 77, 77, 78, 78, 79, 79, 80, 80, 81, 81, 82, 82, 83, 83, 84, 84, 85, 85, 86, 86, 87, 87, 88, 88, 89, 89, 90, 90, 91, 91, 92, 92, 93, 93, 94, 94, 95, 95, 96, 96, 97, 97, 98, 98, 99, 99]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), beacuse values in the rows of Stem and Leaf represent the decimal and individual digits, respectively
    number_of_amusement_parks_with_fewer_than_40_roller_coasters = 0
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because this is to initialize the number_of_amusement_parks_with_fewer_than_40_roller_coasters
    for number_of_roller_coasters in number_of_roller_coasters_per_amusement_park:
        if number_of_roller_coasters < 40:
            number_of_amusement_parks_with_fewer_than_40_roller_coasters += 1
            # Is the above line of code:
            # (A) Correct
            # (B) Incorrect
            # The above line of code is: (A), but the value of number_of_roller_coasters_per_amusement_park is incorrect
    result = number_of_amusement_parks_with_fewer_than_40_roller_coasters
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of number_of_amusement_parks_with_fewer_than_40_roller_coasters is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Table of "People on the bus":
Day | Number of people
Thursday | 419
Friday | 454
Saturday | 451
Sunday | 441
Question: A bus driver paid attention to how many passengers her bus had each day. On which day did the bus have the fewest passengers?
Choose from the the options: [Thursday, Friday, Saturday, Sunday]

# solution in Python:


def solution():
    """Table of "People on the bus":
    Day | Number of people
    Thursday | 419
    Friday | 454
    Saturday | 451
    Sunday | 441
    Question: A bus driver paid attention to how many passengers her bus had each day. On which day did the bus have the fewest passengers?
    Choose from the the options: [Thursday, Friday, Saturday, Sunday]
    """
    number_of_people_on_the_bus = [419, 454, 451, 441]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    min_number_of_people_on_the_bus = min(number_of_people_on_the_bus)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    result = min_number_of_people_on_the_bus
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should take a further step to get the day corresponding to this min number of people
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Table of "":
x | y
14 | 1
15 | 8
16 | 15
Question: The table shows a function. Is the function linear or nonlinear?
Choose from the the options: [linear, nonlinear]

# solution in Python:


def solution():
    """Table of "":
    x | y
    14 | 1
    15 | 8
    16 | 15
    Question: The table shows a function. Is the function linear or nonlinear?
    Choose from the the options: [linear, nonlinear]
    """
    x = [14, 15, 16]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    y = [1, 8, 15]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    if y[0] == y[1] - y[2]:
        result = 'linear'
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (B), because should check both x and y as whether (y[0] - y[1]) / (x[0] - x[1]) == (y[0] - y[2]) / (x[0] - x[2])
    else:
        result = 'nonlinear'
        # Is the above line of code:
        # (A) Correct
        # (B) Incorrect
        # The above line of code is: (B)
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Table of "Flower garden":
Color | Daisies | Tulips
Yellow | 17 | 11
Pink | 4 | 10
White | 3 | 7
Question: Gardeners at the Elliott estate counted the number of flowers growing there. How many more pink flowers than white flowers are there?

# solution in Python:


def solution():
    """Table of "Flower garden":
    Color | Daisies | Tulips
    Yellow | 17 | 11
    Pink | 4 | 10
    White | 3 | 7
    Question: Gardeners at the Elliott estate counted the number of flowers growing there. How many more pink flowers than white flowers are there?
    """
    pink_flowers = 4
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), the number of pink flowers should be the sum of the numbers of pink Daisies and pink Tulips
    white_flowers = 3
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), the number of white flowers should be the sum of the numbers of white Daisies and white Tulips
    result = pink_flowers - white_flowers
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the values of pink_flowers and white_flowers are incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Table of "":
 | Fear of snakes | Fear of heights
Social worker | 5 | 4
Doctor | 6 | 2
Question: A college professor asked her Psychology students to complete a personality test. She paid special attention to her students' career goals and their greatest fears. What is the probability that a randomly selected student wants to be a doctor and has a fear of heights? Simplify any fractions.

# solution in Python:


def solution():
    """Table of "":
     | Fear of snakes | Fear of heights
    Social worker | 5 | 4
    Doctor | 6 | 2
    Question: A college professor asked her Psychology students to complete a personality test. She paid special attention to her students' career goals and their greatest fears. What is the probability that a randomly selected student wants to be a doctor and has a fear of heights? Simplify any fractions.
    """
    total_number_of_students = 11
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the total number should be the sum of all values, which should be 5 + 4 + 6 + 2 = 17
    number_of_students_who_want_to_be_doctor = 6
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because it should the sum of the whole line, which is 6 + 2 = 8
    number_of_students_who_have_fear_of_heights = 6
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because it should the sum of the whole column, which is 4 + 2 = 6
    number_of_students_who_want_to_be_doctor_and_have_fear_of_heights = 2
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    probability = number_of_students_who_want_to_be_doctor_and_have_fear_of_heights / total_number_of_students
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of total_number_of_students is incorrect
    result = probability
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of probability is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
'''

choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']

