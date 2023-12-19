from functools import partial
from copy import copy
from math import prod


def is_valid(rng):
    return rng[0] < rng[1]


def greater(d_, property_, num, result):
    rng_start, rng_end = d_[property_]

    accept_rng = (num + 1, rng_end)
    reject_rng = (rng_start, num + 1)

    if is_valid(accept_rng):
        d_accept = copy(d_)
        d_accept[property_] = accept_rng

    else:
        d_accept = None

    if is_valid(reject_rng):
        d_reject = copy(d_)
        d_reject[property_] = reject_rng
    else:
        d_reject = None

    return (d_accept, result), d_reject


def smaller(d_, property_, num, result):
    rng_start, rng_end = d_[property_]

    accept_rng = (rng_start, num)
    reject_rng = (num, rng_end)

    if is_valid(accept_rng):
        d_accept = copy(d_)
        d_accept[property_] = accept_rng

    else:
        d_accept = None

    if is_valid(reject_rng):
        d_reject = copy(d_)
        d_reject[property_] = reject_rng
    else:
        d_reject = None

    return (d_accept, result), d_reject


def parse_workflow(line):
    name_, end = line.split('{')
    end = end[:-1]
    pieces = end.split(',')

    functions = []

    for piece in pieces[:-1]:

        piece_x, piece_y = piece.split(':')

        if '<' in piece_x:
            first, second = piece_x.split('<')
            functions.append(partial(smaller, property_=first, num=int(second), result=piece_y))

        else:
            assert '>' in piece_x
            first, second = piece_x.split('>')
            functions.append(partial(greater, property_=first, num=int(second), result=piece_y))

    functions.append(
        lambda d: ((d, pieces[-1]), None)
    )

    def big_function(d):

        done = []

        for f_ in functions:
            (d_accept, result), d_reject = f_(d)
            if d_accept is not None:
                done.append((d_accept, result))
            if d_reject is None:
                return done
            d = d_reject

        assert False

    return name_, big_function


def count_combos(d):
    if not d:
        return 0

    return prod(rng[1] - rng[0] for rng in d.values())


if __name__ == "__main__":

    workflows = {}

    with (open('input/input.txt') as f):
        for line_ in f:

            line_ = line_.strip()
            if not line_:
                break
            name, func = parse_workflow(line_)
            workflows[name] = func


    def get_all_ds(ds):

        if not ds:
            return

        for d, func_name in ds:

            if func_name == 'A':
                yield d
                continue

            if func_name == 'R':
                continue

            current_func = workflows[func_name]
            yield from get_all_ds(current_func(d))


    print(
        sum(map(count_combos, get_all_ds(
            [({'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)}, 'in')]
        )))
    )
