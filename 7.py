IN = open("./7.txt", "r").read().splitlines()
W = len(IN[0])
H = len(IN)

res = 0
tails = set()
for y, line in enumerate(IN):
    new_tails = set()
    for x, char in enumerate(line):
        if char == "S":
            new_tails.add(x)
        elif char == "^" and x in tails:
            new_tails.add(x - 1)
            new_tails.add(x + 1)
            res += 1
        elif x in tails:
            new_tails.add(x)
    tails = new_tails

print(res)
