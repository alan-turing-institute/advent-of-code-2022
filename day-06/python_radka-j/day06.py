with open("input06.txt") as f:
    text = f.readlines()[0]


def evaluate(my_str, n_required):
    """
    Return index at which message starts.

    my_str: str
        message to parse
    n_required: int
        number of unique characters required to indicate start of message
    """

    for i, char in enumerate(my_str):
        # do nothing until have n_required characters
        if i <= n_required - 1:
            continue
        else:
            # check number of unique characters in substring
            substring = my_str[i-n_required:i]
            n_unique = len(set(substring))
            if n_unique==n_required:
                return i
    # nothing found
    return -1

assert evaluate("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
assert evaluate("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
assert evaluate("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10

part1_ans = evaluate(text, 4)
print("part1:", part1_ans)

assert evaluate("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
assert evaluate("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
assert evaluate("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23

part2_ans = evaluate(text, 14)
print("part2:", part2_ans)