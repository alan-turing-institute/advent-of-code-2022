import unittest
from src.day12 import (
    one,
    two,
    build_graph,
    Node,
    get_lrud,
    unweighted_shortest_path,
    bfs,
)


class TestOne(unittest.TestCase):
    maxDiff = None
    nones = None, None, None, None

    def test_example(self):
        with open("../examples/day12.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 31
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_get_lrud(self):
        nodes = [
            [Node("a", self.nones), Node("b", self.nones)],
            [Node("a", self.nones), Node("x", self.nones)],
        ]

        actual = get_lrud(nodes, 0, 0)
        expected = None, nodes[0][1], None, nodes[1][0]
        self.assertEqual(expected, actual)

        actual = get_lrud(nodes, 1, 1)
        expected = nodes[1][0], None, nodes[0][1], None
        self.assertEqual(expected, actual)

    def test_build_graph(self):
        content = ("SabcdefghijklmnopqrstuvwxyzE",)
        actual = build_graph(content, get_lrud)

        expected = [[Node(c, (None, None, None, None)) for c in content[0]]]

        for i, node in enumerate(expected[0]):
            node.lrud = (
                expected[0][i - 1] if i > 0 else None,
                expected[0][i + 1] if i + 1 < len(expected[0]) else None,
                None,
                None,
            )

        for i, n in enumerate(expected[0][1:-1]):
            self.assertEqual(n.letter, actual[0][i + 1].letter)
            self.assertEqual(n.lrud[0].letter, actual[0][i + 1].lrud[0].letter)
            self.assertEqual(n.lrud[1].letter, actual[0][i + 1].lrud[1].letter)
            self.assertIsNone(actual[0][i + 1].lrud[2])
            self.assertIsNone(actual[0][i + 1].lrud[3])

    def test_unweighted_shortest_path(self):

        start = Node("S", self.nones)
        end = Node("E", (start, None, None, None))
        start.lrud = None, end, None, None

        path = unweighted_shortest_path([[start, end]], "S", "E")
        assert path == [start, end], path

        path = unweighted_shortest_path([[end, start]], "S", "E")
        assert path == [start, end], path

    def test_bfs(self):
        a = Node("a", self.nones)
        b = Node("b", (a, None, None, None))
        c = Node("c", (None, a, None, None))
        a.lrud = None, b, c, None

        path = bfs([[a]])
        assert path == [[a, b], [a, c]], path


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day12.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 29
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
