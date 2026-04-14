CV_WALL: int = 1
CV_PATH: int = 0
CV_ENTRY: int = 2
CV_EXIT: int = 3
CV_42BG: int = 4
CV_42WALL: int = 5
CV_SOL: int = 6

THEMES: list[tuple[str, str, str]] = [
    ("   ", " ", "EE"),
    ("WW", "..", "XX"),
    ("WW", "..", "XX"),

]

PATH_EMOJI: str = "  "
THUMB_EMOJI: str = "▓▓"


def dmaze_display(canvas: list[list[int]], theme_index: int) -> None:
    wall_e, entry_e, exit_e = THEMES[theme_index]

    for row in canvas:
        line: str = ""
        for cell in row:
            if cell == CV_PATH:
                line += PATH_EMOJI
            elif cell == CV_WALL:
                line += wall_e
            elif cell == CV_ENTRY:
                line += entry_e
            elif cell == CV_EXIT:
                line += exit_e
            elif cell == CV_42BG:
                line += THUMB_EMOJI
            elif cell == CV_42WALL:
                line += wall_e
            elif cell == CV_SOL:
                line += entry_e
        print(line)


def convert_to_canvas(
    logic: list[list[int]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> list[list[int]]:
    ALL_WALLS: int = 15
    E: int = 2
    W: int = 8
    N: int = 1
    S: int = 4

    cw: int = 2 * width + 1
    ch: int = 2 * height + 1

    canvas: list[list[int]] = [
        [CV_WALL for _ in range(cw)]
        for _ in range(ch)
    ]

    for logy in range(height):
        for logx in range(width):
            cell: int = logic[logy][logx]
            gx: int = 2 * logx + 1
            gy: int = 2 * logy + 1

            canvas[gy][gx] = CV_PATH

            if not (cell & E):
                canvas[gy][gx + 1] = CV_PATH
            if not (cell & W):
                canvas[gy][gx - 1] = CV_PATH
            if not (cell & N):
                canvas[gy - 1][gx] = CV_PATH
            if not (cell & S):
                canvas[gy + 1][gx] = CV_PATH

    for logy in range(height):
        for logx in range(width):
            if logic[logy][logx] == ALL_WALLS:
                gx = 2 * logx + 1
                gy = 2 * logy + 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        canvas[gy + dy][gx + dx] = CV_42BG

    ex, ey = entry
    canvas[2 * ey + 1][2 * ex + 1] = CV_ENTRY

    xx, xy = exit
    canvas[2 * xy + 1][2 * xx + 1] = CV_EXIT

    return canvas
