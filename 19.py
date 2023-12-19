from functools import partial

def greater(d_, property, num, result):
    return result if d_[property] > num else None

def smaller(d_, property, num, result):
    return result if d_[property] < num else None

def parse_workflow(line):
    name, end = line.split('{')
    end = end[:-1]
    pieces = end.split(',')
    #print()
    #print(name)

    functions = []

    for piece in pieces[:-1]:
        #print(piece)

        piece_x, piece_y = piece.split(':')

        if '<' in piece_x:
            first, second = piece_x.split('<')
            functions.append(partial(smaller, property=first, num=int(second), result=piece_y))

        else:
            assert '>' in piece_x
            first, second = piece_x.split('>')
            functions.append(partial(greater, property=first, num=int(second), result=piece_y))

    functions.append(
        lambda d: pieces[-1]
    )

    def big_function(d):
        for f in functions:
            out = f(d)
            if out is not None:
                return out

        assert False

    return name, big_function


def parse_object(line):
    attributes = line[1:-1].split(',')
    obj = {}
    for at in attributes:
        a, b = at.split('=')
        obj[a] = int(b)

    return obj


if __name__ == "__main__":

    workflows = {}
    accepted = []

    with (open('input/input.txt') as f):
        for line_ in f:

            line_ = line_.strip()
            if not line_:
                break

            name, func = parse_workflow(line_)
            workflows[name] = func

        for line_ in f:

            line_ = line_.strip()

            obj = parse_object(line_)
            work_name = 'in'
            #print(obj)

            while True:

                #print(work_name)
                work = workflows[work_name]
                work_name = work(obj)
                if work_name not in workflows:
                    if work_name == 'A':
                        accepted.append(obj)
                        break
                    else:
                        assert work_name == 'R'
                        break

                work = workflows[work_name]
            #print()

    print(sum(sum(obj.values()) for obj in accepted))
