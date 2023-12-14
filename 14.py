import numpy as np
from tqdm import tqdm


def move_north(mat):
    mat2 = np.copy(mat)
    mat2[mat2 == 'O'] = '.'
    width = mat.shape[1]

    last_pos = -1 * np.ones((width,), dtype=int)

    for i, line in enumerate(mat):
        for j, char in enumerate(line):

            if char == '#':
                last_pos[j] = i
                continue

            if char == 'O':
                last_pos[j] += 1
                mat2[last_pos[j], j] = 'O'
                continue

    return mat2


def move_south(mat):
    return np.flip(
        move_north(
            np.flip(
                mat,
                0
            )
        ),
        0
    )


def move_east(mat):
    return move_south(mat.T).T


def move_west(mat):
    return move_north(mat.T).T


def cycle(mat):
    return move_east(move_south(move_west(move_north(mat))))


def strain(mat):
    return sum(
        (row == 'O').sum() * (i + 1)
        for i, row in enumerate(mat[::-1])
    )


def many_cycles(mat, k):
    indices = dict()
    states = list()

    for step in tqdm(range(k)):

        ind = indices.get(mat.data.tobytes())
        if ind is not None:
            loop_length = step - ind
            print(f'found loop of length {loop_length} after {ind} steps')
            return states[ind + (k - ind) % loop_length]

        states.append(mat)
        indices[mat.data.tobytes()] = step
        mat = cycle(mat)

    print('found no cycle :(')
    return mat


if __name__ == "__main__":
    with open('input/input.txt') as f:
        chars = np.array([
            [x for x in line.strip()]
            for line in f
        ])

    # part one
    print(strain(move_north(chars)))

    # part two
    print(strain(many_cycles(chars, 1000000000)))
