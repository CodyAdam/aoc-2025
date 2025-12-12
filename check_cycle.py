from collections import defaultdict

IN = open("./11.txt", "r").read().splitlines()

graph = defaultdict(list)
for line in IN:
    parts = line.split(": ")
    if len(parts) != 2:
        continue
    a, b_str = parts
    b = b_str.split(" ")
    for item in b:
        graph[a].append(item)

visited = set()
rec_stack = set()


def has_cycle(u):
    visited.add(u)
    rec_stack.add(u)
    for v in graph[u]:
        if v not in visited:
            if has_cycle(v):
                return True
        elif v in rec_stack:
            return True
    rec_stack.remove(u)
    return False


cycle_found = False
for node in list(graph.keys()):
    if node not in visited:
        if has_cycle(node):
            cycle_found = True
            break

print(f"Cycle found: {cycle_found}")
