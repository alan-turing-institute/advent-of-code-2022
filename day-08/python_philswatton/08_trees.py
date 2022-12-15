from argparse import ArgumentParser

# Usage: python 08_trees.py input_file_path
def get_input_file_path() -> str:
    parser = ArgumentParser(description="AOC Day 0 Function")
    parser.add_argument("input_file_path") # required (positional) arguments
    args = parser.parse_args()
    return args.input_file_path

# Row and column number of tree
def tree_grid_dims(grid: list[str]) -> int:
    nrow = len(grid)
    ncol = len(grid[0])
    return nrow, ncol

# Part 1: Row search function
def row_search(grid: list[str], nrow: int, col_start: int, col_fin: int, increment: int) -> set:
    out = set()
    for i in range(1, nrow-1):
        prev_height = grid[i][col_start-increment]
        for j in range(col_start, col_fin, increment):
            if grid[i][j] > prev_height:
                out.add((i,j))
                prev_height = grid[i][j]
    return out

# Part 1: Column search function
def col_search(grid: list[str], ncol: int, row_start: int, row_fin: int, increment: int) -> set:
    out = set()
    for j in range(1, ncol-1):
        prev_height = grid[row_start-increment][j]
        for i in range(row_start, row_fin, increment):
            if grid[i][j] > prev_height:
                out.add((i,j))
                prev_height = grid[i][j]
    return out

# Part 1: function that can search for visible trees
def tree_search(grid: list[str]) -> set[int]:
    # Dimensions
    nrow, ncol = tree_grid_dims(grid)
    
    # search in all directions, indexing trees that are visible
    left_visible = row_search(grid, nrow, 1, ncol-2, 1)
    right_visible = row_search(grid, nrow, ncol-2, 0, -1)
    top_visible = col_search(grid, ncol, 1, nrow-2, 1)
    bottom_visible = col_search(grid, ncol, nrow-2, 0, -1)
    
    # Union
    visible_union = right_visible | left_visible | top_visible | bottom_visible
    
    # Number visible
    n_visible = len(visible_union) + (nrow-1)*2 + (ncol-1)*2
    
    # Return
    return n_visible

# Part 2: Row distance function
def row_dist(grid: list[str], row: int, col: int, end, increment: int) -> int:
    value = grid[row][col]
    dist = 0
    for i in range(col+increment, end, increment):
        dist += 1
        print("Current Value: " + str(value))
        print("New Value: " + str(grid[row][i]))
        if value <= grid[row][i]:
            break
    return dist

# Part 2: Column distance function
def col_dist(grid: list[str], row: int, col: int, end, increment: int) -> int:
    value = grid[row][col]
    dist = 0
    for i in range(row+increment, end, increment):
        dist += 1
        if value <= grid[i][col]:
            break
    return dist

# Part 2: find maximum view value
def value_search(grid: list[str]) -> int:
    # Dimensions
    nrow, ncol = tree_grid_dims(grid)
    
    # Setup
    current_max = 0
    
    # Loop
    for i in range(1, nrow-1):
        for j in range(1, ncol-1):
            dist_left = row_dist(grid, i, j, -1, -1)
            dist_right = row_dist(grid, i, j, ncol, 1)
            dist_up = col_dist(grid, i, j, -1, -1)
            dist_bottom = col_dist(grid, i, j, nrow, 1)
            dist_product = dist_left * dist_right * dist_up * dist_bottom
            if dist_product > current_max:
                current_max = dist_product
    
    # Return
    return current_max

# Main
def main():
    # Get file path
    file_path = get_input_file_path()
    
    # Read in input file
    with open(file_path) as input_file:
        tree_grid = input_file.read().rstrip().split("\n")
    
    # Part 1: Number of visible trees
    n_visible = tree_search(tree_grid)
    print("Number of trees visible: " + str(n_visible))
    
    # print(row_dist(tree_grid, row=2, col=1, end=4, increment=1))
    max_value = value_search(tree_grid)
    print("Highest possible scenic score: " + str(max_value))
    
    

# Run
if __name__ == "__main__":
    main()