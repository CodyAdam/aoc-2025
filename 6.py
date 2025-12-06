from collections import defaultdict
from math import prod


IN = open("./6.txt", "r").read().splitlines()

ops = defaultdict(list)

for row, line in enumerate(IN):
    for column, value in enumerate(line.split()):
        ops[column].append(value)

result = 0
for values in ops.values():
    nums = map(int, values[:-1])
    op = values[-1]

    if op == "+":
        result += sum(nums)
    elif op == "*":
        result += prod(nums)


print(result)
