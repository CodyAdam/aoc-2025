IN = open("./9.txt", "r").read().splitlines()
IN.append(IN[0])


# get all x and y values
x_vals = set()
y_vals = set()
points = []
for line in IN:
    x, y = line.split(",")
    points.append((int(x), int(y)))
    x_vals.add(int(x))
    y_vals.add(int(y))

x_vals = list(x_vals)
x_vals.sort()
y_vals = list(y_vals)
y_vals.sort()

# make virtual grid
to_virtual_x = {}
to_virtual_y = {}
to_true_x = {}
to_true_y = {}
for i, x in enumerate(x_vals):
    to_virtual_x[x] = i
    to_true_x[i] = x
for i, y in enumerate(y_vals):
    to_virtual_y[y] = i
    to_true_y[i] = y

W = len(x_vals)
H = len(y_vals)


def show():
    global W, H
    global edges
    global vertices
    global air_cells

    out = ""
    for virtual_y in range(-1, H + 1):
        for virtual_x in range(-1, W + 1):
            if (virtual_x, virtual_y) in vertices:
                out += "O "
            elif (virtual_x, virtual_y) in edges:
                out += "+ "
            elif (virtual_x, virtual_y) in air_cells:
                out += ". "
            else:
                out += "  "
        out += "\n"
    if len(out) < 10000:
        print(out)
    with open("9.virtual-visualization.txt", "w") as f:
        f.write(out)
    return out


air_cells = set()
vertices = set()
edges = set()
prev = None
for p in points:
    true_x, true_y = p
    x = to_virtual_x[true_x]
    y = to_virtual_y[true_y]
    if prev is not None:
        nx, ny = prev
        neg = 1 if x > nx else -1
        for x_ in range(nx, x + neg, neg):
            edges.add((x_, ny))
        neg = 1 if y > ny else -1
        for y_ in range(ny, y + neg, neg):
            edges.add((x, y_))
    vertices.add((x, y))
    prev = (x, y)
show()


def get_neigh(pos):
    x, y = pos
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def is_outside(pos):
    global W, H
    x, y = pos
    padding = 1
    return x < -padding or x >= W + padding or y < -padding or y >= H + padding


# Fill air cells
queue = [(0, 0)]
while queue:
    pos = queue.pop(0)
    if pos in air_cells or pos in edges or is_outside(pos):
        continue
    air_cells.add(pos)
    for neighbor in get_neigh(pos):
        if (
            neighbor not in air_cells
            and neighbor not in edges
            and not is_outside(neighbor)
        ):
            queue.append(neighbor)

show()


def valid(p1, p2):
    global air_cells
    tl = (min(p1[0], p2[0]), min(p1[1], p2[1]))
    br = (max(p1[0], p2[0]), max(p1[1], p2[1]))
    for x in range(tl[0], br[0] + 1):
        for y in range(tl[1], br[1] + 1):
            if (x, y) in air_cells:
                return False
    return True


def area(p1, p2):
    true_p1 = (to_true_x[p1[0]], to_true_y[p1[1]])
    true_p2 = (to_true_x[p2[0]], to_true_y[p2[1]])
    return (abs(true_p2[0] - true_p1[0]) + 1) * (abs(true_p2[1] - true_p1[1]) + 1)


maxi = 0
for p1 in vertices:
    for p2 in vertices:
        new_area = area(p1, p2)
        if maxi < new_area and valid(p1, p2):
            maxi = new_area
print(maxi)
