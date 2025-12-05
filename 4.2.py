from collections import Counter

IN = open("./in.txt", "r").read().splitlines()
W = len(IN[0])
H = len(IN)

grid = [[x for x in line] for line in IN]


def get_neigh(x, y):
    neigh = [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]
    return [n for n in neigh if 0 <= n[0] < W and 0 <= n[1] < H]


result = 0
to_remove = set()
has_changed = True

while has_changed:
    has_changed = False
    for y in range(H):
        for x in range(W):
            neigh = [grid[n[1]][n[0]] for n in get_neigh(x, y)]
            count = Counter(neigh)
            if count["@"] < 4 and grid[y][x] == "@":
                to_remove.add((x, y))
    for x, y in to_remove:
        has_changed = True
        grid[y][x] = "."
    result += len(to_remove)
    to_remove = set()


print(result)
