from tqdm import tqdm


class Monkey:
    def __init__(self, items, operation, divisor, if_true, if_false):
        self.items = items  # List of items
        self.operation = operation  # Operation to apply each turn
        self.divisor = divisor  # Test divisor
        self.if_true = if_true  # Monkey to pass to if true
        self.if_false = if_false  # Monkey to pass to if false

        self.troupe = []
        self.items_inspected = 0

    def join_troupe(self, troupe):
        # Need to know other members to pass them items
        self.troupe = troupe

    def take_turn(self):
        while len(self.items):
            self.items_inspected += 1

            item = self.items.pop(0)
            item = self.operation(item)
            item = self.relax(item)
            send_to = self.if_true if (item % self.divisor) == 0 else self.if_false
            self.troupe[send_to].receive(item)

    def receive(self, item):
        self.items.append(item)

    def relax(self, worry):
        raise NotImplementedError

    def __eq__(self, other):
        # For testing only
        return (
            self.troupe == other.troupe
            and self.items == other.items
            # Arbitrary test values
            and self.operation(10) == other.operation(10)
            and self.operation(110) == other.operation(110)
            and self.if_true == other.if_true
            and self.if_false == other.if_false
        )


class MonkeyOne(Monkey):
    def relax(self, worry):
        return worry // 3


class MonkeyTwo(Monkey):
    wrap_at = None

    def relax(self, worry):

        if not self.wrap_at:
            self.wrap_at = 1
            for m in self.troupe:
                self.wrap_at *= m.divisor

        # We have a fixed number of prime divisors that we care about
        # so wrap around when we exceed the product of all of them
        return worry % self.wrap_at


def parse_monkey(text, monkey_class):
    num, items_line, op_line, test_line, true_line, false_line, *_ = text.split("\n")

    # e.g. Starting items: 79, 98
    items = [int(x) for x in items_line[items_line.index(":") + 1 :].split(",")]

    # e.g. Operation: new = old * 19
    index = op_line.index("=")
    op = eval("lambda old: " + op_line[index + 1 :])

    # e.g. Test: divisible by 23
    index = test_line.index("divisible by")
    divisor = int(test_line[index + 12 :])

    # e.g. If true: throw to monkey 2
    index = true_line.index("throw to monkey")
    if_true = int(true_line[index + 15 :])

    # e.g. If true: throw to monkey 2
    index = false_line.index("throw to monkey")
    if_false = int(false_line[index + 15 :])

    zero = monkey_class(items, op, divisor, if_true, if_false)
    return zero


def run_around(text, monkey_class, rounds):
    troupe = []
    for monkey_text in text.split("Monkey ")[1:]:
        troupe.append(parse_monkey(monkey_text, monkey_class))

    for monkey in troupe:
        monkey.join_troupe(troupe)

    for _ in tqdm(range(rounds)):
        for monkey in troupe:
            monkey.take_turn()

    most_inspected = sorted([m.items_inspected for m in troupe])[-2:]
    return most_inspected[0] * most_inspected[1]


def one(text):
    return run_around(text, MonkeyOne, 20)


def two(text):
    return run_around(text, MonkeyTwo, 10_000)


def main():
    with open("../inputs/day11.txt", encoding="utf-8") as f:
        lines = f.read()
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
