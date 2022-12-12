import unittest
from unittest.mock import MagicMock, call
from src.day8 import one, two, from_below, from_left, from_right, from_above


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day8.txt") as f:
            content = [line.rstrip() for line in f]

        expected = 21
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_from_below(self):
        mock = MagicMock()
        from_below(mock, [[1, 2], [3, 4]])
        mock.assert_has_calls(
            [call(), call()(1), call()(2), call(), call()(3), call()(4)]
        )

        actual = from_below(lambda: lambda x: x, [[1, 2], [3, 4]])
        expected = [[1, 2], [3, 4]]
        self.assertEqual(expected, actual)

    def test_from_left(self):
        mock = MagicMock()
        from_left(mock, [[1, 2], [3, 4]])
        mock.assert_has_calls(
            [
                call(),
                call()(1),
                call()(3),
                call(),
                call()(2),
                call()(4),
            ]
        )

        actual = from_left(lambda: lambda x: x, [[1, 2], [3, 4]])
        expected = [(1, 2), (3, 4)]
        self.assertEqual(expected, actual)

    def test_from_right(self):
        mock = MagicMock()
        from_right(mock, [[1, 2], [3, 4]])
        mock.assert_has_calls(
            [
                call(),
                call()(3),
                call()(1),
                call(),
                call()(4),
                call()(2),
            ]
        )

        actual = from_right(lambda: lambda x: x, [[1, 2], [3, 4]])
        expected = [(1, 2), (3, 4)]
        self.assertEqual(expected, actual)

    def test_from_above(self):
        mock = MagicMock()
        from_above(mock, [[1, 2], [3, 4]])
        mock.assert_has_calls(
            [call(), call()(2), call()(1), call(), call()(4), call()(3)]
        )

        actual = from_above(lambda: lambda x: x, [[1, 2], [3, 4]])
        expected = [[1, 2], [3, 4]]
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day8.txt") as f:
            content = [line.rstrip() for line in f]

        scores = two(content)

        self.assertEqual(scores[0][0], 4)
        self.assertEqual(scores[0][0], 8)


if __name__ == "__main__":
    unittest.main()
