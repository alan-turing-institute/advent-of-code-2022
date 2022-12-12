def from_below(get_func, grid):
    result = []
    for xs in grid:
        func = get_func()
        result.append([func(x) for x in xs])
    return result


def from_above(get_func, grid):
    result = []
    for xs in grid:
        func = get_func()
        result.append([func(x) for x in xs[::-1]][::-1])
    return result


def from_left(get_func, grid):
    return list(zip(*from_below(get_func, zip(*grid))))


def from_right(get_func, grid):
    return list(zip(*from_above(get_func, zip(*grid))))


def one(lines):
    grid = [[int(char) for char in line] for line in lines]

    def get_func():
        maximum = -1

        def func(height):
            nonlocal maximum

            if height > maximum:
                maximum = height
                return 1
            else:
                return 0

        return func

    as_viewed_from_left = from_left(get_func, grid)
    as_viewed_from_right = from_right(get_func, grid)
    as_viewed_from_below = from_below(get_func, grid)
    as_viewed_from_above = from_above(get_func, grid)

    count_visible = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            visible = (
                as_viewed_from_below[i][j]
                or as_viewed_from_above[i][j]
                or as_viewed_from_left[i][j]
                or as_viewed_from_right[i][j]
            )
            count_visible += visible

    print(grid)

    return count_visible


def two(lines):
    grid = [[int(char) for char in line] for line in lines]

    def get_func():
        visited_trees = []

        def func(height):
            count_visible = 0

            # Look back over our shoulder
            for tree in visited_trees[::-1]:
                count_visible += 1

                if tree >= height:
                    break

            visited_trees.append(height)

            return count_visible

        return func

    as_viewed_from_left = from_left(get_func, grid)
    as_viewed_from_right = from_right(get_func, grid)
    as_viewed_from_below = from_below(get_func, grid)
    as_viewed_from_above = from_above(get_func, grid)

    max_score = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            visible = (
                as_viewed_from_below[i][j]
                * as_viewed_from_above[i][j]
                * as_viewed_from_left[i][j]
                * as_viewed_from_right[i][j]
            )
            max_score = max(visible, max_score)

    return max_score


def main():
    with open("../inputs/day8.txt") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
