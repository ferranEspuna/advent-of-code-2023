def pred_next(values):

    flag = False
    if not values:
        return 0

    diffs = []
    for i in range(len(values) - 1):
        diff = values[i + 1] - values[i]
        diffs.append(diff)
        if diff != 0:
            flag = True

    if not flag:
        return values[-1]

    nd = pred_next(diffs)
    return values[-1] + nd


with open('input/input.txt') as f:
    print(
        sum(
            map(
                pred_next,
                map(
                    lambda line: [int(x) for x in line.strip().split()][::-1],
                    f
                )
            )
        )
    )
