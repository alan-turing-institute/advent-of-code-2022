import unittest
from src.day18 import one, two, get_locations, calc_adjacents, make_mold, fill_mold, melt_wax, get_outer_area


class TestOne(unittest.TestCase):
    content = None

    @classmethod
    def setUpClass(cls):
        with open("../examples/day18.txt", encoding="utf-8") as f:
            cls.content = [line.rstrip() for line in f]

    def test_example(self):
        expected = 64
        actual = one(self.content)
        self.assertEqual(expected, actual)

    def test_get_locations(self):
        expected = [
            (2, 2, 2),
            (1, 2, 2),
            (3, 2, 2),
            (2, 1, 2),
            (2, 3, 2),
            (2, 2, 1),
            (2, 2, 3),
            (2, 2, 4),
            (2, 2, 6),
            (1, 2, 5),
            (3, 2, 5),
            (2, 1, 5),
            (2, 3, 5),
        ]
        actual = get_locations(self.content)
        self.assertListEqual(expected, actual)

    def test_calc_adjacents(self):
        locations = [
            (1, 1, 1),
            (1, 2, 1),
            (3, 1, 1)
        ]
        actual = calc_adjacents(locations)
        expected = [
            [1, 0],
            [1, 0],
            [0, 0]
        ]
        self.assertListEqual(expected, actual)


class TestTwo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("../examples/day18.txt", encoding="utf-8") as f:
            cls.content = [line.rstrip() for line in f]

    def test_example(self):
        expected = 58
        actual = two(self.content)
        self.assertEqual(expected, actual)

    def test_make_mold(self):
        expected = [
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]],
            [[0, 0, 0],
             [0, 1, 0],
             [0, 0, 0]],
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]],
        ]
        actual = make_mold([(1, 1, 1)])
        self.assertListEqual(expected, actual)

        actual = make_mold([(1, 2, 3)])
        self.assertListEqual(expected, actual)

    def test_fill_mold(self):
        mold = [
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]],
            [[0, 0, 0],
             [0, 1, 0],
             [0, 0, 0]],
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]],
        ]
        expected = [
            [[2, 2, 2],
             [2, 2, 2],
             [2, 2, 2]],
            [[2, 2, 2],
             [2, 1, 2],
             [2, 2, 2]],
            [[2, 2, 2],
             [2, 2, 2],
             [2, 2, 2]],
        ]
        actual = fill_mold(mold)
        self.assertListEqual(expected, actual[0])
        self.assertEqual(26, actual[1])

        mold = [
            [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 1, 1, 0],
             [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 0, 1, 0],
             [0, 1, 1, 1, 0],
             [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 1, 1, 0],
             [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]],
        ]
        expected = [
            [[2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2]],
            [[2, 2, 2, 2, 2],
             [2, 1, 1, 1, 2],
             [2, 1, 1, 1, 2],
             [2, 1, 1, 1, 2],
             [2, 2, 2, 2, 2]],
            [[2, 2, 2, 2, 2],
             [2, 1, 1, 1, 2],
             [2, 1, 0, 1, 2],
             [2, 1, 1, 1, 2],
             [2, 2, 2, 2, 2]],
            [[2, 2, 2, 2, 2],
             [2, 1, 1, 1, 2],
             [2, 1, 1, 1, 2],
             [2, 1, 1, 1, 2],
             [2, 2, 2, 2, 2]],
            [[2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2],
             [2, 2, 2, 2, 2]],
        ]
        actual = fill_mold(mold)
        self.assertListEqual(expected, actual[0])

    def test_melt_wax(self):
        filled_mold = [
            [[2, 2, 2],
             [2, 2, 2],
             [2, 2, 2]],
            [[2, 2, 2],
             [2, 1, 2],
             [2, 2, 2]],
            [[2, 2, 2],
             [2, 2, 2],
             [2, 2, 2]],
        ]
        actual = melt_wax(filled_mold)
        expected = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0),
                    (0, 0, 1), (1, 0, 1), (2, 0, 1), (0, 1, 1), (2, 1, 1), (0, 2, 1), (1, 2, 1), (2, 2, 1), (0, 0, 2),
                    (1, 0, 2), (2, 0, 2), (0, 1, 2), (1, 1, 2), (2, 1, 2), (0, 2, 2), (1, 2, 2), (2, 2, 2)]
        self.assertListEqual(expected, actual)

    def test_get_outer_area(self):
        filled_mold = [
            [[2, 2, 2],
             [2, 2, 2],
             [2, 2, 2]],
            [[2, 2, 2],
             [2, 1, 2],
             [2, 2, 2]],
            [[2, 2, 2],
             [2, 2, 2],
             [2, 2, 2]],
        ]
        expected = 54
        actual = get_outer_area(filled_mold)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
