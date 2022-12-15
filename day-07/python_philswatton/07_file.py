from argparse import ArgumentParser
from typing import Optional
DIR, FILE = "dir", "file"
SEARCH_SIZE, TOTAL_SPACE, NEEDED_SPACE = 100000, 70000000, 30000000

# Usage: python 07_file.py input_file_path
def get_input_file_path() -> str:
    parser = ArgumentParser(description="AOC Day 0 Function")
    parser.add_argument("input_file_path") # required (positional) arguments
    args = parser.parse_args()
    return args.input_file_path

# Define a class that keeps track of parent and children
class Node:
    def __init__(self,
                 type: str,
                 name: str,
                 children: Optional[dict] = None,
                 parent: Optional["Node"] = None,
                 size: Optional[int] = None
                ) -> None:
        self.type = type
        self.name = name
        self.parent = parent
        self.children = children
        self.size = size

# Function to parse terminal output into Nodes
def output2filesystem(terminal_output: list[str]) -> Node:
    filesystem = Node(type=DIR, name="/", children={}, parent=None)
    current = filesystem
    for line in terminal_output:
        if line[0:4] == "$ cd":
            if line[5] == "/":
                current = filesystem
            elif line[5:] == "..":
                current = current.parent
            else:
                current = current.children[line[5:]]
        elif line[0:3] == "dir":
            dir_name = line[4:]
            current.children[dir_name] = Node(type=DIR,
                                              name=current.name + dir_name + "/",
                                              children={},
                                              parent=current)
        elif line[0:4] != "$ ls":
            parts = line.split()
            current.children[parts[1]] = Node(type=FILE,
                                              name=current.name + parts[1],
                                              children=None,
                                              parent=current,
                                              size=int(parts[0]))
    return filesystem
        
# Function that recursively finds sizes of dirs in Node structure
def node2sizes(node: Node):
    dir_sizes = {node.name : 0}
    for child in node.children.values():
        if child.type == FILE:
            dir_sizes[node.name] += child.size
        if child.type == DIR:
            dir_sizes = dir_sizes | node2sizes(child)
            dir_sizes[node.name] += dir_sizes[child.name]
    return dir_sizes

# Main
def main():
    # Get file path
    file_path = get_input_file_path()
    
    # Read in input file
    with open(file_path) as input_file:
        terminal_output = input_file.read().rstrip().split("\n")
    
    # Parse output into file system
    filesystem = output2filesystem(terminal_output)
    
    # Get dict of dir sizes
    dir_sizes = node2sizes(filesystem)
    
    # Part 1: Use dict comprehension to calculate sum
    print("Part 1: " + str(sum([x for x in dir_sizes.values() if x <= SEARCH_SIZE])))
    
    # Part 2: find smallest sufficiently large file to delete
    unused_space = TOTAL_SPACE - dir_sizes["/"]
    space_needed = NEEDED_SPACE - unused_space
    print("Part 2: " + str(min([x for x in dir_sizes.values() if x >= space_needed])))

# Run
if __name__ == "__main__":
    main()