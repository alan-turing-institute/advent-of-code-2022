
def check_for_start_one(chars):
    a, b, c, d = chars
    for x in [b, c, d]:
        if a == x:
            return False

    for y in [c, d]:
        if b == y:
            return False

    if c == d:
        return False

    return True


def check_for_start_two(chars):
    for check_pos in range(0, len(chars)):
        check_char = chars[check_pos]
        for x in chars[check_pos+1:len(chars)]:
            if check_char == x:
                return False
    return True


if __name__ == '__main__':
    f = open('input.txt', 'r')
    buf = f.readlines()[0].strip()
    buf = list(buf)

    start_found = False
    num_chars_in_start = 14
    pos = num_chars_in_start
    while not start_found:
        chars = buf[pos-num_chars_in_start:pos]
        if check_for_start_two(chars):
            start_found = True
        else:
            pos += 1

    print(pos)
