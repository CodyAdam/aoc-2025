from collections import defaultdict


IN = open("./11.txt", "r").read().splitlines()

graph = defaultdict(list)
for line in IN:
    a, b = line.split(": ")
    b = b.split(" ")
    for item in b:
        graph[a].append(item)


cache = {}


def find_ways(start, target):
    key = (start, target)
    if key in cache:
        return cache[key]
    if start == target:
        return 1
    result = 0
    for neighbor in graph[start]:
        result += find_ways(neighbor, target)
    cache[key] = result
    return result


start1 = find_ways("svr", "fft")
middle1 = find_ways("fft", "dac")
end1 = find_ways("dac", "out")

start2 = find_ways("svr", "dac")
middle2 = find_ways("dac", "fft")
end2 = find_ways("fft", "out")


print(start1 * middle1 * end1 + start2 * middle2 * end2)
