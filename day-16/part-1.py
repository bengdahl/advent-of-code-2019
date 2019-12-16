from itertools import chain, repeat, islice, cycle
import time

with open('input.txt', 'r') as f:
    data = [int(d) for d in f.readline()]

pattern = [0, 1, 0, -1]


def phase(data):
    result = []
    for i in range(len(data)):
        new_pattern = cycle(chain(*(repeat(c, i+1) for c in pattern)))
        # Pop out the first element in the cycle
        next(new_pattern)

        d = sum(n*c for n, c in zip(data, new_pattern))
        result.append(abs(d) % 10)
    return result


start = time.time()
for i in range(100):
    data = phase(data)
end = time.time()
print(''.join(str(n) for n in data[:8]))
print('Time:', end-start)
