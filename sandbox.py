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
    current_colors = init_colors
    init_colors_sorted = sorted(init_colors)
    #print(init_colors)
    first_of_cycle = True
    is_end_cycle = False
    while not is_end_cycle: # 1 cycle
        letter,coord0,coord1 = EDGES_STICKERS_REV[current_colors]
        colors2 = (
            int(cube.state[current_colors[0]][coord0[0]][coord0[1]]),
            int(cube.state[current_colors[1]][coord1[0]][coord1[1]])
        )
        print(colors2)
        remaining_cubies.remove(colors2)
        colors2_sorted = sorted(colors2)
        is_end_cycle = sorted(colors2)==init_colors_sorted
            
        if not (is_end_cycle and first_cycle):
            if True: # verif if it was already solved
                print("NEW LETTER:")
                letters.append(letter)


        current_colors = colors2
        first_of_cycle = False

    init_colors: tuple[int, int] = random.choice(tuple(CUBIES)) # type: ignore # if plan mode, the user choose
    print(init_colors)
    print(remaining_cubies)
    print(letters)
    pass
print(EDGES_STICKERS_REV[init_colors])
