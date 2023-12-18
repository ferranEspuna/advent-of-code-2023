import numpy as np
import matplotlib.pyplot as plt

min_x = min_y = max_x = max_y = 0

instructions = []


def get_index(loc, sorted_locs):
    return sorted_locs.index(loc)


def get_indices(start, end, sorted_locs):
    return get_index(start, sorted_locs), get_index(end, sorted_locs)


dire_to_vec = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
dire_index = ['R', 'D', 'L', 'U']

part = 2

if __name__ == "__main__":

    pos = (0, 0)
    positions_x = {0}
    positions_y = {0}

    with open('input/input.txt') as f:

        for line in f:
            dire_, steps_, color_ = line.strip().split()

            match part:
                case 1:
                    steps = int(steps_)
                    dire_y, dire_x = dire_to_vec[dire_]

                case 2:
                    # actually, the elves are f***ing stupid
                    assert len(color_) == 9
                    steps = int(color_[2:7], 16)
                    dire_name = dire_index[int(color_[7])]
                    dire_y, dire_x = dire_to_vec[dire_name]

                case _:
                    raise Exception('Unknown part: {}'.format(part))

            new_pos = pos[0] + dire_y * steps, pos[1] + dire_x * steps

            if dire_y != 0:

                instructions.append(((pos[0],), pos[1], dire_y))

                instructions.append(((pos[0], new_pos[0]), pos[1], 2 * dire_y))

                instructions.append(((new_pos[0],), pos[1], dire_y))

            positions_y.add(new_pos[0] - 1)
            positions_y.add(new_pos[0] + 1)
            positions_x.add(pos[1]-1)
            positions_x.add(pos[1]+1)

            pos = new_pos

            positions_y.add(pos[0])
            positions_x.add(pos[1])

    positions_x = sorted(positions_x)
    positions_y = sorted(positions_y)

    row_multipliers = [1] + [positions_y[i] - positions_y[i-1] for i in range(1, len(positions_y))]
    assert sum(row_multipliers) == positions_y[-1] - positions_y[0] + 1
    column_multipliers = [1] + [positions_x[i + 1] - positions_x[i] for i in range(len(positions_x) - 1)]
    assert sum(column_multipliers) == positions_x[-1] - positions_x[0] + 1

    n, m = len(positions_y), len(positions_x)
    grid = np.zeros((n, m), dtype=np.int8)

    for y_pack, x, summand in instructions:

        x = get_index(x, positions_x)

        if len(y_pack) == 2:
            y_start, y_end = y_pack
            y_start, y_end = get_indices(y_start, y_end, positions_y)
            y_start, y_end = sorted((y_start, y_end))
            y_start += 1
            grid[y_start: y_end, x] += summand
        else:
            assert len(y_pack) == 1
            y, = y_pack
            y = get_index(y, positions_y)
            grid[y, x] += summand

    painted = np.zeros((n, m), dtype=np.int8)

    running_total = 0

    for i in range(n):
        inside = 0
        for j in range(m):
            pos = grid[i, j]
            inside += pos
            inside %= 4

            if inside != 0 or pos != 0:
                painted[i, j] = 1
                running_total += row_multipliers[i] * column_multipliers[j]

    print(running_total)

    plt.imshow(painted)
    plt.show()
