from collections import defaultdict
from math import prod
from unittest import result


IN = open("./6.txt", "r").read().splitlines()

ops = defaultdict(list)
lengths = []
ops = []

# get lengths
current = 0
current_op = None
OPS_LINE = IN[-1]

for i in range(len(OPS_LINE)):
    if OPS_LINE[i] == "+":
        if current_op is not None:
            lengths.append(current)
            ops.append(current_op)
            current = 0
        current_op = "+"

    elif OPS_LINE[i] == "*":
        if current_op is not None:
            lengths.append(current)
            ops.append(current_op)
            current = 0
        current_op = "*"
    current += 1
lengths.append(current)
ops.append(current_op)

print(lengths)

grid = defaultdict(list)


def rotate_90_counter_clockwise(grid):
    return [list(row) for row in zip(*grid)][::-1]


result = 0
for index, width in enumerate(lengths):
    height = len(IN) - 1
    op = ops[index]

    start_col = sum(lengths[:index])
    end_col = start_col + width
    start_row = 0
    end_row = height

    grid = []
    for y in range(start_row, end_row):
        grid.append([x for x in IN[y][start_col:end_col]])
    print(grid)

    grid = rotate_90_counter_clockwise(grid)
    strings = ["".join(row) for row in grid]
    print(strings)
    ints = [int(x) for x in strings if x.strip() != ""]

    if op == "+":
        result += sum(ints)
    elif op == "*":
        result += prod(ints)


print(result)
