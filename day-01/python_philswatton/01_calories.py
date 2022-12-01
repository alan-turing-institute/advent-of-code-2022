from argparse import ArgumentParser

# Usage: python 01_calories.py input_file_path
def get_input_file_path() -> str:
    parser = ArgumentParser(description="Calculate elf with the most calories")
    parser.add_argument("input_file_path") # required (positional) arguments
    args = parser.parse_args()
    return args.input_file_path

# Main
def main():
    # Get file path
    file_path = get_input_file_path()
    
    # Iterate over input file, calculate list of elf total calories
    elfList = [0]
    iterator = 0
    with open(file_path) as inputFile:
        for line in inputFile.readlines():
            if line == "\n":
                iterator += 1 #assuming only one new line between elves
                elfList.append(0)
            else:
                elfList[iterator] = elfList[iterator] + int(line)
    
    # Function that returns index of elfList sorted by calories
    def sortIndex(list: list[int], rev: bool=True) -> list[int]:
        index = range(len(list))
        sortedIndex = sorted(index, key=lambda i: list[i], reverse=rev)
        return sortedIndex
    
    # Got top 3 indices
    top3Elves = sortIndex(elfList)[:3]
    
    # Part 1: Print top elf calories to console
    print("Elf " + str(top3Elves[0] + 1) + " is carrying " + str(elfList[top3Elves[0]]) + " calories")
    
    # Part 2: Print top 3 elves combined calories to console
    print("The top three elves are carrying " + str(sum([elfList[index] for index in top3Elves])) + " calories together")

# Run
if __name__ == "__main__":
    main()