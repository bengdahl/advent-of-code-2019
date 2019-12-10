from math import gcd

with open("input.txt", "r") as f:
    grid = f.read()

asteroids = []

for row, line in enumerate(grid.split('\n')):
    for col, c in enumerate(line):
        if c == '#':
            asteroids.append((col,row))

targetCount = {}

# All asteroids are represented as (dx,dy) compared 
# to the station. Two target asteroids (dxA,dyA) 
# and (dxB,dyB) are colinear if and only if dxA is
# proportional to dxB, and dyA is proportional to 
# dyB. 
for (ox,oy) in asteroids:
    visibleAngles = set()
    for (tx,ty) in asteroids:
        if (tx,ty) == (ox,oy):
            continue
        dx = tx-ox
        dy = ty-oy
        f = gcd(dx,dy)
        if f == 1:
            visibleAngles.add((dx,dy))
        else:
            visibleAngles.add((dx//f, dy//f))
    #print((dx,dy), visibleAngles)
    targetCount[(ox,oy)] = len(visibleAngles)

print(max(targetCount.values()))