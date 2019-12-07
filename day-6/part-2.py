with open("input.txt", "r") as f:
    orbits = [o.strip().split(')') for o in f.readlines()]


def find_orbit_by(name):
    return [v[0] for v in orbits if v[1] == name][0]


you_orbiting = find_orbit_by('YOU')
you_trail = [you_orbiting]
while True:
    current = you_trail[-1]
    if current == 'COM':
        break
    parent = find_orbit_by(current)
    you_trail.append(parent)

san_orbiting = find_orbit_by('SAN')
san_trail = [san_orbiting]
while True:
    current = san_trail[-1]
    if current == 'COM':
        break
    parent = find_orbit_by(current)
    san_trail.append(parent)

print("YOU:", you_orbiting)
print("SAN:", san_orbiting)

path = []
while True:
    current = you_trail.pop(0)
    path.append(current)
    if current in san_trail:
        print("LINK:", current)
        path.extend(san_trail[:san_trail.index(current)][::-1])
        break
print(path)
# Subtract one because `path` includes our starting orbit
print(len(path) - 1)
