import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

n_to_char = {EMPTY: ' ', WALL: '#', BLOCK: 'X', PADDLE: '_', BALL: 'O'}

cpu = intcode.Intcode(program)

screen = {}
max_x = 0
max_y = 0

try:
    while True:
        x = next(cpu)
        max_x = max(max_x, x)
        y = next(cpu)
        max_y = max(max_y, y)
        tile = next(cpu)
        screen[(x, y)] = tile

except StopIteration:
    print('Done')
    for r in range(max_y):
        for c in range(max_x):
            print(n_to_char[screen[(c, r)]], end='')
        print('')
    print('Blocks:', list(screen.values()).count(BLOCK))
