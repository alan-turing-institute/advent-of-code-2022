import math


def read_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    grid = [list(line) for line in lines]
    return grid


def go_up(i, j, grid):
    if i > 0:
        return i-1, j
    return None, None


def go_down(i, j, grid):
    if i < len(grid) - 1:
        return i+1, j
    return None, None


def go_right(i, j, grid):
    if j < len(grid) - 1:
        return i, j+1
    return None, None
    

def go_left(i, j, grid):
    if j > 0:
        return i, j-1
    return None, None


def check_visibility(i, j, tree_height, grid):
    
    # is the tree visible
    visible = False
    # keep track of how many trees can see in each direction
    # return product of distances
    viewing_distances = 1

    # try all directions and see if can get to the edge
    for go_f in (go_up, go_down, go_right, go_left):
        # starting position and tree height
        posi, posj = i, j
        view_d = 0
        while True:
            # reached an edge so tree is visible
            if posi == 0 or posj == 0 or posi == (len(grid) - 1) or posj == (len(grid) - 1):
                if view_d != 0:
                    viewing_distances *= view_d
                visible = True
                break

            # otherwise, make a move in the given direction 
            posi, posj = go_f(posi, posj, grid)
            new_height = int(grid[posi][posj])
            view_d += 1

            # stop if encounter higher tree
            if tree_height <= new_height:
                if view_d != 0:
                    viewing_distances *= view_d
                break            
            
    # never reached the edge i.e., this tree is not visible
    return visible, viewing_distances

grid = read_input("input08.txt")
n_visible = 0
max_scenic = 0
for i, row in enumerate(grid):
    for j, tree_height in enumerate(row):
        visible, viewing_distances = check_visibility(i, j, int(tree_height), grid)
        if viewing_distances > max_scenic:
            max_scenic = viewing_distances
        if visible:
            n_visible += 1

print(n_visible)
print(max_scenic)
