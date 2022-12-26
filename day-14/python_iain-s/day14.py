import numpy as np

# def calc_mins_maxs(paths):
#     xmin = 10_000
#     xmax = 1
#     ymax = 0
#
#     for path in paths:
#         for x, y in path:
#             xmin = min(xmin, x)
#             xmax = max(xmax, x)
#             ymax = max(ymax, y)
#
#     return xmin, xmax, 0, ymax


class Cave:
    def calc_mins_maxs(self,paths):
        xmin = 10_000
        xmax = 1
        ymax = 0

        for path in paths:
            for x, y in path:
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymax = max(ymax, y)

        return xmin, xmax, 0, ymax

    # def fudge_paths(self, paths):
    #     # for part 2
    #     return paths

    def __init__(self, paths):
        # paths = self.fudge_paths(paths)

        xmin, xmax, ymin, ymax = self.calc_mins_maxs(paths)

        # A 2D copy of the cave's contents, where 0s are air
        self.contents = np.zeros((ymax - ymin + 1, xmax - xmin + 1))

        # Add the rocks paths as 4s
        for path in paths:
            for start, stop in zip(path[:-1], path[1:]):
                startx = min(start[0], stop[0]) - xmin
                stopx = max(start[0], stop[0]) + 1 - xmin
                starty = min(start[1], stop[1])
                stopy = max(start[1], stop[1]) + 1
                self.contents[starty:stopy, startx:stopx] = 4

        # Show the source of the sand with a 1
        self.sourcex = 500 - xmin
        # self.contents[0, self.sourcex] = 1

        # Simulate a stream of sand rather than one grain at a time
        self.falling_sand = []  # the sand in motion
        self.static_sand = []  # the sand that has stopped

    def take_turn(self):
        while self.falling_sand:
            # Note these are in y,x not x,y
            particle = self.falling_sand[0]

            # Set the old location of the sand particle back to air
            self.contents[particle[0], particle[1]] = 0

            if self.contents[particle[0] + 1, particle[1]] == 0:
                # down
                particle[0] += 1
            elif self.contents[particle[0] + 1, particle[1] - 1] == 0:
                # diag left
                particle[0] += 1
                particle[1] -= 1
            elif self.contents[particle[0] + 1, particle[1] + 1] == 0:
                # diag right
                particle[0] += 1
                particle[1] += 1
            else:
                # stops
                self.static_sand.append(self.falling_sand.pop(0))

            # Set the new location of the sand particle
            self.contents[particle[0], particle[1]] = 3

        # Add a new grain
        assert self.contents[0, self.sourcex] == 0
        # self.contents[0, self.sourcex] = 3
        self.falling_sand.append([0, self.sourcex])

class CaveTwo(Cave):
    def calc_mins_maxs(self,paths):
        xmin = 10_000
        xmax = 1
        ymax = 0

        for path in paths:
            for x, y in path:
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymax = max(ymax, y)

        return xmin, xmax, 0, ymax
    def __init__(self, paths):
        xmin, xmax, ymin, ymax = super().calc_mins_maxs(paths)

        # We can, at most, form a triangle as wide as it is high from the start point
        paths.append([(0, ymax+2), (1_000, ymax+2)])
        # paths.append([(480, ymax+2), (520, ymax+2)])

        super().__init__(paths)



def get_paths(lines):
    paths = []
    for line in lines:
        path = []
        for pair in line.split(" -> "):
            path.append(eval(pair))
        paths.append(path)
    return paths


def build_cave(lines):
    cave = Cave(get_paths(lines))

    return cave


def one(lines):
    cave = Cave(get_paths(lines))
    while True:
        try:
            cave.take_turn()
        except IndexError:
            # If sand goes outside the cave then we know it will fall forever
            return len(cave.static_sand)


def two(lines):
    cave = CaveTwo(get_paths(lines))
    while True:
        try:
            cave.take_turn()
        except AssertionError:
            # If sand goes outside the cave then we know it will fall forever
            return len(cave.static_sand)


def main():
    with open("../inputs/day14.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
