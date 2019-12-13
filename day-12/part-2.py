import re
from math import gcd

moon_parse = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")

with open('input.txt', 'r') as f:
    moons = [(int(x),int(y),int(z)) for (x,y,z) in moon_parse.findall(f.read())]

periods = [0,0,0]

for axis in (0,1,2):
    state = list(zip(*moons))[axis]
    state = [(p,0) for p in state]
    init_state = state[:]
    steps = 0
    while True:
        if steps > 0 and state == init_state:
            break
        # Gravity
        for i in range(len(state)):
            for (p2,v2) in state:
                p,v = state[i]
                new_v = state[i][1] + (0 if p==p2 else \
                                       1 if p<p2 else \
                                       -1)
                state[i] = (p,new_v)
        # Velocity 
        for i in range(len(state)):
            p,v = state[i]
            state[i] = (p+v, v)
        steps += 1
    
    periods[axis] = steps
    print("AXIS {}:".format(axis), steps)

# To find when the periods of all three axes coincide,
# we take the LCM of all three periods.
lcm = periods[0]
for i in periods[1:]:
    lcm = lcm*i // gcd(lcm,i)

print(lcm)