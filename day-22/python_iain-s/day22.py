from itertools import chain

# Some hard coded differences depending on whether we're
# using the example or real input
testing = False


def split_on(a_string, char):
    b = a_string.split(char)
    c = list(chain(*[[b[0]]] + [[char, x] for x in b[1:]]))
    return c


def parse_instructions(instruction_string):
    a = split_on(instruction_string, "R")
    b = list(chain(*[split_on(x, "L") for x in a]))
    for i in range(len(b)):
        try:
            b[i] = int(b[i])
        except ValueError:
            pass

    return b


ROTATIONS = {
    "RR": "D",
    "RL": "U",
    "DR": "L",
    "DL": "R",
    "LR": "U",
    "LL": "D",
    "UR": "R",
    "UL": "L",
}

ARROWS = {
    "R": ">",
    "D": "v",
    "U": "^",
    "L": "<",
}

FACING_VALUES = {
    "R": 0,
    "D": 1,
    "L": 2,
    "U": 3,
}

NOT_EMPTY = (".", "#", ">", "<", "^", "v")

DIM = 50


def one(content):
    a, b = content.split("\n\n")
    board_map = [list(line) for line in a.split("\n")]
    instructions = parse_instructions(b)

    last_position, last_facing = simulate(board_map, instructions)

    [print("".join(x)) for x in board_map]

    rownum = last_position[0] + 1
    colnum = last_position[1] + 1
    facing_val = FACING_VALUES[last_facing]
    return (1000 * rownum) + (4 * colnum) + facing_val


def simulate(board_map, instructions):
    pos = 0, board_map[0].index(".")  # y, x from top left
    direction = "R"
    assert board_map[pos[0]][pos[1]] != "#"
    board_map[pos[0]][pos[1]] = ARROWS[direction]

    for i_inst, instruction in enumerate(instructions):
        if isinstance(instruction, str):
            direction = ROTATIONS[direction + instruction]
            assert board_map[pos[0]][pos[1]] != "#"
            board_map[pos[0]][pos[1]] = ARROWS[direction]
        else:
            for _ in range(instruction):
                if direction in ("R", "L"):
                    row = board_map[pos[0]]

                    if direction == "R":
                        if pos[1] + 1 >= len(row):
                            # wrap around
                            x = min([row.index(z) for z in NOT_EMPTY if z in row])
                        else:
                            x = pos[1] + 1

                        next_pos = pos[0], x
                        tile_to_right = row[x]
                        if tile_to_right == "#":
                            # stop
                            break
                        else:
                            # move right
                            pos = next_pos
                            assert board_map[pos[0]][pos[1]] != "#"
                            board_map[pos[0]][pos[1]] = ARROWS[direction]
                    else:
                        # Left
                        if pos[1] - 1 < 0 or row[pos[1] - 1] == " ":
                            # wrap around
                            x = len(row) - 1
                        else:
                            x = pos[1] - 1

                        next_pos = pos[0], x
                        tile_to_left = row[x]
                        if tile_to_left == "#":
                            # stop
                            break
                        else:
                            # move left
                            pos = next_pos
                            assert board_map[pos[0]][pos[1]] != "#"
                            board_map[pos[0]][pos[1]] = ARROWS[direction]
                else:
                    # Up or Down
                    above = pos[0]
                    while True:
                        if above - 1 < 0 or board_map[above - 1][pos[1]] == " ":
                            break
                        else:
                            above -= 1

                    below = pos[0]
                    while True:
                        if (
                                below + 1 >= len(board_map)
                                or pos[1] >= len(board_map[below + 1])
                                or board_map[below + 1][pos[1]] == " "
                        ):
                            break
                        else:
                            below += 1

                    column = [c[pos[1]] for c in board_map[above: below + 1]]

                    if column[0] == " " or column[-1] == " ":
                        print("error!")

                    r_pos = pos[0] - above, pos[1]

                    if direction == "D":
                        if r_pos[0] + 1 >= len(column):
                            # wrap around
                            y = 0
                        else:
                            y = r_pos[0] + 1

                        next_r_pos = y, r_pos[1]
                        # try:
                        tile_below = column[y]
                        # except IndexError:
                        #     pass
                        if tile_below == "#":
                            # stop
                            break
                        else:
                            # move down
                            r_pos = next_r_pos
                            assert board_map[pos[0]][pos[1]] != "#"
                            board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                    else:
                        # Up
                        if r_pos[0] - 1 < 0:
                            # wrap around

                            # here
                            y = len(column) - 1
                        else:
                            y = r_pos[0] - 1

                        next_r_pos = y, r_pos[1]
                        tile_above = column[y]
                        if tile_above == "#":
                            # stop
                            break
                        else:
                            # move up
                            r_pos = next_r_pos
                            assert board_map[pos[0]][pos[1]] != "#"
                            board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                    pos = r_pos[0] + above, r_pos[1]

    return pos, direction


def myrange(pointa, pointb):
    # inclusive ranges in either direction
    if pointa[0] == pointb[0]:
        # horizontal
        x = pointa[1]
        y = pointb[1]
        a = pointa[0]

        if not testing:
            assert abs(y - x) == 49, f"{y=} {x=}"

        return [(a, j) for j in (range(x, y + 1) if y > x else range(x, y - 1, -1))]
    else:
        # vertical
        x = pointa[0]
        y = pointb[0]
        a = pointa[1]

        if not testing:
            assert abs(y - x) == 49, f"{y=} {x=}"

        return [(j, a) for j in (range(x, y + 1) if y > x else range(x, y - 1, -1))]


def make_seam(first, second):
    inverse = {
        "U": "D",
        "D": "U",
        "L": "R",
        "R": "L",
    }
    j = myrange(first[0], first[1])
    k = myrange(second[0], second[1])
    assert len(j) == len(k), f"{j}, {k}"

    result = {}
    for i in range(len(j)):
        result[(j[i], first[2])] = (k[i], second[2])

    for i in range(len(j)):
        result[(k[i], inverse[second[2]])] = (j[i], inverse[first[2]])

    return result


def new_direction_pos(direction, pos):
    # change direction and y,x position

    # hard coding the wrapping of the shapes is
    # not pretty but perhaps quicker than coding a more elegant solution
    # and, AFAIK, the input shape is the same for everyone
    # (only the . and # locations change)
    if testing:
        seams = {
            **make_seam(((0, 8), (0, 11), "U"), ((4, 3), (4, 0), "D")),
            **make_seam(((0, 8), (3, 8), "L"), ((4, 4), (4, 7), "D")),
            **make_seam(((4, 0), (7, 0), "L"), ((11, 15), (11, 12), "U")),
            **make_seam(((8, 15), (8, 12), "U"), ((4, 11), (7, 11), "L")),
            **make_seam(((7, 4), (7, 7), "D"), ((8, 8), (11, 8), "R")),
            **make_seam(((7, 0), (7, 3), "D"), ((11, 11), (11, 8), "U")),
            **make_seam(((0, 11), (3, 11), "R"), ((11, 15), (8, 15), "L")),
        }
    else:
        seams = {
            # make_seams makes this a little less tedious than my previous strategy
            **make_seam(((49, 100), (49, 149), "D"), ((50, 99), (99, 99), "L")),
            **make_seam(((49, 149), (0, 149), "R"), ((100, 99), (149, 99), "L")),
            **make_seam(((0, 100), (0, 149), "U"), ((199, 0), (199, 49), "U")),
            **make_seam(((0, 50), (0, 99), "U"), ((150, 0), (199, 0), "R")),
            **make_seam(((0, 50), (49, 50), "L"), ((149, 0), (100, 0), "R")),
            **make_seam(((50, 50), (99, 50), "L"), ((100, 0), (100, 49), "D")),
            **make_seam(((149, 50), (149, 99), "D"), ((150, 49), (199, 49), "L")),
        }

    new_pos, new_direction = seams[(pos, direction)]
    return new_direction, new_pos


def simulate_two(board_map, instructions):
    pos = 0, board_map[0].index(".")  # y, x from top left
    direction = "R"
    assert board_map[pos[0]][pos[1]] != "#"
    board_map[pos[0]][pos[1]] = ARROWS[direction]

    for i_inst, instruction in enumerate(instructions):
        if isinstance(instruction, str):
            direction = ROTATIONS[direction + instruction]
            assert board_map[pos[0]][pos[1]] != "#"
            board_map[pos[0]][pos[1]] = ARROWS[direction]
        else:
            for _ in range(instruction):
                if direction in ("R", "L"):
                    row = board_map[pos[0]]

                    if direction == "R":
                        if pos[1] + 1 >= len(row):
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            x = pos[1] + 1
                            next_pos = pos[0], x
                            tile_to_right = row[x]

                            if tile_to_right == "#":
                                # stop
                                break
                            else:
                                # move right
                                pos = next_pos
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                    else:
                        # Left
                        if pos[1] - 1 < 0 or row[pos[1] - 1] == " ":
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            x = pos[1] - 1

                            next_pos = pos[0], x
                            tile_to_left = row[x]
                            if tile_to_left == "#":
                                # stop
                                break
                            else:
                                # move left
                                pos = next_pos
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                else:
                    # Up or Down
                    above = pos[0]
                    while True:
                        if above - 1 < 0 or len(board_map[above - 1]) < pos[1] or board_map[above - 1][pos[1]] == " ":
                            break
                        else:
                            above -= 1

                    below = pos[0]
                    while True:
                        if (
                                below + 1 >= len(board_map)
                                or pos[1] >= len(board_map[below + 1])
                                or board_map[below + 1][pos[1]] == " "
                        ):
                            break
                        else:
                            below += 1

                    column = [c[pos[1]] for c in board_map[above: below + 1]]

                    if column[0] == " " or column[-1] == " ":
                        print("error!")

                    r_pos = pos[0] - above, pos[1]

                    if direction == "D":
                        if r_pos[0] + 1 >= len(column):
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            y = r_pos[0] + 1

                            next_r_pos = y, r_pos[1]
                            tile_below = column[y]
                            if tile_below == "#":
                                # stop
                                break
                            else:
                                # move down
                                r_pos = next_r_pos
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                            pos = r_pos[0] + above, r_pos[1]

                    else:
                        # Up
                        if r_pos[0] - 1 < 0:
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            y = r_pos[0] - 1

                            next_r_pos = y, r_pos[1]
                            tile_above = column[y]
                            if tile_above == "#":
                                # stop
                                break
                            else:
                                # move up
                                r_pos = next_r_pos
                                assert board_map[pos[0]][pos[1]] != "#"
                                board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                            pos = r_pos[0] + above, r_pos[1]

    return pos, direction


def two(content):
    a, b = content.split("\n\n")
    board_map = [list(line) for line in a.split("\n")]
    instructions = parse_instructions(b)

    last_position, last_facing = simulate_two(board_map, instructions)

    [print("".join(x)) for x in board_map]

    rownum = last_position[0] + 1
    colnum = last_position[1] + 1
    facing_val = FACING_VALUES[last_facing]
    return (1000 * rownum) + (4 * colnum) + facing_val


def main():
    with open("../inputs/day22.txt", encoding="utf-8") as f:
        content = f.read()
    print("one:", one(content))
    print("two:", two(content))


if __name__ == "__main__":
    main()
