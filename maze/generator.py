import random
from typing import Any

N: int = 1
E: int = 2
S: int = 4
W: int = 8
ALL_WALLS: int = 15

DX: dict[int, int] = {E: 1, W: -1, N: 0, S: 0}
DY: dict[int, int] = {E: 0, W: 0, N: -1, S: 1}
OPP: dict[int, int] = {N: S, S: N, E: W, W: E}


def compute_42_cells(width: int, height: int) -> list[tuple[int, int]]:
    """Compute cells that form the '42' pattern obstacle.

    Args:
        width: Maze width in cells.
        height: Maze height in cells.

    Returns:
        List of (x, y) coordinates for the 42 pattern cells.
        Returns empty list if maze is too small.
    """
    MIN_W, MIN_H = 10, 8
    if width < MIN_W or height < MIN_H:
        return []

    cx: int = width // 2
    cy: int = height // 2

    forty_two_offsets: list[tuple[int, int]] = [
        (cx - 3, cy - 2),
        (cx - 1, cy - 2),
        (cx - 3, cy - 1),
        (cx - 1, cy - 1),
        (cx - 3, cy),
        (cx - 2, cy),
        (cx - 1, cy),
        (cx - 1, cy + 1),
        (cx - 1, cy + 2),
        (cx + 1, cy - 2),
        (cx + 2, cy - 2),
        (cx + 3, cy - 2),
        (cx + 3, cy - 1),
        (cx + 1, cy),
        (cx + 2, cy),
        (cx + 3, cy),
        (cx + 1, cy + 1),
        (cx + 1, cy + 2),
        (cx + 2, cy + 2),
        (cx + 3, cy + 2),
    ]

    valid_cells = [
        (x, y)
        for (x, y) in forty_two_offsets
        if 0 <= x < width and 0 <= y < height
    ]

    return valid_cells


def generate_maze_dfs(
    width: int,
    height: int,
    entry: tuple[int, int],
    blocked_cells: list[tuple[int, int]],
    seed: int | None = None,
) -> tuple[list[list[int]], list[tuple[int, int]]]:
    """Generate maze using iterative DFS (Recursive Backtracker).

    Args:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: Starting position (x, y) for generation.
        blocked_cells: List of cells that should remain walled (42 pattern).
        seed: Optional random seed for reproducibility.

    Returns:
        Tuple of (maze grid, generation_stack) where maze grid is a 2D
        list of wall/path bitmasks and generation_stack is the order
        cells were visited.
    """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    maze: list[list[int]] = [
        [ALL_WALLS for _ in range(width)] for _ in range(height)
    ]

    visited: list[list[bool]] = [
        [False for _ in range(width)] for _ in range(height)
    ]
    for bx, by in blocked_cells:  # nice
        visited[by][bx] = True
        maze[by][bx] = ALL_WALLS

    sx, sy = entry
    visited[sy][sx] = True
    stack: list[tuple[int, int]] = [(sx, sy)]
    generation_stack: list[tuple[int, int]] = [(sx, sy)]

    while stack:
        x, y = stack[-1]

        directions = [N, E, S, W]
        random.shuffle(directions)

        moved: bool = False

        for direction in directions:
            nx: int = x + DX[direction]
            ny: int = y + DY[direction]

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if not visited[ny][nx]:
                maze[y][x] ^= direction
                maze[ny][nx] ^= OPP[direction]

                visited[ny][nx] = True
                stack.append((nx, ny))
                generation_stack.append((nx, ny))
                moved = True
                break

        if not moved:
            stack.pop()

    return maze, generation_stack


def make_imperfect(
    canvas: list[list[int]],
    logic: list[list[int]],
    chance: float = 0.30,
) -> None:
    """Add extra passages to make the maze non-perfect (with loops).

    Args:
        canvas: The display canvas to modify in place.
        logic: The maze logic grid to update.
        chance: Probability (0-1) of breaking each wall. Default 0.30.
    """
    h: int = len(canvas)
    w: int = len(canvas[0])

    breakable: list[tuple[int, int, str, tuple[int, int], tuple[int, int]]] = (
        []
    )

    for cy in range(1, h - 1):
        for cx in range(1, w - 1):
            if canvas[cy][cx] != 1:
                continue

            if cy % 2 == 1 and cx % 2 == 0:
                lcx = cx // 2 - 1
                lcy = (cy - 1) // 2
                breakable.append((cx, cy, "V", (lcx, lcy), (lcx + 1, lcy)))

            elif cy % 2 == 0 and cx % 2 == 1:
                lcx = (cx - 1) // 2
                lcy = cy // 2 - 1
                breakable.append((cx, cy, "H", (lcx, lcy), (lcx, lcy + 1)))

    n_break: int = int(len(breakable) * chance)

    for cx, cy, wtype, (ax, ay), (bx, by) in random.sample(breakable, n_break):
        canvas[cy][cx] = 0

        if wtype == "V":
            logic[ay][ax] &= ~E
            logic[by][bx] &= ~W
        else:
            logic[ay][ax] &= ~S
            logic[by][bx] &= ~N


class MazeGenerator:
    """Maze generator using iterative DFS with 42 pattern support."""

    def __init__(self, config: dict[str, Any]):
        """Initialize maze generator with configuration.

        Args:
            config: Dictionary with WIDTH, HEIGHT, ENTRY, EXIT, PERFECT, SEED.
        """
        self.config = config
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]
        self.seed = config.get("SEED")
        self.logic: list[list[int]] = []
        self.canvas: list[list[int]] = []
        self.generation_stack: list[tuple[int, int]] = []
        self.show_42 = True

    def generate(self) -> None:
        """Generate the maze based on configuration.

        Raises:
            ValueError: If entry or exit is within the 42 pattern area.
        """
        blocked = compute_42_cells(self.width, self.height)

        if not blocked:
            self.show_42 = False

        if self.entry in blocked or self.exit in blocked:
            raise ValueError(
                "neither entry nor exit can be within the 42 squares"
            )

        self.logic, self.generation_stack = generate_maze_dfs(
            self.width, self.height, self.entry, blocked, seed=self.seed
        )

        if not self.perfect:
            canvas_tmp = self.convert_to_canvas()
            make_imperfect(canvas_tmp, self.logic)

        self.canvas = self.convert_to_canvas()

    def convert_to_canvas(self) -> list[list[int]]:
        """Convert maze logic to display canvas.

        Returns:
            2D list representing the maze for terminal display,
            where each cell is a constant (CV_WALL, CV_PATH, etc.).
        """
        CV_WALL: int = 1
        CV_PATH: int = 0
        CV_ENTRY: int = 2
        CV_EXIT: int = 3

        width: int = self.width
        height: int = self.height
        cw: int = 2 * width + 1
        ch: int = 2 * height + 1

        canvas: list[list[int]] = [
            [CV_WALL for _ in range(cw)] for _ in range(ch)
        ]

        for logy in range(height):
            for logx in range(width):
                cell: int = self.logic[logy][logx]
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
                if self.logic[logy][logx] == ALL_WALLS:
                    gx = 2 * logx + 1
                    gy = 2 * logy + 1
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            canvas[gy + dy][gx + dx] = 4

        ex, ey = self.entry
        canvas[2 * ey + 1][2 * ex + 1] = CV_ENTRY

        xx, xy = self.exit
        canvas[2 * xy + 1][2 * xx + 1] = CV_EXIT

        return canvas
