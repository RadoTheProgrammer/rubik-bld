
M_PLAN  = 1
M_MEMO  = 0
M_DO    = 0

T_EDGES = True
T_CORNERS = True

SCRAMBLE = "B' D2 R' U2 B2 R2 U' R' B D F2 L2 U2 D F2 B2 D L2 D F2"

FILE_DATA_SINGLE = "data-single.csv"

FILE_DATA_ALL = "data-all.csv"


DISABLE_MEMO_END = False
import random
import pandas as pd
import time
import os


RESET_DATA = False
END_INPUT = "end"
EDGES_STICKERSDATA = {
    "A":(0,4),
    "B":(0,3),
    "C":(0,2),
    "D":(0,1),
    "E":(1,0),
    "F":(1,2),
    "G":(1,5),
    "H":(1,4),
    "I":(2,0),
    "J":(2,3),
    "K":(2,5),
    "L":(2,1),
    "M":(3,0),
    "N":(3,4),
    "O":(3,5),
    "P":(3,2),
    "Q":(4,0),
    "R":(4,1),
    "S":(4,5),
    "T":(4,3),
    "U":(5,2),
    "V":(5,3),
    "W":(5,4),
    "X":(5,1)
}

EDGES_CUBIESDATA = {
    (0,4): ((0,1),(0,1)),
    (0,3): ((1,2),(0,1)),
    (0,2): ((2,1),(0,1)),
    (0,1): ((1,0),(0,1)),
    (1,4): ((1,0),(1,2)),
    (1,2): ((1,2),(1,0)),
    (2,3): ((1,2),(1,0)),
    (3,4): ((1,2),(1,0)),
    (1,5): ((2,1),(1,0)),
    (2,5): ((2,1),(0,1)),
    (3,5): ((2,1),(1,2)),
    (4,5): ((2,1),(2,1))
}


CORNERS_STICKERS = {
    "A":(0,4,1),
    "B":(0,3,4),
    "C":(0,2,3),
    "D":(0,1,2),
    "E":(1,0,4),
    "F":(1,2,0),
    "G":(1,5,2),
    "H":(1,4,5),
    "I":(2,0,1),
    "J":(2,3,0),
    "K":(2,5,3),
    "L":(2,1,5),
    "M":(3,0,2),
    "N":(3,4,0),
    "O":(3,5,4),
    "P":(3,2,5),
    "Q":(4,0,3),
    "R":(4,1,0),
    "S":(4,5,1),
    "T":(4,3,5),
    "U":(5,2,1),
    "V":(5,3,2),
    "W":(5,4,3),
    "X":(5,1,4)
}

CORNERS_CUBIES = {
    (0,1,4): ((0,0),(0,0),(0,2)),
    (0,1,2): ((2,0),(0,2),(0,0)),
    (0,2,3): ((2,2),(0,2),(0,0)),
    (0,3,4): ((0,2),(0,2),(0,0)),
    (1,2,5): ((2,2),(2,0),(0,0)),
    (2,3,5): ((2,2),(2,0),(0,2)),
    (3,4,5): ((2,2),(2,0),(2,2)),
    (1,4,5): ((2,0),(2,2),(2,0))
}

EOC_EDGES = 0
EOC_CORNERS = 1

def tsort(colors: tuple[int, ...]) -> tuple[int, ...]:
    """Sorts the input tuple and returns a tuple of the same length and type."""
    return tuple(sorted(colors))


#CUBIES = set([(1,2),2])

import rubik_impl
cube = rubik_impl.Cube.solved(rubik_impl.C_NUMBERS)
cube.apply(SCRAMBLE)
print(cube)
def input_letter():
    letter=""
    while not letter:
        letter = input("Letter?")
    return letter

def get_tt_delta():
    global tt
    new_tt = time.time()
    tt_delta = new_tt-tt
    tt = new_tt
    return round(tt_delta,3)

def get_letters(buffer_colors,stickersdata,cubiesdata):
    """
    func_getlp: func to get letter and pos from colors
    func_getc: func to get colors from pos
    """

            
    def get_posf(colors):
        """
        Get pos on face
        """
        colors_sorted = tsort(colors)
        posf_sorted = cubiesdata[colors_sorted]
        posf = tuple(posf_sorted[colors_sorted.index(c)] for c in colors)
        return posf
    
    def get_at(colors,posf):
        if colors ==(4,5,1):
            pass
        colors = tuple(int(cube.state[color][p[0]][p[1]]) for color,p in zip(colors,posf))
        return colors
    def remove_solved_cubies():
        buffer_colors_sorted = tsort(buffer_colors)
        for colors in cubiesdata:
            posf = get_posf(colors) # type: ignore # posf = pos on face
            colors2 = get_at(colors,posf)
            if colors in (colors2,buffer_colors_sorted):
                remaining_cubies.remove(colors)


    def input_init_colors():
        planMistake = ""
        while True:
            letter_input = input_letter()
            if letter_input == ".": # Bro gave up, let's tell possible cubies
                planMistake = letter_input
                print("Possible letters: "+" ".join(("/".join(cubies_letters[colors]) for colors in remaining_cubies)))
                continue
            elif letter_input == END_INPUT:
                planMistake = letter_input
                print("It's not end")
                continue
            try: # Check if it's a valid letter
                init_colors = stickersdata[letter_input]
            except:
                continue
            init_colors_sorted = tsort(init_colors)
            if init_colors_sorted in remaining_cubies:
                print("Well chosen")
                dfd["Letter"].append(letter_input)
                dfd["IsFoC"].append(True)
                dfd["PlanMistake"].append(planMistake)
                dfd["PlanTime"].append(get_tt_delta())
                if M_MEMO:
                    memorize_letter(letter_input)
                remaining_cubies.remove(init_colors_sorted)
                return init_colors,init_colors_sorted

            else:
                planMistake = letter_input
                print("Incorrect, choose another one")

    def get_init_colors():
        if first_cycle:
            init_colors = buffer_colors
            init_colors_sorted = tsort(init_colors)
            
        else:
            if M_PLAN: # ask for init letter
                init_colors,init_colors_sorted = input_init_colors()
            else:
                init_colors_sorted = remaining_cubies.pop() # type: ignore # if plan mode, the user choose
                letter = cubies_letters[init_colors_sorted][0]
                init_colors = stickersdata[cubies_letters[init_colors_sorted][0]]
                dfd["Letter"].append(letter)
                dfd["IsFoC"].append(True)
        return init_colors,init_colors_sorted


    def test_letter(letter):
        dfd["Letter"].append(letter)
        dfd["IsFoC"].append(False)
        if M_PLAN:
            letter_input = input_letter()
            if letter==letter_input:
                planMistake = ""
                print("Correct")
            else:
                planMistake = letter_input
                print(f"Incorrect: {letter}")
            dfd["PlanMistake"].append(planMistake)
            dfd["PlanTime"].append(get_tt_delta())
            if M_MEMO:
                memorize_letter(letter)



    first_cycle = True
    letters = []
    stickersdata_rev = {value:key for key,value in stickersdata.items()}
    cubies_letters = {key:[] for key in cubiesdata}

    for letter,colors in stickersdata.items():
        cubies_letters[tsort(colors)].append(letter)



    all_letters = tuple(stickersdata)
    remaining_cubies = list(cubiesdata)

    remove_solved_cubies()

    
            #print(f"Removed cubie: {colors}")

    while remaining_cubies:
        init_colors,init_colors_sorted = get_init_colors()

        current_colors = init_colors
    
        #print(init_colors)
        first_of_cycle = True
        last_of_cycle = False
        cycle_letters = []
        while not last_of_cycle: # 1 cycle
            #print(init_colors)
            last_of_cycle = not first_of_cycle and tsort(current_colors) == init_colors_sorted
            #print(colors2,last_of_cycle)
            posf = get_posf(current_colors)
            letter = stickersdata_rev[current_colors]
            #print(letter)
            #print(f"Letter: {letter}")
            if not (first_cycle and (first_of_cycle or last_of_cycle)):
                if first_of_cycle:
                    letter = FirstOfCycle(letter)
                else:
                    test_letter(letter)

                letters.append(letter)
                cycle_letters.append(letter)
                #print(letter)

                    #print(f"letter: {letter}")
            if not (first_of_cycle or last_of_cycle):
                remaining_cubies.remove(tsort(current_colors))

            current_colors = get_at(current_colors,posf)
            first_of_cycle = False



        first_cycle = False
        # Here user input test
        pass
    test_letter(END_INPUT)
    return letters

class FirstOfCycle(str):pass

def getc_edges(colors,posf):
    return (
        int(cube.state[colors[0]][posf[0][0]][posf[0][1]]),
        int(cube.state[colors[1]][posf[1][0]][posf[1][1]])
    )
def memo_recall(letters):
    for letter in letters+[END_INPUT]:
        if letter == END_INPUT and DISABLE_MEMO_END:
            memoMistake =""
            memoRecallTime = 0
        else:

            letter_input = input_letter()
            if letter==letter_input:
                memoMistake = ""
                print("Correct")
            else:
                memoMistake = letter_input
                print(f"Incorrect: {letter}")

        dfd["MemoMistake"].append(memoMistake)
        dfd["MemoRecallTime"].append(get_tt_delta())

        if M_DO:
            #print("HELLO")
            do_letter(letter)


def do_letter(letter):
    if letter==END_INPUT:
        user_input=""
        doTime = 0
    else:
        user_input = input(f"Do {letter}")

        if not user_input:
            print("Congrats")
        elif isinstance(letter,FirstOfCycle):
            print("It's normal it's failed, it's first of cycle")
            user_input = ""
        else:
            print("Oh crap")
        doTime = get_tt_delta()
    dfd["DoMistake"].append(user_input)
    dfd["DoTime"].append(doTime)


def test_do(letters):
    for letter in letters+[END_INPUT]:
        do_letter(letter)

def memorize_letter(letter):
    if letter==END_INPUT:
        dfd["MemoTime"].append(0)
    else:
        input(f"Memorize {letter}")
        print("\n"*20)
        dfd["MemoTime"].append(get_tt_delta())

def memorize(letters):
    for letter in letters:
        memorize_letter(letter)

    dfd["MemoTime"].append(0) # for end time

def do_parity():
    if has_parity:
        input("Do parity")

columns = ["Letter","IsFoC"]
if M_PLAN:
    columns += ["PlanMistake","PlanTime"]


if M_MEMO:
    columns += ["MemoMistake","MemoTime","MemoRecallTime"]

if M_DO:
    columns += ["DoMistake","DoTime"]


dfd = {column:[] for column in columns}


tt = time.time()
now = pd.Timestamp.now()

if T_EDGES:
    if M_PLAN:
        print("Plan edges letters")
    edges_letters = get_letters((0,3),EDGES_STICKERSDATA,EDGES_CUBIESDATA)
    has_parity = len(edges_letters)%2

if T_CORNERS:
    if M_PLAN:
        print("Plan corners letters")
    corners_letters = get_letters((1,0,4),CORNERS_STICKERS,CORNERS_CUBIES)

if M_MEMO:
    if not M_PLAN:
        if T_EDGES:
            print("Edges letters to memorise")
            memorize(edges_letters)

        if T_CORNERS:
            print("Corners letters to memorise")
            memorize(corners_letters)

    if T_EDGES:
        print("Type edges letters you memorised")
        memo_recall(edges_letters)

    if M_DO:
        do_parity()
    if T_CORNERS:
        print("Type corner letters you memorised")
        memo_recall(corners_letters)

elif M_DO:
    if T_EDGES:
        print("Do edges letters")
        test_do(edges_letters)

    do_parity()
    if T_CORNERS:
        print("Do corners letters")
        test_do(corners_letters)

#print(dfd)
df = pd.DataFrame(dfd)
df.to_csv(FILE_DATA_SINGLE,index=False)
print(df)

def any(col):
    return int(df[col].any())

def timeSum(col):
    return round(df[col].sum(),3)
planMistake = any("PlanMistake") if M_PLAN else ""
planTime = timeSum("PlanTime") if M_PLAN else 0

memoMistake = any("MemoMistake") if M_MEMO else ""
memoTime = timeSum("MemoTime") if M_MEMO else 0
memoRecallTime = timeSum("MemoRecallTime") if M_MEMO else 0

doMistake = any("DoMistake") if M_DO else ""
doTime = timeSum("DoTime") if M_DO else 0

totalTime = round(planTime + memoTime + memoRecallTime + doTime,3)

if not os.path.exists(FILE_DATA_ALL) or RESET_DATA:
    with open(FILE_DATA_ALL,"w") as f:
        f.write("Datetime,Scramble,TotalTime,PlanMistake,MemoMistake,DoMistake,PlanTime,MemoTime,MemoRecallTime,DoTime\n")

with open(FILE_DATA_ALL,"a") as f:
    f.write(f"{now},{SCRAMBLE},{totalTime},{planMistake},{memoMistake},{doMistake},{planTime},{memoTime},{memoRecallTime},{doTime}\n")

