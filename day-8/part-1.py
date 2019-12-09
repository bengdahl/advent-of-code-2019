with open("input.txt", "r") as f:
    raw_data = [int(digit) for digit in f.readline()]

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH*HEIGHT

layers = []
for i in range(len(raw_data) // LAYER_SIZE):
    layers.append(raw_data[i*LAYER_SIZE:(i+1)*LAYER_SIZE])

num_zeroes = [l.count(0) for l in layers]

least_zeroes = min(enumerate(num_zeroes), key=lambda x: x[1])[0]

print(layers[least_zeroes].count(1) * layers[least_zeroes].count(2))