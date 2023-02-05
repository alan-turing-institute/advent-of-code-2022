import unittest
from src.day25 import (
    one,
    two,
    snafu_to_dec,
    dec_to_snafu,
    num_snafu_digits,
    dec_to_base_five,
)


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day25.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = "2=-1=0"
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_snafu_to_dec(self):
        self.assertEqual(1, snafu_to_dec("1"))
        self.assertEqual(2, snafu_to_dec("2"))
        self.assertEqual(3, snafu_to_dec("1="))
        self.assertEqual(4, snafu_to_dec("1-"))
        self.assertEqual(5, snafu_to_dec("10"))
        self.assertEqual(6, snafu_to_dec("11"))
        self.assertEqual(7, snafu_to_dec("12"))
        self.assertEqual(8, snafu_to_dec("2="))
        self.assertEqual(9, snafu_to_dec("2-"))
        self.assertEqual(10, snafu_to_dec("20"))
        self.assertEqual(15, snafu_to_dec("1=0"))
        self.assertEqual(20, snafu_to_dec("1-0"))
        self.assertEqual(2022, snafu_to_dec("1=11-2"))
        self.assertEqual(12345, snafu_to_dec("1-0---0"))
        self.assertEqual(314159265, snafu_to_dec("1121-1110-1=0"))

    def test_dec_to_snafu(self):
        self.assertEqual(dec_to_snafu(0), "0")
        self.assertEqual(dec_to_snafu(1), "1")
        self.assertEqual(dec_to_snafu(2), "2")
        self.assertEqual(dec_to_snafu(3), "1=")
        self.assertEqual(dec_to_snafu(4), "1-")
        self.assertEqual(dec_to_snafu(5), "10")
        self.assertEqual(dec_to_snafu(6), "11")
        self.assertEqual(dec_to_snafu(7), "12")
        self.assertEqual(dec_to_snafu(8), "2=")
        self.assertEqual(dec_to_snafu(9), "2-")
        self.assertEqual(dec_to_snafu(10), "20")
        self.assertEqual(dec_to_snafu(15), "1=0")
        self.assertEqual(dec_to_snafu(20), "1-0")
        self.assertEqual(dec_to_snafu(2022), "1=11-2")
        self.assertEqual(dec_to_snafu(12345), "1-0---0")
        self.assertEqual(dec_to_snafu(314159265), "1121-1110-1=0")

    def test_num_snafu_digits(self):
        self.assertEqual(1, num_snafu_digits(2))
        self.assertEqual(2, num_snafu_digits(3))
        self.assertEqual(2, num_snafu_digits(12))
        self.assertEqual(13, num_snafu_digits(314159265))

    def test_dec_to_base_five(self):
        # self.assertEqual(1, dec_to_base_five(0))
        # self.assertEqual(1, dec_to_base_five(4))
        # self.assertEqual(2, dec_to_base_five(5))
        # self.assertEqual(3, dec_to_base_five(25))
        self.assertEqual([0], dec_to_base_five(0))
        self.assertEqual([4], dec_to_base_five(4))
        self.assertEqual([1, 0], dec_to_base_five(5))
        self.assertEqual([1, 0, 0], dec_to_base_five(25))


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day25.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = -1
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
