# read the input file
with open('input01.txt') as f:
    lines = f.read().splitlines()

# remove newline, convert to ints and sum blocks
elf_calorie_sums = []
elf_sum = 0
for line in lines:
    if line == "":
        elf_calorie_sums.append(elf_sum)
        elf_sum = 0
    else:
        elf_sum += int(line)

# return top 3
elf_calorie_sums.sort()
print("top:", elf_calorie_sums[-1])
print("top 3:", sum(elf_calorie_sums[-3:]))