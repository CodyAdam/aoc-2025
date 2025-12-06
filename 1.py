IN = open("./1.txt", "r").read().splitlines()


current = 50
result = 0
for line in IN:
    letter, rest = line[0], line[1:]

    num = int(rest)

    if letter == "L":
        current -= num
    elif letter == "R":
        current += num
    current = current % 100

    if current == 0:
        result += 1

print(result)
