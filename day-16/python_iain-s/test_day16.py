import unittest
import networkx as nx
from networkx.utils.misc import graphs_equal
from matplotlib import pyplot as plt
from src.day16 import one, two, build_graph, prune_graph, max_pressure, calls
from src import day16


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day16.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 1651
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_build_graph(self):
        with open("../inputs/day16.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        g = build_graph(content)
        g = prune_graph(g)

        labels = {node: node for node in g.nodes}
        pos = nx.spring_layout(g)
        nx.draw_networkx_labels(g, pos, labels)
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_nodes(g, pos)
        plt.show()

    def test_prune_graph(self):
        g1 = nx.Graph()
        g1.add_node("AA", flow=0)
        g1.add_node("BB", flow=1)
        g1.add_node("CC", flow=0)
        g1.add_node("DD", flow=1)
        g1.add_weighted_edges_from([("AA", "BB", 1), ("BB", "CC", 1), ("CC", "DD", 1)])

        # We expect CC to be removed
        expected = nx.Graph()
        expected.add_node("AA", flow=0)
        expected.add_node("BB", flow=1)
        expected.add_node("DD", flow=1)
        expected.add_weighted_edges_from([("AA", "BB", 1), ("BB", "DD", 2)])

        actual = prune_graph(g1)

        self.assertTrue(graphs_equal(expected, actual))

    def test_max_pressurea(self):
        with open("../examples/day16.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 1651
        G = build_graph(content)
        # G = prune_graph(build_graph(content))
        nodes = {node: G.nodes[node]["flow"] for node in G.nodes if G.nodes[node]["flow"] > 0 or node == "AA"}
        distances = dict(nx.all_pairs_shortest_path_length(G))

        actual, path = max_pressure("AA", nodes, distances, 30)
        print(day16.calls, "calls")
        print("path", path[::-1])
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day16.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 1707
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
