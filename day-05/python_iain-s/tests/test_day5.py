import unittest
from src.day5 import one, two


class TestOne(unittest.TestCase):

    def test_example(self):
        with open("../examples/day5.txt") as f:
            content = f.read()

        expected = "CMZ"
        actual = one(content)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day5.txt") as f:
            content = f.read()

        expected = "MCD"
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
