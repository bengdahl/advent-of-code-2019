import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

program[0] = 2

# Full sequence found by hand: 
# L 4 L 10 L 6 L 4 L 10 L 6 L 6 L 4 R 8 R 8 L 6 R 8 L 10 L 8 L 8 L 4 L 10 L 6 L 6 R 8 L 10 L 8 L 8 L 6 L 4 R 8 R 8 L 6 R 8 L 10 L 8 L 8 L 4 L 10 L 6 L 6 L 4 R 8 R 8

# Functions found by hand:
# A: L6 R8 L10 L8 L8 (AKA the first one i noticed)
# B: L6 L4 R8 R8 (AKA the Sickle)
# C: L4 L10 L6 (AKA the bracket)

# All together now:
# C C B A C A B A C B

main = "C,C,B,A,C,A,B,A,C,B"
func_a = "L,6,R,8,L,10,L,8,L,8"
func_b = "L,6,L,4,R,8,R,8"
func_c = "L,4,L,10,L,6"

directions = main + '\n' + func_a + '\n' + func_b + '\n' + func_c + '\n' + 'n\n'
cpu = intcode.Intcode(program, list(ord(c) for c in directions))
out = list(cpu)
answer = out[-1]
print(''.join(chr(c) for c in out[:-1]))
print('DUST COLLECTED:', answer)