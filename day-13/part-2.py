import time
import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

n_to_char = {EMPTY: ' ', WALL: '#', BLOCK: 'X', PADDLE: '_', BALL: 'O'}

cpu = intcode.Intcode(program, [0])

screen = {}
max_x = 0
max_y = 0

cpu.set_data(0, 2)

ball = (0, 0)
paddle = (0, 0)
blocks = -1
score = 0
game_started = False


def move_joystick():
    if ball[0] < paddle[0]:
        cpu.send_input(-1)
    elif ball[0] > paddle[0]:
        cpu.send_input(1)
    else:
        cpu.send_input(0)


def show_screen():
    string = ""
    string += chr(27) + "[1;H" + chr(27) + "[J"
    string += "Score: " + str(score) + '\n'
    for r in range(max_y+1):
        for c in range(max_x+1):
            string += str(n_to_char[screen[(c, r)]])
        string += str('\n')
    string += ('-' * max_x + '\n')
    print(string)


try:
    while True:
        x = next(cpu)
        max_x = max(max_x, x)
        y = next(cpu)
        max_y = max(max_y, y)
        tile = next(cpu)
        if (x, y) == (-1, 0):
            # Before the first score update, the game is
            # just drawing the first tiles to the screen.
            game_started = True
            score = tile
            continue
        if tile == BALL:
            ball = (x, y)
        elif tile == PADDLE:
            paddle = (x, y)
        screen[(x, y)] = tile
        if game_started:
            if tile == BALL:
                move_joystick()
            blocks = list(screen.values()).count(BLOCK)
            if tile == BALL or tile == PADDLE:
                show_screen()
                time.sleep(0.016)
except StopIteration:
    pass

print("Final score:", score)
