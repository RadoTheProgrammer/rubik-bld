A tool to practice and train Rubik's cube blindfolded with the Pochmann method.

Note: this project is only focused on practicing, not on learning.

## Why this project
The problem with Rubik's cube blindfolded is that if you do a single error, you mess up everything, and get a DNF.

But the worst thing is that you can't even know where you messed up, if it was during planification, memorisation or execution.

I used to film myself solving, but it never really worked with me.

With this project, you gets more aware of what you did right, and the mistake you made, it regularly check your step, to see if something is wrong.

## How it works

My project focus on constant checking
For me there is 3 steps, or parts during the blindfolded solve:
1. **plan**: Planification, that means determining the letters to solve, for example "FP QG HT UD".
2. **memo**: memorisation, it implies memorizing the sequence of letters I planned before
3. **do**: simply executing the algorithms associated with the letters

My program is designed to verify and test each of those 3 steps, and check for mistakes.

For plan, it check if you determine the right letter, for memo, it check if you memorize properly, and for do of course it check if it's executed properly.

## How to use
First, install python if you haven't, and clone this repository.

Then install the requirements `pip install requirements.txt`

And then, open the file `main.py`, you can edit the parameters at the very first lines.
`ALGORITHM` is to put the scramble algorithm.

`M_PLAN`, `M_MEMO`, `M_DO` are for choosing the modes you want to train, it toggles between True and False, and you can choose multiples

Toggle `T_EDGES` and `T_CORNERS` to choose if you want to train for edges or corners, they are both True by defaults.

### M_PLAN
This mode is to train the planification.

It check you to determine the right letter.

When you are beginning a new cycle and you don't remember which are the remaining cubies, type "."

When you finished the letters, it's normal if it asks you again, it's to check if you noticed that you are at the end, simply type `end`

### M_MEMO
This mode is to train the memorization.

You get a quick look on each letter, and then it asks you to recall the letters.

When you finished the letters, it's normal

### M_DO
This mode is to train the execution.

You just apply the algorithm of the letter it tells you to apply. And you verify if the corresponding cubie is solved, if it is, leave it blank and tape enter, if it's not, write something (anything) so you know