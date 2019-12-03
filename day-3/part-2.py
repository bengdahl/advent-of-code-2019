import math

with open("input.txt", "r") as f:
  wires = f.readlines()

grid = []
x_range = [0,0]
y_range = [0,0]

def get_direction(d):
  if d == 'R': return (1, 0)
  elif d == 'L': return (-1, 0)
  elif d == 'D': return (0, -1)
  elif d == 'U': return (0, 1)


def draw_wire(wire):
  head = (0,0)
  this_grid = set()
  for segment in wire:
    (dx,dy) = get_direction(segment[0])
    length = int(segment[1:])
    for i in range(length):
      head = (head[0] + dx, head[1] + dy)
      if head[0] < x_range[0]:
        x_range[0] = head[0]
      elif head[0] > x_range[1]:
        x_range[1] = head[0]
      if head[1] < y_range[0]:
        y_range[0] = head[1]
      elif head[1] > y_range[1]:
        y_range[1] = head[1]
      
      this_grid.add(head)
  grid.extend(this_grid)

for wire in wires:
  draw_wire(wire.split(','))

occurrences = {}
for block in grid:
  try:
    occurrences[block] += 1
  except KeyError:
    occurrences[block] = 1

intersections = [x for x,n in occurrences.items() if n > 1]
closest = (None, math.inf)
for i in intersections:
  d = abs(i[0]) + abs(i[1])
  if d < closest[1]:
    closest = (i,d)

#for y in range(y_range[0], y_range[1]+1):
#  for x in range(x_range[0], x_range[1]+1):
#    if (x,y) == (0,0):
#      print('O',end='')
#      continue
#    o = occurrences.get((x,y),0)
#    if o == 0:
#      print('.', end='')
#    elif o == 1:
#      print('=', end='')
#    else:
#      print('X', end='')
#  print('')

# To find the distance along a wire, we'll retrace our steps.
def steps_to_intersections(wire):
  head = (0,0)
  steps = 0
  for segment in wire:
    (dx,dy) = get_direction(segment[0])
    length = int(segment[1:])
    for i in range(length):
      head = (head[0] + dx, head[1] + dy)
      steps += 1
      if head in intersections:
        yield (head, steps)

int_steps = {i:0 for i in intersections}

for wire in wires:
  for (i,s) in steps_to_intersections(wire.split(',')):
    int_steps[i] += s

print(min(int_steps.items(), key=lambda item: item[1]))