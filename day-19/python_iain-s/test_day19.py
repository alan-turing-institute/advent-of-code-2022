import unittest
from unittest.mock import patch

from src.day19 import one, two, get_blueprint, run_one

with open("../examples/day19.txt", encoding="utf-8") as f:
    content = [line.rstrip() for line in f]


class TestOne(unittest.TestCase):

    def test_example(self):
        expected = 33
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_one(self):
        with patch("src.day19.calc_most_geodes") as mock_geodes:
            mock_geodes.side_effect = [9, 12]

            expected = 33
            actual = one(content)
            self.assertEqual(expected, actual)

    def test_run_one(self):
        expected = 9
        actual = run_one(get_blueprint(content[0]))
        self.assertEqual(expected, actual)

        expected = 12
        actual = run_one(get_blueprint(content[1]))
        self.assertEqual(expected, actual)

    def test_blueprints(self):
        expected = HashableDict({
            "ore_cost": (4,),
            "clay_cost": (2,),
            "obsidian_cost": (3, 14),
            "geode_cost": (2, 7),
        })
        actual = get_blueprint(
            "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.")
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        expected = -1
        actual = two(content)
        self.assertEqual(expected, actual)

    def test_run_two(self):
        expected = 56 * 62
        actual = two(content[0:2])
        self.assertEqual(expected, actual)

    def test_run_one(self):
        expected = 62
        actual = run_one(get_blueprint(content[1]), 32)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
