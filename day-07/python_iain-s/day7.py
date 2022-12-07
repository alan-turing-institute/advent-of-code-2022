from typing import Dict


def get_next():
    # An infinite generator of +ve ints
    x = 0
    while True:
        yield x
        x += 1


sequence = get_next()


def build_tree(lines, tree: Dict):
    # Given a list of commands, build a tree as a nested dictionary.
    assert lines[0] == "$ ls"

    while len(lines):
        line = lines.pop(0)

        if line.startswith("$ cd"):
            folder = line.split(" ")[2]
            if folder == "..":
                return

            build_tree(lines, tree[folder])

        elif line.startswith("$ ls"):
            pass
        else:
            beginning, end = line.split(" ")
            if beginning == "dir":
                # Directory
                tree[end] = {}
            else:
                # File
                tree[end] = int(beginning)


def walk_tree(tree: Dict):
    # Return the size of a dir and a dict of the sizes of its children.
    # (90, {1: 90, 2: 85})
    size = 0
    sizes = {}
    for key, value in tree.items():
        if isinstance(value, dict):
            sub_size, sub_sizes = walk_tree(value)

            # We replace child names with ints to deal with duplicates
            sizes[next(sequence)] = sub_size

            sizes.update(sub_sizes)
            size += sub_size
        else:
            size += value

    return size, sizes


def one(lines):
    assert lines[0] == "$ cd /"
    tree = {"/": {}}
    build_tree(lines[1:], tree["/"])

    _, sizes = walk_tree(tree)

    answer = sum([value for value in sizes.values() if value <= 100000])

    return answer


def two(lines):
    assert lines[0] == "$ cd /"
    tree = {"/": {}}
    build_tree(lines[1:], tree["/"])

    used, sizes = walk_tree(tree)

    remaining = 70000000 - used

    to_free = 30000000 - remaining

    freeable = sorted(sizes.values())

    for x in freeable:
        if x >= to_free:
            return x

    raise Exception("Could not free enough space for update")


def main():
    with open("../../AoC_2022/src/inputs/07.txt") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))  # 1046278 too low
    print("two:", two(lines))


if __name__ == "__main__":
    main()
