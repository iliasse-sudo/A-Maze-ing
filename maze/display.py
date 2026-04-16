import time
import random
import os

CV_WALL: int = 1
CV_PATH: int = 0
CV_ENTRY: int = 2
CV_EXIT: int = 3
CV_42BG: int = 4
CV_42WALL: int = 5
CV_SOL: int = 6


TEAL_GREEN = "\x1b[48;2;0;109;91m \x1b[0m\x1b[48;2;0;109;91m \x1b[0m"

THEMES: list[tuple[str, str, str]] = [
    ("\033[31m▓▓\033[0m", "\033[34m▓▓\033[0m", "XX"),
    ("\033[32m▓▓\033[0m", "\033[35m▓▓\033[0m", "XX"),
    ("\033[33m▓▓\033[0m", TEAL_GREEN, "XX"),
]

EMPTY_PATH: str = "  "
SOL: str = "ZZ"
_42_PATTERN: str = "\033[36m▓▓\033[0m"


def dmaze_display(canvas: list[list[int]], theme_index: int) -> None:
    wall_e, entry_e, exit_e = THEMES[theme_index]

    for row in canvas:
        line: str = ""
        for cell in row:
            if cell == CV_PATH:
                line += EMPTY_PATH
            elif cell == CV_WALL:
                line += wall_e
            elif cell == CV_ENTRY:
                line += "EE"
            elif cell == CV_EXIT:
                line += exit_e
            elif cell == CV_42BG:
                line += _42_PATTERN
            elif cell == CV_42WALL:
                line += wall_e
            elif cell == CV_SOL:
                line += entry_e
        print(line)

def toggle_solution(path, gen, show):

    color = 6 if show else 0
    wall_change_interval = 30

    theme_index = random.randint(0, 2)

    for i in range(len(path) - 1):
        os.system("clear")
        cx, cy = path[i + 1]
        px, py = path[i]

        dx = cx - px
        dy = cy - py

        gx = 2 * px + 1
        gy = 2 * py + 1

        if gen.canvas[gy][gx] not in (2, 3):
            gen.canvas[gy][gx] = color

        if dx == 1:  # im moving east
            gen.canvas[gy][gx + 1] = color
        elif dx == -1:  # im moving west
            gen.canvas[gy][gx - 1] = color

        if dy == 1:  # im moving south
            gen.canvas[gy + 1][gx] = color
        elif dy == -1:  # im moving north
            gen.canvas[gy - 1][gx] = color
        if i > 0 and i % wall_change_interval == 0:
            theme_index = random.randint(0,2)
        dmaze_display(gen.canvas, theme_index)
        time.sleep(.005)