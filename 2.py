from collections import Counter
from math import prod


def power(games):
    final_counter = Counter()
    games = games.split(';')
    for game in games:
        color_counter = Counter()
        for color_count in game.split(','):
            count, color = color_count.strip().split(' ')
            count = int(count)
            color_counter[color] += count

        for c, n in color_counter.items():
            final_counter[c] = max(final_counter[c], n)

    return prod(final_counter.values())


if __name__ == '__main__':

    with open('input/input.txt', 'r') as f:
        total = 0
        for line in f:

            id_, games_ = line.split(':')
            total += power(games_)
        print(total)
