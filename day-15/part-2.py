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

OXY = 3

cpu = intcode.Intcode(program)

min_x, max_x = 0, 0
min_y, max_y = 0, 0
drone = (0, 0)
spaces = {(0,0): OK}
has_dead_end = False

def move_direction(d,p):
    dx, dy = {
        NORTH: (0, -1),
        SOUTH: (0, 1),
        WEST: (-1, 0),
        EAST: (1, 0)
    }[d]
    return (p[0] + dx, p[1] + dy)

def move_drone(d):
    global drone, min_x, max_x, min_y, max_y
    drone2 = move_direction(d, drone)
    min_x = min(min_x, drone2[0])
    max_x = max(max_x, drone2[0])
    min_y = min(min_y, drone2[1])
    max_y = max(max_y, drone2[1])
    return drone2

def show_maze(part=1):
    o = ""
    o += chr(27) + "[1;H" + chr(27) + "[J"
    show = {WALL: '\u001b[37m\u2588',
            OK: '\u001b[31m\u2588', 
            OXY: '\u001b[36m\u2588',
            -1: '\u001b[39; 49m '}
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            o += '\u001b[34m\u2588' if (x, y) == drone and part == 1 else \
                 show[spaces.get((x, y), -1)]
        o += '\n\u001b[39;49m'
    print(o)
    time.sleep(0.016)


def traverse_maze(path, previous_move=None, found=None):
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
            spaces[new_drone] = WALL
            path.pop()
        elif status == FINISH:
            spaces[new_drone] = OXY
            found = new_drone
        if status == OK or status == FINISH:
            drone = new_drone
            if drone not in spaces:
                spaces[drone] = OK
            show_maze()
            branch = traverse_maze(path, d, found=found)
            if branch:
                found = branch
            cpu.send_input(opposite_direction[d])
            next(cpu)
            path.pop()
            drone = old_drone
            show_maze()
    has_dead_end = True
    return found


path = []
oxygen_center = traverse_maze(path)

# BFS from the oxygen center
oxygen_heads = [oxygen_center]
t = 0
while len(oxygen_heads) > 0:
    new_oxy_heads = []
    for head in oxygen_heads:
        neighbors = [point 
                        for point in 
                            (move_direction(d, head) for d in (NORTH,SOUTH,EAST,WEST)) 
                        if spaces.get(point,-1) == OK]
        for n in neighbors:
            spaces[n] = OXY
            new_oxy_heads.append(n)
    oxygen_heads = new_oxy_heads
    t += 1
    show_maze(part=2)

# Minus 1 because the last step of the BFS already has oxygen filling all rooms.
# The last step just removes the last nodes from the queue
print(t-1)
