import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

BLACK = 0
WHITE = 1
LEFT = 0
RIGHT = 1

cpu = intcode.Intcode(program)

max_x, min_x = 0, 0
max_y, min_y = 0, 0
x, y = 0, 0
dx, dy = 0, -1


def rotate(t):
    global dx, dy
    if t == LEFT:
        old_dx, old_dy = dx, dy
        dx = old_dy
        dy = -old_dx
    if t == RIGHT:
        old_dx, old_dy = dx, dy
        dx = -old_dy
        dy = old_dx


color = {(0, 0): WHITE}
while True:
    cpu.send_input(color.get((x, y), BLACK))
    new_color = next(cpu, None)
    turn = next(cpu, None)
    if new_color == None or turn == None:
        break
    color[(x, y)] = new_color
    rotate(turn)
    x += dx
    y += dy
    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)

for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        c = color.get((x, y), BLACK)
        if c == WHITE:
            print('##', end='')
        elif c == BLACK:
            print('  ', end='')
    print('')
