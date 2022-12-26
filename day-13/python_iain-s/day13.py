from typing import List


def split_text(text):
    """Convert text to a list of tuples of lists."""
    return [
        (eval(a), eval(b)) for a, b in [line.split("\n") for line in text.split("\n\n")]
    ]


def right_order(left: List, right: List):
    """True if L>R, False if R>L and None otherwise."""
    if left and right:
        left0_is_list = isinstance(left[0], list)
        right0_is_list = isinstance(right[0], list)

        if left0_is_list and right0_is_list:
            ro = right_order(left[0], right[0])
        elif left0_is_list:
            ro = right_order(left[0], [right[0]])
        elif right0_is_list:
            ro = right_order([left[0]], right[0])
        else:
            if left[0] < right[0]:
                ro = True
            elif left[0] > right[0]:
                ro = False
            else:
                ro = None

        if ro is None:
            return right_order(left[1:], right[1:])
        else:
            return ro

    elif left:
        return False
    elif right:
        return True
    else:
        return None


def one(text):
    result = [right_order(x, y) for (x, y) in split_text(text)]

    # Sum the (one-indexed) indices of the True values
    return sum(i + 1 for i in range(len(result)) if result[i])


def two(text):
    list_of_pairs = split_text(text)
    packets = (
        [x[0] for x in list_of_pairs] + [x[1] for x in list_of_pairs] + [[[2]], [[6]]]
    )

    class MyList(list):
        def __lt__(self, other):
            return right_order(self, other)

    for i in range(len(packets)):
        packets[i] = MyList(packets[i])

    packets.sort()

    # Sum the (one-indexed) indices of the divider packets
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


def main():
    with open("../inputs/day13.txt", encoding="utf-8") as f:
        lines = f.read()
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
