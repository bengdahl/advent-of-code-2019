with open("input.txt", "r") as f:
    s = f.read()
    data = [int(n) for n in s.split(',')]

data[1] = 12
data[2] = 2

i = 0
while True:
    op = data[i]
    ai = i+1
    bi = i+2
    ci = i+3
    if op == 1:
        print("add {} and {} into {}".format(data[ai],data[bi],data[ci]))
        data[data[ci]] = data[data[ai]] + data[data[bi]]
    elif op == 2:
        print("mult {} and {} into {}".format(data[ai],data[bi],data[ci]))
        data[data[ci]] = data[data[ai]] * data[data[bi]]
    elif op == 99:
        break
    else:
        raise ValueError("Invalid opcode "+str(op))
    i += 4

print(data[0])
