
def intersect(list1, list2):
    for item in list1:
        if item in list2:
            return True


if __name__ == '__main__':
    f = open('input.txt', 'r')
    lines = f.readlines()

    score = [0, 0]
    for line in lines:
        line = line.strip()
        elves = line.split(',')

        assg = []
        for nums in elves:
            assg.append([int(num) for num in nums.split('-')])

        if (assg[0][0]<=assg[1][0] and assg[0][1]>=assg[1][1]) or (assg[0][0]>=assg[1][0] and assg[0][1]<=assg[1][1]):
            score[0] += 1

        if intersect(range(assg[0][0], assg[0][1]+1), range(assg[1][0], assg[1][1]+1)):
            score[1] += 1

    print(f'Part one: {score[0]}')
    print(f'Part two: {score[1]}')

