with open("input.txt", "r") as f:
    raw_data = [int(digit) for digit in f.readline()]

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH*HEIGHT

layers = []
for i in range(len(raw_data) // LAYER_SIZE):
    layers.append(raw_data[i*LAYER_SIZE:(i+1)*LAYER_SIZE])

image = []
for row in range(HEIGHT):
    row_data = []
    for col in range(WIDTH):
        i = (row*WIDTH)+col
        for l in layers:
            if l[i] == 2:
                continue
            else:
                row_data.append(l[i])
                break
    image.append(row_data)

with open("out.txt", "w") as f:
    for row in image:
        for col in row:
            f.write('#' if col == 1 else ' ')
        f.write('\n')
