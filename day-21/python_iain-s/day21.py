from functools import cache


def get_func(monkeys):
    @cache
    def monkey_shouts(monkey_name):
        try:
            return int(monkeys[monkey_name])
        except ValueError:
            monkey_one, operator, monkey_two = monkeys[monkey_name].split(" ")
            value_one = monkey_shouts(monkey_one)
            value_two = monkey_shouts(monkey_two)
            return eval(
                "{a} {x} {b}".format(a=str(value_one), x=operator, b=str(value_two))
            )

    return monkey_shouts


def one(lines):
    monkeys = {k: v for k, v in [line.split(": ") for line in lines]}

    # Traverse the tree, calculating only as necessary
    return get_func(monkeys)("root")


def two(lines):

    monkeys = {k: v for k, v in [line.split(": ") for line in lines]}

    # humn only seems to influence one branch of the tree
    left, _, right = monkeys["root"].split(" ")
    monkeys["humn"] = None

    branch_has_humn = right

    f = get_func(monkeys)
    try:
        value = f(left)
    except TypeError:
        branch_has_humn = left
        value = f(right)

    def make_branch_equal(x, branch):
        """branch is the name of a monkey, x is a target value"""
        if monkeys[branch] is None:
            return x

        l, op, r = monkeys[branch].split(" ")

        humn_branch = r
        try:
            val = f(l)
        except TypeError:
            humn_branch = l
            val = f(r)

        # Solve for unknown branch value
        if op == "+":
            return make_branch_equal(x - val, humn_branch)
        elif op == "*":
            return make_branch_equal(x / val, humn_branch)
        elif op == "-":
            if humn_branch == l:
                return make_branch_equal(x + val, humn_branch)
            else:
                return make_branch_equal(-1 * (x - val), humn_branch)
        elif op == "/":
            if humn_branch == l:
                return make_branch_equal(x * val, humn_branch)
            else:
                return make_branch_equal(val / x, humn_branch)
        else:
            assert False

    return make_branch_equal(value, branch_has_humn)


def main():
    with open("../inputs/day21.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
