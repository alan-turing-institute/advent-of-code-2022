import unittest
from src.day2 import one, ready_steady_go, two


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day2.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 15
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_ready_steady_go(self):
        expected = 7
        actual = ready_steady_go("C", "X")
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day2.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 12
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
