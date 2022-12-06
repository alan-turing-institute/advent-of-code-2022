with open("./day_04_input.csv") as f:
    sections = f.read().splitlines()

def check_overlap(first_range, second_range, partial = False):
    contained = 0
    complete = 0
    for i in first_range:
        if i in second_range:
            contained += 1
    if partial:
        if contained > 0:
            complete = 1
        return(complete)
    if contained > 0:
        if contained == len(first_range) or contained == len(second_range):
            complete = 1
    return(complete)

contained_range = []
complete_overlap = 0
partial_overlap = 0

# gives overlap
for row in sections:
    contained_range = 0
    elves = row.split(sep=',')
    seats = [seat.split(sep='-') for seat in elves]
    first_range = range(int(seats[0][0]), int(seats[0][1]) + 1)
    second_range = range(int(seats[1][0]), int(seats[1][1]) + 1)
    complete_overlap += check_overlap(first_range, second_range)
    partial_overlap += check_overlap(first_range, second_range, partial = True)

print("Completely overlapping ranges:", complete_overlap)
print("Partially overlapping ranges:", partial_overlap)
