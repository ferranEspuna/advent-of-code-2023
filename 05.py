from typing import List, Tuple


class rangeFunction:

    @classmethod
    def from_string(cls, s: str) -> 'rangeFunction':

        a, b, c = s.split()
        return cls(int(a), int(b), int(c))

    def __init__(self, target_start: int, source_start: int, length: int):
        self.target_start: int = target_start
        self.target_end: int = target_start + length

        self.source_start: int = source_start
        self.source_end: int = source_start + length

        self.length: int = length
        self.diff = self.target_start - self.source_start

    def __call__(self, source: int) -> int:
        if self.source_start <= source < self.source_end:
            return source - self.source_start + self.target_start

    def apply_to_range(self, rng: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:

        if rng[0] >= rng[1]:
            return [], []

        if rng[0] <= self.source_start:
            if rng[1] < self.source_start:
                return [], [rng]
            elif rng[1] < self.source_end:
                return (
                    [(self.target_start, rng[1] + self.diff)],
                    [(rng[0], self.source_start - 1)]
                )
            else:
                return (
                    [(self.target_start, self.target_end)],
                    [(rng[0], self.source_start - 1), (self.source_end, rng[1])]
                )

        elif rng[0] < self.source_end:
            if rng[1] < self.source_end:
                return (
                    [(rng[0] + self.diff, rng[1] + self.diff)],
                    []
                )
            else:
                return (
                    [(rng[0] + self.diff, self.target_end)],
                    [(self.source_end, rng[1])]
                )

        else:
            return [], [rng]

    def apply_to_ranges(self, rngs: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        done = []
        todo = []
        for rng in rngs:
            d, t = self.apply_to_range(rng)
            done.extend(d)
            todo.extend(t)
        return done, todo


class many_range_function:

    @classmethod
    def from_string(cls, s: str) -> 'many_range_function':
        return cls([rangeFunction.from_string(x) for x in s.strip().split('\n')[1:]])

    def __init__(self, funcs: List[rangeFunction]):
        self.functions = funcs

    def __call__(self, source):

        for f_ in self.functions:
            target = f_(source)
            if target is not None:
                return target

        return source

    def apply_to_range(self, rng: Tuple[int, int]) -> list[tuple[int, int]]:
        todo = [rng]
        all_done = []
        for f_ in self.functions:
            done, todo = f_.apply_to_ranges(todo)
            all_done.extend(done)
            if not todo:
                break

        return all_done + todo

    def apply_to_ranges(self, rngs: List[Tuple[int, int]]) -> list[tuple[int, int]]:
        final = []
        for rng in rngs:
            final.extend(self.apply_to_range(rng))
        return final


class multimap:

    @classmethod
    def from_string(cls, s: str) -> 'multimap':
        return cls([many_range_function.from_string(x) for x in s.split('\n\n')])

    def __init__(self, funcs: List[many_range_function]):
        self.functions = funcs

    def __call__(self, source):
        for f_ in self.functions:
            source = f_(source)
        return source

    def apply_to_range(self, rng: Tuple[int, int]) -> list[tuple[int, int]]:
        rngs = [rng]
        for f_ in self.functions:
            rngs = f_.apply_to_ranges(rngs)
        return rngs

    def apply_to_ranges(self, rngs: List[Tuple[int, int]]) -> list[tuple[int, int]]:
        my_final_ranges = []
        for rng in rngs:
            my_final_ranges.extend(self.apply_to_range(rng))

        return my_final_ranges


if __name__ == '__main__':
    with open('input/input.txt') as f:
        seed_line = f.readline()
        seeds = [int(x) for x in seed_line.split()[1:]]
        m = multimap.from_string(f.read())


        def range_gen():
            for i in range(0, len(seeds), 2):
                start = seeds[i]
                end = start + seeds[i + 1]
                yield start, end

    print(min(m.apply_to_ranges(list(range_gen()))))
