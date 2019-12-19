import intcode

with open("input.txt", "r") as f:
    program = [int(s) for s in f.readline().split(',')]

def pulled_at(x,y):
    cpu = intcode.Intcode(program[:])
    cpu.send_input(x)
    cpu.send_input(y)
    pulled = next(cpu)
    return pulled


x=0
y=99
while True:
    while pulled_at(x,y) == 0:
        x += 1
    # If (x,y) is at the bottom left corner, and the top right corner (x+99,y-99) is true, (x,y-99) is the top left corner
    if pulled_at(x+99,y-99):
        print(x*10000 + (y-99))
        break
    y += 1