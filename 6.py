from math import sqrt
from math import ceil, floor

with open('input/input.txt') as f:
    t = int(''.join(f.readline().strip().split()[1:]))
    d = int(''.join(f.readline().strip().split()[1:]))

    pos = (t + sqrt(t ** 2 - 4 * d)) / 2
    neg = (t - sqrt(t ** 2 - 4 * d)) / 2
    pos = floor(pos)
    neg = ceil(neg)

    if pos * (t - pos) == d:
        pos -= 1

    if neg * (t - neg) == d:
        neg += 1

    print(pos, neg)
    total_ways = (pos - neg + 1)
    print(total_ways)
