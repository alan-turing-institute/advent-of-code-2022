from argparse import ArgumentParser

# Usage: python 03_bagpack.py input_file_path
def get_input_file_path() -> str:
    parser = ArgumentParser(description="AOC Day 4 Function")
    parser.add_argument("input_file_path") # required (positional) arguments
    args = parser.parse_args()
    return args.input_file_path

# Part 1
def assignment_to_ints(assignment: str) -> list[int]:
    return [int(x) for x in assignment.split("-")]

def complete_pair_overlap(pair: str) -> int:
    pair = pair.split(",")
    assignment_1 = assignment_to_ints(pair[0])
    assignment_2 = assignment_to_ints(pair[1])
    min_boundary = min(assignment_1[0], assignment_2[0])
    max_boundary = max(assignment_1[1], assignment_2[1])
    if min_boundary == assignment_1[0] and max_boundary == assignment_1[1]:
        overlap = 1
    elif min_boundary == assignment_2[0] and max_boundary == assignment_2[1]:
        overlap = 1
    else:
        overlap = 0
    return overlap

# Part 2
def partial_pair_overlap(pair: str) -> int:
    pair = pair.split(",")
    assignment_1 = assignment_to_ints(pair[0])
    assignment_2 = assignment_to_ints(pair[1])
    if assignment_1[1] < assignment_2[0] or assignment_1[0] > assignment_2[1]:
        return 0
    else:
        return 1

# Main
def main():
    # Get file path
    file_path = get_input_file_path()
    
    # Read in input file
    with open(file_path) as input_file:
        # Process input
        assignment_pairs = input_file.read().rstrip()
        assignment_list = assignment_pairs.split("\n")
        
        # Part 1
        num_complete_overlap = sum(list(map(complete_pair_overlap, assignment_list)))
        print("The number of completely overlapped pairs is " + str(num_complete_overlap))
        
        # Part 2
        num_partial_overlap = sum(list(map(partial_pair_overlap, assignment_list)))
        print("The number of partially overlapping pairs is " + str(num_partial_overlap))

# Run
if __name__ == "__main__":
    main()