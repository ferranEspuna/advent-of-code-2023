myd = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def get_first_digit(s):

    try:
        return int(s[0])
    except ValueError:
        for j in range(len(myd)):
            if len(myd[j]) <= len(line) and myd[j] == line[:len(myd[j])]:
                d = j + 1
                return d


if __name__ == '__main__':

    with open('input/input.txt.txt', 'r') as f:

        total = 0
        for line in f:
            first = last = None
            for i in range(len(line)):

                if first is None:
                    first = get_first_digit(line[i:])
                else:
                    last = get_first_digit(line[i:])

            assert first is not None
            if last is None:
                last = first

            total += last
            total += 10 * first

        print(total)
