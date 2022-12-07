import unittest
from src.day7 import one, two, build_tree, walk_tree


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day7.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 95437
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_build_tree(self):
        with open("../examples/day7_ii.txt") as f:
            content = [line.rstrip() for line in f]

        expected = {
            "/": {
                "a": {"f": 29116, "g": 2557},
                "b.txt": 14848514,
                "c.dat": 8504156,
                "d": {},
            }
        }
        actual = {"/": {}}
        build_tree(content[1:], actual["/"])
        self.assertEqual(expected, actual)

    def test_walk_tree(self):
        tree = {"/": {"a": {}, "b.txt": 14848514, "c.dat": 8504156, "d": {}}}
        self.assertEqual((23352670, {"a": 0, "/": 23352670, "d": 0}), walk_tree(tree))

        tree = {
            "/": {
                "a": {"f": 29116, "g": 2557},
                "b.txt": 14848514,
                "c.dat": 8504156,
                "d": {},
            }
        }
        self.assertEqual(
            (23384343, {"/": 23384343, "a": 31673, "d": 0}), walk_tree(tree)
        )


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day7.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 24933642
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
