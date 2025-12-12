IN = open("./12.txt", "r").read().split("\n\n")

shapes = []
for block in IN[:-1]:
    shape = []
    for y, line in enumerate(block.splitlines()[1:]):
        for x, char in enumerate(line):
            if char == "#":
                shape.append((x, y))
    shapes.append(shape)

valid = 0
for region in IN[-1].splitlines():
    size, counts = region.split(": ")
    w, h = map(int, size.split("x"))
    counts = [int(c) for c in counts.split(" ")]

    # check obvious invalid cases
    pixels_needed = sum([len(shapes[i]) * counts[i] for i in range(len(counts))])
    if pixels_needed > w * h:
        continue

    # check obvious valid cases
    shape_needed = sum(counts)
    if shape_needed <= w // 3 * h // 3:
        valid += 1
        continue

    # unknown case, this should not happen
    raise ValueError(f"Unknown case")

print(valid)
