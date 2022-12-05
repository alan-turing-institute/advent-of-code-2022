
def parse_input(lines):
    config, moves = [], []

    config_over = False
    for line in lines:

        if not config_over:
            if line == '\n':
                config_over = True
            else:
                config.append(line)

        else:
            moves.append(line)

    num_crates = int(config[-1].split()[-1])

    return config, moves, num_crates


def move_crates_one(crates, num_to_move, from_, to):
    for i in range(num_to_move):
        crate = crates[from_].pop()
        crates[to].append(crate)
    return crates


def move_crates_two(crates, num_to_move, from_, to):
    crate_stack = []  # haha 
    for i in range(num_to_move):
        crate_stack.append(crates[from_].pop())
    crate_stack.reverse()
    for crate in crate_stack:
        crates[to].append(crate)
    return crates


if __name__ == '__main__':
    f = open('input.txt', 'r')
    lines = f.readlines()

    config, moves, num_crates = parse_input(lines)

    crates = [[] for i in range(num_crates)]

    positions = list(range(1, (num_crates)*4, 4))
    for line in config[0:-1]:
        for i, pos in enumerate(positions):
            if line[pos].strip() != '':
                crates[i].insert(0, line[pos])

    for move in moves:
        move = list(move)
        if move[6] == ' ':
            num_to_move = int(move[5])
            from_ = int(move[12]) - 1
            to = int(move[17]) - 1
            crates = move_crates_two(crates, num_to_move, from_, to)

        else:
            num_to_move = int(move[5]+move[6])
            from_ = int(move[13]) - 1
            to = int(move[18]) - 1
            crates = move_crates_two(crates, num_to_move, from_, to)

    soln = ''
    for crate in crates:
        soln += str(crate.pop())

    print(soln)

