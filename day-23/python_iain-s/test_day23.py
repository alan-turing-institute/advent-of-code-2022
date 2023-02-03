import unittest
from src.day23 import one, double_grove, calc_score, DoneException, two


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day23.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 110
        actual = one(content)

        self.assertEqual(expected, actual)

    def test_double_grove(self):
        expected = [[]]
        actual = double_grove([[]])
        self.assertListEqual(expected, actual)

    def test_calc_score(self):
        expected = 110
        grove = [
            [".", ".", ".", ".", ".", ".", "#", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", "#", ".", "#", ".", ".", "#", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "#", ".", ".", ".", ".", ".", "."],
            [".", ".", "#", ".", ".", ".", ".", ".", "#", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", "#", "#", ".", ".", "."],
            [".", ".", ".", ".", "#", "#", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", ".", ".", "#", ".", "#", ".", ".", "#", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "#", ".", ".", "#", ".", ".", "#", ".", "."],
        ]
        actual = calc_score(grove)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day23.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 20
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
