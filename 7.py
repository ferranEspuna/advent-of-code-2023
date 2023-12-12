from collections import Counter

cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
lc = len(cards)
strengths = {x: lc - i for i, x in enumerate(cards)}


def hand_type(hand):

    hand_without_jokers = [x for x in hand if x != 'J']
    c = Counter(hand_without_jokers)
    v = sorted(c.values(), reverse=True)
    n_of_jokers = 5 - len(hand_without_jokers)

    if n_of_jokers == 5:
        return 5

    v[0] += n_of_jokers

    if v[0] == 5:
        return 5

    if v[0] == 4:
        return 4

    if v[0] == 3:
        if v[1] == 2:
            return 3.5
        return 3

    if v[0] == 2:
        if v[1] == 2:
            return 2.5
        return 2

    return 1


def hand_power(hand):
    return (hand_type(hand), *(strengths[x] for x in hand))


if __name__ == '__main__':
    with open('input/input.txt') as f:
        print(
            sum(
                (i + 1) * bid
                for i, (_, bid) in
                enumerate(
                    sorted(
                        (hand_power(hand), int(bid))
                        for hand, bid in
                        map(str.split, f)
                    )
                )
            )
        )
