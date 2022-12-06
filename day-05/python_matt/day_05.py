def parse_moves(lines):
    moves = []
    for line in lines:
        if 'move' in line:
            new_line = [int(x) for x in line.split(' ') if x.isdigit()]
            moves.append(new_line)
    return (moves)

def parse_stacks(lines):
    stacks = []
    for line in lines:
        if line == '':
            break
        stacks.append(line)
    # Work out which elements actually contain useful values from the last row
    indices = [ind for ind, val in enumerate(stacks[-1]) if val.isdigit()]
    # Get rid of the last row, then pick out only the useful elements
    stacks.pop()
    stacks[:] = [[x[i] for i in indices] for x in stacks]
    # Transpose the lists so each list is now one stack
    stacks[:] = [list(x) for x in zip(*stacks)]
    # Lose the empty values
    final_stacks = []
    for _, s in enumerate(stacks):
        final_stacks.append([crate for crate in s if crate != ' '])
    return (final_stacks)

def move_crates(stack, n=0, start=0, to=0, keep_order=False):
    if keep_order:
        stack[to - 1][:0] = stack[start - 1][0:n]
        del stack[start - 1][0:n]
    else:
        for i in range(0, n):
            stack[to - 1].insert(0, stack[start - 1].pop(0))
    return (stack)

def get_string(stacks):
    return(''.join([crate[0] for crate in stacks]))

def stack_crates(moves, stacks, keep_order):
    for x in moves:
        stacks = move_crates(stacks, x[0], x[1], x[2], keep_order)
    return(get_string(stacks))
    
def main():
    
    with open("./day_05_input.txt") as f:
        cargo = f.read().splitlines()
    
    moves = parse_moves(cargo)
    stacks = parse_stacks(cargo)
    print("First rules:", stack_crates(moves, stacks, keep_order = False))
    print("Second rules:", stack_crates(moves, stacks, keep_order = True))

if __name__ == "__main__":
    main()
    