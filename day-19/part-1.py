import intcode


with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

points = 0
for r in range(50):
    for c in range(50):
        cpu = intcode.Intcode(program[:])
        cpu.send_input(c)
        cpu.send_input(r)
        pulled = next(cpu)
        if pulled:
            points += 1
            print('#',end='')
        else:
            print('.',end='')
    print('')

print(points)
