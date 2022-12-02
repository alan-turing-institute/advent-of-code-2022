with open("day_02_input.txt") as f:
    elf_code = f.read().splitlines()

wins = [["A", "Y"], ["B", "Z"], ["C", "X"]]
draws = [["A", "X"], ["B", "Y"], ["C", "Z"]]

# Helper function
def shape_score(shape):
    shape_score = []
    match shape:
        case "X":
            shape_score = 1
        case "Y":
            shape_score = 2
        case "Z":
            shape_score = 3
    return (shape_score)

# Strategy one
def score_one(plays):
    final_score = []
    final_score = shape_score(plays[1])
    if plays in wins:
        final_score += 6
    elif plays in draws:
        final_score += 3
    return (final_score)

# Strategy two
def score_two(plays):
    final_score = []
    match plays[1]:
        case "X":
            final_score = 0
            match plays[0]:
                case "A":
                    plays[1] = "Z"
                case "B":
                    plays[1] = "X"
                case "C":
                    plays[1] = "Y"
        case "Y":
            final_score = 3
            match plays[0]:
                case "A":
                    plays[1] = "X"
                case "B":
                    plays[1] = "Y"
                case "C":
                    plays[1] = "Z"
        case "Z":
            final_score = 6
            match plays[0]:
                case "A":
                    plays[1] = "Y"
                case "B":
                    plays[1] = "Z"
                case "C":
                    plays[1] = "X"
    final_score += shape_score(plays[1])
    return (final_score)

elf_code = [x.split() for x in elf_code]
strategy_one = sum([score_one(y) for y in elf_code])
strategy_two = sum([score_two(y) for y in elf_code])

# Totals
print("Strategy one score:", strategy_one)
print("Strategy two score:", strategy_two)
