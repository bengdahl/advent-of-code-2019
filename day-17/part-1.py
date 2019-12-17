import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

SCAFFOLD = ord('#')
SPACE = ord('.')
NEWLINE = ord('\n')

cpu = intcode.Intcode(program, [])
picture = ""
grid = {}
row = 0
col = 0
for c in cpu:
    picture += chr(c)
    if c == NEWLINE:
        row += 1
        col = 0
    else:
        grid[(col,row)] = c
        col += 1

#print(picture)

intersections = []
for (x,y) in grid:
    neighbors = [(x+1,y),(x,y+1),(x-1,y),(x,y-1), (x,y)]
    if all(grid.get(n,0) == SCAFFOLD for n in neighbors):
        intersections.append((x,y))

print(sum([x*y for x,y in intersections]))