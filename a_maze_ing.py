import os
import sys
import random
import time

from maze.config_parser import config_parser
from maze.generator import MazeGenerator
from maze.solver import bfs_solve
from maze.display import dmaze_display, THEMES
from maze.writer import write_output as _write_output


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        settings = config_parser(config_file)
    except (FileNotFoundError, KeyError, ValueError) as err:
        print(f"Config error: {err}")
        sys.exit(1)

    gen = MazeGenerator(settings)

    try:
        gen.generate()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    path = bfs_solve(gen.logic, settings)
    _write_output(settings, gen.logic, path)

    theme = random.randint(0, len(THEMES) - 1)
    solution_shown = False

    os.system("clear")
    dmaze_display(gen.canvas, theme)

    running = True
    while running:
        print("\n+--------------------+")
        print("| A-Maze-Ing Menu    |")
        print("+--------------------+")
        print("| 1. Re-generate     |")
        print("| 2. Show/Hide       |")
        print("| 3. Change color    |")
        print("| 4. Quit            |")
        print("+--------------------+")
        try:
            choice = input("Enter choice (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted - goodbye!")
            break

        if choice == "1":
            print("\nRegenerating...")
            settings.pop("SEED", None)
            solution_shown = False

            gen = MazeGenerator(settings)
            gen.generate()
            path = bfs_solve(gen.logic, settings)
            _write_output(settings, gen.logic, path)

            os.system("clear")
            dmaze_display(gen.canvas, theme)

        elif choice == "2":
            if solution_shown:
                solution_shown = False
                os.system("clear")
                dmaze_display(gen.canvas, theme)
                print("Solution hidden")
            else:
                solution_shown = True
                canvas_copy = [row[:] for row in gen.canvas]

                for i in range(len(path) - 1):
                    cx, cy = path[i + 1]
                    px, py = path[i]

                    print(cx, cy, px, py)

                    dx = cx - px
                    dy = cy - py

                    gx = 2 * px + 1
                    gy = 2 * py + 1

                    if canvas_copy[gy][gx] not in (2, 3):
                        canvas_copy[gy][gx] = 6

                    if dx == 1:  # im moving east
                        print("going east")
                        canvas_copy[gy][gx + 1] = 6
                    elif dx == -1:  # im moving west
                        print("going west")
                        canvas_copy[gy][gx - 1] = 6

                    if dy == 1:  # im moving south
                        print("going southj")
                        canvas_copy[gy + 1][gx] = 6
                    elif dy == -1:  # im moving north
                        print("going north")
                        canvas_copy[gy - 1][gx] = 6

                os.system("clear")
                dmaze_display(canvas_copy, theme)
                print("Solution shown")

        elif choice == "3":
            other_themes = [i for i in range(len(THEMES)) if i != theme]
            theme = random.choice(other_themes)
            os.system("clear")
            dmaze_display(gen.canvas, theme)
            print(f"Theme changed to {theme}")

        elif choice == "4":
            print("Goodbye!")
            running = False

        else:
            os.system("clear")
            dmaze_display(gen.canvas, theme)
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
