from functools import cache


@cache
def get_ways(s, nums, require_dot=False, tabs=0):
    if len(s) == 0:
        return len(nums) == 0

    if len(nums) == 0:
        return len(s) == 0

    if s[0] == '#' and require_dot:
        return 0

    if len(s) < sum(nums) + len(nums) - 1 + require_dot:
        return 0

    num = nums[0]
    other_nums = nums[1:]

    if any((s[i] == '.' for i in range(require_dot, num + require_dot))):
        return 0

    ret = 0

    for i in range(num + require_dot, len(s) + require_dot):
        ret += get_ways(s[i:], other_nums, require_dot=True, tabs=tabs + 1)
        if i == len(s) or s[i] == '#':
            break

    return ret


total = 0

with open('input/input.txt') as f:
    for line in f:
        my_s, my_nums = line.split()
        my_nums = tuple([0] + [int(x) for x in my_nums.split(',')] * 5)
        my_s = '.' + '?'.join([my_s] * 5)
        total += get_ways(my_s, my_nums)

print(total)
