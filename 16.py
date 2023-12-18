import sys
import numpy as np
from collections import deque, defaultdict
from functools import partial, cache
from time import perf_counter

from tqdm import tqdm

sys.setrecursionlimit(100000)


def kosajaru(starts_, get_next):

    inverse_graph = defaultdict(list)
    visited = set()
    ass = dict()
    inv_ass = defaultdict(list)
    ordered_nodes = []

    def visit(node):

        for n_ in get_next(node):
            inverse_graph[n_].append(node)

        if node in visited:
            return

        visited.add(node)

        for n_ in get_next(node):
            visit(n_)

        ordered_nodes.append(node)

    for start_ in starts_:
        visit(start_)

    def assign(node, root):
        if node in ass:
            return
        ass[node] = root
        inv_ass[root].append(node)
        for _n in inverse_graph[node]:
            assign(_n, root)

    for node_ in reversed(ordered_nodes):
        assign(node_, node_)

    return ass, inv_ass, ordered_nodes


def get_next_dirs_maze(state, maze):
    pos, dire = state
    dire_y, dire_x = dire

    if maze[pos] == '.':
        return [dire]

    if maze[pos] == '/':
        return [(-dire_x, -dire_y)]

    if maze[pos] == '\\':
        return [(dire_x, dire_y)]

    if maze[pos] == '-':
        if dire_x == 0:
            return [(0, 1), (0, -1)]
        else:
            return [dire]

    if maze[pos] == '|':
        if dire_y == 0:
            return [(1, 0), (-1, 0)]
        else:
            return [dire]

    raise Exception('Unknown char: {}'.format(maze[pos]))


def get_next_states_maze(state, maze):
    n, m = maze.shape

    (px, py), _ = state
    for dire_x, dire_y in get_next_dirs_maze(state, maze):
        new_px = px + dire_x
        new_py = py + dire_y
        if 0 <= new_px < m and 0 <= new_py < n:
            yield (new_px, new_py), (dire_x, dire_y)


if __name__ == "__main__":

    with open('input/input.txt') as f:
        chars = np.array([
            [x for x in line.strip()]
            for line in f
        ])

    n, m = chars.shape

    max_neighbors = float('-inf')
    get_next_state_chars = partial(get_next_states_maze, maze=chars)

    t0 = perf_counter()

    starts = []

    for i in range(n):
        starts.append(
            ((i, 0), (0, 1))
        )

        starts.append(
            ((i, m - 1), (0, -1))
        )

    for j in range(m):
        starts.append(((0, j), (1, 0)))
        starts.append(((n - 1, j), (-1, 0)))

    print('running kosajaru')
    assigned, inv_assigned, inv_graph = kosajaru(starts, get_next_state_chars)

    print(len(inv_assigned))

    @cache
    def find_all_neighbors(root):
        return {assigned[child] for rep in inv_assigned[root] for child in get_next_state_chars(rep)}

    @cache
    def find_all_children(root):

        children = find_all_neighbors(root)

        if root in children:
            children.remove(root)

        return {root} | set(assigned[x] for child in children for x in find_all_children(child))


    for start in tqdm(starts):
        my_children = find_all_children(assigned[start])

        all_representatives = set(

            x[0] for child in my_children for x in inv_assigned[child]
        )
        max_neighbors = max(max_neighbors, len(all_representatives))

    t1 = perf_counter()
    print(t1 - t0)

    print(max_neighbors)
