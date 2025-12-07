from collections import Counter

IN = open("./7.txt", "r").read().splitlines()
W = len(IN[0])
H = len(IN)

tails = []
for y, line in enumerate(IN):
    new_tails = Counter()
    for x, char in enumerate(line):
        if char == "S":
            new_tails[x] += 1
        elif char == "^" and x in tails:
            new_tails[x - 1] += tails[x]
            new_tails[x + 1] += tails[x]
        elif x in tails:
            new_tails[x] += tails[x]
    tails = new_tails

print(sum(tails.values()))
