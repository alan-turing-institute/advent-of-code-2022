from collections import defaultdict


def read_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def create_path_str(directory_path_list, marker="*"):
    return f"{marker}".join(directory_path_list)


def parse_data(lines):
    """
    Create dictionary of {directory path: size}.
    """

    # keep track of what directories have passed through
    directory_path = []
    # keep sum of file sizes per directory path
    directory_sizes = defaultdict(int)

    for line in lines:
        vals = line.split()
        # traverse directories and keep track of where at
        if "cd" in vals:
            if ".." in vals:
                directory_path.pop()
            else:
                directory_path.append(vals[-1])
        # while inside a directory, add each file size to dir and all parent dirs
        elif "$" not in vals and "dir" not in vals:
            file_size = int(vals[0])
            dir_path_str = create_path_str(directory_path)
            directory_sizes[dir_path_str] += file_size
            for i in range(len(directory_path)):
                parent_path_str = create_path_str(directory_path[:-i])
                directory_sizes[parent_path_str] += file_size

    return directory_sizes


# ================================================================
# parse input
# ================================================================

# lines = read_input("test.txt")
lines = read_input("input07.txt")
directory_sizes = parse_data(lines)

# ================================================================
# part 1: sum sizes of directories within max_allowed_size
# ================================================================

total_sum = 0
max_allowed_size = 100000
for size in directory_sizes.values():
    if size <= max_allowed_size:
        total_sum += size

print("part 1:", total_sum)

# ================================================================
# part 2: find smallest dir to delete to free up required space
# ================================================================

total_space = 70000000 
required_capacity = 30000000
taken_up = directory_sizes["/"]
free_space = total_space - taken_up
to_free_up = required_capacity - free_space

smallest_so_far = total_space
for size in directory_sizes.values():
    if size >= to_free_up and size < smallest_so_far:
        smallest_so_far = size

print("part 2:", smallest_so_far)