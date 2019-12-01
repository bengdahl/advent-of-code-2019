import math

with open("input.txt", "r") as f:
    masses = [int(line.strip()) for line in f.readlines()]

def calculate_fuel(mass):
    accumulated = 0
    while True:
        fuel = math.floor(mass/3) - 2
        if fuel <= 0:
            break
        accumulated += fuel
        mass = fuel
    return accumulated

print("fuel for mass 1969:",calculate_fuel(1969))

fuel_counts = [calculate_fuel(m) for m in masses]
print(fuel_counts)
fuel_sum = sum(fuel_counts)
print(fuel_sum)
