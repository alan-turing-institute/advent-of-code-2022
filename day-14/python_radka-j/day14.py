
def parse_input(filename):
    """
    Return locations of rocks.
    """
    with open(filename) as f:
        lines = f.read().splitlines()
    rocks = []
    for line in lines:
        vals = line.split(" -> ")
        for v1,v2 in zip(vals[:-1], vals[1:]):
            x1, y1 = [int(v) for v in v1.split(",")]
            x2, y2 = [int(v) for v in v2.split(",")]
            if x1 == x2:   
                x_val = x1
                for y_val in range(min(y1,y2), max(y1,y2)+1):
                    rocks.append((x_val, y_val))
            else:
                y_val = y1
                for x_val in range(min(x1,x2), max(x1,x2)+1):
                    rocks.append((x_val, y_val))
    return rocks


def construct_grid(rocks, floor=False):
    """
    Populate grid with `#` for rocks (and foor if required).
    """
    grid = {}
    max_y = max([v[1] for v in rocks])

    for col in range(0, 1000):
        grid[col] = [0] * (max_y + 3)
    for rock in rocks:
        grid[rock[0]][rock[1]] = "#"
    if floor:
        for col, arr in grid.items():
            grid[col][max_y+2] = "#"
    return grid, max_y


def move_sand(col, row, grid):
    """
    Simulate single sand movement. 
    """
    if grid[col][row+1] not in ["#", "o"]:
        row += 1
    elif grid[col-1][row+1] not in ["#", "o"]:
        col -= 1
        row += 1
    elif grid[col+1][row+1] not in ["#", "o"]:
        col += 1
        row += 1
    return (col, row)


def sand_flow(grid, part, max_y, sand_col=500):
    """
    Simulate sand flow until end condition (part dependant)
    and return units of sands that fell.
    """
    sand_units = 0
    done = False
    while not done:
        col, row = sand_col, 0
        while True:
            new_col, new_row = move_sand(col, row, grid)
            if part=="1":
                if new_row > max_y:
                    return sand_units
            else:
                if (new_col, new_row) == (sand_col, 0):
                    sand_units += 1
                    return sand_units
            # can't move anymore
            if (col, row) == (new_col, new_row):
                grid[col][row] = "o"
                sand_units += 1
                break
            col = new_col
            row = new_row


## PARSE INPUT
sand_col = 500
rocks = parse_input("input14.txt")

## PART 1
grid, max_y = construct_grid(rocks)
sand_units = sand_flow(grid, "1", max_y)
print("part1: ", sand_units)


## PART 2
grid, max_y = construct_grid(rocks, True)
sand_units = sand_flow(grid, "2", max_y)
print("part2: ", sand_units)