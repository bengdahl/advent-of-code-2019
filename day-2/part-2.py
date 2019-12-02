with open("input.txt", "r") as f:
    s = f.read()
    data = [int(n) for n in s.split(',')]

def run_with_word(data, noun, verb):
    data[1] = noun
    data[2] = verb

    i = 0
    while True:
        op = data[i]
        ai = i+1
        bi = i+2
        ci = i+3
        if op == 1:
            data[data[ci]] = data[data[ai]] + data[data[bi]]
        elif op == 2:
            data[data[ci]] = data[data[ai]] * data[data[bi]]
        elif op == 99:
            break
        else:
            raise ValueError("Invalid opcode "+str(op))
        i += 4
    return data[0]

for n in range(1,100):
    for v in range(1,100):
        data_copy = data[:]
        r = run_with_word(data_copy, n, v)
        if r == 19690720:
            print("{}{}".format(n,v))
            exit()

print("uh oh")