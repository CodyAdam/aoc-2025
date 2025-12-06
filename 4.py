from collections import Counter

IN = open("./4.txt", "r").read().splitlines()
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
for y in range(H):
    for x in range(W):
        neigh = [grid[n[1]][n[0]] for n in get_neigh(x, y)]
        count = Counter(neigh)
        if count["@"] < 4 and grid[y][x] == "@":
            result += 1

print(result)
