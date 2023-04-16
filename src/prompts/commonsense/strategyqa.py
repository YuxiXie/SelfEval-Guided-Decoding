# 6-shot
answer_prompt = '''
Q: Do hamsters provide food for any animals?

A:
Hamsters are prey animals.
Prey animals are food for predators.
Thus, hamsters provide food for some animals.
So the answer is yes.





Q: Could Brooke Shields succeed at University of Pennsylvania?

A:
Brooke Shields graduated from Princeton University.
According to US news, Princeton University and University of Pennsylvania are ranked as the number 1 and 6 national college, respectively.
This can indicate that Princeton University is about as academically rigorous as the University of Pennsylvania.
Thus, Brooke Shields could also succeed at University of Pennsylvania.
So the answer is yes.





Q: Hydrogen’s atomic number squared exceeds number of Spice Girls?

A:
Hydrogen is the first element and has an atomic number of one.
To square a number, you multiply it by itself, so one squared is one.
In comparison, the Spice Girls has five members.
Thus, Hydrogen’s atomic number squared is less than 5.
So the answer is no.





Q: Is it common to see frost during some college commencements?

A:
College commencement ceremonies often happen during the months of December, May, and sometimes June.
December is in the winter, so usually there can be frost.
Thus, there could be frost at some commencements and it is common.
So the answer is yes.





Q: Could a llama birth twice during War in Vietnam (1945-46)?

A:
The War in Vietnam (1945-46) lasted around 6 months.
The gestation period for a llama is 11 months, which is longer than 6 months.
Thus, it was impossible for a llama to give birth twice during the War in Vietnam.
So the answer is no.





Q: Would a pear sink in water?

A:
Objects only sink if they are denser than the surrounding fluid.
The density of water is about 1 g/cm^3.
In comparison, the density of a raw pear is about 0.59 g/cm^3, which is less than water.
Thus, a pear would float.
So the answer is no.
'''

# 4-shot
evaluate_prompt = '''
Q: While viewing "Scary Movie" is the viewer likely to experience an increase in adrenaline?

A:
Adrenaline is a hormone that is released when the body is under stress.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Scary movies are designed to make the viewer feel stressed.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because Scary Movie is a film that is a comedy take on horror, intended to make viewers laugh
Thus, the viewer is likely to experience an increase in adrenaline.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
So the answer is yes.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: Could a bee hummingbird balance a scale with a single pea on it?

A:
The bee hummingbird is the smallest bird in the world.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
The average weight of a bee hummingbird is about 1.8 grams.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
In comparison, the average weight of a pea is about 0.1 grams.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Thus, the bee hummingbird is heavier than a pea.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
So the answer is yes.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because the bee hummingbird is multiple times heavier than a pea, so it cannot balance





Q: Are the majority of Reddit users familiar with the Pledge of Allegiance?

A:
The Pledge of Allegiance was written in 1892.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
In comparison, Reddit was founded in 2005.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Thus, the Pledge of Allegiance was written 113 years before Reddit was founded.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Since the majority of Reddit users were born after 2005, it is unlikely that the majority of Reddit users are familiar with the Pledge of Allegiance.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because many Reddit users were born before 2005 as they need to be mature enough to use social media, and they can still be familiar with the Pledge of Allegianace as long as they're American
So the answer is no.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: Would a broadcast from Spirit make the news in 2020?

A:
Spirit is a rover that landed on Mars in 2004.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
It stopped working in 2010.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Thus, it is impossible for Spirit to broadcast in 2020.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because Spirit still made the news with its viral "final words" in 2019 even it stopped working in 2010
So the answer is no.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
'''

choice_prefix = ['# Is the above step of reasoning:', '# (A) Correct', '# (B) Incorrect', '# The above step of reasoning is:']


prev_answer_prompt = '''
Q: Do hamsters provide food for any animals?

A:
Hamsters are prey animals.
Prey animals are food for predators.
Thus, hamsters provide food for some animals.
So the answer is yes.





Q: Could Brooke Shields succeed at University of Pennsylvania?

A:
Brooke Shields went to Princeton University.
Princeton University is about as academically rigorous as the University of Pennsylvania.
Thus, Brooke Shields could also succeed at the University of Pennsylvania.
So the answer is yes.





Q: Yes or no: Hydrogen’s atomic number squared exceeds number of Spice Girls?

A:
Hydrogen has an atomic number of 1.
1 squared is 1. There are 5 Spice Girls.
Thus, Hydrogen’s atomic number squared is less than 5.
So the answer is no.





Q: Yes or no: Is it common to see frost during some college commencements?

A:
College commencement ceremonies can happen in December, May, and June.
December is in the winter, so there can be frost.
Thus, there could be frost at some commencements.
So the answer is yes.





Q: Yes or no: Could a llama birth twice during War in Vietnam (1945-46)?

A:
The War in Vietnam was 6 months.
The gestation period for a llama is 11 months, which is more than 6 months.
Thus, a llama could not give birth twice during the War in Vietnam.
So the answer is no.





Q: Yes or no: Would a pear sink in water?

A:
The density of a pear is about 0.6g/cm3, which is less than water.
Objects less dense than water float.
Thus, a pear would float.
So the answer is no.
'''


prev_evaluate_prompt = '''
Q: While viewing "Scary Movie" is the viewer likely to experience an increase in adrenaline?

A:
Adrenaline is a hormone that is released when the body is under stress.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Scary movies are designed to make the viewer feel stressed.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because Scary Movie is a film that is a comedy take on horror, intended to make viewers laugh but not afraid
Thus, the viewer is likely to experience an increase in adrenaline.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
So the answer is yes.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: Could a bee hummingbird balance a scale with a single pea on it?

A:
The bee hummingbird is the smallest bird in the world.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
The average weight of a bee hummingbird is about 1.8 grams.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
In comparison, the average weight of a pea is about 0.1 grams.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Thus, the bee hummingbird is heavier than a pea.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
So the answer is yes.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because the bee hummingbird is multiple times heavier than a pea, so it cannot balance





Q: Would a broadcast from Spirit make the news in 2020?

A:
Spirit is a rover that landed on Mars in 2004.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
It stopped working in 2010.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Thus, it is impossible for Spirit to broadcast in 2020.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because Spirit still made the news with its viral "final words" in 2019 even it stopped working in 2010
So the answer is no.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
'''
