from collections import defaultdict
import math

IN = open("./8.txt", "r").read().splitlines()


def calc_dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


graph = {}
for line in IN:
    nums = tuple([int(x) for x in line.split(",")])
    graph[nums] = set()


edges_dist = {}
keys = list(graph.keys())
for i, a in enumerate(keys):
    for b in keys[i + 1 :]:
        edges_dist[(a, b)] = calc_dist(a, b)

sorted_dist = sorted(edges_dist.items(), key=lambda x: x[1])


def is_connected(current, target, seen=None):
    if seen is None:
        seen = set()
    if current == target:
        return True
    if current in seen:
        return False
    seen.add(current)
    result = False
    for neighbor in graph[current]:
        result = result or is_connected(neighbor, target, seen)
    return result


ITER = 1000
for i in range(ITER):
    (a, b), _ = sorted_dist[i]
    graph[a].add(b)
    graph[b].add(a)


def dfs(node, seen):
    if node in seen:
        return 0
    seen.add(node)
    length = 0
    for neighbor in graph[node]:
        length += dfs(neighbor, seen)
    return length + 1


seen = set()
lengths = []
# count the number of nodes in each cycle
for node in graph:
    lengths.append(dfs(node, seen))

lengths.sort()
print(lengths[-5:])
print(math.prod(lengths[-3:]))
