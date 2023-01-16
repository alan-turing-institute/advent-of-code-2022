import unittest

from src.day17 import one, two, combine, repeat, RockFour, RockOne, RockThree, RockTwo, calc_highest_y, optimise, \
    find_cycle


class TestOne(unittest.TestCase):

    def test_example(self):
        with open("../examples/day17.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 3068
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_optimise(self):
        # Can't optimise the start point any further
        highpoints = [[1] for _ in range(7)]
        expected = 0
        actual = optimise(highpoints)
        self.assertEqual(expected, actual)
        self.assertListEqual([[1] for _ in range(7)], highpoints)

        highpoints = [[1, 1] for _ in range(7)]
        expected = 1
        actual = optimise(highpoints)
        self.assertEqual(expected, actual)
        self.assertListEqual([[1] for _ in range(7)], highpoints)

        highpoints = [
            [1, 1, 1, 1],
            [1, 1, 1, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        copy = [
            [1, 1, 1, 1],
            [1, 1, 1, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        expected = 0
        actual = optimise(highpoints)
        self.assertEqual(expected, actual)
        self.assertListEqual(copy, highpoints)

        highpoints = [
            [1, 1, 1, 1],
            [1, 1, 0, 1],
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        copy = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        expected = 1
        actual = optimise(highpoints)
        self.assertEqual(expected, actual)
        self.assertListEqual(copy, highpoints)

        print("!!")
        highpoints = [
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 0],
        ]
        copy = [
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 0],
        ]
        expected = 0
        actual = optimise(highpoints)
        self.assertEqual(expected, actual)
        self.assertListEqual(copy, highpoints)

    def test_repeat(self):
        with open("../examples/day17.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        for i, m in enumerate(repeat(content[0])):
            if i == 4:
                self.assertEqual("<", m)

            if i == 41:
                self.assertEqual(">", m)
                return

    def test_intersects(self):
        highpoints = [[1] for _ in range(7)]
        rock = RockFour(0)
        for _ in range(2):
            rock.move_down()

        self.assertFalse(rock.intersects_down(highpoints))
        rock.move_down()
        self.assertTrue(rock.intersects_down(highpoints))

        # |..##...|
        # |..#.@..|
        # |..#@@@.|
        # |####@..|
        # |.......|
        # +-------+
        rock = RockTwo(0)
        rock.xy_positions = [(3, 3), (4, 2)]
        highpoints = [
            [1, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
        ]
        self.assertTrue(rock.intersects_down(highpoints))

    def test_hits_wall(self):
        highpoints = [[1] for _ in range(7)]

        # Hit the left wall if we move left
        rock = RockOne(0)
        self.assertFalse(rock.intersects_side("<", highpoints))
        rock.move_side("<")
        self.assertFalse(rock.intersects_side("<", highpoints))
        rock.move_side("<")
        self.assertTrue(rock.intersects_side("<", highpoints))
        self.assertFalse(rock.intersects_side(">", highpoints))

        # Hit the left wall if we move left
        rock = RockOne(0)
        self.assertFalse(rock.intersects_side(">", highpoints))
        rock.move_side(">")
        self.assertTrue(rock.intersects_side(">", highpoints))
        self.assertFalse(rock.intersects_side("<", highpoints))

    def test_hits_other_rock(self):
        # |.......|
        # |.......|
        # |..#....|
        # |.###.@.|
        # |..#.@@@|
        # |####.@.|
        # +-------+
        rock = RockTwo(0)
        rock.xy_positions = [(4, 2), (5, 1)]
        highpoints = [
            [1, 1, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 0, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
        ]
        self.assertFalse(rock.intersects_side("<", highpoints))
        self.assertTrue(rock.intersects_side(">", highpoints))
        # |.......|
        # |.......|
        # |....#..|
        # |.@.###.|
        # |@@@.#..|
        # |.@.####|
        # +-------+
        rock = RockTwo(0)  # dummy highpoints
        rock.xy_positions = [(0, 2), (1, 1)]
        highpoints = [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 0, 1, 0],
            [1, 1, 0, 0, 0],
        ]
        self.assertFalse(rock.intersects_side(">", highpoints))
        self.assertTrue(rock.intersects_side("<", highpoints))

        # |..@....|
        # |..@....|
        # |@@@#...|
        # |..###..|
        # |...#...|
        # |..####.|
        # +-------+
        rock = RockThree(0)  # dummy highpoints
        rock.xy_positions = [(0, 4), (2, 5)]
        highpoints = [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 0, 1, 0],
            [1, 1, 0, 0, 0],
        ]
        self.assertTrue(rock.intersects_side(">", highpoints))
        self.assertTrue(rock.intersects_side("<", highpoints))

        # |......@|
        # |......@|
        # |...#@@@|
        # |..###..|
        # |...#...|
        # |..####.|
        # +-------+
        rock = RockThree(0)  # dummy highpoints
        rock.xy_positions = [(4, 4), (6, 5)]
        highpoints = [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 0, 1, 0],
            [1, 1, 0, 0, 0],
        ]
        self.assertTrue(rock.intersects_side(">", highpoints))
        self.assertTrue(rock.intersects_side("<", highpoints))

    def test_spawn(self):
        rock = RockFour(0)

        expected = [(2, 4)]
        self.assertListEqual(expected, rock.xy_positions)

    def test_combine(self):
        # highpoints = [[1]] * 7

        highpoints = [
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ]
        rock = RockThree(0)
        rock.move_down()
        rock.move_down()
        rock.move_down()

        expected = [
            [1] + [0] * 3,
            [1] + [0] * 3,
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 1, 1],
            [1] + [0] * 3,
            [1] + [0] * 3,
        ]
        combine(highpoints, rock)
        self.assertListEqual(expected, highpoints)
        return

        highpoints = [0] * 7
        rock = RockTwo(highpoints)

        expected = [0, 0, 5, 6, 5, 0, 0]
        combine(highpoints, rock)
        self.assertListEqual(expected, highpoints)

    def test_calc_highest_y(self):
        expected = 0
        actual = calc_highest_y([
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ])
        self.assertEqual(expected, actual)

        expected = 2
        actual = calc_highest_y([
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [1, 0, 0],
            [1, 1, 0],
            [1, 0, 0],
            [1, 1, 1],
        ])
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day17.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 1514285714288
        actual = two(content)
        self.assertEqual(expected, actual)

    def test_find_cycle(self):
        with open("../inputs/day17.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 101, 1816
        actual = find_cycle(content[0])
        self.assertTupleEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
