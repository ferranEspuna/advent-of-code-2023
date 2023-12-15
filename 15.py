from functools import reduce


def h(s):
    return reduce(
        lambda x, y: ((x + ord(y)) * 17) % 256,
        s,
        0
    )


def parse(s):
    if s[-1] == '-':
        return '-', {'label': s[:-1]}

    if s[-2] == '=':
        return '=', {'label': s[:-2], 'focal': int(s[-1])}

    raise ValueError(f'Unexpected format: "{s}"')


def process(operation, boxes):
    opcode, details = parse(operation)
    new_label = details['label']
    idx = h(new_label)

    box = boxes[idx]

    if opcode == '-':

        for position, (old_label, old_lens) in enumerate(box):
            if old_label == new_label:
                del box[position]
                break

        return

    if opcode == '=':
        new_focal = details['focal']
        for position, (old_label, old_lens) in enumerate(box):
            if old_label == new_label:
                box[position] = (new_label, new_focal)
                break
        else:
            box.append((new_label, new_focal))

        return

    raise ValueError(f'Unexpected Opcode: {opcode} in operation "{operation}"')


def power(args):
    box_idx, box = args

    return (box_idx + 1) * sum(
        (lens_idx + 1) * focal
        for lens_idx, (_, focal)
        in enumerate(box)
    )


if __name__ == '__main__':

    current_boxes = [[] for _ in range(256)]

    with open('input/input.txt') as f:
        for op in f.read().strip().split(','):
            process(op, current_boxes)

    print(sum(map(power, enumerate(current_boxes))))
