import unittest
from src.day13 import one, two, split_text, right_order


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day13.txt", encoding="utf-8") as f:
            content = f.read()

        expected = 13
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_split(self):
        text = "[[]]\n[1]\n\n1\n2"
        expected = [([[]], [1]), (1, 2)]
        actual = split_text(text)
        self.assertListEqual(expected, actual)

    def test_right_order(self):
        self.assertTrue(right_order([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]))
        self.assertTrue(right_order([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]))
        self.assertFalse(right_order([9], [[8, 7, 6]]))
        self.assertTrue(right_order([[4, 4], 4, 4], [[4, 4], 4, 4, 4]))


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day13.txt", encoding="utf-8") as f:
            content = f.read()

        expected = 140
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
