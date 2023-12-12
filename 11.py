import numpy as np


def sum_distances(axis):
    total = 0
    expansions = np.zeros_like(axis)

    for i in range(1, len(axis)):
        expansions[i] = expansions[i - 1]

        if axis[i] == 0:
            expansions[i] += 1
            continue

        for j in range(i):
            total += (i - j + (expansions[i] - expansions[j]) * (1_000_000-1)) * axis[i] * axis[j]
    return total


if __name__ == '__main__':
    with open('input/input.txt') as f:
        chars = np.array([
            [x for x in line.strip()]
            for line in f
        ])

    galaxies = (chars == '#')

    galaxy_rows = galaxies.sum(axis=1)
    galaxy_cols = galaxies.sum(axis=0)
    print(galaxy_cols)

    print(sum_distances(galaxy_rows) + sum_distances(galaxy_cols))
