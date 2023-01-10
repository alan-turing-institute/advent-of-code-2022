import re


def extract_diamonds(sensor_data):
    """A diamond is a centre point and the number of extra pixels of width."""
    return [
        ((sb[0][0], sb[0][1]), abs(sb[0][0] - sb[1][0]) + abs(sb[0][1] - sb[1][1]))
        for sb in sensor_data
    ]


def parse(lines):
    """[((sensorx, sensory), (beaconx, beacony)), ...]"""
    sensor_data = []
    for line in lines:
        matches = re.findall(r"-?\d+", line)
        sensor_data.append(
            ((int(matches[0]), int(matches[1])), (int(matches[2]), int(matches[3])))
        )

    return sensor_data


def slice_at(diamond, rownum):
    """The beginning and end of the sensor area at this row."""
    (x, y), radius = diamond
    radius_at_y = radius - abs(rownum - y)
    return [x - radius_at_y, x + radius_at_y + 1]


def get_ranges(diamonds, rownum):
    """Get the non-overlapping ranges that the beacon cannot be in."""
    # Keep diamonds that have the right y vals
    keep = []
    for (x, y), width in diamonds:
        if y + width >= rownum >= y - width:
            keep.append(((x, y), width))

    # Get the x co-ords of diamonds that intersect with our row
    ranges = []
    for diamond in keep:
        # The width of the diamond at our row
        excluded = slice_at(diamond, rownum)
        if not combine_ranges(ranges, excluded):
            ranges.append(excluded)

    # See whether we can combine any further
    # NB We should probably do this until we get no further combinations
    i = 0
    while i < len(ranges):
        x = ranges.pop(i)
        if not combine_ranges(ranges, x):
            ranges.insert(i, x)
            i += 1

    return ranges


def count_covered(ranges, sensors_beacons, rownum):
    pass


def one(lines, rownum):
    """Part 1."""
    sensors_beacons = parse(lines)
    diamonds = extract_diamonds(sensors_beacons)

    ranges = get_ranges(diamonds, rownum)

    # Get all beacons...
    beacons = set()
    for sb in sensors_beacons:
        beacons.add((sb[1][0], sb[1][1]))

    # ...and count how many are within our ranges
    beacon_count = 0
    for rang in ranges:
        for beacon in beacons:
            if beacon[1] == rownum and rang[0] <= beacon[0] < rang[1]:
                beacon_count += 1

    # Count how many squares are covered by our ranges
    total = 0
    for rang in ranges:
        total += rang[1] - rang[0]
    return total - beacon_count


def combine_ranges(ranges, excluded):
    # Combine ranges to a minimum number
    for rang in ranges:
        # .....#####........
        # .......$$$$$$$....
        # ...........####...
        # if rang[0] < excluded[1] <= rang[1] or rang[0] <= excluded[0] < rang[1]:
        if not (excluded[1] < rang[0] or excluded[0] > rang[1]):
            rang[0] = min(rang[0], excluded[0])
            rang[1] = max(rang[1], excluded[1])
            return True

    return False


def two(lines, xy_max):
    """Part 2."""
    sensors_beacons = parse(lines)
    diamonds = extract_diamonds(sensors_beacons)

    # Get all beacons...
    beacons = set()
    for sb in sensors_beacons:
        beacons.add((sb[1][0], sb[1][1]))

    all_ranges = []
    for y in range(xy_max):
        ranges = get_ranges(diamonds, y)

        # We can drop any ranges that are outside 0-xy_max
        for i in range(len(ranges)):

            if ranges[i][0] < 0:
                ranges[i][0] = 0

            if ranges[i][1] < 0:
                ranges.pop(i)
                continue

            if ranges[i][0] > xy_max:
                ranges.pop(i)
                continue

            if ranges[i][1] > xy_max:
                ranges[i][1] = xy_max

            i += 1

        all_ranges.append(ranges)

    for y in range(xy_max):
        ranges = all_ranges[y]

        if len(ranges) > 1 or ranges[0][0] > 0 or ranges[-1][1] < xy_max:
            break

    ranges = all_ranges[y]
    if len(ranges) == 2:
        x = ranges[0][1]
    elif ranges[0][0] == 1:
        x = 0
    elif ranges[-1][1] == xy_max - 1:
        x = xy_max
    else:
        assert False, ranges

    return (x * 4000000) + y


def main():
    with open("../inputs/day15.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines, 2_000_000))
    print("two:", two(lines, 4_000_000))


if __name__ == "__main__":
    main()
