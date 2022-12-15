from argparse import ArgumentParser
from typing import Union

# Usage: python 09_rope.py input_file_path
def get_input_file_path() -> str:
    parser = ArgumentParser(description="AOC Day 0 Function")
    parser.add_argument("input_file_path") # required (positional) arguments
    args = parser.parse_args()
    return args.input_file_path

# Sign function
def sign(num: Union[int, float]) -> int:
    if num > 0:
        return 1
    if num < 0:
        return -1
    if num == 0:
        return 0

# Function to compute a single move
def update_positions(direction: str, num_moves: int, positions: list[list[int]]):
    
    # Sign of head movement direction
    if direction == "R" or direction == "U":
        move_sign = 1
    else:
        move_sign = -1
    
    # Index of head movement direction
    if direction == "L" or direction == "R":
        index = 0
    else:
        index = 1
    
    # Track unique positions of tail
    num_knots = len(positions)
    tail_visited = set()
    
    # Loop over, update tail if necessary
    for i in range(num_moves):
        # Move head
        positions[0][index] += move_sign
        
        # Loop over head-tail pairs of knots, updating sequentially
        for i in range(num_knots-1):
            
            # Get differences
            row_difference = positions[i][0] - positions[i+1][0]
            col_difference = positions[i][1] - positions[i+1][1]
        
            # Move tail horizontally
            if abs(row_difference) > 1 and col_difference == 0:
                positions[i+1][0] += sign(row_difference)
            
            # Move tail vertically
            if row_difference == 0 and abs(col_difference) > 1:
                positions[i+1][1] += sign(col_difference)
            
            # Move tail diagnoally - simple case
            if (abs(row_difference) > 1 and abs(col_difference) > 0) or (abs(row_difference) > 0 and abs(col_difference) > 1):
                positions[i+1][0] += sign(row_difference)
                positions[i+1][1] += sign(col_difference)
            
            
        
        # Store new tail position
        # print("Position ahead: " + str(positions[num_knots-2]))
        # print("Tail Position: " + str(positions[num_knots-1]))
        tail_visited.add(tuple(positions[num_knots-1]))
    
    # Return
    return positions, tail_visited

# Function that iterates through moves and stores positions
def compute_positions(move_list: list[str], num_knots: int) -> set[tuple[int]]:
    # Initialise tracking vars
    position_list = []
    for i in range(num_knots):
        position_list.append([0,0])
    
    # Initialise tail location visits
    tail_visited = set()
    
    # Iterate over moves
    for move in move_list:
        direction, number = move.split()
        position_list, new_tail_visited = update_positions(direction, int(number), position_list)
        tail_visited = tail_visited | new_tail_visited
    
    # Return
    return set(tail_visited)

# Main
def main():
    # Get file path
    file_path = get_input_file_path()
    
    # Read in input file
    with open(file_path) as input_file:
        motions = input_file.read().rstrip().split("\n")
    
    # Part 1: Compute number of unique positions for 2 knots
    tail_vistied_2 = compute_positions(motions, 2)
    print("Part 1: The tail has visited " + str(len(tail_vistied_2)) + " unique positions")
    
    # Part 2: Compute number of unique positions for 10 knots
    tail_vistied_10 = compute_positions(motions, 10)
    print("Part 2: The tail has visited " + str(len(tail_vistied_10)) + " unique positions")

# Run
if __name__ == "__main__":
    main()