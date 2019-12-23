import itertools

with open('input.txt', 'r') as f:
    moves = f.read().splitlines()

def deal_into_new(deck):
    yield from reversed(list(deck))

def cut_N(deck, n):
    deck = list(deck)
    top = deck[n:]
    bottom = deck[:n]
    yield from top
    yield from bottom

def increment_N(deck,n):
    deck = list(deck)
    new_deck = {}
    for i,v in enumerate(deck):
        new_deck[(i*n) % len(deck)] = v
    for i in range(len(new_deck)):
        yield new_deck[i]

def run_moves(deck, moves):
    for move in moves:
        if move == 'deal into new stack':
            deck = deal_into_new(deck)
        elif move.startswith('cut '):
            deck = cut_N(deck, int(move[4:]))
        elif move.startswith('deal with increment '):
            deck = increment_N(deck, int(move[20:]))
        else:
            print("ERR:",move)
    return list(deck)

test_1 = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".splitlines()

deck = range(10)
print(run_moves(deck, test_1))

deck = range(10007)
print(list(run_moves(deck,moves)).index(2019))
