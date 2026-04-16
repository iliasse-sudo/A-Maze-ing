<em>This project has been created as part of the 42 curriculum by itemlali, ibaya.</em>

## Description

A maze generator and solver with configurable algorithms and interactive terminal display.
Generates random mazes using the iterative Recursive Backtracker (DFS) algorithm with
a '42' pattern obstacle, finds the shortest path using BFS, and displays the
result in the terminal with interchangeable color themes.

## Instructions

### Run

```bash
python3 a_maze_ing.py config.txt
```

### Interactive Menu

1. Re-generate a new maze
2. Show/Hide solution path
3. Change color theme
4. Quit

## Configuration File Format

```
WIDTH=20
HEIGHT=14
ENTRY=0,0
EXIT=19,13
PERFECT=True
OUTPUT_FILE=maze.txt
# Optional: SEED=42
```

- WIDTH/HEIGHT: Must be integers >= 2 (>= 10x8 for '42' pattern)
- ENTRY/EXIT: Must be in 'x,y' format within bounds
- PERFECT: True (single path) or False (multiple routes)
- OUTPUT_FILE: Path to write the maze output

## Maze Generation Algorithm

Uses iterative Recursive Backtracker (DFS):

1. Start at entry cell, mark visited, push to stack
2. While stack not empty: find unvisited neighbors, carve random passage, push
3. If dead end: pop from stack (backtrack)
4. Result is a perfect maze (single path between any two cells)

### Why Iterative DFS?

- Avoids Python recursion limit (stack overflow on large mazes)
- Easy to implement and debug
- Produces long, winding passages
- Straightforward to understand

The '42' pattern is centered in the maze for mazes >= 10x8, containing
impassable cells that must be routed around.

## Resources

- Maze Generation Algorithm: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- BFS Pathfinding: https://www.redblobgames.com/pathfinding/a-star/introduction.html

AI was used for code review and explanation of complex algorithms (BFS pathfinding, maze generation logic).

## Reusable Maze Module

The `maze/` package can be imported:

```python
from maze import config_parser, MazeGenerator, bfs_solve

config = config_parser("config.txt")
gen = MazeGenerator(config)
gen.generate()
path = bfs_solve(gen.logic, config)
```

## Team and Project Management

### Roles
- **itemlali**: Primary development, maze generator algorithm implementation
- **ibaya**: Display system, configuration parsing, testing

### Planning
- Initial phase: Core maze generation using iterative DFS
- Development phase: Added BFS solver, color themes, configuration system
- Testing phase: Bug fixes, animation features, performance optimization

### What worked well
- Clean separation between modules (generator, solver, display, writer)
- Iterative DFS avoided recursion limit issues
- Color themes and animation added as bonus features

### What could be improved
- More maze algorithm options (Prim's, Kruskal's)
- Better error messages for edge cases

### Tools used
- Python standard library only (no external dependencies)
- Git for version control
- flake8 and mypy for code quality
