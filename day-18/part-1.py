import string
import math
import heapq

CLEAR = 0
WALL = 1

DOORS = list(string.ascii_uppercase)
KEYS = list(string.ascii_lowercase)

with open("input.txt","r") as f:
    maze = f.read()
    grid = []
    doors = {}
    keys = {}
    you = (0,0)
    r,c=0,0
    for line in maze.splitlines():
        row = []
        for ch in line:
            if ch=='.':
                row.append(CLEAR)
            elif ch=='#':
                row.append(WALL)
            elif ch=='@':
                row.append(CLEAR)
                you = (c,r)
            elif ch in DOORS:
                row.append(ch)
                doors[ch] = (c,r)
            elif ch in KEYS:
                row.append(ch)
                keys[ch] = (c,r)
            c += 1
        grid.append(row)
        r += 1
        c = 0

def search_for_keys(start,start_key):
    to_explore = [(0,start,frozenset())]
    keys = {}
    known = set(start)
    while len(to_explore) > 0:
        d,(px,py),doors = to_explore.pop(0)
        neighbors = [(px+1,py),(px,py+1),(px-1,py),(px,py-1)]
        available_neighbors = [(nx,ny) for nx,ny in neighbors 
            if ny < len(grid) and ny >= 0 and
               nx < len(grid[ny]) and nx >= 0
            and (nx,ny) not in known
            and (grid[ny][nx] == CLEAR
                or grid[ny][nx] in KEYS
                or grid[ny][nx] in DOORS)]
        for nx,ny in available_neighbors:
            known.add((nx,ny))
            if grid[ny][nx] in KEYS and grid[ny][nx] != start_key:
                keys[grid[ny][nx]] = (d+1, doors)
            if grid[ny][nx] in DOORS:
                to_explore.append((d+1,(nx,ny),doors|{grid[ny][nx]}))
            else:
                to_explore.append((d+1,(nx,ny),doors))
    return keys

# Imagine each key we can choose from as a vertex on a graph.
# We can search this graph of choices the same way we search
# a real graph.
def meta_search(key_to_key):
    # A state is:
    # (current_pos, set of keys, distance)
    states = [(0,('@',frozenset()))]
    heapq.heapify(states)
    known = frozenset()
    ds = {('@', frozenset()): 0}
    # t=0
    while len(states) > 0:
        # t += 1
        # if t % 100 == 0: print(t)
        _, (pos, path) = heapq.heappop(states)
        d = ds[(pos,path)]
        if pos == 'GOAL':
            return d
        if len(path) == len(keys):
            ds[('GOAL',frozenset())] = d
            heapq.heappush(states, (d, ('GOAL', frozenset())))
        # print(d, ''.join(path))
        keys_available = [(k,d) for k,(d,doors_needed) 
            in key_to_key[pos].items() 
            if len(doors_needed - path) == 0
            and k not in path]
        # print(pos, path, keys_available)
        new_states = [(d+d2, (k, path|frozenset(k.upper()))) for k,d2 in keys_available]
        for d3,n in new_states:
            if n not in ds or d3 < ds[n]:
                ds[n] = d3
                heapq.heappush(states,(ds[n], n))

key_to_key = {
    k:search_for_keys(p,k) for
    k,p in [('@',you)]+list(keys.items())
}

print(meta_search(key_to_key))
