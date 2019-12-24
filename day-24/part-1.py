with open('input.txt', 'r') as f:
    board = tuple(f.read().splitlines())

def get_space(c,r):
    if c < 0 or r < 0:
        return '.'
    try:
        row = board[r]
        return row[c]
    except IndexError:
        return '.'

states = set()
while True:
    print('\n'.join(board)+'\n')
    if board in states:
        score = 0
        for i,v in enumerate(c for r in board for c in r):
            if v == '#':
                score += 1 << i
        print("SCORE:",score)
        break
    states.add(board)
    board_new = []
    for r in range(len(board)):
        r_new = ""
        for c in range(len(board[r])):
            neighbors = sum(1 for dc,dr in ((1,0),(-1,0),(0,1),(0,-1)) if get_space(c+dc, r+dr) == '#')
            if board[r][c] == '#':
                if neighbors == 1:
                    r_new += '#'
                else:
                    r_new += '.'
            else:
                if neighbors in (1,2):
                    r_new += '#'
                else:
                    r_new += '.'
        board_new.append(r_new)
    board = tuple(board_new)
