def one(lines):
    locations = get_locations(lines)
    return calc_total_area(locations)


def calc_total_area(locations):
    # Make a n * n-1 matrix
    adjacents = calc_adjacents(locations)

    # The max surface area we could have
    surface_area = len(locations) * 6

    # Subtract one for each neighbouring edge
    for adjacent in adjacents:
        surface_area -= sum(adjacent)

    return surface_area

def calc_adjacents(locations):
    adjacents = []
    for i in range(len(locations)):
        inner = []
        for j in range(len(locations)):
            if j != i:
                inner.append(
                    1 if abs(locations[i][0] - locations[j][0]) +
                         abs(locations[i][1] - locations[j][1]) +
                         abs(locations[i][2] - locations[j][2]) == 1 else 0
                )
        adjacents.append(inner)
    return adjacents


def get_locations(lines):
    return [tuple(int(a.strip()) for a in a.split(",")) for a in lines]


def make_mold(locations):
    """Make a wax mold."""

    # Make the empty mold
    minx, maxx, miny, maxy, minz, maxz = locations[0][0], locations[0][0], locations[0][1], locations[0][1], \
    locations[0][2], locations[0][2]
    for location in locations[1:]:
        minx = min(minx, location[0])
        maxx = max(maxx, location[0])
        miny = min(miny, location[1])
        maxy = max(maxy, location[1])
        minz = min(minz, location[2])
        maxz = max(maxz, location[2])
    mold = [[[0 for x in range((maxx + 2) - (minx - 1))] for y in range((maxy + 2) - (miny - 1))] for z in
            range((maxz + 2) - (minz - 1))]

    # Place the lava drop inside the mold
    for location in locations:
        mold[location[2] + 1 - minz][location[1] + 1 - miny][location[0] + 1 - minx] = 1

    return mold


def fill_mold(mold):
    """Fill the mold with lead."""

    filled = 0
    filled_this_loop = 1
    while filled_this_loop:
        filled_this_loop = 0
        for iz in range(len(mold)):
            for iy in range(len(mold[0])):
                for ix in range(len(mold[0][0])):

                    if iz in (0, len(mold) - 1) or iy in (0, len(mold[0]) - 1) or ix in (0, len(mold[0][0]) - 1):
                        # Fill the perimeter with lead
                        # assert mold[iz][iy][ix] == 0, f"Expected 0 but got {mold[iz][iy][ix]}"
                        try:
                            if mold[iz][iy][ix] == 0:
                                mold[iz][iy][ix] = 2
                                filled_this_loop += 1
                        except IndexError as e:
                            raise e

                    else:
                        # Fill with lead if we are in an air cube and have an adjacent lead cube
                        if mold[iz][iy][ix] == 0 and 2 in (
                                mold[iz - 1][iy][ix],
                                mold[iz + 1][iy][ix],
                                mold[iz][iy - 1][ix],
                                mold[iz][iy + 1][ix],
                                mold[iz][iy][ix - 1],
                                mold[iz][iy][ix + 1]):
                            mold[iz][iy][ix] = 2
                            filled_this_loop += 1

        filled += filled_this_loop

    return mold, filled


def melt_wax(filled_mold):
    """Get the locations of the lead cubes."""
    remains = []
    for iz in range(len(filled_mold)):
        for iy in range(len(filled_mold[0])):
            for ix in range(len(filled_mold[0][0])):
                if filled_mold[iz][iy][ix] == 2:
                    remains.append((ix, iy, iz))

    return remains


def get_outer_area(filled_mold):
    area = 0
    area += 2 * (len(filled_mold) * len(filled_mold[0]))
    area += 2 * (len(filled_mold) * len(filled_mold[0][0]))
    area += 2 * (len(filled_mold[0]) * len(filled_mold[0][0]))
    return area


def two(lines):
    locations = get_locations(lines)

    # Make a mold
    mold = make_mold(locations)

    # Fill it with lead
    filled_mold = fill_mold(mold)[0]

    # Remove the contents
    remains = melt_wax(filled_mold)

    # Get the total surface area of the lead
    surface_area = calc_total_area(remains)

    # Subtract the outer area
    outer_area = get_outer_area(filled_mold)

    return surface_area - outer_area


def main():
    with open("../inputs/day18.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
