import unittest
from unittest.mock import patch

from src.day22 import one, two, parse_instructions, simulate_two, make_seam
from src import day22

with open("../examples/day22.txt", encoding="utf-8") as f:
    content = f.read()


class TestOne(unittest.TestCase):
    def test_example(self):
        expected = 6032
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_parse_instructions(self):
        expected = [10, "R", 5, "L", 5, "R", 10, "L", 4, "L", 1]
        actual = parse_instructions("10R5L5R10L4L1")
        self.assertEqual(expected, actual)

    def test_one(self):
        with patch("src.day22.simulate") as mock_simulate:
            mock_simulate.return_value = (1, 2), "U"
            actual = one(content)
            expected = (1000 * 2) + (4 * 3) + 3
            self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        day22.testing = True
        expected = 5031
        actual = two(content)
        self.assertEqual(expected, actual)

    def test_simulate_two(self):
        with open("../examples/day22_II.txt", encoding="utf-8") as f:
            lines = f.readlines()

        board_map = [list(line)[:-1] for line in lines]
        instructions = ["R", 14, "L", 6]
        try:
            simulate_two(board_map, instructions)
        except KeyError:
            pass

    def test_make_seams(self):
        expected = {
            ((0, 8), "U"): ((4, 3), "D"),
            ((0, 9), "U"): ((4, 2), "D"),
            ((0, 10), "U"): ((4, 1), "D"),
            ((0, 11), "U"): ((4, 0), "D"),
            ((4, 3), "U"): ((0, 8), "D"),
            ((4, 2), "U"): ((0, 9), "D"),
            ((4, 1), "U"): ((0, 10), "D"),
            ((4, 0), "U"): ((0, 11), "D"),
        }
        actual = make_seam(((0, 8), (0, 11), "U"), ((4, 3), (4, 0), "D"))
        self.assertDictEqual(expected, actual)

        expected = {
            ((0, 8), "L"): ((4, 4), "D"),
            ((1, 8), "L"): ((4, 5), "D"),
            ((2, 8), "L"): ((4, 6), "D"),
            ((3, 8), "L"): ((4, 7), "D"),
            ((4, 4), "U"): ((0, 8), "R"),
            ((4, 5), "U"): ((1, 8), "R"),
            ((4, 6), "U"): ((2, 8), "R"),
            ((4, 7), "U"): ((3, 8), "R"),
        }
        actual = make_seam(((0, 8), (3, 8), "L"), ((4, 4), (4, 7), "D"))
        self.assertDictEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
