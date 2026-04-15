CV_WALL: int = 1
CV_PATH: int = 0
CV_ENTRY: int = 2
CV_EXIT: int = 3
CV_42BG: int = 4
CV_42WALL: int = 5
CV_SOL: int = 6

THEMES: list[tuple[str, str, str]] = [
    ("\033[31m▓▓\033[0m", "\033[34m▓▓\033[0m", "XX"),
    ("\033[32m▓▓\033[0m", "\033[35m▓▓\033[0m", "XX"),
    ("\033[33m▓▓\033[0m", "\033[36m▓▓\033[0m", "XX"),

]

EMPTY_PATH: str = "  "
SOL: str = "▓▓"
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
                line += entry_e
            elif cell == CV_EXIT:
                line += exit_e
            elif cell == CV_42BG:
                line += _42_PATTERN
            elif cell == CV_42WALL:
                line += wall_e
            elif cell == CV_SOL:
                line += entry_e
        print(line)
