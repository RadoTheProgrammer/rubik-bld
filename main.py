
M_PLAN  = 0
M_MEMO  = 0
M_DO    = 0

T_EDGES = True
T_CORNERS = True

SCRAMBLE = "F2 D2 B2 U B2 L2 D' R2 D R2 U2 F' R' D' L B' D2 L2 D' R' B'"
SCRAMBLE = "M2 U M2 U2 M2 U M2"
DIR_RECONSTRUCTIONS = "my-reconstructions"

FILE_DATA_ALL = "my-data.csv"


DISABLE_MEMO_END = False
import random
import pandas as pd
import time
import os


RESET_DATA = False
END_LETTER = "END"
PARITY_LETTER = "PARITY"

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
    return letter.upper()

def get_tt_delta():
    global tt
    new_tt = time.time()
    tt_delta = new_tt-tt
    tt = new_tt
    return round(tt_delta,3)

def plan_memo(buffer_colors,stickersdata,cubiesdata,possible_parity):
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
            elif letter_input == END_LETTER:
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
                if M_MEMO:
                    memorize_letter(letter)
        return init_colors,init_colors_sorted


    def test_letter(letter):
        dfd["Letter"].append(letter)
        dfd["IsFoC"].append(False)
        if M_PLAN:
            if letter==PARITY_LETTER:
                planMistake = ""
                planTime = 0
            else:
                letter_input = input_letter()
                if letter==letter_input:
                    planMistake = ""
                    print("Correct")
                else:
                    planMistake = letter_input
                    print(f"Incorrect: {letter}")
                planTime = get_tt_delta()

            dfd["PlanMistake"].append(planMistake)
            dfd["PlanTime"].append(planTime)
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
                if not first_of_cycle:
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
    test_letter(END_LETTER)
    group_letters = []
    has_parity = False
    for letter in letters:
        if has_parity:
            group_letters[-1] += letter
        else:
            group_letters.append(letter)
        has_parity = not has_parity

    if possible_parity and has_parity:
        test_letter(PARITY_LETTER)
    return " ".join(group_letters)

class FirstOfCycle(str):pass

def getc_edges(colors,posf):
    return (
        int(cube.state[colors[0]][posf[0][0]][posf[0][1]]),
        int(cube.state[colors[1]][posf[1][0]][posf[1][1]])
    )
def memorecall_do():
    for letter,isFoC in zip(dfd["Letter"],dfd["IsFoC"]):
        if M_MEMO:
            if letter == END_LETTER and DISABLE_MEMO_END:
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
            do_letter(letter,isFoC)


def do_letter(letter,isFoC):
    if letter==END_LETTER:
        user_input=""
        doTime = 0
        print("\n"*10)
    else:
        user_input = input(f"Do {letter}")

        if not user_input:
            print("Congrats")
        elif isFoC:
            print("It's normal it's failed, it's first of cycle")
            user_input = ""
        else:
            print("Oh crap")
        doTime = get_tt_delta()
    dfd["DoMistake"].append(user_input)
    dfd["DoTime"].append(doTime)


def do():
    for letter in dfd["Letter"]:
        do_letter(letter)

def memorize_letter(letter):
    if letter in (END_LETTER,PARITY_LETTER):
        dfd["MemoTime"].append(0)
    else:
        input(f"Memorize {letter}")
        print("\n"*20)
        dfd["MemoTime"].append(get_tt_delta())


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
    print("Edges letters")
    edges_letters = plan_memo((0,3),EDGES_STICKERSDATA,EDGES_CUBIESDATA,1)

if T_CORNERS:
    print("Corners letters")
    corners_letters = plan_memo((1,0,4),CORNERS_STICKERS,CORNERS_CUBIES,0)


memorecall_do()



df = pd.DataFrame(dfd)
# save reconstruction
if not os.path.exists(DIR_RECONSTRUCTIONS):
    os.mkdir(DIR_RECONSTRUCTIONS)
file_reconstruction = os.path.join(DIR_RECONSTRUCTIONS,f"{now}.csv")
df.to_csv(file_reconstruction,index=False)
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
        f.write("Datetime,Scramble,TotalTime,PlanMistake,MemoMistake,DoMistake,PlanTime,MemoTime,MemoRecallTime,DoTime,EdgesLetters,CornersLetters,Comment\n")

with open(FILE_DATA_ALL,"a") as f:
    f.write(f"{now},{SCRAMBLE},{totalTime},{planMistake},{memoMistake},{doMistake},{planTime},{memoTime},{memoRecallTime},{doTime},{edges_letters},{corners_letters},\n")

