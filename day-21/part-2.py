import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

# Stolen from /u/bluepichu
springscript = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT H T
NOT T T
OR E T
AND T J
RUN
"""

cpu = intcode.Intcode(program)
for c in springscript:
    cpu.send_input(ord(c))

print(''.join(list(chr(c) if c < 128 else str(c) for c in cpu)))
