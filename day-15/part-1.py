import time
import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

opposite_direction = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

WALL = 0
OK = 1
FINISH = 2

cpu = intcode.Intcode(program)

min_x, max_x = 0, 0
min_y, max_y = 0, 0
drone = (0, 0)
spaces = {}
has_dead_end = False


def move_drone(d):
    global drone, min_x, max_x, min_y, max_y
    dx, dy = {
        NORTH: (0, -1),
        SOUTH: (0, 1),
        WEST: (-1, 0),
        EAST: (1, 0)
    }[d]
    drone2 = (drone[0] + dx, drone[1] + dy)
    min_x = min(min_x, drone2[0])
    max_x = max(max_x, drone2[0])
    min_y = min(min_y, drone2[1])
    max_y = max(max_y, drone2[1])
    return drone2

def show_maze(path):
    o = ""
    o += chr(27) + "[1;H" + chr(27) + "[J"
    show = {0: u"\u001b[37m\u2588",
            1: '\u001b[31m\u2588', 
            -1: '\u001b[39;49m '}
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            o += '\u001b[34m\u2588' if (x, y) == drone else \
                 show[spaces.get((x, y), -1)]
        o += '\n\u001b[37m'
    print(o)
    time.sleep(0.016)


def traverse_maze(path, previous_move=None):
    global has_dead_end, drone
    directions = [NORTH, SOUTH, WEST, EAST]
    old_drone = drone
    if previous_move != None:
        directions.remove(opposite_direction[previous_move])
    for d in directions:
        path.append(d)
        cpu.send_input(d)
        status = next(cpu)
        new_drone = move_drone(d)
        if status == WALL:
            spaces[new_drone] = 0
            path.pop()
            show_maze(path)
        elif status == FINISH:
            print("GOT IT!")
            return True
        elif status == OK:
            drone = new_drone
            spaces[drone] = 1
            show_maze(path)
            if traverse_maze(path, d):
                return True
            else:
                cpu.send_input(opposite_direction[d])
                next(cpu)
                path.pop()
                drone = old_drone
                show_maze(path)
    has_dead_end = True
    return False


path = []
print(traverse_maze(path))
print(len(path))
print(drone)
