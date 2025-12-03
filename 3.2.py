IN = open("./in.txt", "r").read().splitlines()

res = 0
repeat = 12

for line in IN:
    nums = [int(x) for x in line]
    min_index = 0
    current = []
    for i in range(repeat):
        max_index = -repeat + i + 1
        if max_index == 0:
            max_index = len(nums)
        window = nums[min_index:max_index]
        max_value = max(window)
        min_index = window.index(max_value) + min_index + 1
        current.append(max_value)

    res += int("".join([str(x) for x in current]))

print(res)
