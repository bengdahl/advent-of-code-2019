import re

with open("input.txt", "r") as f:
    reactions = f.readlines()

reaction_re = re.compile(r"((?:\d+ \w+(?:, )?)+) => (\d+ \w+)")
ingredient_re = re.compile(r"(\d+) (\w+)")


def parse_ingredient(s, many=False):
    if many:
        return tuple(parse_ingredient(i) for i in s.split(', '))
    match = ingredient_re.findall(s)[0]
    return (int(match[0]), match[1])


reactions = [reaction_re.findall(r)[0] for r in reactions]
reactions = [(parse_ingredient(i, True), parse_ingredient(o))
             for i, o in reactions]

reactions_dict = {}
for i, o in reactions:
    reactions_dict[o[1]] = (o[0], i)

def ore_needed(fuel):
    have = {}
    quantities_needed = {'FUEL': fuel}
    while True:
        ingredient = next((i for i in quantities_needed if i != 'ORE'), '')
        if ingredient == '':
            break
        n, requirements = reactions_dict[ingredient]
        n_need = quantities_needed[ingredient]
        del quantities_needed[ingredient]
        if n_need % n != 0:
            have[ingredient] = n - (n_need % n)
            n_need += n
        for m, i2 in requirements:
            quantities_needed[i2] = quantities_needed.get(
                i2, 0) + m * (n_need//n) - have.get(i2, 0)
            if i2 in have:
                del have[i2]
    return quantities_needed['ORE']

# Binary search for the fuel we can produce
ore = 1000000000000
low, high = 1, 2
while ore_needed(high) < ore:
    low,high = high, high * 2
# We now know the upper and lower bound of the result
while high - low >= 2:
    half = low + (high - low)//2
    if ore_needed(half) > ore:
        high = half
    else:
        low = half

print(low)