import numpy as np


def read_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


class Monkey:
    def __init__(self, worry_vals, worry_update, worry_change, test_val, true_monkey, false_monkey):
        # worry values of currently held items
        self.worry_vals = worry_vals
        # operation to perform
        self.worry_update = worry_update
        self.worry_change = worry_change
        # value to test division by
        self.test_val = test_val
        # who to throw to when division evaluates to true/false
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        # counter for how many items handled
        self.items_handled = 0
        # lowest common multiple to use in module operation
        self.mod_val = None

    def inspect_items(self):
        for i, val in enumerate(self.worry_vals):
            if self.worry_change == "old":
                num = val
            else:
                num = int(self.worry_change)
            if self.worry_update == "+":
                self.worry_vals[i] += num
            elif self.worry_update == "*":
                self.worry_vals[i] *= num
            # monkey stopped inspecting item
            if self.mod_val is None:
                # part 1: floor divide worry by 3
                self.worry_vals[i] //= 3
            else:
                # part 2: use modulo to manage size
                self.worry_vals[i] %= self.mod_val
            self.items_handled += 1

    def pass_items(self):
        items = {self.true_monkey:[], self.false_monkey:[]}
        for val in self.worry_vals:
            if val % self.test_val == 0:
                items[self.true_monkey].append(val)
            else:
                items[self.false_monkey].append(val)
        self.worry_vals = []
        return items

    def receive_items(self, items):
        self.worry_vals.extend(items)


def main(filename, n_rounds, part1):

    # READ INPUT
    lines = read_input(filename)

    # CREATE MONKEYS
    monkeys = []
    test_vals = []
    for line in lines:
        if "Starting items" in line:
            vals = [int(val) for val in line.split(": ")[-1].split(", ")]
        elif "Operation" in line:
            _, op, amount = line.split("=")[-1].split()
        elif "Test" in line:
            divisor = int(line.split()[-1])
            test_vals.append(divisor)
        elif "true" in line:
            true_monkey = int(line.split(" ")[-1])
        elif "false" in line:
            false_monkey = int(line.split(" ")[-1])
            monkeys.append(Monkey(vals, op, amount, divisor, true_monkey, false_monkey))
    
    # PART 2: give monkeys lowest common multiple value to use
    if not part1:
        mod_val = np.lcm.reduce(test_vals)
        for m in monkeys:
            m.mod_val = mod_val

    # PLAY N ROUNDS
    for i in range(n_rounds):
        for m in monkeys:
            m.inspect_items()
            items = m.pass_items()
            for monkey, vals in items.items():
                monkeys[monkey].receive_items(vals)

    # GET NUMBER OF ITEMS HANDLED BY TOP 2 MONKEYS
    n_handled = []
    for m in monkeys:
        n_handled.append(m.items_handled)
    n_handled.sort()
    print(n_handled[-2] * n_handled[-1])


if __name__ == "__main__":
    main("input11.txt", 20, True)
    main("input11.txt", 10000, False)