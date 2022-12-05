import copy
from collections import deque


def parse_stacks(lines):
    """
    Construct dictionary of [stack: crate array].
    """

    n_stacks = int(len(lines[0]) / 4)
    stacks = {i+1:deque() for i in range(n_stacks)}

    for line in lines:
        # the end line for stacks in both test and input
        if " 1   2   3" in line:
            break

        # crate contents correspond to indices 1, 5, 9 etc
        chars = list(line)
        for n in range(n_stacks):
            index = 1 + n * 4
            val = chars[index]
            if val != " ":
                stacks[n+1].append(val)

    return stacks


def parse_instructions(lines):
    """
    Contruct list of (count, move_from, move_to) instructions.
    """

    instructions = []
    for line in lines:
        if "move" in line:
            # vals are (count, move_from, move_to)
            instructions.append([int(val) for val in line.split()[1::2]])
    return instructions


def part1(stacks, instructions):
    """
    For each instruction, move one crate at a time.
    """

    for (count, move_from, move_to) in instructions:
        for _ in range(count):
            val = stacks[move_from].popleft()
            stacks[move_to].appendleft(val)
    return stacks


def part2(stacks, instructions):
    """    
    For each instruction, move all crates at once.
    """

    for (count, move_from, move_to) in instructions:
        # NOTE: deque().extendleft reverses order of iterable
        # therefore we store vals in reverse order
        vals = deque()
        for _ in range(count):
            vals.appendleft(stacks[move_from].popleft())
        stacks[move_to].extendleft(vals)
    return stacks


def get_ans(stacks):
    """
    Create string of crate labels that are on top of each stack.
    """

    ans = ""
    for vals in stacks.values():
        ans += vals[0]
    return ans


def main(filename="input05.txt"):

    # read input
    with open(filename) as f:
        lines = f.readlines()
    stacks = parse_stacks(lines)
    instructions = parse_instructions(lines)

    # apply instructions
    CrateMover9000 = part1(copy.deepcopy(stacks), instructions)
    CrateMover9001 = part2(copy.deepcopy(stacks), instructions)

    # get final answer
    print("part1", get_ans(CrateMover9000))
    print("part2", get_ans(CrateMover9001))


if __name__ == "__main__":

    # main("test_input.txt")
    main()