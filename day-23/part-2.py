import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

VERBOSE = False

cpus = []
for addr in range(50):
    cpus.append(intcode.Intcode(program[:], [addr]))

queues = [[] for _ in cpus]
awaiting = [False for _ in cpus]

nat = None
previous_y = set()
i = 0
while True:
    addr, x, y = next(cpus[i]), next(cpus[i]), next(cpus[i])
    if addr is None:
        if queues[i]:
            x, y = queues[i].pop(0)
            if VERBOSE: print(i, 'GOT', (x, y))
            cpus[i].send_input(x)
            cpus[i].send_input(y)
            awaiting[i] = False
        else:
            cpus[i].send_input(-1)
            awaiting[i] = True
    else:
        awaiting[i] = False
        if VERBOSE: print(i, 'TO', addr)
        if addr == 255:
            nat = (x,y)
        else:
            queues[addr].append((x, y))
    i += 1
    if i >= 50:
        i %= 50
        if all(len(q) == 0 for q in queues) and all(awaiting) and nat is not None:
            # Network is idle
            if VERBOSE: print("IDLE, NAT SENDING:", nat)
            if nat[1] in previous_y:
                print("NETWORK STOPPED ON Y =",nat[1])
                break
            previous_y.add(nat[1])
            queues[0].append(nat)
