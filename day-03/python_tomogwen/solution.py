
def intersect(list1, list2):
    for item in list1:
        if item in list2:
            return item


def triple_int(tl):
    for item in tl[0]:
        if item in tl[1] and item in tl[2]:
            return item


def value(item):
    asc = ord(item)
    if 65 <= asc <= 90:
        return asc - 38
    else:
        return asc - 96


if __name__ == '__main__':
    f = open('input.txt', 'r')
    lines = f.readlines()
    stripped_lines = []

    score = 0
    for line in lines:
        line = line.strip()
        stripped_lines.append(line)
        half_idx = int(len(line)/2)
        compart = [line[0:half_idx], line[half_idx:len(line)]]

        item = intersect(compart[0], compart[1])
        score += value(item)

    print(f'Part one: {score}')

    score = 0
    for i in range(0, len(lines), 3):
        three_lines = stripped_lines[i:i+3]
        item = triple_int(three_lines)
        score += value(item)

    print(f'Part two: {score}')
