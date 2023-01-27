def one(lines):
    return mix(lines, 1, 1)


def mix(lines, times, key):
    length = len(lines)
    indexes = [x for x in range(length)]
    values = [int(x) for x in lines]

    values = [x * key for x in values]

    for _ in range(times):
        for i in range(length):
            index = indexes.index(i)
            value = values[index]

            move_right(indexes, index, value)
            move_right(values, index, value)

    return calc_coords(values)


def calc_coords(numbers):
    zero_index = numbers.index(0)
    result = 0
    for x in (1_000, 2_000, 3_000):
        index = (zero_index + x) % (len(numbers))
        result += numbers[index]

    return result


def move_right(a_list, i, spaces):
    """Move what is currently at index i spaces to the right."""

    # Note that it's length-1 because the space before the 0th element and the
    # space after the last element are one and the same
    new_index = (i + spaces) % (len(a_list) - 1)

    # As per the example, we plonk the value at the end
    # if it's between the first and last items
    new_index = len(a_list) - 1 if new_index == 0 else new_index

    x = a_list.pop(i)
    a_list.insert(new_index, x)


def two(lines):
    return mix(lines, 10, 811589153)


def main():
    with open("../inputs/day20.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
