import string
with open("day_03_input.txt") as f:
    rucksacks = f.read().split()

def split_list(x):
    chunk_size = len(x) // 2
    return (x[0:chunk_size], x[chunk_size:])

def convert_to_num(x):
    return (string.ascii_letters.index(x) + 1)

def chunk_list(x, n):
    return ([x[i:i + n] for i in range(0, len(x), n)])

def rucksack_priority(x):
    comp_one, comp_two = split_list(x)
    common = list(set(comp_one) & set(comp_two))[0]
    return(convert_to_num(common))

def group_priority(group):
    elfx, elfy, elfz = [set(elf) for elf in group]
    return(convert_to_num(list(elfx & elfy & elfz)[0]))

print("Total rucksack priorities:", sum([rucksack_priority(rucksack) for rucksack in rucksacks]))
print("Total group priorities:", sum([group_priority(group) for group in chunk_list(rucksacks, 3)]))
