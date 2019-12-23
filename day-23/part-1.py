import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

cpus = []
for addr in range(50):
    cpus.append(intcode.Intcode(program[:], [addr]))

queues = [[] for _ in cpus]

i = 0
while True:
    addr, x, y = next(cpus[i]), next(cpus[i]), next(cpus[i])
    if addr is None:
        if queues[i]:
            x, y = queues[i].pop(0)
            print(i, 'GOT', (x,y))
            cpus[i].send_input(x)
            cpus[i].send_input(y)
        else:
            cpus[i].send_input(-1)
    else:
        print(i,'TO',addr)
        if addr == 255:
            print('Y =',y,'TO 255')
            break
        queues[addr].append((x,y))
    i += 1
    i %= 50
