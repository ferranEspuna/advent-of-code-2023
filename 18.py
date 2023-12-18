import numpy as np
import matplotlib.pyplot as plt

min_x = min_y = max_x = max_y = 0
pos = (0, 0)

dire_to_vec = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
if __name__ == "__main__":

    instructions = []

    with open('input/input.txt') as f:
        for line in f:
            dire, steps, color = line.strip().split()
            steps = int(steps)
            dire_y, dire_x = dire_to_vec[dire]
            instructions.append((dire_y, dire_x, steps, color))
            pos = pos[0] + dire_y * steps, pos[1] + dire_x * steps
            min_x = min(min_x, pos[1])
            min_y = min(min_y, pos[0])
            max_x = max(max_x, pos[1])
            max_y = max(max_y, pos[0])

    lab = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=int)

    start_pos = (-min_y, -min_x)
    pos = start_pos
    for dire_y, dire_x, steps, color in instructions:

        lab[pos] += dire_y

        for _ in range(steps-1):
            pos = pos[0] + dire_y, pos[1] + dire_x
            lab[pos] += 2 * dire_y

        pos = pos[0] + dire_y, pos[1] + dire_x
        lab[pos] += dire_y

    lab_filled = np.zeros_like(lab)

    for i, row in enumerate(lab):
        inside = 0
        for j, pos in enumerate(row):

            inside += pos
            inside %= 4

            if inside != 0 or pos != 0:
                lab_filled[i, j] = 1

    print(lab.shape)
    plt.imshow(lab)
    plt.show()
    plt.imshow(lab_filled)
    plt.show()
    #print()
    #print(lab_filled)
    print(lab_filled.sum())
