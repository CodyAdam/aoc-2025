from z3 import *

IN = open("./10.txt", "r").read().splitlines()

result = 0
for idx, line in enumerate(IN):
    items = line.split(" ")
    counter, buttons = items[-1], items[1:-1]
    counter = [int(x) for x in counter[1:-1].split(",")]
    buttons_list = []
    for button in buttons:
        indexes = [int(x) for x in button[1:-1].split(",")]
        buttons_list.append(indexes)

    vars_button_press = [Int(f"x_{i}") for i in range(len(buttons_list))]
    vars_jolts = [Int(f"y_{i}") for i in range(len(counter))]

    s = Optimize()

    # output constraints
    for jolt_i, target in enumerate(counter):
        jolt = vars_jolts[jolt_i]
        s.add(jolt == target)

        total_sum = 0
        for button_i, button in enumerate(buttons_list):
            s.add(vars_button_press[button_i] >= 0)
            if jolt_i in button:
                total_sum += vars_button_press[button_i]
        s.add(jolt == total_sum)

    s.minimize(Sum(vars_button_press))
    s.check()
    model = s.model()
    presses = model.eval(Sum(vars_button_press))
    # print(model)
    # print(idx, presses)
    result += presses.as_long()

print(result)
