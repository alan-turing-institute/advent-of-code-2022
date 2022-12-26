import unittest

from numpy import array

from src.day14 import one, two, build_cave


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day14.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 24
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_build_cave(self):
        with open("../examples/day14.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        cave = build_cave(content)
        actual = cave.contents
        expected = array(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 4.0, 4.0],
                [0.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 4.0, 0.0],
                [0.0, 0.0, 4.0, 4.0, 4.0, 0.0, 0.0, 0.0, 4.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0],
                [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 0.0],
            ]
        )
        self.assertTrue((expected == actual).all())

        cave.take_turn()
        actual = cave.contents
        expected[1, 6] = 3
        self.assertTrue((expected == actual).all())


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day14.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 93
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
