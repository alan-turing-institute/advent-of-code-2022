
import string

# read input file
with open('input03.txt') as f:
    lines = f.read().splitlines()

# each time has a value
# a to z --> 1 to 26
# A to Z --> 27 to 52
values = {char:i+1 for i,char in enumerate(string.ascii_letters)}

# part 1 - find common item between two compartments
# get sum of item values
total = 0

for line in lines:

    # each half of line are items in a compartment --> split
    split = len(line) // 2
    compartment1 = line[:split]
    compartment2 = line[split:]

    # find common item in both compartments and get value
    common_item = next(iter(set(compartment1).intersection(compartment2)))
    total += values[common_item]

print(total)

# part 2 - find common item between each 3 consecutive lines 
# get sum of item values
total2 = 0

# split lines into groups of 3
groups = [lines[i:i+3] for i in range(0, len(lines), 3)] 
for group in groups:
    common_item = next(iter(set(group[0]).intersection(set(group[1])).intersection(set(group[2]))))
    total2 += values[common_item]

print(total2)