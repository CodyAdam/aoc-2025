IN = open("./in.txt", "r").read().splitlines()

current = 50
result = 0
for line in IN:
    letter, rest = line[0], line[1:]

    num = int(rest)

    for i in range(num):
        if letter == "L":
            current -= 1
        elif letter == "R":
            current += 1
        current = current % 100

        if current == 0:
            result += 1

print(result)
