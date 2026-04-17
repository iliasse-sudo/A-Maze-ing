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

1. **Re-generate** - Generates a completely new maze with a random seed
2. **Show/Hide** - Toggles the solution path display between visible and hidden
3. **Change color** - Cycles through different color themes for walls and paths
4. **Animate Generation** - Watch the maze being carved out step-by-step in real-time
5. **Domain Expansion - Infinite Tsukuyomi** - Displays a continuously regenerating animated maze
6. **Quit** - Exits the program

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
- **itemlali**: Project architecture and code structure, configuration parsing, error handling, display system, color theming
- **ibaya**: Algorithm research (BFS pathfinding, DFS maze generation), maze generator and canvas logic implementation, debugging, display assistance and animations

### Planning and Evolution
1. **Foundation phase**: itemlali established the project structure, config parsing, and basic display framework. Learned from peer examples and 42 resources.
2. **Algorithm phase**: ibaya researched and implemented maze generation (iterative DFS) and BFS pathfinding. Built the core logic/canvas system.
3. **Integration phase**: Combined algorithms with display. Added error handling, refined output format.
4. **Enhancement phase**: itemlali added color themes and theming system. ibaya implemented generation animation and visual polish.
5. **Final polish**: Both worked on debugging, interactive menu features, and refinements.

### Project Evolution
- **Basic logic**: Numbers displayed on screen representing maze cells
- **Letter representation**: Transitioned to letters for better visualization
- **Path drawing**: Added solution path visualization
- **Color and animation**: Full colored themes, animated generation, interactive features
- **Final result**: Robust, lively animated maze with good design and interactive features

### What worked well
- Clean separation between modules (generator, solver, display, writer)
- Iterative DFS avoided recursion limit issues
- Strong collaboration between algorithmic and UI development
- Color themes and animation added as bonus features

### What could be improved
- More maze algorithm options (Prim's, Kruskal's)
- Better error messages for edge cases

### Tools used
- Python standard library only (no external dependencies)
- Git for version control
- flake8 and mypy for code quality
