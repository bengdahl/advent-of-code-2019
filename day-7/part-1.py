import intcode
import itertools

with open("input.txt", "r") as f:
    program = [int(n) for n in f.readline().split(',')]

# Test
test_prg = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
            101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
test_sig = 0
for s in [0,1,2,3,4]:
    cpu = intcode.Intcode(test_prg, [s,test_sig])
    test_sig = next(cpu)
print("TEST:", test_sig)

outputs = []
for settings in itertools.permutations(range(5)):
    current_sig = 0
    for s in settings:
        cpu = intcode.Intcode(program, [s, current_sig])
        current_sig = next(cpu)
    outputs.append(current_sig)

print(max(outputs))
