import unittest
from src.day15 import one, two, extract_diamonds, parse, slice_at, combine_ranges


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day15.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 26
        actual = one(content, 10)
        self.assertEqual(expected, actual)

    def test_extract_diamonds(self):
        actual = extract_diamonds([((2, 2), (3, 2))])
        expected = [((2, 2), 1)]
        self.assertEqual(expected, actual)

        actual = extract_diamonds([((4, 4), (4, 4))])
        expected = [((4, 4), 0)]
        self.assertEqual(expected, actual)

    def test_parse(self):
        lines = ("Sensor at x=2, y=18: closest beacon is at x=-2, y=15",)
        actual = parse(lines)
        expected = [((2, 18), (-2, 15))]
        self.assertEqual(expected, actual)

    def test_slice_at(self):
        actual = slice_at(((8, 7), 9), 16)
        expected = [8, 9]
        self.assertEqual(expected, actual)

        actual = slice_at(((8, 7), 9), 7)
        expected = [-1, 18]
        self.assertEqual(expected, actual)

    def test_combine_ranges(self):
        ranges = []
        excluded = 1, 2

        self.assertFalse(combine_ranges(ranges, excluded))
        self.assertListEqual([], ranges)

        ranges = [[1, 2]]
        excluded = 1, 2

        self.assertTrue(combine_ranges(ranges, excluded))
        self.assertListEqual([[1, 2]], ranges)

        ranges = [[1, 2]]
        excluded = 0, 2

        self.assertTrue(combine_ranges(ranges, excluded))
        self.assertListEqual([[0, 2]], ranges)

        ranges = [[1, 2]]
        excluded = 1, 3

        self.assertTrue(combine_ranges(ranges, excluded))
        self.assertListEqual([[1, 3]], ranges)

        ranges = [[1, 2]]
        excluded = 0, 3

        self.assertTrue(combine_ranges(ranges, excluded))
        self.assertListEqual([[0, 3]], ranges)

        ranges = [[0, 3]]
        excluded = 1, 2

        self.assertTrue(combine_ranges(ranges, excluded))
        self.assertListEqual([[0, 3]], ranges)

        ranges = [[1, 2]]
        excluded = 2, 3

        self.assertTrue(combine_ranges(ranges, excluded))
        self.assertListEqual([[1, 3]], ranges)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day15.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 56000011
        actual = two(content, 20)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
