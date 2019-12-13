import re
import itertools

moon_parse = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")

with open('input.txt', 'r') as f:
    moons = [(int(x),int(y),int(z)) for (x,y,z) in moon_parse.findall(f.read())]

moons = [(p, (0,0,0)) for p in moons]

for _ in range(1000):
    # Apply gravity calculations
    for i in range(len(moons)):
        other_moons = moons[:i]+moons[i+1:]
        for p2,v2 in other_moons:
            p = moons[i][0]
            v = moons[i][1]
            vx = v[0] + (0 if p[0]==p2[0] else \
                         1 if p[0]<p2[0] else \
                         -1)
            vy = v[1] + (0 if p[1]==p2[1] else \
                         1 if p[1]<p2[1] else \
                         -1)
            vz = v[2] + (0 if p[2]==p2[2] else \
                         1 if p[2]<p2[2] else \
                         -1)
            moons[i] = (p,(vx,vy,vz))
            
    # Apply velocity calculations
    for i,(p,v) in enumerate(moons):
        px = p[0] + v[0]
        py = p[1] + v[1]
        pz = p[2] + v[2]
        moons[i] = ((px,py,pz), v)

# Calculate energy
energy = 0
for p,v in moons:
    pot = abs(p[0]) + abs(p[1]) + abs(p[2])
    kin = abs(v[0]) + abs(v[1]) + abs(v[2])
    energy += pot*kin

print(energy)