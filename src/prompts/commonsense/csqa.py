# 7-shot
answer_prompt = '''
Q: What do people use to absorb extra ink from a fountain pen?
Answer Choices:
(a) shirt pocket
(b) calligrapher’s hand
(c) inkwell
(d) desk drawer
(e) blotter

A:
The answer must be an item that can absorb ink.
Of the above choices, only blotters are used to absorb ink.
So the answer is (e).





Q: What home entertainment equipment requires cable?
Answer Choices:
(a) radio shack
(b) substation
(c) television
(d) cabinet

A:
The answer must require cable.
Of the above choices, only television requires cable.
So the answer is (c).





Q: The fox walked from the city into the forest, what was it looking for?
Answer Choices:
(a) pretty flowers
(b) hen house
(c) natural habitat
(d) storybook

A:
The answer must be something in the forest.
Of the above choices, only natural habitat is in the forest.
So the answer is (b).





Q: Sammy wanted to go to where the people were. Where might he go?
Answer Choices:
(a) populated areas
(b) race track
(c) desert
(d) apartment
(e) roadblock

A:
The answer must be a place with a lot of people.
Of the above choices, only populated areas have a lot of people.
So the answer is (a).





Q: Where do you put your grapes just before checking out?
Answer Choices:
(a) mouth
(b) grocery cart
(c)super market
(d) fruit basket
(e) fruit market

A:
The answer should be the place where grocery items are placed before checking out.
Of the above choices, grocery cart makes the most sense for holding grocery items.
So the answer is (b).





Q: Google Maps and other highway and street GPS services have replaced what?
Answer Choices:
(a) united states
(b) mexico
(c) countryside
(d) atlas

A:
The answer must be something that used to do what Google Maps and GPS services do, which is to give directions.
Of the above choices, only atlases are used to give directions.
So the answer is (d).





Q: Before getting a divorce, what did the wife feel who was doing all the work?
Answer Choices:
(a) harder
(b) anguish
(c) bitterness
(d) tears
(e) sadness

A:
The answer should be the feeling of someone getting divorced who was doing all the work.
Of the above choices, the closest feeling is bitterness.
So the answer is (c).
'''


# 3-shot
evaluate_prompt = '''
Q: John's took his appointment book with him to a checkup but couldn't find it anywhere. He looked and he looked but he didn't know where it was.  It wasn't until he bought a new one, went home, took a shower that he found it.  Where was it?
Answer Choices:
(a) office supply store
(b) wallet
(c) doctor's office
(d) handbag
(e) pocket

A:
The answer must be a place where John could have put his appointment book.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because it fails to reason out that John will check the place when taking a shower (taking off clothes)
Of the above choices, only wallet makes sense.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because wallet is too small to put his appointment book, and it cannot be the only one which makes sense (pocket is also plausible)
So the answer is (b).
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: It might make you think of buckeyes, but an apple tree also grows well in which of the fifty?
Answer Choices:
(a) spain
(b) ohio
(c) orchid
(d) bible
(e) washington state

A:
The answer must be a state where an apple tree grows well.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because it fails to reason out the place might be known for buckeyes
Of the above choices, only Washington State is known for growing apples.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but Washington State is not the only place where apple trees grow well (Ohio is also plausible)
So the answer is (e).
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: How might one go about instituting a civil action?
Answer Choices:
(a) disobedience
(b) court case
(c) trial
(d) anger
(e) complications

A:
The answer must be something that is done in a court case.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Of the above choices, only trial is done in a court case.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because the court case itself is more suitable here
So the answer is (c).
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
'''


# 3-shot
prev_evaluate_prompt = '''
Q: John's took his appointment book with him to a checkup but couldn't find it anywhere. He looked and he looked but he didn't know where it was.  It wasn't until he bought a new one, went home, took a shower that he found it.  Where was it?
Answer Choices:
(a) office supply store
(b) wallet
(c) doctor's office
(d) handbag
(e) pocket

A:
The answer must be a place where John could have put his appointment book.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because the reasoning should be more specific, like the answer must be a place where John will check when taking a shower
Of the above choices, only wallet makes sense.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because the reasoning should be more specific and directly inferred from the first step
So the answer is (b).
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: It might make you think of buckeyes, but an apple tree also grows well in which of the fifty?
Answer Choices:
(a) spain
(b) ohio
(c) orchid
(d) bible
(e) washington state

A:
The answer must be a state where an apple tree grows well.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because the important concept of buckeyes is missing, making this inference incomplete
Of the above choices, only Washington State is known for growing apples.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
So the answer is (e).
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: How might one go about instituting a civil action?
Answer Choices:
(a) disobedience
(b) court case
(c) trial
(d) anger
(e) complications

A:
The answer must be something that is done in a court case.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
Of the above choices, only trial is done in a court case.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because the court case itself is more suitable here
So the answer is (c).
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
'''

to_discard = [
'''
Q: Sammy wanted to go to where the people were. Where might he go?
Answer Choices:
(a) populated areas
(b) race track
(c) desert
(d) apartment
(e) roadblock

A:
The answer must be a place with a lot of people.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), because a place where the people were means there must be a lot of people
Of the above choices, only populated areas have a lot of people.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), because except for populated areas, there're many people in the other choices
So the answer is (a).
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A)
''',
]

choice_prefix = ['# Is the above step of reasoning:', '# (A) Correct', '# (B) Incorrect', '# The above step of reasoning is:']

