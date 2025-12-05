RANGE, FOOD = open("./in.txt", "r").read().split("\n\n")
RANGE, FOOD = RANGE.splitlines(), FOOD.splitlines()

ranges = set([tuple(map(int, r.split("-"))) for r in RANGE])

# merge ranges


def is_lap(r1, r2):
    a1, b1 = r1
    a2, b2 = r2
    return a1 <= b2 and b1 >= a2


changed = True
while changed:
    new_ranges = set()
    changed = False
    for r in ranges:
        for other in ranges:
            if r != other and is_lap(r, other):
                r = (min(r[0], other[0]), max(r[1], other[1]))
                changed = True
        new_ranges.add(r)
    ranges = new_ranges


# compute count

res = 0
for r in ranges:
    a, b = r
    res += b - a + 1

print(res)
