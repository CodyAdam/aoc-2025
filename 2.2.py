IN = open("./2.txt", "r").read().splitlines()


def is_invalid_divided_by(x, divider):
    s = str(x)
    if len(s) % divider != 0:
        return False

    parts = set()
    part_len = len(s) // divider

    for i in range(divider):
        parts.add(s[i * part_len : i * part_len + part_len])

    return len(parts) == 1


def invalid(x):
    s = str(x)
    start = len(s)  # this is the only line that changed

    for divider in range(start, 1, -1):
        if is_invalid_divided_by(x, divider):
            # print(x, divider)
            return True
    return False


result = 0
for r in IN[0].split(","):
    l, r = r.split("-")
    l = int(l)
    r = int(r)

    for x in range(l, r + 1):
        if invalid(x):
            result += x

print(result)
