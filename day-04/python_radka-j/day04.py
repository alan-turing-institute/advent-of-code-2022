# read input file
with open('input04.txt') as f:
    lines = f.read().splitlines()

# part 1 - find number of pairs where one interval fully contains the other
n_contain_pairs = 0
# part 2 - find number of overlapping pairs
n_overlap_pairs = 0

for line in lines:

    # parse to get min/max of both intervals
    min1, max1, min2, max2 = [int(num) for interval in line.split(",") for num in interval.split('-')]

    # check for containment of one interval within the other
    if (min1 >= min2 and max1 <= max2) or (min2 >= min1 and max2 <= max1):
        n_contain_pairs += 1
        
    # check for overlap of the two intervals
    intervals = [[min1, max1], [min2, max2]]
    # sort by min value
    intervals.sort()
    # if min of higher interval is less than max of lower interval 
    # --> they overlap
    if intervals[1][0] <= intervals[0][1]:
        n_overlap_pairs += 1

print("part 1:", n_contain_pairs)
print("part 2:", n_overlap_pairs)