from collections import deque
from typing import Any

N: int = 1
E: int = 2
S: int = 4
W: int = 8

DX: dict[int, int] = {N: 0, E: 1, S: 0, W: -1}
DY: dict[int, int] = {N: -1, E: 0, S: 1, W: 0}


def bfs_solve(
    logic: list[list[int]],
    settings: dict[str, Any],
) -> list[tuple[int, int]]:
    start: tuple[int, int] = settings["ENTRY"]
    goal: tuple[int, int] = settings["EXIT"]
    width: int = settings["WIDTH"]
    height: int = settings["HEIGHT"]

    if start == goal:
        return [start]

    queue: deque[tuple[int, int, list[tuple[int, int]]]] = deque()
    queue.append((start[0], start[1], [start]))

    visited: set[tuple[int, int]] = {start}

    steps_explored: int = 0

    while queue:
        x, y, path = queue.popleft()
        steps_explored += 1

        if (x, y) == goal:
            return path

        for direction in [N, E, S, W]:
            if (logic[y][x] & direction) == 0:
                nx: int = x + DX[direction]
                ny: int = y + DY[direction]

                if (
                    0 <= nx < width
                    and 0 <= ny < height
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(nx, ny)]))

    return []
