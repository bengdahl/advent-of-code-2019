# I gave up
# The critical logic of this was taken from https://repl.it/@joningram/AOC-2019 
# and paraphrased to work with the format of my part 1 solution

import string
import math
import heapq

CLEAR = '.'
WALL = '#'

DOORS = list(string.ascii_uppercase)
KEYS = list(string.ascii_lowercase)

with open("input2.txt", "r") as f:
    maze = f.read()
    grid = []
    doors = {}
    keys = {}
    robots = []
    r, c = 0, 0
    for line in maze.splitlines():
        row = []
        for ch in line:
            if ch == '.':
                row.append(CLEAR)
            elif ch == '#':
                row.append(WALL)
            elif ch == '@':
                row.append(str(len(robots)))
                robots.append((c, r))
            elif ch in DOORS:
                row.append(ch)
                doors[ch] = (c, r)
            elif ch in KEYS:
                row.append(ch)
                keys[ch] = (c, r)
            c += 1
        grid.append(row)
        r += 1
        c = 0


def search_for_keys(start, start_key):
    to_explore = [(0, start, "")]
    keys = {}
    known = set(start)
    while len(to_explore) > 0:
        d, (px, py), route = to_explore.pop(0)
        neighbors = [(px+1, py), (px, py+1), (px-1, py), (px, py-1)]
        available_neighbors = [(nx, ny) for nx, ny in neighbors
                               if ny < len(grid) and ny >= 0 and
                               nx < len(grid[ny]) and nx >= 0
                               and (nx, ny) not in known
                               and grid[ny][nx] != WALL]
        for nx, ny in available_neighbors:
            known.add((nx, ny))
            if grid[ny][nx] in KEYS and grid[ny][nx] != start_key:
                keys[grid[ny][nx]] = (d+1, route)
            if grid[ny][nx] in DOORS or grid[ny][nx] in KEYS:
                to_explore.append((d+1, (nx, ny), route + grid[ny][nx]))
            else:
                to_explore.append((d+1, (nx, ny), route))
    return keys

# Imagine each key we can choose from as a vertex on a graph.
# We can search this graph of choices the same way we search
# a real graph.

# This code is paraphrased from:
# https://github.com/mcpower/adventofcode/blob/8622aadfd1b93fce8403e10357a1b175d2dff2c2/2019/18/a-p2.py
def meta_search(key_to_key):
    keys = frozenset(k for k in key_to_key.keys() if k in KEYS)
    start = (('0', '1', '2', '3'), frozenset())
    states = {start: 0}
    for _ in range(len(keys)):
        next_states = {}
        for s in states:
            curlocs, curkeys, curdist = s[0], s[1], states[s]

            for newkey in keys:
                if newkey not in curkeys:
                    for robot in range(4):
                        if newkey in key_to_key[curlocs[robot]]:
                            dist, route = key_to_key[curlocs[robot]][newkey]
                            reachable = all(
                                (c in curkeys or c.lower() in curkeys) for c in route)

                            if reachable:
                                newdist = curdist + dist
                                newkeys = frozenset(curkeys | set((newkey,)))
                                newlocs = list(curlocs)
                                newlocs[robot] = newkey
                                newlocs = tuple(newlocs)

                                if (newlocs, newkeys) not in next_states or newdist < next_states[(newlocs, newkeys)]:
                                    next_states[(newlocs, newkeys)] = newdist
        states = next_states
    return min(states.values())

key_to_key = {}
for y in range(len(grid)):
    for x in range(len(grid[y])):
        content = grid[y][x]
        if content in KEYS or content in "@0123":
            key_to_key[content] = search_for_keys((x, y),content)

print(key_to_key)

print(meta_search(key_to_key))
