import string
import heapq

with open('input.txt', 'r') as f:
    raw_data = [l.strip('\n') for l in f.readlines()]

data = [l[2:-2] for l in raw_data[2:-2]]
grid = set()
portals = {}
reverse_portals = {}
for r in range(len(data)):
    for c in range(len(data[r])):
        s = data[r][c]
        if s == '.':
            grid.add((c,r))
            r2,c2 = r+2,c+2 # Portal names take two lines of padding
            neighbors = ((1,0),(0,1),(-1,0),(0,-1))
            try:
                for dc,dr in neighbors:
                    p = raw_data[r2+dr][c2+dc]
                    if p in string.ascii_uppercase:
                        p2 = raw_data[r2+dr+dr][c2+dc+dc]
                        ps = p+p2 if neighbors.index((dc,dr)) in (0,1) else p2+p # Names must be read top-bottom or left-right
                        # print((c, r), (dc, dr), p, p2, ps)
                        reverse_portals[(c,r)] = ps
                        if ps in portals:
                            portals[ps].append((c,r))
                        else:
                            portals[ps] = [(c,r)]
            except IndexError:
                pass

outer_portals = set()
for p,ps in portals.items():
    ops = {(x,y) for x,y in ps if x==0 or x==len(data[0])-1 or y == 0 or y == len(data)-1}
    outer_portals |= ops
inner_portals = {n for ns in portals.values() for n in ns if n not in outer_portals}

def other_side(n):
    p = reverse_portals[n]
    return next((n2 for n2 in portals[p] if n2 != n), None)

# print('portals:', portals)
# print('reverse_portals:', reverse_portals)
# print('outer_portals:', outer_portals)
# print('inner_portals:', inner_portals)
assert all(k in ('AA','ZZ') or len(v)==2 for k,v in portals.items())

def search_for_portals(p):
    start = [p]
    visited = set()
    queue = [(0, c) for c in start]
    to_portals = {}
    while len(queue)>0:
        d, (x,y) = queue.pop(0)
        neighbors = ((x+1,y),(x,y+1),(x-1,y),(x,y-1))
        visited.add((x,y))
        if (x,y) in reverse_portals and (x,y) != p:
            to_portals[(x,y)] = (d,1 if (x,y) in inner_portals else -1)
        for n in neighbors:
            if n not in grid or n in visited:
                continue
            queue.append((d+1, n))
    return to_portals

portals_to_portals = {
    p:search_for_portals(p) for ps in portals.values() for p in ps
}

# [print(p, ps) for p,ps in portals_to_portals.items()]

START = (portals['AA'][0], 0)
GOAL = (portals['ZZ'][0], 0)

# print('START:', START)
# print('GOAL:',GOAL)

# A* search using the portals as nodes
queue = [(0, 0, START, [])]
heapq.heapify(queue)
visited = set()
while len(queue) > 0:
    _, d, node, path = heapq.heappop(queue)
    # if node[1] > 100:
    #     continue
    # if node[1] == 0:
    #     print(d,(reverse_portals[node[0]],node[1]),[reverse_portals[p] for p,l in path])
    if node == GOAL:
        print('FINISH:',d-1, [(reverse_portals[p],l) for p,l in path+[node]]) # There is no need to teleport on the goal node, so we use d-1
        break
    visited.add(node)
    neighbors = [(d2,p) for p,d2 in portals_to_portals[node[0]].items()]
    for (d2,level_change),new_p in neighbors:
        new_d = (d+1+d2) # It takes 1 step to teleport
        new_level = node[1] + level_change
        new_p2 = other_side(new_p)
        if new_p2 == None:
            # We can't walk through a portal with no exit
            new_p2 = new_p
            new_level += 1
            if new_level > 0:
                continue
        if new_level < 0:
            continue
        if (new_p2,new_level) in visited:
            continue

        # Okay, so I wanted to use the layer number as a heuristic, 
        # and it worked for me, but i'm not sure if it will work in all cases. 
        # The following snippet will use the layer heuristic:

        # heapq.heappush(queue, (new_d+new_level, new_d, (new_p2, new_level), path+[node]))
        heapq.heappush(queue, (new_d, new_d, (new_p2, new_level), path+[node]))
