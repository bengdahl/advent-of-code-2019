import time

with open('input.txt', 'r') as f:
    data = [int(d) for d in f.readline()]
    offset = int(''.join([str(d) for d in data[:7]]))

# The phase computation propagates backwards, so if we
# want to start from offset N, we only need to know the
# numbers that come after offset N
data = (data * 10000)[offset:]

# If the offset is greater than half the length of the
# data, each line is just the sum of digits past the
# offset.
#
# Length = 6
# if Offset >= 3:
# i = 0 | 1 0 -1 0 1 0  |
# i = 1 | 0 1 1 0 0 1   |-- Don't count because of
# i = 2 | 0 0 1 1 1 0   |   the reasons listed on line 7
# i = 3 | 0 0 0 1 1 1   <-- Sum of digits d[3:]
# i = 4 | 0 0 0 0 1 1   <-- Above sum - d[3]
# i = 5 | 0 0 0 0 0 1   <-- Above sum - d[4]


def phase(data):
    result = []
    p_sum = sum(data)
    for i in range(len(data)):
        t = p_sum
        p_sum -= data[i]
        result.append(abs(t) % 10)
    return result


start = time.time()
# Our optimization only works if O > |d|/2
assert offset > len(data) / 2
for i in range(100):
    data = phase(data)
end = time.time()

print(''.join(str(n) for n in data[:8]))
print('Time:', end-start)
