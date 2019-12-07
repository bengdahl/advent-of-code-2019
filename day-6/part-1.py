with open("input.txt", "r") as f:
    orbits = [o.strip().split(')') for o in f.readlines()]


def find_orbits(name):
    return [i for i, v in enumerate(orbits) if v[0] == name]


orbit_counts = {'COM': 0}
queue = ['COM']

# Breadth-first search along the orbit tree
while len(queue) > 0:
    name = queue.pop(0)
    print(name)
    # When `A)B`, the indirect orbits of B = the orbits of A
    ind_orbits = orbit_counts[name]
    for i in find_orbits(name):
        moon = orbits[i][1]
        orbit_counts[moon] = 1 + ind_orbits
        queue.append(moon)

print(sum(orbit_counts.values()))
