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

# print(portals)
# print(reverse_portals)
assert all(k in ('AA','ZZ') or len(v)==2 for k,v in portals.items())

def search_for_portals(p):
    start = portals[p]
    visited = set()
    queue = [(0, c) for c in start]
    to_portals = {}
    while len(queue)>0:
        d, (x,y) = queue.pop(0)
        neighbors = ((x+1,y),(x,y+1),(x-1,y),(x,y-1))
        visited.add((x,y))
        if (x,y) in reverse_portals and reverse_portals[(x,y)] != p:
            to_portals[reverse_portals[(x,y)]] = d
        for n in neighbors:
            if n not in grid or n in visited:
                continue
            queue.append((d+1, n))
    return to_portals

portals_to_portals = {
    p:search_for_portals(p) for p in portals.keys()
}

# [print(p, ps) for p,ps in portals_to_portals.items()]

START = 'AA'
GOAL = 'ZZ'

# Dijkstra search using the portals as nodes
queue = [(0, START, [])]
heapq.heapify(queue)
visited = set()
while len(queue) > 0:
    d, node, path = heapq.heappop(queue)
    if node == GOAL:
        print(d-1, path+[node]) # There is no need to teleport on the goal node
        break
    visited.add(node)
    neighbors = [(d2,p) for p,d2 in portals_to_portals[node].items() if p not in visited]
    for d2,p in neighbors:
        heapq.heappush(queue, (d+1+d2, p, path+[node])) # It takes 1 step to teleport