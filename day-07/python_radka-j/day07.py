from collections import defaultdict

# with open("test.txt") as f:
with open("input07.txt") as f:
    lines = f.read().splitlines()

# keep track of what directories have passed through
directory_path = []
# keep sum of file sizes per directory path
directory_file_sizes = defaultdict(int)

for line in lines:
    vals = line.split()
    # traverse directories and keep track of where at
    if "cd" in vals:
        if ".." in vals:
            # leaving directory - remove from path
            directory_path.pop()
            dir_path_str = "*".join(directory_path)
        else:
            # entering new directory - append name to path
            directory_path.append(vals[-1])
            dir_path_str = "*".join(directory_path)
    # while inside a directory, sum file sizes
    elif "$" not in vals:    
        if "dir" not in vals:
            file_size = int(vals[0])
            directory_file_sizes[dir_path_str] += file_size

# add file sizes in each directory to all to the top level directories in the path 
# to get directory sizes
directory_sizes = defaultdict(int)
for directory, size in directory_file_sizes.items():
    directory_sizes[directory] += size
    dir_path = directory.split("*")
    for i in range(len(dir_path)):
        parent = "*".join(dir_path[:-i])
        directory_sizes[parent] += size

# part 1: sum sizes of directories with size <= max_val
total_sum = 0
max_val = 100000
for size in directory_sizes.values():
    if size <= max_val:
        total_sum += size

print("part 1:", total_sum)

# part 2: find smallest directory that can delete to free up space
smallest_so_far = 70000000 # start at max capacity
free_space = smallest_so_far - directory_sizes["/"]
required_space = 30000000 - free_space
for size in directory_sizes.values():
    if size >= required_space and size < smallest_so_far:
        smallest_so_far = size

print("part 2:", smallest_so_far)