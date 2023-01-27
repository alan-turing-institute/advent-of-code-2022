import unittest
from src.day20 import one, two, move_right, calc_coords


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day20.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 3
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_switch_element(self):
        actual = ["a", "b", "c", "d"]
        expected = ["a", "c", "b", "d"]
        move_right(actual, 1, 1)
        self.assertListEqual(expected, actual)

        actual = ["a", "b", "c", "d"]
        expected = ["a", "b", "c", "d"]
        move_right(actual, 1, 3)
        self.assertListEqual(expected, actual)

        actual = ["a", "b", "c"]
        expected = ["a", "b", "c"]
        move_right(actual, 1, 0)
        self.assertListEqual(expected, actual)

        actual = [1, -3, 2, 3, -2, 0, 4]
        expected = [1, 2, 3, -2, -3, 0, 4]
        move_right(actual, 1, -3)
        self.assertListEqual(expected, actual)

        actual = [1, 2, -3, 0, 3, 4, -2]
        expected = [1, 2, -3, 4, 0, 3, -2]
        move_right(actual, 5, 4)
        self.assertListEqual(expected, actual)

        actual = [1, 2, -2, -3, 0, 3, 4]
        expected = [1, 2, -3, 0, 3, 4, -2]
        move_right(actual, 2, -2)
        self.assertListEqual(expected, actual)

    def test_calc_coords(self):
        self.assertEqual(3, calc_coords([1, 2, -3, 4, 0, 3, -2]))


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day20.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 1623178306
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
