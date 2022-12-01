def argmax(list_):
    argmax, max_ = 0, list_[0]
    for idx, val in enumerate(list_):
        if val > max_:
            max_ = val
            argmax = idx
    return argmax, max_


def argmin(list_):
    argmin, min_ = 0, list_[0]
    for idx, val in enumerate(list_):
        if val < min_:
            min_ = val
            argmin = idx
    return argmin, min_


if __name__ == '__main__':
    f = open('input.txt', 'r')
    lines = f.readlines()

    totals = []
    running_total = 0

    for line in lines:
        line = line.strip()
        if line != '':
            running_total += int(line)
        else:
            totals.append(running_total)
            running_total = 0

    argmax, max_ = argmax(totals)
    print(f'Challenge 1: max = {max_}')


    top3 = [0, 0, 0]
    for total in totals:
        argmin_, min_ = argmin(top3)
        if total > min_:
            top3[argmin_] = total

    total = 0
    for val in top3:
        total += val
    print(f'Challenge 2: total = {total}')
