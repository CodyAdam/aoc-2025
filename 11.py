from collections import defaultdict


IN = open("./11.txt", "r").read().splitlines()

graph = defaultdict(list)
for line in IN:
    a, b = line.split(": ")
    b = b.split(" ")
    for item in b:
        graph[a].append(item)

q = [("you", set())]
result = 0
while len(q):
    current, seen = q.pop(0)
    seen = seen.copy()
    seen.add(current)
    if current == "out":
        result += 1
        continue
    for neighbor in graph[current]:
        if neighbor not in seen:
            q.append((neighbor, seen))

print(result)
