import string


def score_item(char):
    # {"a":1 ... "Z":52}
    return {letter: i + 1 for i, letter in enumerate(string.ascii_letters)}[char]


def score_rucksack(line):
    return score_item(
        set(line[len(line) // 2 :]).intersection(set(line[: len(line) // 2])).pop()
    )


def one(lines):
    return sum([score_rucksack(line) for line in lines])


def score_trio(elfx, elfy, elfz):
    return score_item(set(elfx).intersection(set(elfy).intersection(set(elfz))).pop())


def two(lines):
    return sum(
        [
            score_trio(x, y, z)
            for x, y, z in [lines[i : i + 3] for i in range(0, len(lines), 3)]
        ]
    )


def main():
    with open("../AoC_2022/src/inputs/03.txt") as f:
        lines = [line.rstrip() for line in f]
        print("one:", one(lines))
        print("two:", two(lines))


if __name__ == "__main__":
    main()
