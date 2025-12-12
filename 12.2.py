def print_ascii_christmas_tree(height=10):
    width = 2 * height - 1
    # Tree body
    for i in range(height):
        stars = 2 * i + 1
        line = "*" * stars
        print(line.center(width))
    # Tree trunk
    trunk_width = height // 3 if height > 6 else 1
    trunk_width = trunk_width if trunk_width % 2 == 1 else trunk_width + 1
    trunk_height = max(1, height // 4)
    trunk = "|" * trunk_width
    for _ in range(trunk_height):
        print(trunk.center(width))


print_ascii_christmas_tree()
