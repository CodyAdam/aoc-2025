from types import CodeType
from typing import Dict, Tuple
from colored import fg, bg, attr


IN = open("./12.txt", "r").read().split("\n\n")
shapes = []
for block in IN[:-1]:
    shape = []
    for y, line in enumerate(block.splitlines()[1:]):
        for x, char in enumerate(line):
            if char == "#":
                shape.append((x, y))
    shapes.append(shape)


def show_grid(grid: Dict[Tuple[int, int], int], w: int, h: int):
    # color palette for up to 6 different shape indices
    colors = [
        bg(1),
        bg(2),
        bg(3),
        bg(4),
        bg(5),
        bg(6),
        bg(7),
    ]
    grey = bg(8)  # ANSI grey
    reset = attr("reset")
    print()
    for y in range(h):
        line = ""
        for x in range(w):
            idx = grid.get((x, y), None)
            if idx is not None:
                color = colors[idx % len(colors)]
                line += f"{color}{idx} {reset}"
            else:
                line += f"{grey}. {reset}"
        print(line)


def get_rotations_and_mirrors(points):
    # Get all (4 rotations + 4 mirrored rotations)
    variants = []
    for mirror in [False, True]:
        for rot in range(4):
            transformed = []
            for x, y in points:
                nx, ny = x, y
                # Mirror horizontally
                if mirror:
                    nx = 2 - nx  # since max x is 2 in original 3x3 block (0-based)
                # Rotate
                for _ in range(rot):
                    nx, ny = ny, 2 - nx  # rotate 90 deg CCW each time
                transformed.append((nx, ny))
            # Normalize top-left to (0,0)
            min_x = min(px for px, _ in transformed)
            min_y = min(py for _, py in transformed)
            normalized = [(px - min_x, py - min_y) for px, py in transformed]
            if normalized not in variants:
                variants.append(normalized)
    return variants


def place_shape(
    grid: Dict[Tuple[int, int], int], w: int, h: int, x: int, y: int, shape_index: int
) -> bool:
    if x + 3 > w or y + 3 > h:
        return False
    origin_shape = shapes[shape_index]
    all_variants = get_rotations_and_mirrors(origin_shape)
    for variant in all_variants:
        # Try to place this variant
        new_points = [(x + point[0], y + point[1]) for point in variant]
        if any(
            point in grid or not (0 <= point[0] < w and 0 <= point[1] < h)
            for point in new_points
        ):
            continue
        # Valid!
        for point in new_points:
            grid[point] = shape_index
        return True
    return False


from colored import fg, attr

GREEN = fg("green")
RED = fg("red")
RESET = attr("reset")

valid = 0
for region in IN[-1].splitlines():
    size, counts = region.split(": ")
    w, h = map(int, size.split("x"))
    counts = [int(c) for c in counts.split(" ")]
    blocks_needed = sum(counts)
    pixels_needed = sum([len(shapes[i]) * counts[i] for i in range(len(counts))])

    if pixels_needed > w * h:
        print(
            f"{RED}INVALID{RESET}, pixels needed > grid size", pixels_needed, ">", w * h
        )
        continue

    grid = {}
    cursor = (0, 0)
    for y in range(h):
        for x in range(w):
            for shape_index in range(len(shapes)):
                if counts[shape_index] == 0:
                    continue
                if place_shape(grid, w, h, x, y, shape_index):
                    counts[shape_index] -= 1
                    # show_grid(grid, w, h)
                    break

    show_grid(grid, w, h)
    if sum(counts) == 0:
        valid += 1
        print(f"{GREEN}VALID{RESET}")
    else:
        print(f"{RED}INVALID{RESET}, missing", sum(counts), "shapes", counts)

print(valid)
