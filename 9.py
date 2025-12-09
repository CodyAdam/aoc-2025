IN = open("./9.txt", "r").read().splitlines()

tiles = set()
for line in IN:
    x, y = line.split(",")
    tiles.add((int(x), int(y)))


def area(p1, p2):
    return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)


maxi = 0
for p1 in tiles:
    for p2 in tiles:
        maxi = max(maxi, area(p1, p2))

print(maxi)
