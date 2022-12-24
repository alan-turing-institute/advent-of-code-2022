from dataclasses import dataclass
from typing import Optional, Final, Dict

HEIGHTS: Final[Dict[str, int]] = {
    "S": 0,
    "E": 25,
    **{chr(x + 97): x for x in range(26)},
}


@dataclass
class Node:
    letter: str
    lrud: tuple[Optional["Node"], Optional["Node"], Optional["Node"], Optional["Node"]]

    def __eq__(self, other):
        # For performance and to avoid infinite recursion
        return self is other


def get_lrud(nodes, x, y):
    """Get the nodes that can be reached from x,y."""
    left, right, up, down = None, None, None, None
    threshold = HEIGHTS[nodes[y][x].letter] + 2

    if x > 0 and HEIGHTS[nodes[y][x - 1].letter] < threshold:
        left = nodes[y][x - 1]

    if x + 1 < len(nodes[y]) and HEIGHTS[nodes[y][x + 1].letter] < threshold:
        right = nodes[y][x + 1]

    if y > 0 and HEIGHTS[nodes[y - 1][x].letter] < threshold:
        up = nodes[y - 1][x]

    if y + 1 < len(nodes) and HEIGHTS[nodes[y + 1][x].letter] < threshold:
        down = nodes[y + 1][x]

    return left, right, up, down


def get_lrud_two(nodes, x, y):
    """Get the nodes that can be reached from x,y by travelling backwards."""
    left, right, up, down = None, None, None, None

    # Reverse our calcs as we can now go up any amount but only down one
    threshold = HEIGHTS[nodes[y][x].letter] - 2

    if x > 0 and HEIGHTS[nodes[y][x - 1].letter] > threshold:
        left = nodes[y][x - 1]

    if x + 1 < len(nodes[y]) and HEIGHTS[nodes[y][x + 1].letter] > threshold:
        right = nodes[y][x + 1]

    if y > 0 and HEIGHTS[nodes[y - 1][x].letter] > threshold:
        up = nodes[y - 1][x]

    if y + 1 < len(nodes) and HEIGHTS[nodes[y + 1][x].letter] > threshold:
        down = nodes[y + 1][x]

    return left, right, up, down


def build_graph(lines, get_allowed_moves_with):
    nodes = []

    for line in lines:
        line_nodes = []

        for char in line:
            line_nodes.append(Node(char, (None, None, None, None)))

        nodes.append(line_nodes)

    for y in range(len(nodes)):
        for x in range(len(nodes[y])):
            nodes[y][x].lrud = get_allowed_moves_with(nodes, x, y)

    return nodes


def unweighted_shortest_path(nodes, start_on, end_on):

    # Is this a good way to break a nested loop?
    class BreakLoop(Exception):
        pass

    try:
        for row in nodes:
            for node in row:
                if node.letter == start_on:
                    start = node
                    raise BreakLoop
    except BreakLoop:
        pass

    paths = [[start]]
    while True:
        print(len(paths[0]), len(paths))

        paths = bfs(paths)
        for path in paths:
            if path[-1].letter == end_on:
                return path


def bfs(paths):
    new_paths = []
    for path in paths:
        last_node = path[-1]
        for next_node in last_node.lrud:
            if next_node and next_node not in path:
                new_paths.append(path + [next_node])

    # Trim the longer paths every time
    i = 0
    while i < len(new_paths):
        node = new_paths[i][-1]
        j = 0
        while j < len(new_paths):
            if i != j:
                if node in new_paths[j]:
                    new_paths.pop(i)
                    i -= 1
                    break
            j += 1
        i += 1

    return new_paths


def one(lines):
    nodes = build_graph(lines, get_lrud)
    shortest_path = unweighted_shortest_path(nodes, "S", "E")
    return len(shortest_path) - 1


def two(lines):
    nodes = build_graph(lines, get_lrud_two)
    shortest_path = unweighted_shortest_path(nodes, "E", "a")
    return len(shortest_path) - 1


def main():
    with open("../inputs/day12.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
