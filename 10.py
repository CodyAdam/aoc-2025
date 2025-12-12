IN = open("./10.txt", "r").read().splitlines()


def bfs(code, buttons, n):
    cache = set()
    # bfs
    queue = [(code, 0)]
    while queue:
        current_code, i = queue.pop(0)
        if current_code == 0:
            return i
        for button in buttons:
            new_code = current_code ^ button
            if new_code in cache:
                continue
            cache.add(new_code)
            queue.append((new_code, i + 1))
    return -1


result = 0
for line in IN:
    items = line.split(" ")
    code, buttons = items[0], items[1:-1]

    bin_code = ""
    for char in code[1:-1]:
        if char == ".":
            bin_code += "0"
        if char == "#":
            bin_code += "1"
    n = len(bin_code)
    bin_code = int(bin_code, 2)

    bin_buttons = []
    for button in buttons:
        indexes = [int(x) for x in button[1:-1].split(",")]
        bin_button = ["0"] * n
        for index in indexes:
            bin_button[index] = "1"
        bin_button = int("".join(bin_button), 2)
        bin_buttons.append(bin_button)

    result += bfs(bin_code, bin_buttons, n)
print(result)
