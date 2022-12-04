import unittest
from src.day3 import one, score_item, two


class TestOne(unittest.TestCase):

    def test_score(self):
        self.assertEqual(score_item('a'), 1)
        self.assertEqual(score_item('z'), 26)
        self.assertEqual(score_item('A'), 27)
        self.assertEqual(score_item('Z'), 52)

    def test_example(self):
        with open("../examples/day3.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 157
        actual = one(content)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day3.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 70
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
