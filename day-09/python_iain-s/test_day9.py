import unittest
from src.day9 import one, two, rope


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day9.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 13
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_rope(self):
        with open("../examples/day9.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 13
        actual = rope(content, 2)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day9.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 1
        actual = two(content)
        self.assertEqual(expected, actual)

        second_example = ["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"]
        self.assertEqual(two(second_example), 36)


if __name__ == "__main__":
    unittest.main()
