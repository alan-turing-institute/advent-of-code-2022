import numpy as np


def read_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def move_head(head_pos, direction):
    if direction == "R":
        head_pos[1] += 1
    elif direction == "L":
        head_pos[1] -= 1
    elif direction == "U":
        head_pos[0] -= 1
    elif direction == "D":
        head_pos[0] += 1 
    return head_pos
    

def calc_distance(head_pos, tail_pos):
    return np.array(head_pos) - np.array(tail_pos)


def move_tail(head_pos, tail_pos):

    # [row_dist, col_dist]
    dist = calc_distance(head_pos, tail_pos)

    # if touching do, nothing
    touching = np.array([
        [0, 0], [1, 1], [-1, -1], [0, 1], [0, -1], 
        [1, 0],[-1, 0], [1, -1], [-1, 1]
        ])
    if np.any(np.all(dist == touching, axis=1)):
        return tail_pos
    else:
        # move by 0, 1 or -1 in both horizontal and vertical
        # depending on distance between the two knots
        tail_pos[0] += np.sign(dist[0])
        tail_pos[1] += np.sign(dist[1])
        return tail_pos


def main(n_tails, instructions):

    # set up some initial state
    H_pos = [4, 0]
    tails = []
    for i in range(n_tails):
        tails.append([4, 0])
    # keep track of visited locations of last knot
    visited = [tuple(tails[-1])]

    # move all knots according to instructions
    for instruct in instructions:
        direction, amount = instruct.split()
        for i in range(int(amount)):
            H_pos = move_head(H_pos, direction)
            prev_t = H_pos
            for i in range(n_tails):
                tails[i] = move_tail(prev_t, tails[i])
                prev_t = tails[i]
            visited.append(tuple(tails[-1]))
    return len(set(visited))


if __name__ == "__main__":

    instructions = read_input("input09.txt")

    part1 = main(1, instructions)
    part2 = main(9, instructions)

    print("part1", part1)
    print("part2", part2)