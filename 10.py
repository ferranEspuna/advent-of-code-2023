import numpy as np

joints = {
    '|': ('up', 'down'),
    '-': ('left', 'right'),
    '7': ('right', 'up'),
    'F': ('left', 'up'),
    'L': ('left', 'down'),
    'J': ('right', 'down'),
}

directions = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
}

opposites = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left',
}

direction_and_char_to_new_direction = {
                                          (first, char): opposites[last]
                                          for char, (first, last) in joints.items()
                                      } | {
                                          (last, char): opposites[first]
                                          for char, (first, last) in joints.items()
                                      }


def go(maze, pos, dire):
    pos = tuple(np.array(pos) + np.array(directions[dire]))
    char = maze[pos]
    if char == 'S':
        return pos, None
    dire = direction_and_char_to_new_direction[(dire, char)]
    return pos, dire


if __name__ == '__main__':
    with open('input/input.txt') as f:
        chars = np.array([
            [x for x in line.strip()]
            for line in f
        ])

    x0, y0 = np.where(chars == 'S')
    x0 = x0[0]
    y0 = y0[0]
    first_position = last_position = (x0, y0)

    initial_directions = []

    for dire in directions.keys():
        try:
            go(chars, first_position, dire)
        except:
            continue

        initial_directions.append(dire)

    assert len(initial_directions) == 2
    first_direction, last_direction = initial_directions

    i = 0
    while True:
        last_position, last_direction = go(chars, last_position, last_direction)
        i += 1
        if chars[last_position] == '|':
            chars[last_position] = '!'
        elif chars[last_position] in ('F', 'J'):
            chars[last_position] = '_'
        elif chars[last_position] in ('7', 'L'):
            chars[last_position] = '+'
        else:
            chars[last_position] = 'x'
        if first_position == last_position:
            break

    dir_start = set(initial_directions)

    if dir_start == {'up', 'down'}:
        chars[first_position] = '!'
    elif dir_start == {'left', 'up'} or dir_start == {'right', 'down'}:
        chars[first_position] = '_'
    elif dir_start == {'left', 'down'} or dir_start == {'right', 'up'}:
        chars[first_position] = '+'
    else:
        chars[first_position] = 'x'

    inside_count = 0
    for i, row in enumerate(chars):
        is_inside = 0
        for j, char in enumerate(row):
            if char == '!':
                is_inside += 2
                continue
            if char == '+':
                is_inside += 1
                continue
            if char == '_':
                is_inside -= 1
                continue

            if char == 'x':
                continue

            assert is_inside % 2 == 0, f'{i}, {j}'

            if is_inside % 4 == 2:
                inside_count += 1
                chars[i, j] = 'I'

            else:
                chars[i, j] = 'O'

    print(inside_count)
