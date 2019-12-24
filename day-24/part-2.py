with open('input.txt', 'r') as f:
    board = tuple(f.read().splitlines())

layers = {0: board}

def get_space(c, r, board):
    if c < 0:
        return -1
    elif r < 0:
        return -1
    elif c >= 5:
        return -1
    elif r >= 5:
        return -1
    elif r == 2 and c == 2:
        return 1
    try:
        row = board[r]
        return row[c]
    except IndexError:
        return '.'

def get_neighbors(c,r,l,layers):
    deltas = ((0,1),(0,-1),(1,0),(-1,0))
    count = 0
    new_layer = 0
    board = layers.get(l, ['.....']*5)
    for dc,dr in deltas:
        s = get_space(c+dc, r+dr, board)
        # print("{}: Got".format(time),s,"on",c+dc,r+dr,"in board",l)
        if s == 1:
            if l+1 in layers:
                if (dc,dr) == (-1,0):
                    count += sum(1 for t in list(zip(*layers[l+1]))[4] if t == '#')
                elif (dc,dr) == (1,0):
                    count += sum(1 for t in list(zip(*layers[l+1]))[0] if t == '#')
                elif (dc,dr) == (0,-1):
                    count += sum(1 for t in layers[l+1][4] if t == '#')
                elif (dc,dr) == (0,1):
                    count += sum(1 for t in layers[l+1][0] if t == '#')
            elif board[r][c] == '#':
                new_layer = 1
        elif s == -1:
            if l-1 in layers:
                if (dc, dr) == (-1, 0):
                    count += 1 if layers[l-1][2][1] == '#' else 0
                elif (dc, dr) == (1, 0):
                    count += 1 if layers[l-1][2][3] == '#' else 0
                elif (dc, dr) == (0, -1):
                    count += 1 if layers[l-1][1][2] == '#' else 0
                elif (dc, dr) == (0, 1):
                    count += 1 if layers[l-1][3][2] == '#' else 0
            elif board[r][c] == '#':
                new_layer = -1
        elif s == '#':
            count += 1
    # if new_layer != 0:
        # print("need to run a new layer: ", l+new_layer)
    return count,new_layer

def evaluate_board(l,layers,layers_new):
    if l in layers_done:
        return
    layers_done.add(l)
    board = layers.get(l, ['.....']*5)
    board_new = []
    for r in range(len(board)):
        r_new = ""
        for c in range(len(board[r])):
            if (c, r) == (2, 2):
                r_new += '.'
                continue
            neighbors, new_layer = get_neighbors(c, r, l, layers)
            # print(r,c,l,neighbors)
            if board[r][c] == '#':
                if neighbors == 1:
                    r_new += '#'
                else:
                    r_new += '.'
            else:
                if neighbors in (1, 2):
                    r_new += '#'
                else:
                    r_new += '.'
            if new_layer != 0:
                evaluate_board(l+new_layer, layers, layers_new)
        board_new.append(r_new)
    layers_new[l] = tuple(board_new)

for time in range(200):
    layers_new = {}
    layers_done = set()
    for l, board in layers.items():
        evaluate_board(l,layers,layers_new)
    layers = layers_new
    
    # for l,b in layers.items():
    #     print(l)
    #     print('\n'.join(b))
    # print()

print(sum(1 for board in layers.values() for row in board for c in row if c == '#'), "bugs")
