import itertools

with open('input.txt', 'r') as f:
    moves = f.read().splitlines()

'''
Let's work backwards

Let I_t be the position after going backwards t moves
Let L be the length of the deck

# Cut N:

|--N-||L-N|
------=====
   |  ^
   v  |
=====------
If N is positive, 
    I_t = (I_t+1 - N) if I_t+1 > N
          (I_t+1 + L-N) otherwise
or,
    I_t+1 = (I_t - L-N) if I_t > L-N
            (I_t + N) otherwise

# Deal into new:

0123 ... L-1
   |  ^
   v  |
L-1 ... 3210

    I_t = L-1 - I_t+1
or,
    I_t+1 = L-1 - I_t

# Increment N:

I_t = N * I_t+1 mod L

I_t+1 = (I_t + K * L) / N
    where K is the least number such that I_t + K is divisible by L
'''

def reverse_flip(i,l):
    return l-1-i

def reverse_cut_N(i,l,N):
    if N < 0:
        ln = l + N
        if i < abs(N):
            return i + ln
        else:
            return i - abs(N)
    else:
        ln = l - N
        if i < ln:
            return i + N
        else:
            return i - ln

def reverse_increment_N(i,l,N):
    k = 0
    while (i + k) % N != 0:
        # print('k',k, (i+k) % N)
        k += l
    return (i+k) // N


def reverse_moves(i, l, moves):
    t = 0
    for move in moves:
        t += 1
        # print(t,move,i)
        if move == 'deal into new stack':
            i = reverse_flip(i,l)
        elif move.startswith('cut '):
            i = reverse_cut_N(i,l, int(move[4:]))
        elif move.startswith('deal with increment '):
            i = reverse_increment_N(i,l, int(move[20:]))
        else:
            print("ERR:", move)
    return i


test_moves = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".splitlines()

assert reverse_moves(7,10, reversed(test_moves)) == 0

PREV_SOLN = 1879

assert reverse_moves(PREV_SOLN,10007, reversed(moves)) == 2019

# I've proven that my solution will return the correct answer, but it is not optimized very well at all

# The *real* solution will be using /u/_mcpower's findings

offset, increment = 0, 1
SHUFFLES = 101741582076661
CARDS = 119315717514047

def shuffle(off,inc,moves):
    for move in moves:
        if move == 'deal into new stack':
            inc *= -1
            inc %= CARDS
            off += inc
            off %= CARDS
        elif move.startswith('cut '):
            n = int(move[4:])
            off += inc * n
            off %= CARDS
        elif move.startswith('deal with increment '):
            inv = pow(n % CARDS,CARDS-2,CARDS)
            inc *= inv
            inc %= CARDS
        else:
            print("ERR:", move)
    return off,inc


offset_diff, increment_mul = shuffle(offset, increment, reversed(moves))

huge_inc = pow(increment_mul, SHUFFLES, CARDS)
huge_off = offset_diff * (1 - increment) * pow((1-increment_mul) % CARDS, CARDS-2, CARDS)

print('I dont have a working program for part 2')