from asciimatics.screen import Screen
from time import sleep

from day14 import build_cave, get_paths, CaveTwo

import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=600)

def animate(screen):
    with open("./examples/day14.txt", encoding="utf-8") as f:
        content = [line.rstrip() for line in f]

    # cave = build_cave(content)
    cave = CaveTwo(get_paths(content))

    while True:
        screen.print_at(len(cave.static_sand), 0, 0)

        try:
            cave.take_turn()
        except IndexError as e:
            sleep(100)
        for i, line in enumerate(str(cave.contents).split("\n")):
            screen.print_at(line, 0, i + 2)

        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return

        screen.refresh()
        sleep(.5)


Screen.wrapper(animate)
