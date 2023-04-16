# 8-shot
answer_prompt = '''
Q: Is the following sentence plausible?
“Kyle Palmieri was called for slashing.”

A:
Kyle Palmieri is a hockey player.
Being called for slashing is part of hockey.
So the answer is yes.





Q: Is the following sentence plausible?
“Joao Moutinho caught the screen pass in the NFC championship.”

A:
Joao Moutinho is a soccer player.
The NFC championship is part of American football, not soccer.
So the answer is no.





Q: Is the following sentence plausible?
“Carson Wentz set the pick and roll.”

A:
Carson Wentz is an American football player.
Pick and roll is part of basketball, not football.
So the answer is no.





Q: Is the following sentence plausible?
“Jonas Valanciunas beat the buzzer.”

A:
Jonas Valanciunas is a basketball player.
Beating the buzzer is part of basketball.
So the answer is yes.





Q: Is the following sentence plausible?
“Jamel Murray was perfect from the line.”

A:
Jamal Murray is a basketball player.
Being perfect from the line is part of basketball.
So the answer is yes.





Q: Is the following sentence plausible?
“Sam Darnold passed the puck.”

A:
Sam Darnold is a American football player.
Passing the puck is part of hockey, not American football.
So the answer is no.





Q: Is the following sentence plausible?
“Draymond Green threw a touchdown.”

A:
Draymond Green is an basketball player.
Throwing a touchdown is part of football, not basketball.
So the answer is no.





Q: Is the following sentence plausible?
“Malcolm Brogdon banked the shot in.”

A:
Malcolm Brogdon is a basketball player.
Banking the shot in is part of basketball.
So the answer is yes.
'''

# 2-shot
evaluate_prompt = '''
Q: Is the following sentence plausible?
“Robin Lehner launched the desperation heave”

A:
Robin Lehner is a hockey player.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because Robin Lehner is a goaltender which is different from a player
Launching the desperation heave is part of hockey.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because launching the desperation heave is for player, not goaltender
So the answer is yes.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect





Q: Is the following sentence plausible?
“Giancarlo Stanton launched a triple”

A:
Giancarlo Stanton is a baseball player.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because Giancarlo Stanton is a baseball outfielder in fact, which may be different from being a player
Launching a triple is part of baseball.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (B), because launching a triple is for player, not outfielder
So the answer is yes.
# Is the above step of reasoning:
# (A) Correct
# (B) Incorrect
# The above step of reasoning is: (A), but the previous step is incorrect
'''


choice_prefix = ['# Is the above step of reasoning:', '# (A) Correct', '# (B) Incorrect', '# The above step of reasoning is:']

