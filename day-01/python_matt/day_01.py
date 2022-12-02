with open("day_01_input.txt") as f:
    calories = f.read().split("\n\n")

total_per_elf = sorted([sum(map(int, x))
                       for x in [y.split() for y in calories]])

print("Top elf:", total_per_elf[-1:])
print("Top three total calories:", sum(total_per_elf[-3:]))
