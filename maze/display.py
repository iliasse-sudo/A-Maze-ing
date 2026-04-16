import os
import time
import random

from maze.generator import MazeGenerator, compute_42_cells

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


def toggle_solution(
    path: list[tuple[int, int]], gen: MazeGenerator, show: bool
) -> None:

    color = 6 if show else 0
    wall_change_interval = 30

    theme_index = random.randint(0, 2)

    print("\033[?25l", end="", flush=True)
    for i in range(len(path) - 1):
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
            theme_index = random.randint(0, 2)
        print("\033[H", end="")
        dmaze_display(gen.canvas, theme_index)
        time.sleep(0.005)
    print("\033[?25h", end="", flush=True)


def animate_generation(gen: MazeGenerator, theme: int) -> None:
    print("\033[?25l", end="", flush=True)
    os.system("clear")
    blocked_cells = compute_42_cells(gen.width, gen.height)
    blank_canvas = [
        [1 for _ in range(gen.width * 2 + 1)]
        for _ in range(gen.height * 2 + 1)
    ]
    for cx, cy in blocked_cells:
        cv_x = 2 * cx + 1
        cv_y = 2 * cy + 1
        blank_canvas[cv_y][cv_x] = 4
    for logy in range(gen.height):
        for logx in range(gen.width):
            if gen.logic[logy][logx] == 15:
                gx = 2 * logx + 1
                gy = 2 * logy + 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        blank_canvas[gy + dy][gx + dx] = 4
    entry_x, entry_y = gen.entry
    exit_x, exit_y = gen.exit
    blank_canvas[2 * entry_y + 1][2 * entry_x + 1] = 2
    blank_canvas[2 * exit_y + 1][2 * exit_x + 1] = 3
    dmaze_display(blank_canvas, theme)
    time.sleep(0.3)
    path_stack: list = []
    for x, y in gen.generation_stack:
        cv_x = 2 * x + 1
        cv_y = 2 * y + 1
        blank_canvas[cv_y][cv_x] = 0
        if not path_stack:
            path_stack.append((x, y))
        else:
            while path_stack:
                px, py = path_stack[-1]
                if abs(x - px) + abs(y - py) == 1:
                    break
                path_stack.pop()
            px, py = path_stack[-1]
            pcv_x = 2 * px + 1
            pcv_y = 2 * py + 1
            wall_x = (cv_x + pcv_x) // 2
            wall_y = (cv_y + pcv_y) // 2
            blank_canvas[wall_y][wall_x] = 0
            path_stack.append((x, y))
            print("\033[H", end="")
        blank_canvas[2 * entry_y + 1][2 * entry_x + 1] = 2
        blank_canvas[2 * exit_y + 1][2 * exit_x + 1] = 3
        try:
            print("\033[H", end="")
            dmaze_display(blank_canvas, theme)
        except KeyboardInterrupt:
            print("\033[H", end="")
            dmaze_display(blank_canvas, theme)
            print("\033[?25h", end="", flush=True)
            input("Generation paused. Press Enter to continue...")
            print("\033[?25l", end="", flush=True)
            os.system("clear")
        try:
            time.sleep(0.005)
        except KeyboardInterrupt:
            print("\033[H", end="")
            dmaze_display(blank_canvas, theme)
            print("\033[?25h", end="", flush=True)
            input("Generation paused. Press Enter to continue...")
            print("\033[?25l", end="", flush=True)
            os.system("clear")
            continue
    print("\033[?25h", end="", flush=True)
