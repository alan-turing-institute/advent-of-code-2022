"""Day 17: Pyroclastic Flow"""


def calc_highest_y(highpoints):
    """The y value of the highest occupied square in the cave."""
    highest_y = 0
    for column in highpoints:
        column_max = calc_highest_in_col(column)
        if column_max > highest_y:
            highest_y = column_max

    return highest_y


def calc_highest_in_col(column):
    """The highest occupied square in the column."""
    for i in range(len(column)):
        j = len(column) - i - 1
        if column[j]:
            return j

    assert False, "Bottomed out"


class Rock:
    def __init__(self, highest_y):
        """Spawn the rock above highest_y."""
        del highest_y
        self.rock_num = 0

        # Rock shapes are lists of (one or two) rectangles
        self.xy_positions = None
        self.heights_widths = None

    def rock_hashable(self):
        """A hashable representation of the rock's state."""
        return self.rock_num, tuple(xy for xy in self.xy_positions), self.heights_widths

    def intersects_down(self, highpoints) -> bool:
        """Will the rock crash if we move it any further down?"""
        assert len(self.heights_widths) == len(self.xy_positions)
        for i, position in enumerate(self.xy_positions):
            x, y = position
            height, width = self.heights_widths[i]

            for j in range(width):
                if len(highpoints[x + j]) > y - 1 and highpoints[x + j][y - 1]:
                    return True

        return False

    def intersects_side(self, direction, highpoints) -> bool:
        """Will the rock crash into the wall or another rock if we move it in direction?"""
        assert len(self.heights_widths) == len(self.xy_positions)
        assert direction in ("<", ">")

        for i, position in enumerate(self.xy_positions):
            x, y = position
            height, width = self.heights_widths[i]

            if direction == "<":
                if x - 1 < 0:
                    return True

                column = highpoints[x - 1]
                for elevation in range(height):
                    if y + elevation < len(column) and column[y + elevation]:
                        return True

            else:
                if x + width > 6:
                    return True

                column = highpoints[x + width]
                for elevation in range(height):
                    try:
                        if y + elevation < len(column) and column[y + elevation]:
                            return True
                    except IndexError as e:
                        print(e)

        return False

    def move_side(self, direction) -> None:
        """Move the rock in direction."""
        delta = -1 if direction == "<" else 1
        for i in range(len(self.xy_positions)):
            self.xy_positions[i] = self.xy_positions[i][0] + delta, self.xy_positions[i][1]

    def move_down(self) -> None:
        """Move the rock down."""
        for i in range(len(self.xy_positions)):
            self.xy_positions[i] = self.xy_positions[i][0], self.xy_positions[i][1] - 1
            assert self.xy_positions[i][1] > 0


class RockOne(Rock):
    """-"""
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.rock_num = 1
        self.heights_widths = ((1, 4),)

        self.xy_positions = [(2, highest_y + 4)]


class RockTwo(Rock):
    """+"""
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.rock_num = 2
        self.heights_widths = ((1, 3), (3, 1))

        self.xy_positions = [
            (2, highest_y + 5),
            (3, highest_y + 4)
        ]


class RockThree(Rock):
    """_|"""
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.rock_num = 3
        self.heights_widths = ((1, 3), (2, 1))

        self.xy_positions = [
            (2, highest_y + 4),
            (4, highest_y + 5)
        ]


class RockFour(Rock):
    """|"""
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.rock_num = 4
        self.heights_widths = ((4, 1),)

        self.xy_positions = [(2, highest_y + 4)]


class RockFive(Rock):
    """::"""
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.rock_num = 5
        self.heights_widths = ((2, 2),)

        self.xy_positions = [(2, highest_y + 4)]


def optimise(highpoints):
    """Find the smallest portion of the cave map that we can keep."""

    # Add an extra, empty layer
    for i in range(len(highpoints)):
        highpoints[i].append(0)

    # Start one level above the top of the left-most column
    x = 0
    y = calc_highest_in_col(highpoints[0]) + 1
    assert highpoints[x][y-1]
    facing = "R"
    minz = y-1

    # Keep going until we hit the right wall or the floor
    # todo I think this could simply be `while True`
    while x < 7 and y > 0:
        minz = min(y-1, minz)

        # Enable visualisation
        visualise = False
        if visualise:
            assert highpoints[x][y] == 0
            highpoints[x][y] = 2

            for i, col in enumerate(list(zip(*highpoints))[::-1]):
                print(col)
            print("")

            highpoints[x][y] = 0

        # Keep the rocks to our right, like you do with a maze
        if facing == "R":
            xy_front = x+1, y
            xy_front_right = x+1, y-1
        elif facing == "U":
            xy_front = x, y+1
            xy_front_right = x+1, y+1
        elif facing == "L":
            xy_front = x-1, y
            xy_front_right = x-1, y+1
        else:
            # facing == "D":
            xy_front = x, y-1
            xy_front_right = x-1, y-1

        if xy_front[0] == 7:
            for i in range(len(highpoints)):
                highpoints[i].pop()
                for j in range(min(minz, y - 1)):
                    highpoints[i].pop(0)
            return min(minz, y - 1)

        if highpoints[xy_front[0]][xy_front[1]]:
            # blocked so turn anti-clockwise
            if facing == "R":
                facing = "U"
            elif facing == "U":
                facing = "L"
            elif facing == "L":
                facing = "D"
            else:
                facing = "R"
        elif highpoints[xy_front_right[0]][xy_front_right[1]]:
            # move forward
            x = xy_front[0]
            y = xy_front[1]

        else:
            # move diagonally right and turn clockwise
            x = xy_front_right[0]
            y = xy_front_right[1]

            if facing == "R":
                facing = "D"
            elif facing == "U":
                facing = "R"
            elif facing == "L":
                facing = "U"
            else:
                facing = "L"

        continue


def repeater(iterable):
    """Yield items and their index from iterable, forever."""
    while True:
        i = 0
        for x in iterable:
            yield i, x
            i += 1


def simulate(line, num_rocks):
    """Simulate num_rocks falling in our cave."""
    directions = repeater(line)
    highpoints = [[1] for _ in range(7)]

    for i, RockClass in enumerate(repeat([RockOne, RockTwo, RockThree, RockFour, RockFive])):

        rock = RockClass(calc_highest_y(highpoints))

        if i == num_rocks:
            break

        while True:

            k, direction = next(directions)
            if not rock.intersects_side(direction, highpoints):
                rock.move_side(direction)

            if rock.intersects_down(highpoints):
                combine(highpoints, rock)
                break
            else:
                rock.move_down()

    return calc_highest_y(highpoints)


def find_cycle(line):
    """Find start and end points of the first cycle."""
    directions = repeater(line)
    highpoints = [[1] for _ in range(7)]
    k = 0

    shapes = dict()
    shapes_counter = 0
    combos = dict()
    offset = 0

    for i, RockClass in enumerate(repeat([RockOne, RockTwo, RockThree, RockFour, RockFive])):

        rock = RockClass(calc_highest_y(highpoints))

        # The highpoints need to be hashable so make them into tuples
        hp = tuple(x for x in (tuple(y) for y in highpoints))
        if hp not in shapes:
            shapes[hp] = shapes_counter
            shapes_counter += 1

        if (shapes[hp], rock.rock_hashable(), k) in combos:
            return combos[(shapes[hp], rock.rock_hashable(), k)], i
        else:
            combos[(shapes[hp], rock.rock_hashable(), k)] = i

        while True:

            k, direction = next(directions)
            if not rock.intersects_side(direction, highpoints):
                rock.move_side(direction)

            if rock.intersects_down(highpoints):
                combine(highpoints, rock)
                offset += optimise(highpoints)
                break
            else:
                rock.move_down()

    raise Exception("Cycle not found")


def simulate_two(line, num_rocks, cycle_start, cycle_period, diff):
    """Simulate cave for part two, skipping ahead where possible."""
    directions = repeater(line)
    highpoints = [[1] for _ in range(7)]
    offset = 0

    i = -1
    for RockClass in repeat([RockOne, RockTwo, RockThree, RockFour, RockFive]):
        i += 1

        if i == cycle_start:
            # Skip ahead rather than simulating
            multi = (1_000_000_000_000 - i) // cycle_period
            i += multi*cycle_period
            offset += multi*diff

        if i == num_rocks:
            break

        rock = RockClass(calc_highest_y(highpoints))

        while True:

            k, direction = next(directions)
            if not rock.intersects_side(direction, highpoints):
                rock.move_side(direction)

            if rock.intersects_down(highpoints):
                combine(highpoints, rock)
                offset += optimise(highpoints)
                break
            else:
                rock.move_down()

    return offset + calc_highest_y(highpoints)


def repeat(iterable):
    """Yield items from iterable forever."""
    while True:
        for x in iterable:
            yield x


def combine(highpoints, rock):
    """Combines a stopped rock with previous highpoints.

    :param highpoints: As for intersects()
    :param rock: A Rock
    """
    assert not highpoints[0] is highpoints[1]

    max_height = 0
    for i, position in enumerate(rock.xy_positions):
        x, y = position
        height, width = rock.heights_widths[i]
        if height + y > max_height:
            max_height = height + y

    # Make highpoints rectangular by padding with 0s
    for column in highpoints:
        if len(column) < max_height:
            column.extend([0] * (max_height - len(column)))

    for i, position in enumerate(rock.xy_positions):
        x, y = position
        height, width = rock.heights_widths[i]

        for j in range(width):
            for k in range(height):
                # We can't assert this because the - and | of the + do overlap
                # assert highpoints[x+j][y+k] == 0
                highpoints[x + j][y + k] = 1


def compare(heights1, heights2):
    for i in range(7):
        if len(heights1[i]) != len(heights2[i]):
            return False
        else:
            for j in range(len(heights2[i])):
                if heights1[i][j] != heights2[i][j]:
                    return False

    return True


def one(lines):
    """Part 1."""
    return simulate(lines[0], 2022)


def two(lines):
    """Part 2."""

    line = lines[0]

    # Find the start and end of the cycle
    start, end = find_cycle(line)
    print("cycle found:", start, end)
    period = end - start

    # Find how much the rock stack grows in that time
    height_at_start = simulate(line, start)
    height_at_end = simulate(line, end)
    diff = height_at_end - height_at_start
    print("heights found:", height_at_start, height_at_end, diff)

    # Use the info above to (somewhat) quickly find the answer
    return simulate_two(line, 1_000_000_000_000, start, period, diff)


def main():
    with open("../inputs/day17.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
