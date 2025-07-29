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
EDGES_STICKERS_REV = {(value[0][0],value[1][0]):(key,value[0][1:],value[1][1:]) for key,value in EDGES_STICKERS.items()}
BUFFER_COLORS = (0,3)
CUBIES = set((tuple(sorted(key)) for key in EDGES_STICKERS_REV.keys()))
#CUBIES = set([(1,2),2])
print(CUBIES)
import rubik_impl
cube = rubik_impl.Cube.solved(rubik_impl.C_NUMBERS)
cube.apply("R U R' U' R' F R R U' R' U' R U R' F'")

print(cube)

init_colors = (0,3)
first_cycle = True
letters = []
remaining_cubies = CUBIES.copy()
while remaining_cubies:
    if first_cycle:
        init_colors = BUFFER_COLORS
    else:
        init_colors: tuple[int, int] = random.choice(tuple(remaining_cubies)) # type: ignore # if plan mode, the user choose


    current_colors = init_colors
    init_colors_sorted = sorted(init_colors)
    #print(init_colors)
    first_of_cycle = True
    last_of_cycle = False
    cycle_letters = []
    while not last_of_cycle: # 1 cycle
        last_of_cycle = not first_of_cycle and sorted(current_colors) == init_colors_sorted
        print(current_colors,last_of_cycle)
        letter,pos0,pos1 = EDGES_STICKERS_REV[current_colors]
        if not (first_cycle and (first_of_cycle or last_of_cycle)):
            if letters and letters[-1]==letter: # solved piece
                del letters[-1]
            else:
                letters.append(letter)
                cycle_letters.append(letter)
                if first_of_cycle:
                    print("NEW CYCLE")
                print(f"letter: {letter}")
        if not first_of_cycle:
            remaining_cubies.remove(current_colors)

        current_colors = (
            int(cube.state[current_colors[0]][pos0[0]][pos0[1]]),
            int(cube.state[current_colors[1]][pos1[0]][pos1[1]])
        )
        first_of_cycle = False
    first_cycle = False
    # Here user input test
    pass
print(EDGES_STICKERS_REV[init_colors])
