import random


M_PLAN = False
M_MEMO = False
M_DO = True

T_EDGES = False
T_CORNERS = True

MARK_CYCLE = False
#ALGORITHM = "D2 L2 B2 D2 F2 D L2 U' B2 U' R2 L U2 B2 F U2 F D R' F' D"
ALGORITHM = "U' B2 D L2 U L2 D B2 U F L D R2 B D' F2 R2 B F2"
#ALGORITHM = "M2 U M2 U2 M2 U M2 U2"

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
        while True:
            letter = input_letter()
            if letter == ".": # Bro gave up, let's tell possible cubies
                print("Possible letters: "+" ".join(("/".join(cubies_letters[colors]) for colors in remaining_cubies)))
                continue
            elif letter == END_INPUT:
                print("It's not end")
                continue

            init_colors = stickersdata[letter]
            init_colors_sorted = tsort(init_colors)
            if init_colors_sorted in remaining_cubies:
                print("Well chosen")
                remaining_cubies.remove(init_colors_sorted)
                return init_colors,init_colors_sorted

            else:
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
                init_colors = stickersdata[cubies_letters[init_colors_sorted][0]]
        return init_colors,init_colors_sorted
    

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
            print(init_colors)
            last_of_cycle = not first_of_cycle and tsort(current_colors) == init_colors_sorted
            #print(colors2,last_of_cycle)
            posf = get_posf(current_colors)
            letter = stickersdata_rev[current_colors]
            print(letter)
            #print(f"Letter: {letter}")
            if not (first_cycle and (first_of_cycle or last_of_cycle)):
                if first_of_cycle:
                    letter = FirstOfCycle(letter)
                letters.append(letter)
                cycle_letters.append(letter)
                print(letter)

                    #print(f"letter: {letter}")
            if not (first_of_cycle or last_of_cycle):
                remaining_cubies.remove(tsort(current_colors))

            current_colors = get_at(current_colors,posf)
            first_of_cycle = False


        if M_PLAN:
            quiz_letters(cycle_letters if first_cycle else cycle_letters[1:],False)

        first_cycle = False
        # Here user input test
        pass
    if M_PLAN:
        quiz_letters_end()
    return letters

class FirstOfCycle(str):pass

def getc_edges(colors,posf):
    return (
        int(cube.state[colors[0]][posf[0][0]][posf[0][1]]),
        int(cube.state[colors[1]][posf[1][0]][posf[1][1]])
    )
def quiz_letters(letters,for_memo):
    if for_memo:
        print("Type edges letters you memorised")
    for letter in letters:
        letter_input = input_letter()
        if letter==letter_input:
            print("Correct")
        else:
            print(f"Incorrect: {letter}")
        if for_memo and M_DO:
            print("HELLO")
            is_right = do_letter(letter)
    if for_memo:
        quiz_letters_end()
def quiz_letters_end():
    letter_input = input_letter()
    if letter_input == END_INPUT:
        print("Correct")
    else:
        print(f"Incorrect, it's finished, (you had to type {END_INPUT!r})")

def do_letter(letter):
    user_input = input(f"Do {letter}")
    is_right = not user_input
    if is_right:
        print("Congrats")
    elif isinstance(letter,FirstOfCycle):
        print("It's normal it's failed, it's first of cycle")
        is_right = True
    else:
        print("Oh crap")
def test_do(letters):
    for letter in letters:
        do_letter(letter)

def memorize(letters):
    for letter in letters:
        input(f"Memorize {letter}")
        print("\n"*20)
if T_EDGES:
    edges_letters = get_letters((0,3),EDGES_STICKERSDATA,EDGES_CUBIESDATA)

if T_CORNERS:
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
        quiz_letters(edges_letters,True)

    if T_CORNERS:
        quiz_letters(corners_letters,True)

elif M_DO:
    if T_EDGES:
        print("Edges letters")
        test_do(edges_letters)

    if T_CORNERS:
        test_do(corners_letters)

