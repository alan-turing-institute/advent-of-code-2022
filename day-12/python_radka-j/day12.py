import string
from collections import deque


def read_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


# construct grid of elevations
vals = {char:i for i,char in enumerate(string.ascii_lowercase)}
grid = []
start_pos = None #marker S, elevation a
best_pos = None #marker E, elevation z
lowest_pos = [] #all positions with elevation a

lines = read_input("input12.txt")
for i, line in enumerate(lines):
    if "S" in line:
        j = line.index("S")
        start_pos = (i,j)
        line = line.replace("S", "a")
    if "E" in line:
        j = line.index("E")
        best_pos = (i,j)
        line = line.replace("E", "z")
    if "a" in line:
        j = line.index("a")
        lowest_pos.append((i,j))
    row = [vals[char] for char in line]
    grid.append(row)


def get_children(pos, grid=grid):
    """
    Return positions of valid moves from `pos` 
    """
    children = []
    i,j = pos
    # up
    if i > 0:
        if grid[i-1][j] - grid[i][j] <= 1:
            children.append((i-1, j))
    # down
    if i < len(grid) - 1:
        if grid[i+1][j] - grid[i][j] <= 1:
            children.append((i+1, j))
    # right
    if j < len(grid[0]) - 1:
        if grid[i][j+1] - grid[i][j] <= 1:
            children.append((i, j+1))
    # left
    if j > 0:
        if grid[i][j-1] - grid[i][j] <= 1:
            children.append((i, j-1))

    return children


def search(start_pos, end_pos):
    """
    Breadth first search from start to end pos
    """

    # (current position, number of moves travelled so far)
    queue = deque()
    queue.append((start_pos, 0))
    # keep track of where have been
    visited_so_far = []

    while len(queue) != 0:
        curr_pos, dist_so_far = queue.popleft()
        visited_so_far.append(curr_pos)
        if curr_pos == end_pos:
            return dist_so_far
        else:
            children = get_children(curr_pos)
            for child in children:
                if child not in visited_so_far and child not in [item[0] for item in queue]:
                    queue.append((child, dist_so_far + 1))


# part 1 ===================================================================
steps = search(start_pos, best_pos)
print("part 1:", steps)


# part 2 =================================================================== 
all_steps = [steps]
for pos in lowest_pos:
    if pos != start_pos:
        steps = search(pos, best_pos)
        all_steps.append(steps)
print("part 2:", min(all_steps))
    