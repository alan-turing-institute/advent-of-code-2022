OURS = ["X", "Y", "Z"]
THEIRS = ["A", "B", "C"]
WIN = 6
DRAW = 3


def ready_steady_go(their, our):
    """Calculate the score, given our move and theirs."""
    our_index = OURS.index(our)
    their_index = THEIRS.index(their)

    if our_index == their_index:
        return our_index + 1 + DRAW
    elif (our_index - their_index) % 3 == 1:
        return our_index + 1 + WIN
    else:
        return our_index + 1


def ready_steady_something(their, result):
    """X, Y, Z = lose, draw, win."""
    their_index = THEIRS.index(their)

    if result == "X":
        return ready_steady_go(their, OURS[their_index-1])

    elif result == "Y":
        return ready_steady_go(their, OURS[their_index])

    else:
        return ready_steady_go(their, OURS[their_index-2])


def one(bouts):
    """Takes a list of bouts and returns the expected score."""
    return sum(map(lambda x: ready_steady_go(*x.split()), bouts))


def two(bouts):
    """Takes a list of bouts and returns the expected score, part II."""
    return sum(map(lambda x: ready_steady_something(*x.split()), bouts))


def main():
    with open("../AoC_2022/src/inputs/02.txt") as f:
        bouts = [line.rstrip() for line in f]
        print("one:", one(bouts))
        print("two:", two(bouts))


if __name__ == "__main__":
    main()
