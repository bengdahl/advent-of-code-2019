import intcode

with open("input.txt", "r") as f:
    program = list(map(int, f.readline().split(',')))
cpu = intcode.Intcode(program, [2], debug=False)

try:
    print(list(cpu))
except:
    print("ERR")
    print(cpu.data[973:])
