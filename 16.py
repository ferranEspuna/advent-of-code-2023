import numpy as np
from collections import deque
from functools import partial
from time import perf_counter

from tqdm import tqdm


def bfs(start, get_next):
    visited = dict()
    not_visited = deque()
    not_visited.append((start, 0))

    while not_visited:
        current, current_depth = not_visited.popleft()
        visited[current] = current_depth
        for n in get_next(current):
            if n not in visited:
                not_visited.append((n, current_depth + 1))

    return visited


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

    for i in tqdm(range(n)):

        start_state = ((i, 0), (0, 1))

        visited_states = bfs(start_state, get_next_state_chars)
        visited_positions = set(pos for pos, _ in visited_states.keys())
        l = len(visited_positions)
        max_neighbors = max(max_neighbors, l)

        start_state = ((i, m - 1), (0, -1))
        visited_states = bfs(start_state, get_next_state_chars)
        visited_positions = set(pos for pos, _ in visited_states.keys())
        l = len(visited_positions)
        max_neighbors = max(max_neighbors, l)

    for j in tqdm(range(m)):
        start_state = ((0, j), (1, 0))
        visited_states = bfs(start_state, get_next_state_chars)
        visited_positions = set(pos for pos, _ in visited_states.keys())
        l = len(visited_positions)
        max_neighbors = max(max_neighbors, l)

        start_state = ((n - 1, j), (-1, 0))
        visited_states = bfs(start_state, get_next_state_chars)
        visited_positions = set(pos for pos, _ in visited_states.keys())
        l = len(visited_positions)
        max_neighbors = max(max_neighbors, l)

    t1 = perf_counter()
    print(t1 - t0)

    print(max_neighbors)
