# 8-shot
answer_prompt = '''
Locations = [counter, table, user, trash, bowl, drawer].
Objects = [7up, apple, kettle chips, tea, multigrain chips, coke, lime soda, jalapeno chips, rice chips, orange, grapefruit soda, pepsi, redbull, energy bar, sponge, water, sea salt chips, sprite can, banana, bag of chips].
The robot can pick up items with pick(object) and put down items with put(object) as well as find objects or locations with find(). The robot can also open and close the drawer with open(drawer) and close(drawer), respectively. The robot can only understand the explicit locations and objects listed.





Human: I’m hungry, can you bring me some chips.

Explanation: The user is hungry and has asked for chips. There are several types of chips available, I will bring the user the kettle chips.
Plan:
1. find(kettle chips),
2. pick(kettle chips),
3. find(user),
4. put(kettle chips),
5. done().





Human: How would you move the grapefruit drink from the table to the counter?

Explanation: The user has asked me to move the grapefruit drink to the counter.
Plan:
1. find(table),
2. find(grapefruit soda),
3. pick(grapefruit soda),
4. find(counter),
5. put(grapefruit soda),
6. done().





Human: How would you bring me some snacks?

Explanation: The user has asked for snacks, I will choose two items and bring them. I will bring jalapeno chips and an apple.
Plan:
1. find(jalapeno chips),
2. pick(jalapeno chips),
3. find(user),
4. put(jalapeno chips),
5. find(apple),
6. pick(apple),
7. find(user),
8. put(apple),
9. done().





Human: How would you bring me something to eat that isn’t a fruit?

Explanation: The user has asked for a food that isn’t a fruit, I will bring an energy bar to them.
Plan:
1. find(energy bar),
2. pick(energy bar),
3. find(user),
4. put(energy bar),
5. done().





Human: How would you put the rice chips in the bowl and then move the tea to the table?

Explanation: The user has asked me to do two tasks, I will do one and then the other.
Plan:
1. find(rice chips),
2. pick(rice chips),
3. find(bowl),
4. put(rice chips),
5. find(tea),
6. pick(tea),
7. find(table),
8. put(tea),
9. done().





Human: How would you throw away a redbull?

Explanation: The user has asked me to throw away the redbull, I will move it to the trash.
Plan:
1. find(redbull),
2. pick(redbull),
3. find(trash),
4. put(redbull),
5. done().





Human: Bring me a drink.

Explanation: The user has asked for a drink and there are many options. I will bring them a water.
Plan:
1. find(water),
2. pick(water),
3. find(user),
4. put(water),
5. done().





Human: Put the coke into the drawer.

Explanation: The user has asked me to put the coke into the drawer. To put it into the drawer, I need to open the drawer first. Then when finished, I need to close the drawer.
Plan:
1. find(coke),
2. pick(coke),
3. find(drawer),
4. put(coke),
5. open(drawer),
6. pick(coke),
7. put(coke),
8. close(drawer),
9. done().
'''

# 
evaluate_prompt = '''
Human: Can you bring all the snacks on the table?

Explanation: The user has asked me to bring all the snacks on the table. There are many snacks on the table, I will bring the kettle chips and rice chips.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but still need to check until the table is empty
Plan:
1. find(kettle chips),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because should first go to the table with find(table) before getting anything
2. pick(kettle chips),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
3. find(user),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
4. put(kettle chips),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
5. find(rice chips),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because should go to the table with find(table) before getting anything
6. pick(rice chips),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
7. find(user),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
8. put(rice chips),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
9. done().
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because there is one step missing, which is to check whether the table is empty with find(table)





Human: Could you get me something refreshing?

Explanation: The user has asked for something refreshing, I will bring them a sprite can.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because should bring water since it is more refreshing 
Plan:
1. find(sprite can),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
2. pick(sprite can),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
3. find(user),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
4. put(sprite can),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
5. done().
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)





Human: Lift and hold the coke can up.

Explanation: The user has asked me to lift the coke can up. I will pick it up and then put it down.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because there is no need to put it down
Plan:
1. find(coke),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but this step can be skipped 
2. pick(coke),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
3. put(coke),
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because there is no need to put it down
4. done().
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
'''


choice_prefix = ['# Is the above step of reasoning:', '# (A) Correct', '# (B) Incorrect', '# The above step of reasoning is:']

