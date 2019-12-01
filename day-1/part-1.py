import math

with open("input.txt", "r") as f:
    masses = [int(line.strip()) for line in f.readlines()]

fuel_counts = [math.floor(m/3) - 2 for m in masses]
print(fuel_counts)
fuel_sum = sum(fuel_counts)
print(fuel_sum)