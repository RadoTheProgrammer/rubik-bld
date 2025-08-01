
M_PLAN = True
M_MEMO = True
M_DO = False

T_EDGES = True
T_CORNERS = False

ALGORITHM = "B D B2 R2 B2 D' R2 F2 U F2 D' B2 L' D2 F2 U' B F2 U' L B'"


#ALGORITHM = "D2 L2 B2 D2 F2 D L2 U' B2 U' R2 L U2 B2 F U2 F D R' F' D"

ALGORITHM = "M2 U M2 U2 M2 U M2"
ALGORITHM = "R U R' U' R' F R2 U' R' U' R U R' F'"

import random
import pandas as pd
import time


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
cube.apply(ALGORITHM)
print(cube)
def input_letter():
    return input("Letter?")

def get_tt_delta():
    global tt
    new_tt = time.time()
    tt_delta = new_tt-tt
    tt = new_tt
    return tt_delta

def get_letters(buffer_colors,stickersdata,cubiesdata,EoC):
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
        planMistake = None
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

            init_colors = stickersdata[letter_input]
            init_colors_sorted = tsort(init_colors)
            if init_colors_sorted in remaining_cubies:
                print("Well chosen")
                remaining_cubies.remove(init_colors_sorted)
                return init_colors,init_colors_sorted,planMistake

            else:
                planMistake = letter_input
                print("Incorrect, choose another one")

    def get_init_colors():
        if first_cycle:
            init_colors = buffer_colors
            init_colors_sorted = tsort(init_colors)
            planMistake = None
        else:
            if M_PLAN: # ask for init letter
                init_colors,init_colors_sorted,planMistake = input_init_colors()
            else:
                init_colors_sorted = remaining_cubies.pop() # type: ignore # if plan mode, the user choose
                init_colors = stickersdata[cubies_letters[init_colors_sorted][0]]
                planMistake = None
        return init_colors,init_colors_sorted,planMistake
    
    def new_row(letter,isFoC,planMistake):
        global tt
        print(df.dtypes)
        df.loc[len(df)] = {"Letter":letter,"EoC":EoC,"IsFoC":isFoC,"PlanMistake":planMistake,"PlanTime":get_tt_delta()} # type: ignore
        print(df)
        print(df.dtypes)

    def test_letter(letter):
        if M_PLAN:
            letter_input = input_letter()
            if letter==letter_input:
                planMistake = None
                print("Correct")
            else:
                planMistake = letter_input
                print(f"Incorrect: {letter}")
        else:
            planMistake = None
        new_row(letter,False,planMistake)

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
        init_colors,init_colors_sorted,planMistake = get_init_colors()

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
                    new_row(letter,True,planMistake)
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
def memo_recall(df):

    print("Type edges letters you memorised")
    for i, row in df.iterrows():
        letter = row["Letter"]
        letter_input = input_letter()
        if letter==letter_input:
            memoMistake = None
            print("Correct")
        else:
            memoMistake = letter_input
            print(f"Incorrect: {letter}")
        if M_DO:
            print("HELLO")
            do_row(i, row)
        print(df.dtypes)
        df.loc[i,"MemoMistake"] = memoMistake
        df.loc[i,"MemoRecallTime"] = get_tt_delta()

def quiz_letters_end():
    letter_input = input_letter()
    if letter_input == END_INPUT:
        print("Correct")
    else:
        print(f"Incorrect, it's finished, (you had to type {END_INPUT!r})")

def do_row(i,row):
    letter = row["Letter"]
    if letter==END_INPUT:
        return
    isFoC = row["IsFoC"]
    user_input = input(f"Do {letter}")
    is_right = not user_input
    if is_right:
        print("Congrats")
    elif isFoC:
        print("It's normal it's failed, it's first of cycle")
        is_right = True
    else:
        print("Oh crap")
    doMistake = user_input if not is_right else None
    df.loc[i,"DoMistake"] = doMistake
    df.loc[i,"DoTime"] = get_tt_delta()

def test_do(df):
    for i, row in df.iterrows():
        do_row(i,row)

def memorize(df):
    for i,row in df.iterrows():
        input(f"Memorize {row["Letter"]}")
        df.loc[i,"MemoTime"] = get_tt_delta()
        print("\n"*20)
        print(row)
        print(df)


dtypes = {
    "Letter": "string",
    "EoC": "int8",
    "IsFoC": "bool"
}
if M_PLAN:
    dtypes["PlanMistake"] = "string"
    dtypes["PlanTime"] = "float64"

if M_MEMO:
    dtypes["MemoMistake"] = "string"
    dtypes["MemoTime"] = "float64"
    dtypes["MemoRecallTime"] = "float64"

if M_DO:
    dtypes["DoMistake"] = "string"
    dtypes["DoTime"] = "float64"

df = pd.DataFrame({col: pd.Series(dtype=dt) for col, dt in dtypes.items()})

tt = time.time()
if T_EDGES:
    edges_letters = get_letters((0,3),EDGES_STICKERSDATA,EDGES_CUBIESDATA,EOC_EDGES)
    has_parity = len(edges_letters)%2
    print(f"Has parity: {has_parity}")
    df_edges = df[df["EoC"]==EOC_EDGES]
if T_CORNERS:
    corners_letters = get_letters((1,0,4),CORNERS_STICKERS,CORNERS_CUBIES,EOC_CORNERS)
    df_corners = df[df["EoC"]==EOC_CORNERS]

if M_MEMO:
    if not M_PLAN:
        if T_EDGES:
            print("Edges letters to memorise")
            memorize(df_edges)

        if T_CORNERS:
            print("Corners letters to memorise")
            memorize(df_corners)

    if T_EDGES:
        memo_recall(df_edges)

    if T_CORNERS:
        memo_recall(df_corners)

elif M_DO:
    if T_EDGES:
        print("Edges letters")
        test_do(df_edges)

    if T_CORNERS:
        print("Corners letters")
        test_do(df_corners)

