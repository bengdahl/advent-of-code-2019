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
reactions = [(parse_ingredient(i, True), parse_ingredient(o)) for i,o in reactions]

reactions_dict = {}
for i,o in reactions:
    reactions_dict[o[1]] = (o[0], i)

have = {}
quantities_needed = {'FUEL': 1}
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
        quantities_needed[i2] = quantities_needed.get(i2,0) + m * (n_need//n) - have.get(i2,0)
        if i2 in have: del have[i2]

print(quantities_needed['ORE'])
