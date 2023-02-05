SNAFU_DICT = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

DEC_DICT = {
    0: "=",
    1: "-",
    2: "0",
    3: "1",
    4: "2",
}


def snafu_to_dec(snafu):
    snafu = snafu.strip()
    dec = 0
    for i, x in enumerate(reversed(snafu)):
        dec += (5**i) * SNAFU_DICT[x]

    return dec


def carry(snafu):
    for i in range(1, len(snafu)):
        if snafu[-i]:
            pass


def num_snafu_digits(dec):
    """How many SNAFU digits to represent dec?"""
    i = 0
    num = 0
    while True:
        num += 2 * (5**i)
        if num >= dec:
            return i + 1
        i += 1


def dec_to_base_five(dec):
    if dec == 0:
        return [0]

    digits = 0
    while True:
        num = 5**digits
        if num > dec:
            break
        digits += 1

    digits -= 1
    base_five = []
    while digits >= 0:
        base_five.append(dec // (5**digits))
        dec = dec % (5**digits)
        digits -= 1

    return base_five


def dec_to_snafu(dec):
    digits = num_snafu_digits(dec)
    num_unique_values = 5 ** (digits)
    start_at = -1 * (num_unique_values - 1) // 2
    base_five_target = dec - start_at
    in_base_five = dec_to_base_five(base_five_target)
    in_snafu = [DEC_DICT[ch] for ch in in_base_five]
    return "".join(in_snafu)


def one(lines):
    decimals = [snafu_to_dec(snafu) for snafu in lines]
    the_sum = sum(decimals)
    return dec_to_snafu(the_sum)


def two(lines):
    pass


def main():
    with open("../inputs/day25.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
