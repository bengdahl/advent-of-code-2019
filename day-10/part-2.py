from math import gcd,atan2,inf,sqrt
import sys
from time import sleep

with open("input.txt", "r") as f:
    grid = f.read()

asteroids = []

for row, line in enumerate(grid.split('\n')):
    for col, c in enumerate(line):
        if c == '#':
            asteroids.append((col, row))

targetCount = {}

def calc_angle(dx,dy):
    f = gcd(dx,dy)
    return (dx//f,dy//f)


def calc_true_angle(angle):
    if angle[0]==0 and angle[1] < 0:
        return -inf
    return atan2(-angle[0], angle[1])


def calc_distance(target):
    return sqrt((target[0] - station[0])**2 + (target[1] - station[1])**2)

# All asteroids are represented as (dx,dy) compared
# to the station. Two target asteroids (dxA,dyA)
# and (dxB,dyB) are colinear if and only if dxA is
# proportional to dxB, and dyA is proportional to
# dyB.
for (ox, oy) in asteroids:
    visibleAngles = set()
    for (tx, ty) in asteroids:
        if (tx, ty) == (ox, oy):
            continue
        dx = tx-ox
        dy = ty-oy
        visibleAngles.add(calc_angle(dx,dy))
    #print((dx,dy), visibleAngles)
    targetCount[(ox, oy)] = visibleAngles

station = max(targetCount.items(), key=lambda p:len(p[1]))[0]

print(station)

asteroids.remove(station)
print(len(asteroids))

asteroidsByAngle = {}

ox = station[0]
oy = station[1]
for (tx,ty) in asteroids:
    dx = tx - ox
    dy = ty - oy
    a = calc_angle(dx,dy)
    if a in asteroidsByAngle:
        asteroidsByAngle[a].append((tx,ty))
        asteroidsByAngle[a].sort(key=calc_distance, reverse=True)
    else:
        asteroidsByAngle[a] = [(tx,ty)]

asteroidsByAngle = list(asteroidsByAngle.items())
asteroidsByAngle.sort(key = lambda item: calc_true_angle(item[0]))

# for a in asteroidsByAngle:
#     print(a)

destruction_queue = []
i=0
while len(asteroidsByAngle) > 0:
    if i >= len(asteroidsByAngle):
        i = 0
    in_beam = asteroidsByAngle[i]
    a = in_beam[1].pop()
    destruction_queue.append(a)
    if len(in_beam[1]) == 0:
        del asteroidsByAngle[i]
    else:
        i += 1

print(len(destruction_queue))
print('')
print("ANSWER:",destruction_queue[199][0]*100+destruction_queue[199][1])

# for n in range(50,100):
#     for y in range(len(grid.split('\n'))):
#         for x in range(len(grid.split('\n')[0])):
#             if (x,y) == station:
#                 print('O', end='')
#             elif (x,y) in destruction_queue[:n+1]:
#                 print('#', end='')
#             else:
#                 print('.', end='')
#         print('')
#     print('')
#     sleep(0.2)
