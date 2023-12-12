from collections import defaultdict
from functools import partial
from itertools import cycle
from itertools import product
from math import lcm, gcd, ceil
from modint import ChineseRemainderConstructor


def find_cycle(initial_state, instructions, moves):
    states_dict = dict()
    states_list = list()
    state = initial_state

    for i, instruction in enumerate(cycle(instructions)):

        mod_i = i % len(instructions)

        actual_index = states_dict.get((state, mod_i))
        if actual_index is not None:
            return states_list[:actual_index], states_list[actual_index:]

        states_dict[(state, mod_i)] = i
        states_list.append(state)

        if instruction == 'L':
            state = moves[state][0]
        else:
            state = moves[state][1]


def loop(intro, period):
    yield from intro
    yield from cycle(period)


def get_remainders(intro, period):
    for i, state in enumerate(period):
        if state.endswith('Z'):
            yield (i + len(intro)) % len(period)


def find_first_coincidence(instructions, moves):

    descriptions = list(find_cycle(k, instructions, moves) for k in moves.keys() if k.endswith('A'))
    max_intro = max(len(x[0]) for x in descriptions)
    loops = zip(*(loop(*desc) for desc in descriptions))

    for i, states in zip(range(max_intro), loops):
        if all(s.endswith('Z') for s in states):
            return i

    possible_remainders = [list(get_remainders(*desc)) for desc in descriptions]
    period_lengths = tuple(len(x[1]) for x in descriptions)
    target_lcm = lcm(*period_lengths)
    target_gcd = gcd(*period_lengths)

    remainders_mod_gcd = [defaultdict(list) for _ in range(len(possible_remainders))]
    for i, remainders in enumerate(possible_remainders):
        for rem in remainders:
            remainders_mod_gcd[i][rem % target_gcd].append(rem)

    coincidences = set(remainders_mod_gcd[0].keys()).intersection(*remainders_mod_gcd[1:])
    combinations_of_remainders = [x for rem in coincidences for x in product(*[remainders_mod_gcd[i][rem] for i in range(len(possible_remainders))])]
    final_mod = target_lcm // target_gcd
    divided = tuple(x // target_gcd for x in period_lengths)
    crt = ChineseRemainderConstructor(divided)
    m = float('inf')
    inv = pow(final_mod, -1, target_gcd)

    # we account for the time it takes to get into the loops
    loops_added = ceil(max_intro / target_lcm)
    print(f'Loops added: {loops_added}')
    time_added = loops_added * target_lcm

    for comb in combinations_of_remainders:
        target = comb[0] % target_gcd

        if any(x % target_gcd != target for x in comb[1:]):
            print(f'{comb} will never coincide!')
            continue

        unite = crt.rem(comb)
        times_to_sum = (inv * (target - unite)) % target_gcd
        final_unite = times_to_sum * final_mod + unite + time_added

        print(f'{comb} will coincide after {final_unite} steps!')

        m = min(m, final_unite)

    return m


if __name__ == '__main__':
    with open('input/input.txt') as f:
        inst = f.readline().strip()
        f.readline()

        mov = {
            origin: (dest_left, dest_right)
            for origin, dest_left, dest_right in
            map(
                lambda t: (t[0], *t[1].strip()[1:-1].split(', ')),
                map(
                    partial(str.split, sep=' = '),
                    f)
            )
        }

    print(find_first_coincidence(inst, mov))
