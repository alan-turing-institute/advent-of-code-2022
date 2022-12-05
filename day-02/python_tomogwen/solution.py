
def rename(inp):
    if inp == 'A' or inp == 'X':
        return 0
    elif inp == 'B' or inp == 'Y':
        return 1
    elif inp == 'C' or inp == 'Z':
        return 2


def score_part_one(opponent, you):
    points = [[4, 1, 7],
              [8, 5, 2],
              [3, 9, 6]]
    return points[you][opponent]


def score_part_two(opponent, result):
    points = [[3, 4, 8],
              [1, 5, 9],
              [2, 6, 7]]
    return points[opponent][result]


if __name__ == '__main__':
    f = open('input.txt', 'r')
    lines = f.readlines()

    score = [0, 0]
    for line in lines:
        line = line.strip().split(' ')
        opponent = rename(line[0])
        you = rename(line[1])

        score[0] += score_part_one(opponent, you)
        score[1] += score_part_two(opponent, you)

    print(f'Part one: {score[0]}')
    print(f'Part two: {score[1]}')



