RANGE, FOOD = open("./5.txt", "r").read().split("\n\n")
RANGE, FOOD = RANGE.splitlines(), FOOD.splitlines()

ranges = [tuple(map(int, r.split("-"))) for r in RANGE]
food = [int(f) for f in FOOD]


def is_fresh(f):
    global ranges
    for r in ranges:
        a, b = r
        if f >= a and f <= b:
            return True
    return False


res = 0
for f in food:
    if is_fresh(f):
        res += 1


print(res)
