
def manhattan_distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1]) 


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    sensors = []
    beacons = []
    distances = []
    for line in lines:
        s, b = line.split(":")
        sensor_coords = [int(val.split("=")[-1]) for val in s.split("at ")[-1].split(", ")]
        beacon_coords = [int(val.split("=")[-1]) for val in b.split("at ")[-1].split(", ")]
        sensors.append(sensor_coords)
        beacons.append(beacon_coords)
        distances.append(manhattan_distance(sensor_coords, beacon_coords))
    return sensors, beacons, distances


def merge(intervals):

    # utility functions
    def is_overlap(a, b):
        # consider off by 1 intervals as touching
        return a[0] <= b[1] and b[0] <= a[1] + 1 
    
    def merge_outer(a, b):
        return [min(a[0], b[0]), max(a[1], b[1])]

    # make sure the intervals are sorted by the first element
    sorted_intervals = sorted(intervals)
    # the answer
    merged_intervals = []

    # take the first interval and loop through the rest
    curr_interval = sorted_intervals[0]
    for i, interval in enumerate(sorted_intervals[1:]):
        # for each check if it can be merged - if yes do it
        # and update the current interval to merged
        if is_overlap(curr_interval, interval):
            curr_interval = merge_outer(curr_interval, interval)
        # if not - save the last version of current
        # update current to latest interval
        else:
            merged_intervals.append(curr_interval)
            curr_interval = interval
    
    # append the last interval that saw/created in the loop above
    merged_intervals.append(curr_interval)
    return merged_intervals

    
def check_row(sensors, distances, row):
    intervals = []
    for (s,d) in zip(sensors, distances):
        delta_y = abs(row-s[1])
        if delta_y == d:
            intervals.append([s[0], s[0]])
        elif delta_y < d:
            min_interval = s[0]-(d-delta_y)
            max_interval = s[0]+(d-delta_y)
            intervals.append([min_interval, max_interval])
    return intervals


# Input
sensors, beacons, distances = parse_input("input15.txt")

# Part 1 ================================================================
# row = 10
row = 2000000
intervals = check_row(sensors, distances, row) 
merged_intervals = merge(intervals)
# subtract number of beacons in row
bs = len(set([b[0] for b in beacons if b[1] == row]))
print("part1: ", merged_intervals[0][1] - merged_intervals[0][0] + 1 - bs)

# Part 2 ================================================================
def tuning_freq(x, y):
    return (x * 4000000) + y

# min_val, max_val = 0, 20
min_val, max_val = 0, 4000000

for row in range(min_val, max_val+1):
    intervals = check_row(sensors, distances, row)
    merged_intervals = merge(intervals)
    if len(merged_intervals) > 1:
        y = row
        x = merged_intervals[1][0] - 1

print("part2: ", tuning_freq(x,y))


