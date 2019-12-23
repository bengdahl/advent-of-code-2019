import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

springscript = """NOT C J
NOT A T
OR T J
AND D J
WALK
"""

cpu = intcode.Intcode(program)
for c in springscript:
    cpu.send_input(ord(c))

print(''.join(list(chr(c) if c < 128 else str(c) for c in cpu)))