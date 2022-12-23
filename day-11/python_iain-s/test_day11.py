import unittest
from unittest.mock import MagicMock, call

from src.day11 import MonkeyOne, one, parse_monkey, two

NONE_FUNC = lambda x: None


def null_monkey():
    return MonkeyOne([], NONE_FUNC, 1, 0, 0)


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day11.txt", encoding="utf-8") as f:
            content = f.read()

        expected = 10605
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_monkey_passes(self):
        mone = MagicMock()
        mtwo = MagicMock()
        mthree = MagicMock()

        mzero = MonkeyOne([79, 98], lambda old: old * 19, 19, 2, 3)
        mzero.join_troupe([mzero, mone, mtwo, mthree])

        mzero.take_turn()
        mthree.receive.assert_has_calls([call(500), call(620)])

    def test_monkey_receives(self):
        zero = null_monkey()
        zero.receive(1000)

        self.assertListEqual([1000], zero.items)

    def test_parse_monkey(self):
        text = "\n".join(
            [
                "0:",
                "  Starting items: 79, 98",
                "  Operation: new = old * 19",
                "  Test: divisible by 23",
                "    If true: throw to monkey 2",
                "    If false: throw to monkey 3",
            ]
        )

        expected = MonkeyOne([79, 98], lambda x: x * 19, lambda x: x % 23 == 0, 2, 3)
        actual = parse_monkey(text, MonkeyOne)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day11.txt", encoding="utf-8") as f:
            content = f.read()

        expected = 2713310158
        actual = two(content)
        self.assertEqual(expected, actual)

    def test_theory(self):
        pass


if __name__ == "__main__":
    unittest.main()
