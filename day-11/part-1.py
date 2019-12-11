import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

BLACK = 0
WHITE = 1
LEFT = 0
RIGHT = 1

cpu = intcode.Intcode(program)

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


color = {}
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

print(len(color))
