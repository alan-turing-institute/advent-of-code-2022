from typing import Dict, Tuple

import networkx as nx

calls = 0


def build_graph(lines):
    """Build a graph from lines where each node has a flow rate and state."""
    G = nx.Graph()

    for line in lines:
        this_node = line[6:8]
        flow = line[23:line.index(";")]
        leads_to = [x.strip() for x in line[line.index("valve") + len("valves"):].split(",")]

        G.add_node(this_node, flow=int(flow), on=False)
        G.add_weighted_edges_from([(this_node, that_node, 1) for that_node in leads_to])

    return G


def remove_node(G, n):
    # neighbours = list(G.neighbors(n))
    edges = list(nx.edges(G, n))

    # for each pair of edges, add a new edge
    pairs = [(a, b) for idx, a in enumerate(edges) for b in edges[idx + 1:]]
    for pair in pairs:
        neighbour1 = pair[0][0] if pair[0][1] == n else pair[0][1]
        neighbour2 = pair[1][0] if pair[1][1] == n else pair[1][1]
        G.add_weighted_edges_from(
            [
                (neighbour1, neighbour2, G.edges[pair[0]]["weight"] + G.edges[pair[1]]["weight"])
            ]
        )

    # removing this node also removes all edges from it
    G.remove_node(n)
    return G


def prune_graph(G):
    """Remove nodes with zero flow (except AA)."""

    nodes = list(G.nodes)
    for n in nodes:
        if G.nodes[n]["flow"] == 0 and n != "AA":
            G = remove_node(G, n)

    return G


def max_pressure(start: str, nodes: Dict[str, int], distances: Dict[str, Dict[str, int]], mins):
    global calls
    calls += 1

    # We will activate all of the valves we visit except that the starting node may have no flow
    if nodes[start]:
        mins -= 1
        pressure_from_activating = nodes[start] * mins
    else:
        pressure_from_activating = 0

    # The nodes we might visit next
    other_nodes = nodes.copy()
    # We don't want to return to this node
    other_nodes.pop(start)

    max_pressures = 0
    visited_nodes = []
    for node in other_nodes:

        # Only try other nodes if they are reachable
        if distances[start][node] < mins:
            maximum, nodes = max_pressure(node, other_nodes, distances, mins - distances[start][node])
            if maximum > max_pressures:
                visited_nodes = nodes
                max_pressures = maximum

    visited_nodes.append(start)
    return pressure_from_activating + max_pressures, visited_nodes


def one(lines):
    """Calculate the pressure released."""
    G = build_graph(lines)

    # Shortest paths between nodes with non-zero flow rates
    nodes = {node: G.nodes[node]["flow"] for node in G.nodes if G.nodes[node]["flow"] > 0 or node == "AA"}
    distances = dict(nx.all_pairs_shortest_path_length(G))

    max_p, path = max_pressure("AA", nodes, distances, 30)
    print("path", path[::-1])
    return max_p

def get_max_pressure_three(distances):

    def max_pressure_two(starts: Tuple[str,str], nodes: Dict[str, int], minss: Tuple[int, int]):
        # We will activate all of the valves we visit except that the starting node may have no flow
        if starts[0] == "AA":
            pressure_from_activating = 0
        else:
            minss = minss[0]-1, minss[1]-1
            pressure_from_activating = (nodes[starts[0]] * minss[0]) + (nodes[starts[1]] * minss[1])

        # The nodes we might visit next
        other_nodes1 = nodes.copy()
        other_nodes2 = nodes.copy()
        # We don't want to return to this node
        other_nodes1.pop(starts[0])
        other_nodes2.pop(starts[1])

        max_pressures = 0
        visited_nodes = []

        # todo what if there are other_nodes1 but no other_nodes2
        for node1 in other_nodes1:
            for node2 in other_nodes2:
                # if node1 == node2:
                    # No reason for both you and the 'phant to visit the same one
                    # continue

                # todo is this logic correct?
                # Only try other nodes if at least one is reachable
                if distances[starts[0]][node1] < minss[0] or distances[starts[1]][node2] < minss[2]:
                    maximum, nodes = max_pressure_two((node1, node2), other_nodes, distances, mins - distances[start][node])
                    if maximum > max_pressures:
                        visited_nodes = nodes
                        max_pressures = maximum

        visited_nodes.append(starts)
        return pressure_from_activating + max_pressures, visited_nodes

    return max_pressure_two


def sublists(xs):
    """See https://stackoverflow.com/a/29657078"""
    l = len(xs)
    for i in range(1 << l):
        incl, excl = [], []
        for j in range(l):
            if i & (1 << j):
                incl.append(xs[j])
            else:
                excl.append(xs[j])
        yield (incl, excl)


def get_max_pressure_two(distances):
    def max_pressure_two(nodes: Dict[str, int]):
        # We will activate all of the valves we visit except that the starting node may have no flow

        # 2^n of these!
        node_list = list(nodes.keys())
        node_list.pop(node_list.index("AA"))

        possible_splits = sublists(node_list)

        best_pressure = 0
        best_split = None
        for split in possible_splits:

            p1, n1 = max_pressure("AA", {"AA": nodes["AA"], **{key: value for key, value in nodes.items() if key in split[0]}}, distances, 26)
            p2, n2 = max_pressure("AA", {"AA": nodes["AA"], **{key: value for key, value in nodes.items() if key in split[1]}}, distances, 26)

            if p1+p2 > best_pressure:
                best_pressure = p1+p2
                best_split = n1, n2

        return best_pressure, best_split

    return max_pressure_two


def two(lines):
    """Calculate the pressure released by you and the elephant."""
    G = build_graph(lines)

    # Shortest paths between nodes with non-zero flow rates
    nodes = {node: G.nodes[node]["flow"] for node in G.nodes if G.nodes[node]["flow"] > 0 or node == "AA"}
    distances = dict(nx.all_pairs_shortest_path_length(G))

    max_p, path = get_max_pressure_two(distances)(nodes)
    print("path", path[::-1])
    return max_p


def main():
    with open("../inputs/day16.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
