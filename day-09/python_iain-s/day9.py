import numpy as np

moves = {
    "R": complex(1, 0),
    "L": complex(-1, 0),
    "U": complex(0, 1),
    "D": complex(0, -1),
}

# all_locations = []


def rope(lines, num_segments):
    segments = [complex(0, 0) for _ in range(num_segments)]
    visited = {complex(0, 0)}

    for line in lines:
        direction, steps = line.split(" ")
        move = moves[direction]

        for _ in range(int(steps)):
            # locations = np.zeros((20, 20))

            segments[0] += move
            prior_segment = segments[0]

            # locations[int(segments[0].real), int(segments[0].imag)] = 0.5

            for i in range(1, num_segments):

                to_head = prior_segment - segments[i]

                distance = abs(to_head)
                if distance < 2:
                    # One step away
                    # continue
                    pass

                elif distance == 2:
                    # Two steps vertically or horizontally
                    segments[i] += to_head / 2

                else:
                    # Somewhat diagonal
                    real = to_head.real * (0.5 if abs(to_head.real) == 2 else 1)
                    imag = to_head.imag * (0.5 if abs(to_head.imag) == 2 else 1)
                    segments[i] += complex(real, imag)

                prior_segment = segments[i]
                # if locations[int(segments[i].real),int(segments[i].imag)] < i:
                #     locations[int(segments[i].real), int(segments[i].imag)] = i

            visited.add(segments[i])
            # all_locations.append(locations)

    return len(visited)


def one(lines):
    return rope(lines, 2)


def two(lines):
    return rope(lines, 10)


def main():
    with open("../inputs/day9.txt") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
