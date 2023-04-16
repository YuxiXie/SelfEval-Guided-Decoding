'''
# Write Python Code to solve the following questions. Store your result as a variable named 'ans'.
from sympy import Symbol
from sympy import simplify
import math
from sympy import solve_it
# solve_it(equations, variable): solving the equations and return the variable value.
'''

# 8-shot
code_prompt = '''
Question: In a flight of 600 km, an aircraft was slowed down due to bad weather. Its average speed for the trip was reduced by 200 km/hr and the time of flight increased by 30 minutes. The duration of the flight is:
Answer Choices:
A)1 hour
B)2 hours
C)3 hours
D)4 hours
E)5 hours

# solution in Python:


def solution():
    """Question: In a flight of 600 km, an aircraft was slowed down due to bad weather. Its average speed for the trip was reduced by 200 km/hr and the time of flight increased by 30 minutes. The duration of the flight is:
    Answer Choices:
    A)1 hour
    B)2 hours
    C)3 hours
    D)4 hours
    E)5 hours
    """
    duration = Symbol('duration', positive=True)
    delay = 30 / 60
    total_disntace = 600
    original_speed = total_disntace / duration
    reduced_speed = total_disntace / (duration + delay)
    solution = solve_it(original_speed - reduced_speed - 200, duration)
    duration = solution[duration]
    result = duration
    return result





Question: M men agree to purchase a gift for Rs. D. If 3 men drop out how much more will each have to contribute towards the purchase of the gift?
Answer Choices:
A)D/(M-3)
B)MD/3
C)M/(D-3)
D)3D/(M2-3M)
E)None of these

# solution in Python:


def solution():
    """Question: M men agree to purchase a gift for Rs. D. If 3 men drop out how much more will each have to contribute towards the purchase of the gift?
    Answer Choices:
    A)D/(M-3)
    B)MD/3
    C)M/(D-3)
    D)3D/(M2-3M)
    E)None of these
    """
    M = Symbol('M')
    D = Symbol('D')
    cost_before_dropout = D / M
    cost_after_dropout = D / (M - 3)
    cost_increase = simplify(cost_after_dropout - cost_before_dropout)
    result = cost_increase
    return result





Question: A sum of money at simple interest amounts to Rs. 815 in 3 years and to Rs. 854 in 4 years. The sum is:
Answer Choices:
A)Rs. 650
B)Rs. 690
C)Rs. 698
D)Rs. 700
E)None of these

# solution in Python:


def solution():
    """Question: A sum of money at simple interest amounts to Rs. 815 in 3 years and to Rs. 854 in 4 years. The sum is:
    Answer Choices:
    A)Rs. 650
    B)Rs. 690
    C)Rs. 698
    D)Rs. 700
    E)None of these
    """
    deposit = Symbol('deposit', positive=True)
    interest = Symbol('interest', positive=True)
    money_in_3_years = deposit + 3 * interest
    money_in_4_years = deposit + 4 * interest
    solution = solve_it([money_in_3_years - 815, money_in_4_years - 854], [deposit, interest])
    deposit = solution[deposit]
    result = deposit
    return result





Question: 35% of the employees of a company are men. 60% of the men in the company speak French and 40% of the employees of the company speak French. What is % of the women in the company who do not speak French?
Answer Choices:
A)4%
B)10%
C)96%
D)90.12%
E)70.77%

# solution in Python:


def solution():
    """Question: 35% of the employees of a company are men. 60% of the men in the company speak French and 40% of the employees of the company speak French. What is % of the women in the company who do not speak French?
    Answer Choices:
    A)4%
    B)10%
    C)96%
    D)90.12%
    E)70.77%
    """
    num_women = 65
    men_speaking_french = 0.6 * 35
    employees_speaking_french = 0.4 * 100
    women_speaking_french = employees_speaking_french - men_speaking_french
    women_not_speaking_french = num_women - women_speaking_french
    percent_of_women_not_speaking_french = women_not_speaking_french / num_women
    result = percent_of_women_not_speaking_french
    return result





Question: In one hour, a boat goes 11 km/hr along the stream and 5 km/hr against the stream. The speed of the boat in still water (in km/hr) is:
Answer Choices:
A)4 kmph
B)5 kmph
C)6 kmph
D)7 kmph
E)8 kmph

# solution in Python:


def solution():
    """Question: In one hour, a boat goes 11 km/hr along the stream and 5 km/hr against the stream. The speed of the boat in still water (in km/hr) is:
    Answer Choices:
    A)4 kmph
    B)5 kmph
    C)6 kmph
    D)7 kmph
    E)8 kmph
    """
    boat_speed = Symbol('boat_speed', positive=True)
    stream_speed = Symbol('stream_speed', positive=True)
    along_stream_speed = 11
    against_stream_speed = 5
    solution = solve_it([boat_speed + stream_speed - along_stream_speed, boat_speed - stream_speed - against_stream_speed], [boat_speed, stream_speed])
    boat_speed = solution[boat_speed]
    result = boat_speed
    return result





Question: The difference between simple interest and C.I. at the same rate for Rs.5000 for 2 years in Rs.72. The rate of interest is?
Answer Choices:
A)10%
B)12%
C)6%
D)8%
E)4%

# solution in Python:


def solution():
    """Question: The difference between simple interest and C.I. at the same rate for Rs.5000 for 2 years in Rs.72. The rate of interest is?
    Answer Choices:
    A)10%
    B)12%
    C)6%
    D)8%
    E)4%
    """
    interest_rate = Symbol('interest_rate', positive=True)
    amount = 5000
    amount_with_simple_interest = amount * (1 + 2 * interest_rate / 100)
    amount_with_compound_interest = amount * (1 + interest_rate / 100) ** 2
    solution = solve_it(amount_with_compound_interest - amount_with_simple_interest - 72, interest_rate)
    interest_rate = solution[interest_rate]
    result = interest_rate
    return result





Question: The area of a rectangle is 15 square centimeters and the perimeter is 16 centimeters. What are the dimensions of the rectangle?
Answer Choices:
A)2&4
B)3&5
C)4&6
D)5&7
E)6&8

# solution in Python:


def solution():
    """Question: The area of a rectangle is 15 square centimeters and the perimeter is 16 centimeters. What are the dimensions of the rectangle?
    Answer Choices:
    A)2&4
    B)3&5
    C)4&6
    D)5&7
    E)6&8
    """
    width = Symbol('width', positive=True)
    height = Symbol('height', positive=True)
    area = 15
    permimeter = 16
    solution = solve_it([width * height - area, 2 * (width + height) - permimeter], [width, height])
    dimensions = (solution[width], solution[height])
    result = dimensions
    return result





Question: If a = -0.7, which of the following is true?
Answer Choices:
A)a < a^2 < a^3
B)a^2 < a < a^3
C)a < a^3 < a^2
D)a^3 < a < a^2
E)a^2 < a^3 < a

# solution in Python:


def solution():
    """Question: If a = -0.7, which of the following is true?
    Answer Choices:
    A)a < a^2 < a^3
    B)a^2 < a < a^3
    C)a < a^3 < a^2
    D)a^3 < a < a^2
    E)a^2 < a^3 < a
    """
    a = -0.7
    A = a < a ** 2 < a ** 3
    B = a ** 2 < a < a ** 3
    C = a < a ** 3 < a ** 2
    D = a ** 3 < a < a ** 2
    E = a ** 2 < a ** 3 < a
    if A:
        result = 'a < a^2 < a^3'
    elif B:
        result = 'a^2 < a < a^3'
    elif C:
        result = 'a < a^3 < a^2'
    elif D:
        result = 'a^3 < a < a^2'
    elif E:
        result = 'a^2 < a^3 < a'
    else:
        result = None
    return result
'''

# 5-shot
evaluate_prompt = '''
Question: Two trains of length 150 m and 200 m are 100 m apart. They start moving towards each other on parallel tracks, at speeds 54 kmph and 72 kmph. In how much time will the trains cross each other?
Answer Choices:
A)100/7 sec
B)80/7 sec
C)57/7 sec
D)110/7 sec
E)50/7 sec

# solution in Python:


def solution():
    """Question: Two trains of length 150 m and 200 m are 100 m apart. They start moving towards each other on parallel tracks, at speeds 54 kmph and 72 kmph. In how much time will the trains cross each other?
    Answer Choices:
    A)100/7 sec
    B)80/7 sec
    C)57/7 sec
    D)110/7 sec
    E)50/7 sec
    """
    train_1_speed = 54 / 60
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    train_2_speed = 72 / 60
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    distance_between_trains = 100
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    train_1_length = 150
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    train_2_length = 200
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    time_to_cross = distance_between_trains / (train_1_speed + train_2_speed)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because to cross each other, the total distance should also contain the train length
    result = time_to_cross
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the final result should be in seconds, and the value of time_to_cross is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Question: Brand A coffee costs twice as much as brand B coffee. If a certain blend is 1/4 brand A and 3/4 brand B. what fraction of the cost of the blend is Brand A?
Answer Choices:
A)1/3
B)2/5
C)1/2
D)2/3
E)3/4

# solution in Python:


def solution():
    """Question: Brand A coffee costs twice as much as brand B coffee. If a certain blend is 1/4 brand A and 3/4 brand B. what fraction of the cost of the blend is Brand A?
    Answer Choices:
    A)1/3
    B)2/5
    C)1/2
    D)2/3
    E)3/4
    """
    brand_a_cost = Symbol('brand_a_cost', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    brand_b_cost = Symbol('brand_b_cost', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    blend_cost = Symbol('blend_cost', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    brand_a_fraction = 1 / 4
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    brand_b_fraction = 3 / 4
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    solution = solve_it([brand_a_cost - 2 * brand_b_cost, blend_cost - brand_a_cost * brand_a_fraction - brand_b_cost * brand_b_fraction], [brand_a_cost, brand_b_cost, blend_cost])
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because the three equations reflect the correct relations among the three variables
    brand_a_cost = solution[brand_a_cost]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    blend_cost = solution[blend_cost]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    brand_a_fraction_of_blend_cost = brand_a_cost / blend_cost
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the fraction of Brand A should also be considered, so brand_a_fraction_of_blend_cost = brand_a_cost * brand_a_fraction / blend_cost
    result = brand_a_fraction_of_blend_cost
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of brand_a_fraction_of_blend_cost is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Question: The length of a rectangular floor is more than its breadth by 500%. If Rs. 324 is required to paint the floor at the rate of Rs. 6 per sq m, then what would be the length of the floor?
Answer Choices:
A)24.6m.
B)23.4m.
C)22.5m.
D)23.8m.
E)25.5m.

# solution in Python:


def solution():
    """Question: The length of a rectangular floor is more than its breadth by 500%. If Rs. 324 is required to paint the floor at the rate of Rs. 6 per sq m, then what would be the length of the floor?
    Answer Choices:
    A)24.6m.
    B)23.4m.
    C)22.5m.
    D)23.8m.
    E)25.5m.
    """
    length = Symbol('length', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    breadth = Symbol('breadth', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    cost = 324
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    rate = 6
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    solution = solve_it([length * breadth - cost / rate, length - 5 * breadth], [length, breadth])
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because length is more than breadth by 5 times, which should be (length - breadth) - 5 * breadth
    length = solution[length]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of length is incorrect
    result = length
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of length is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Question: A vessel is filled with liquid, 3 parts of which are water and 5 parts syrup. How much of the mixture must be drawn off and replaced with water so that the mixture may be half water and half syrup?
Answer Choices:
A)1/5
B)2/5
C)3/5
D)4/5
E)None of them

# solution in Python:


def solution():
    """Question: A vessel is filled with liquid, 3 parts of which are water and 5 parts syrup. How much of the mixture must be drawn off and replaced with water so that the mixture may be half water and half syrup?
    Answer Choices:
    A)1/5
    B)2/5
    C)3/5
    D)4/5
    E)None of them
    """
    water_ratio = 3
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    syrup_ratio = 5
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    total_ratio = water_ratio + syrup_ratio
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    water_ratio_after_replacement = total_ratio / 2
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    water_ratio_to_be_replaced = water_ratio_after_replacement - water_ratio
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the syrup ratio will be decreased at the same time, so water_ratio_to_be_replaced = (water_ratio_after_replacement - water_ratio) / 2
    water_ratio_to_be_replaced_percent = water_ratio_to_be_replaced / total_ratio
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of water_ratio_to_be_replaced is incorrect
    result = water_ratio_to_be_replaced_percent
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of water_ratio_to_be_replaced_percent is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Question: Share Rs.4200 among John, Jose & Binoy in the ration 2 : 4 : 6.Find the amount received by John?
Answer Choices:
A)900
B)980
C)1200
D)1240
E)1400

# solution in Python:


def solution():
    """Question: Share Rs.4200 among John, Jose & Binoy in the ration 2 : 4 : 6.Find the amount received by John?
    Answer Choices:
    A)900
    B)980
    C)1200
    D)1240
    E)1400
    """
    john = Symbol('john', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    jose = Symbol('jose', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    binoy = Symbol('binoy', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    total_amount = 4200
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    solution = solve_it([john + jose + binoy - total_amount, 2 * john - 4 * jose, 4 * jose - 6 * binoy], [john, jose, binoy])
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because as the ratio, it should be john / jose - 2 / 4 and jose / binoy - 4 / 6
    john = solution[john]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of john is incorrect
    result = john
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of john is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
'''

# 4-shot
evaluate_prompt_prev = '''
Question: If the true discount on a certain sum due 6 months hence at 15% is Rs.120. What is the banker's discount on the same sum for the same time and at the same rate?
Answer Choices:
A)Rs. 119
B)Rs. 129
C)Rs. 131
D)Rs. 139
E)None

# solution in Python:


def solution():
    """Question: If the true discount on a certain sum due 6 months hence at 15% is Rs.120. What is the banker's discount on the same sum for the same time and at the same rate?
    Answer Choices:
    A)Rs. 119
    B)Rs. 129
    C)Rs. 131
    D)Rs. 139
    E)None
    """
    principal = Symbol('principal', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but it is irrelevant to this question
    interest_rate = 0.15
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    time = 6 / 12
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    true_discount = 120
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    bankers_discount = principal * (1 - interest_rate * time) - principal
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because bankers_discount equals to B.G. + true_discount = true_discount * interest_rate * time + true_discount
    solution = solve_it(bankers_discount - true_discount, principal)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because bankers_discount and true_discount are different
    principal = solution[principal]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the solution is incorrect and it is irrelevant to this question
    result = principal
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the result should be bankers_discount
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Question: Find avrg speed if a man travels at speed of 15km/hr up and 28km/hr dawn at an altitude of 230m.
Answer Choices:
A)25.8
B)19.5
C)18.0
D)12.2

# solution in Python:


def solution():
    """Question: Find avrg speed if a man travels at speed of 15km/hr up and 28km/hr down at an altitude of 230m.
    Answer Choices:
    A)25.8
    B)19.5
    C)18.0
    D)12.2
    """
    up_speed = 15
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    down_speed = 28
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    altitude = 230
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    total_time = altitude / up_speed + altitude / down_speed
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because the up and down are separate
    total_distance = altitude * 2
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because it includes up and down
    average_speed = total_distance / total_time
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    result = average_speed
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)





Question: Which of the following numbers is between 1⁄3 and 1⁄2?
Answer Choices:
A).45
B).32
C).29
D).22
E).20

# solution in Python:


def solution():
    """Question: Which of the following numbers is between 1⁄3 and 1⁄2?
    Answer Choices:
    A).45
    B).32
    C).29
    D).22
    E).20
    """
    result = 0.32
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B)
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Question: 10 women can complete a work in 7 days and 10 children take 14 days to complete the work. How many days will 5 women and 10 children take to complete the work?
Answer Choices:
A)10
B)5
C)7
D)14
E)8

# solution in Python:


def solution():
    """Question: 10 women can complete a work in 7 days and 10 children take 14 days to complete the work. How many days will 5 women and 10 children take to complete the work?
    Answer Choices:
    A)10
    B)5
    C)7
    D)14
    E)8
    """
    num_women = 5
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    num_children = 10
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    women_work_rate = 10 / 7
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should compute the work rate per woman, which is 1 / 7 / 10
    children_work_rate = 10 / 14
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should compute the work rate per child, which is 1 / 14 / 10
    total_work_rate = num_women * women_work_rate + num_children * children_work_rate
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the values of women_work_rate and children_work_rate are incorrect
    days_to_complete_work = 1 / total_work_rate
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of total_work_rate is incorrect
    result = days_to_complete_work
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of days_to_complete_work is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
'''

removed = [
'''Question: If the true discount on a certain sum due 6 months hence at 15% is Rs.120. What is the banker's discount on the same sum for the same time and at the same rate?
Answer Choices:
A)Rs. 119
B)Rs. 129
C)Rs. 131
D)Rs. 139
E)None

# solution in Python:


def solution():
    """Question: If the true discount on a certain sum due 6 months hence at 15% is Rs.120. What is the banker's discount on the same sum for the same time and at the same rate?
    Answer Choices:
    A)Rs. 119
    B)Rs. 129
    C)Rs. 131
    D)Rs. 139
    E)None
    """
    principal = Symbol('principal', positive=True)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but it is irrelevant to this question
    interest_rate = 0.15
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    time = 6 / 12
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    true_discount = 120
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    bankers_discount = principal * (1 - interest_rate * time) - principal
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because bankers_discount equals to B.G. + true_discount = true_discount * interest_rate * time + true_discount
    solution = solve_it(bankers_discount - true_discount, principal)
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because bankers_discount and true_discount are different
    principal = solution[principal]
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the solution is incorrect and it is irrelevant to this question
    result = principal
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because the result should be bankers_discount
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
''',
'''
Question: Which of the following numbers is between 1⁄3 and 1⁄2?
Answer Choices:
A).45
B).32
C).29
D).22
E).20

# solution in Python:


def solution():
    """Question: Which of the following numbers is between 1⁄3 and 1⁄2?
    Answer Choices:
    A).45
    B).32
    C).29
    D).22
    E).20
    """
    result = 0.45
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
''',
'''
Question: Find avrg speed if a man travels at speed of 15km/hr up and 28km/hr dawn at an altitude of 230m.
Answer Choices:
A)25.8
B)19.5
C)18.0
D)12.2

# solution in Python:


def solution():
    """Question: Find avrg speed if a man travels at speed of 15km/hr up and 28km/hr down at an altitude of 230m.
    Answer Choices:
    A)25.8
    B)19.5
    C)18.0
    D)12.2
    """
    up_speed = 15
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    down_speed = 28
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    altitude = 230
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    total_time = altitude / up_speed + altitude / down_speed
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because the up and down are separate
    total_distance = altitude * 2
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), because it includes up and down
    average_speed = total_distance / total_time
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    result = average_speed
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
''',
'''
Question: Which of the following numbers is between 1⁄3 and 1⁄2?
Answer Choices:
A).45
B).32
C).29
D).22
E).20

# solution in Python:


def solution():
    """Question: Which of the following numbers is between 1⁄3 and 1⁄2?
    Answer Choices:
    A).45
    B).32
    C).29
    D).22
    E).20
    """
    result = 0.32
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B)
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
''',
'''
Question: 10 women can complete a work in 7 days and 10 children take 14 days to complete the work. How many days will 5 women and 10 children take to complete the work?
Answer Choices:
A)10
B)5
C)7
D)14
E)8

# solution in Python:


def solution():
    """Question: 10 women can complete a work in 7 days and 10 children take 14 days to complete the work. How many days will 5 women and 10 children take to complete the work?
    Answer Choices:
    A)10
    B)5
    C)7
    D)14
    E)8
    """
    num_women = 5
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    num_children = 10
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    women_work_rate = 10 / 7
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should compute the work rate per woman, which is 1 / 7 / 10
    children_work_rate = 10 / 14
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should compute the work rate per child, which is 1 / 14 / 10
    total_work_rate = num_women * women_work_rate + num_children * children_work_rate
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the values of women_work_rate and children_work_rate are incorrect
    days_to_complete_work = 1 / total_work_rate
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of total_work_rate is incorrect
    result = days_to_complete_work
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of days_to_complete_work is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
''',
]

choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']



# 7-shot
choice_prompt = '''
Find the closest options based on the question and prediction.

Question: A company produces 420 units of a particular computer component every month, at a production cost to the company of $110 per component, and sells all of the components by the end of each month. What is the minimum selling price per component that will guarantee that the yearly profit (revenue from sales minus production costs) will be at least $626,400 ?
Answer Choices:
A)226
B)230
C)240
D)260
E)280
Prediction: 234.28571428571428
Closest Option: B

Question: In how many ways can the letters of the word "PROBLEC" be rearranged to make 7 letter words such that none of the letters repeat?
Answer Choices:
A)2!
B)3!
C)7!
D)8!
E)9!
Prediction: 5040
Closest Option: C

Question: An exam is given in a certain class. The average (arithmetic mean) of the highest score and the lowest score is equal to x. If the average score for the entire class is equal to y and there are z students in the class, where z > 5, then in terms of x, y, and z, what is the average score for the class excluding the highest and lowest scorers?
Answer Choices:
A)(zy – 2x)/z
B)(zy – 2)/z
C)(zx – y)/(z – 2)
D)(zy – 2x)/(z -2)
E)(zy – x)/(z + 2)
Prediction: (-2*x + y*z)/(z - 2)
Closest Option: D

Question: Find the total no. of distinct bike no.'s that can beformed using 2 letters followed by 2 no.'s. How many letters need to be distinct?
Answer Choices:
A)65000
B)64543
C)74325
D)74453
E)97656
Prediction = 67600
Closest Option: A

Question: A wire in the shape of rectangle of length 27 cm and breadth 17 cm is rebent to form a square. What will be the measure of each side?
Answer Choices:
A)9
B)11
C)22
D)25
E)31
Prediction = [-21.42428528562855, 21.42428528562855]
Closest Option: C

Question: A point on the edge of a fan blade that is rotating in a plane 10 centimeters from the center of the fan. What is the distance traveled, in centimeters, by this point after 30 seconds when the fan runs at the rate of 300 revolutions per minutes?
Answer Choices:
A)750pi
B)1500pi
C)1875pi
D)3000pi
E)7500pi
Prediction: 9424.77
Closest Option: D

Question: Sum of two consecutive even terms lacks by 98 from their product. Find the sum of these numbers?
Answer Choices:
A)18
B)24
C)32
D)36
E)None
Prediction: 98
Closest Option: E
'''

