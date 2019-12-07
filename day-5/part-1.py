with open("input.txt", "r") as f:
    s = f.read()
    data = [int(n) for n in s.split(',')]

stdin = [1]

i = 0

def get_arg_a(modes):
    ai = i+1
    return data[ai] if modes[0]==1 else data[data[ai]] if modes[0]==0 else None
def get_raw_a():
    return data[i+1]

def get_arg_b(modes):
    bi = i+2
    return data[bi] if modes[1]==1 else data[data[bi]] if modes[1]==0 else None
def get_raw_b():
    return data[i+2]

def get_arg_c(modes):
    ci = i+3
    return data[ci] if modes[2]==1 else data[data[ci]] if modes[2]==0 else None
def get_raw_c():
    return data[i+3]

while True:
    op = data[i]
    modes = [(op//100)%10, (op//1000)%10, (op//10000)%10]
    opcode = op % 100
    if opcode == 1:
        data[get_raw_c()] = get_arg_a(modes) + get_arg_b(modes)
        i += 4
    elif opcode == 2:
        data[get_raw_c()] = get_arg_a(modes) * get_arg_b(modes)
        i += 4
    elif opcode == 3:
        data[get_raw_a()] = stdin.pop(0)
        i += 2
    elif opcode == 4:
        print(get_arg_a(modes))
        i += 2
    elif opcode == 99:
        break
    else:
        raise ValueError("Invalid opcode "+str(op))
