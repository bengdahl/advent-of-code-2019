with open("input.txt", "r") as f:
  r = tuple(int(n) for n in f.read().split('-'))

possible = []

def is_valid(n):
  has_double = False
  last_digit = 0
  has_decrease = False
  for d in str(n):
    d = int(d)
    if d == last_digit:
      has_double = True
    if d < last_digit:
      has_decrease = True
    last_digit = d
  return has_double and (not has_decrease)

for n in range(r[0],r[1]+1):
  # The number is already a six digit number by 
  # the nature of the input
  if is_valid(n):
    possible.append(n)

print(len(possible))