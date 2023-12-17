import numpy as np
import heapq
from time import perf_counter

# TODO THINK OF A BETTER HEURISTIC. RIGHT NOW IT'S OFF BECAUSE IT DOESN'T HELP
def heuristic(state, end_, c):
    if state == end_:
        return 0

    (posy, posx), (diry, dirx), steps = state
    endy, endx = end_[0]
    return abs(posy - endy) + abs(posx - endx)


def Dijkstra(c, starts_, end_=None, h=lambda x, y, z: 0):
    visited = dict()
    unvisited = [(h(start_, end_, c), start_, start_) for start_ in starts_]

    while len(unvisited) != 0:

        current_cost, current_node, current_parent = heapq.heappop(unvisited)

        if current_node not in visited:

            visited[current_node] = (current_cost, current_parent)

            for neighbor in get_nexts(current_node, c, end_):
                if neighbor not in visited:
                    heapq.heappush(unvisited,
                                   (c[neighbor[0]] + current_cost + h(neighbor, end_, c) -h(current_node, end_, c),
                                    neighbor,
                                    current_node)
                                   )

    if end_ is None:
        return {node: visited[node][0] for node in visited}

    if end_ in visited:

        current_node = end_
        current_cost, current_parent = visited[current_node]
        pth = [(current_node, current_cost)]

        while current_node not in starts_:
            current_cost, current_parent = visited[current_node]
            pth.append((current_node, current_cost))
            current_node = current_parent

        pth.append((current_node, 0))

        pth.reverse()

        return True, pth, visited[end][0]

    return False, [], 0


def get_nexts(state, c, end_):
    if state == end_:
        return []

    (posy, posx), (diry, dirx), steps = state
    dirs_turn = [(dirx, diry), (-dirx, -diry)]

    if steps >= 4:

        for dir_ in dirs_turn:
            new = (posy + dir_[0], posx + dir_[1]), (dir_[0], dir_[1]), 1
            if 0 <= new[0][0] < c.shape[0] and 0 <= new[0][1] < c.shape[1]:
                if not (((posy + dir_[0], posx + dir_[1]),) == end_):
                    yield new

    if steps < 10:
        new = (posy + diry, posx + dirx), (diry, dirx), steps + 1
        if 0 <= new[0][0] < c.shape[0] and 0 <= new[0][1] < c.shape[1]:
            if not (((posy + diry, posx + dirx),) == end_):
                yield new
            else:
                if steps >= 4 - 1:
                    yield end_


if __name__ == "__main__":
    with open('input/input.txt') as f:
        chars = np.array([
            [int(x) for x in line.strip()]
            for line in f
        ])

    starts = [
        ((0, 0), (1, 0), 0),
        ((0, 0), (0, 1), 0)
    ]

    n, m = chars.shape
    end = ((n - 1, m - 1),)

    start = perf_counter()
    done, path, value = Dijkstra(chars, starts, end)
    end = perf_counter()
    print(end - start)

    print(value)
