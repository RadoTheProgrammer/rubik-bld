import random
"""
This script simulates edge piece cycles for a Rubik's Cube using a sticker-letter mapping.
It uses a solved cube state and iterates through edge cycles, tracking visited cubies and their corresponding letters.
Variables:
    init_colors (tuple[int, int]): The current buffer colors, representing the sticker colors of the edge being cycled.
        This variable is always a tuple of two integers, which correspond to face indices/colors.
        (Type annotation is provided to assist static analysis tools like VS Code Pylance.)
Functions and Logic:
    - EDGES_STICKERS: Dictionary mapping letters to edge sticker coordinates.
    - EDGES_STICKERS_REV: Reverse mapping from sticker coordinates to letter and positions.
    - CUBIES: Set of all unique edge cubies, represented as sorted tuples of face indices.
    - The main loop cycles through all edge cubies, following the permutation cycles and recording the letter sequence.
Note:
    To avoid Pylance type errors, annotate `init_colors` as `tuple[int, int]`:
        init_colors: tuple[int, int] = (0, 3)
"""

M_PLAN = False
M_MEMO = True
M_DO = True

T_EDGES = True
T_CORNERS = True

MARK_CYCLE = False
#ALGORITHM = "D2 L2 B2 D2 F2 D L2 U' B2 U' R2 L U2 B2 F U2 F D R' F' D"
ALGORITHM = "M2 U M2 U2 M2 U M2"


EDGES_STICKERS = {
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

EDGES_CUBIES = {
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
    "A":((0,0,0),(4,0,2),(1,0,0)),
    "B":((0,0,2),(3,0,2),(4,0,0)),
    "C":((0,2,2),(2,0,2),(3,0,0)),
    "D":((0,2,0),(1,0,2),(2,0,0)),
    "E":((1,0,0),(0,0,0),(4,0,2)),
    "F":((1,0,2),(2,0,0),(0,2,0)),
    "G":((1,2,2),(5,0,0),(2,2,0)),
    "H":((1,2,0),(4,2,2),(5,2,0)),
    "I":((2,0,0),(0,2,0),(1,0,2)),
    "J":((2,0,2),(3,0,0),(0,2,2)),
    "K":((2,2,2),(5,0,2),(3,2,0)),
    "L":((2,2,0),(1,2,2),(5,0,0)),
    "M":((3,0,0),(0,2,2),(2,0,2)),
    "N":((3,0,2),(4,0,0),(0,0,2)),
    "O":((3,2,2),(5,2,2),(4,2,0)),
    "P":((3,2,0),(2,2,2),(5,0,2)),
    "Q":((4,0,0),(0,0,2),(3,0,2)),
    "R":((4,0,2),(1,0,0),(0,0,0)),
    "S":((4,2,2),(5,2,0),(1,2,0)),
    "T":((4,2,0),(3,2,2),(5,2,2)),
    "U":((5,0,0),(2,2,0),(1,2,2)),
    "V":((5,0,2),(3,2,0),(2,2,2)),
    "W":((5,2,2),(4,2,0),(3,2,2)),
    "X":((5,2,0),(1,2,0),(4,2,2))
}


def tsort(colors: tuple[int, ...]) -> tuple[int, ...]:
    """Sorts the input tuple and returns a tuple of the same length and type."""
    return tuple(sorted(colors))


#CUBIES = set([(1,2),2])

import rubik_impl
cube = rubik_impl.Cube.solved(rubik_impl.C_NUMBERS)
cube.apply(ALGORITHM)
print(cube)

def get_letters(buffer_colors,stickersdata,cubiesdata):
    """
    func_getlp: func to get letter and pos from colors
    func_getc: func to get colors from pos
    """
    def input_letter(*possible_answers):
        while True:
            letter=input("Letter?")
            if letter in all_letters+possible_answers:
                return letter
            
    def get_posf(colors):
        """
        Get pos on face
        """
        colors_sorted = tsort(colors)
        posf_sorted = cubiesdata[colors_sorted]
        posf = tuple(posf_sorted[colors_sorted.index(c)] for c in colors)
        return posf
    
    def get_at(colors,posf):
        return tuple(int(cube.state[color][p[0]][p[1]]) for color,p in zip(colors,posf))

    def remove_solved_cubies():
        buffer_colors_sorted = tsort(buffer_colors)
        for colors in cubiesdata:
            posf = get_posf(colors) # type: ignore # posf = pos on face
            colors2 = get_at(colors,posf)
            if colors in (colors2,buffer_colors_sorted):
                remaining_cubies.remove(colors)
                print(colors)
    def input_init_colors():
        while True:
            letter = input_letter(".")
            if letter == ".": # Bro gave up, let's tell possible cubies
                print("Possible letters: "+" ".join(("/".join(cubies_letters[colors]) for colors in remaining_cubies)))
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
                init_colors = init_colors_sorted = remaining_cubies.pop() # type: ignore # if plan mode, the user choose
        return init_colors,init_colors_sorted
    
    print(get_posf((4,1)))
    first_cycle = True
    letters = []
    stickersdata_rev = {value:key for key,value in stickersdata.items()}
    cubies_letters = {key:[] for key in cubiesdata}
    print(cubies_letters)
    for letter,colors in stickersdata.items():
        cubies_letters[tsort(colors)].append(letter)

    print(cubies_letters)

    all_letters = tuple(stickersdata)
    remaining_cubies = list(cubiesdata)

    remove_solved_cubies()

    
            #print(f"Removed cubie: {colors}")
    print(remaining_cubies)
    while remaining_cubies:
        init_colors,init_colors_sorted = get_init_colors()

        current_colors = init_colors
    
        #print(init_colors)
        first_of_cycle = True
        last_of_cycle = False
        cycle_letters = []
        while not last_of_cycle: # 1 cycle
            last_of_cycle = not first_of_cycle and tsort(current_colors) == init_colors_sorted
            #print(colors2,last_of_cycle)
            posf = get_posf(current_colors)
            letter = stickersdata_rev[current_colors]
            #print(f"Letter: {letter}")
            if not (first_cycle and (first_of_cycle or last_of_cycle)):
                if first_of_cycle and MARK_CYCLE:
                    letter = letter.lower()
                letters.append(letter)
                cycle_letters.append(letter)

                    #print(f"letter: {letter}")
            if not (first_of_cycle or last_of_cycle):
                remaining_cubies.remove(current_colors)

            current_colors = get_at(current_colors,posf)
            first_of_cycle = False


        if M_PLAN:
            for letter in (cycle_letters if first_cycle else cycle_letters[1:]):
                letter_input=input_letter()
                if letter_input == letter:
                    print("Correct")
                else:
                    print(f"Incorrect: {letter}")
        first_cycle = False
        # Here user input test
        pass
    return letters



def getc_edges(colors,posf):
    return (
        int(cube.state[colors[0]][posf[0][0]][posf[0][1]]),
        int(cube.state[colors[1]][posf[1][0]][posf[1][1]])
    )

if T_EDGES:
    print(get_letters((0,3),EDGES_STICKERS,EDGES_CUBIES))

