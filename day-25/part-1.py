import intcode

with open('input.txt', 'r') as f:
    program = [int(n) for n in f.read().split(',')]

items = {
    "ornament",
    "loom",
    "spool of cat6",
    "wreath",
    "fixed point",
    "shell",
    "candy cane",
    "weather machine"
}

# These commands collect every safe item and move to the security room
commands = """east
take loom
south
take ornament
west
north
take candy cane
south
east
north
east
take fixed point
north
take spool of cat6
north
take weather machine
south
west
take shell
east
south
west
west
north
take wreath
north
east
inv
"""

cpu = intcode.Intcode(program, [ord(c) for c in commands])
while True:
    c = next(cpu)
    if c is None:
        break
    print(chr(c), end='')

for item in items:
    cmd = "drop "+item+"\n"
    [cpu.send_input(ord(c)) for c in cmd]
    while True:
        c = next(cpu)
        if c is None:
            break
        print(chr(c), end='')
cmd = "inv\n"
[cpu.send_input(ord(c)) for c in cmd]
while True:
    c = next(cpu)
    if c is None:
        break
    print(chr(c), end='')

tried = set()
def brute_force(items, inventory=None):
    inventory = [] if inventory==None else inventory
    if frozenset(tuple(inventory)) in tried:
        return
    tried.add(frozenset(tuple(inventory)))
    for item in items:
        cmd = "take "+item+"\n"
        [cpu.send_input(ord(c)) for c in cmd]
        while True:
            c = next(cpu)
            if c is None:
                break
            # print(chr(c), end='')
        inventory.append(item)
        new_items = items - {item}
        print("Trying:",inventory)
        cmd = "south\n"
        [cpu.send_input(ord(c)) for c in cmd]
        output = ""
        too_heavy = False
        try:
            while True:
                c = next(cpu)
                if c is None:
                    break
                output += chr(c)
            if output.find("lighter") != -1:
                too_heavy = True
        except StopIteration:
            print(output)
            return True
        print("Too heavy" if too_heavy else "Too light")
        if not too_heavy and len(new_items) > 0:
            if brute_force(new_items, inventory):
                return True
        cmd = "drop "+item+"\n"
        [cpu.send_input(ord(c)) for c in cmd]
        while True:
                c = next(cpu)
                if c is None:
                    break
                # print(chr(c), end='')
        inventory.remove(item)

brute_force(items)
