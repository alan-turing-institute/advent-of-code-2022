import unittest
from src.day21 import one, two


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day21.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 152
        actual = one(content)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day21.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 301
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
