import numpy as np

matrices = []


def find_reflection(mat, dim=0):
    length = mat.shape[dim]
    for k in range(1, length):

        slices_left = [slice(None)] * dim + [slice(None, k)]
        slices_right = [slice(None)] * dim + [slice(k, None)]

        left = mat[tuple(slices_left)]
        right = mat[tuple(slices_right)]

        m = min(left.shape[dim], right.shape[dim])
        my_idx = [slice(None)] * dim + [slice(-m, None)]

        cmp_left = left[tuple(my_idx)]
        cmp_right = np.flip(right, dim)[tuple(my_idx)]

        if np.sum((cmp_left != cmp_right)) == 1:
            return k


def value(mat):
    val = find_reflection(mat, dim=0)
    if val:
        return val * 100

    val = find_reflection(mat, dim=1)
    if val:
        return val


def my_input(filename):

    with open(filename) as f:
        my_mat = []
        for line in f:
            l = line.strip()
            if l:
                my_mat.append([s for s in l])
            else:
                yield np.array(my_mat)
                my_mat = []

    if my_mat:
        yield np.array(my_mat)


if __name__ == "__main__":
    print(sum(map(value, my_input('input/input.txt'))))

