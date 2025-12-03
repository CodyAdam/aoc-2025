IN = open("./in.txt", "r").read().splitlines()

res = 0
for line in IN:
    nums = [int(x) for x in line]
    a = max(nums[:-1])
    a_index = nums.index(a)
    b = max(nums[a_index + 1 :])
    res += int(str(a) + str(b))

print(res)
