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


EDGES_STICKERS = {
    "A":((0,0,1),(4,0,1)),
    "B":((0,1,2),(3,0,1)),
    "C":((0,2,1),(2,0,1)),
    "D":((0,1,0),(1,0,1)),
    "E":((1,0,1),(0,1,0)),
    "F":((1,1,2),(2,1,0)),
    "G":((1,2,1),(5,1,0)),
    "H":((1,1,0),(4,1,2)),
    "I":((2,0,1),(0,2,1)),
    "J":((2,1,2),(3,1,0)),
    "K":((2,2,1),(5,0,1)),
    "L":((2,1,0),(1,1,2)),
    "M":((3,0,1),(0,1,2)),
    "N":((3,1,2),(4,1,0)),
    "O":((3,2,1),(5,1,2)),
    "P":((3,1,0),(2,1,2)),
    "Q":((4,0,1),(0,0,1)),
    "R":((4,1,2),(1,1,0)),
    "S":((4,2,1),(5,2,1)),
    "T":((4,1,0),(3,1,2)),
    "U":((5,0,1),(2,2,1)),
    "V":((5,1,2),(3,2,1)),
    "W":((5,2,1),(4,2,1)),
    "X":((5,1,0),(1,2,1))
}


def input_letter(*possible_answers):
    while True:
        letter=input("Letter?")
        if letter in ALPHABET+possible_answers:
            return letter

def tsort(colors: tuple[int, ...]) -> tuple[int, ...]:
    """Sorts the input tuple and returns a tuple of the same length and type."""
    return tuple(sorted(colors))

ALPHABET = tuple(EDGES_STICKERS.keys())
EDGES_STICKERS_REV = {(value[0][0],value[1][0]):(key,value[0][1:],value[1][1:]) for key,value in EDGES_STICKERS.items()}

BUFFER_COLORS = (0,3)
CUBIES = set((tsort(key)) for key in EDGES_STICKERS_REV.keys()) # type: ignore


INPUT_MODE = True
MARK_CYCLE = False
#CUBIES = set([(1,2),2])

import rubik_impl
cube = rubik_impl.Cube.solved(rubik_impl.C_NUMBERS)
#cube.apply("R U R' U' R' F R R U' R' U' R U R' F'")
#cube.apply("R R L L U R R L L U U R R L L U R R L L")
#cube.apply("L F' R' F' L2 B U2 B' L2 U2 L2 R2 B2 R2 L F' L2 U' F' L R")
cube.apply("D2 L2 B2 D2 F2 D L2 U' B2 U' R2 L U2 B2 F U2 F D R' F' D")
print(cube)

first_cycle = True
letters = []
remaining_cubies = CUBIES.copy()

# remove solved cubies
buffer_colors_sorted = tsort(BUFFER_COLORS)
for colors in CUBIES:
    letter,pos0,pos1 = EDGES_STICKERS_REV[colors] # type: ignore
    colors2 = (
        int(cube.state[colors[0]][pos0[0]][pos0[1]]),
        int(cube.state[colors[1]][pos1[0]][pos1[1]])
    )
    if colors in (colors2,buffer_colors_sorted):
        remaining_cubies.remove(colors)
        #print(f"Removed cubie: {colors}")
while remaining_cubies:
    if first_cycle:
        init_colors = BUFFER_COLORS
    else:
        if INPUT_MODE: # ask for init letter
            while True:
                letter = input_letter(".")
                if letter == ".": # Bro gave up, let's tell possible cubies
                    cubies_to_tell = remaining_cubies.copy()
                    possible_letters = []
                    for colors,data in EDGES_STICKERS_REV.items():
                        colors = tsort(colors)
                        if colors in cubies_to_tell:
                            possible_letters.append(data[0])
                            cubies_to_tell.remove(colors)
                    print("Possible letters: "+" ".join(possible_letters))
                    continue
                pos0,pos1 = EDGES_STICKERS[letter]

                init_colors: tuple[int,int] = tsort((pos0[0],pos1[0])) # type: ignore
                if init_colors in remaining_cubies:
                    print("Well chosen")
                    break
                else:
                    print("Incorrect, choose another one")
            remaining_cubies.remove(init_colors)
        else:
            init_colors = remaining_cubies.pop() # type: ignore # if plan mode, the user choose


    colors2 = init_colors
    init_colors_sorted = tsort(init_colors)
    #print(init_colors)
    first_of_cycle = True
    last_of_cycle = False
    cycle_letters = []
    while not last_of_cycle: # 1 cycle
        last_of_cycle = not first_of_cycle and tsort(colors2) == init_colors_sorted
        #print(colors2,last_of_cycle)
        letter,pos0,pos1 = EDGES_STICKERS_REV[colors2]
        #print(f"Letter: {letter}")
        if not (first_cycle and (first_of_cycle or last_of_cycle)):
            if first_of_cycle and MARK_CYCLE:
                letter = letter.lower()
            letters.append(letter)
            cycle_letters.append(letter)

                #print(f"letter: {letter}")
        if not (first_of_cycle or last_of_cycle):
            remaining_cubies.remove(tsort(colors2))

        colors2 = (
            int(cube.state[colors2[0]][pos0[0]][pos0[1]]),
            int(cube.state[colors2[1]][pos1[0]][pos1[1]])
        )
        first_of_cycle = False


    if INPUT_MODE:
        for letter in (cycle_letters if first_cycle else cycle_letters[1:]):
            letter_input=input_letter()
            if letter_input == letter:
                print("Correct")
            else:
                print(f"Incorrect: {letter}")
    first_cycle = False
    # Here user input test
    pass
print(letters)
