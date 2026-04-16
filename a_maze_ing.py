import os
import sys
import random
import time

from maze.config_parser import config_parser
from maze.generator import MazeGenerator
from maze.solver import bfs_solve
from maze.display import (
    dmaze_display,
    THEMES,
    toggle_solution,
    animate_generation,
)
from maze.writer import write_output as _write_output


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        settings = config_parser(config_file)
    except (FileNotFoundError, KeyError, ValueError, PermissionError) as err:
        print(f"Config error: {err}")
        sys.exit(1)

    gen = MazeGenerator(settings)

    try:
        gen.generate()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    path = bfs_solve(gen.logic, settings)
    try:
        _write_output(settings, gen.logic, path)
    except PermissionError as err:
        print(f"Write error: {err}")
        sys.exit(1)

    theme = random.randint(0, len(THEMES) - 1)
    solution_shown = False

    os.system("clear")
    dmaze_display(gen.canvas, theme)

    running = True
    while running:
        if not gen.show_42:
            print("\nthe maze is too small to show the 42 pattern.")
        print("\n+--------------------------------------------+")
        print("|                A-Maze-Ing Menu             |")
        print("+--------------------------------------------+")
        print("| 1. Re-generate                             |")
        print("| 2. Show/Hide                               |")
        print("| 3. Change color                            |")
        print("| 4. Animate Generation                      |")
        print("| 5. Domain Expansion - Infinite Tsukuyomi   |")
        print("| 6. Quit                                    |")
        print("+--------------------------------------------+")

        try:
            choice = input("Enter choice (1-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted - goodbye!")
            break

        if choice == "1":
            print("\033[?25l", end="", flush=True)
            os.system("clear")
            settings.pop("SEED", None)

            gen = MazeGenerator(settings)
            gen.generate()
            path = bfs_solve(gen.logic, settings)
            if solution_shown:
                toggle_solution(path, gen, True)
            _write_output(settings, gen.logic, path)

            print("\033[H", end="")
            dmaze_display(gen.canvas, theme)
            print("\033[?25h", end="", flush=True)

        elif choice == "2":
            os.system("clear")
            print("\033[?25l", end="", flush=True)
            try:
                if solution_shown:
                    solution_shown = False
                    print("\033[H", end="")
                    toggle_solution(path, gen, False)
                    print("Solution hidden")
                else:
                    solution_shown = True
                    print("\033[H", end="")
                    toggle_solution(path, gen, True)
                    print("Solution shown")
            except KeyboardInterrupt:
                print("\nBack to menu")
            print("\033[?25h", end="", flush=True)

        elif choice == "3":
            other_themes = [i for i in range(len(THEMES)) if i != theme]
            theme = random.choice(other_themes)
            os.system("clear")
            dmaze_display(gen.canvas, theme)
            print(f"Theme changed to {theme}")

        elif choice == "4":
            try:
                animate_generation(gen, theme)
            except (KeyboardInterrupt, EOFError):
                print("\033[?25h", end="", flush=True)
                print("\033[38;0f", end="")
                print("                                     " +
                      "                                    ", end="")
                continue

        elif choice == "5":
            try:
                os.system("clear")
                print("\033[?25l", end="", flush=True)
                while True:
                    os.system("clear")
                    settings.pop("SEED", None)
                    gen = MazeGenerator(settings)
                    gen.generate()
                    path = bfs_solve(gen.logic, settings)
                    if solution_shown:
                        toggle_solution(path, gen, True)
                    print("\033[H", end="")
                    # dmaze_display(gen.canvas, theme)
                    time.sleep(0.5)
            except KeyboardInterrupt:
                os.system("clear")
                dmaze_display(gen.canvas, theme)
                print("\nYou have escaped the Infinite Tsukuyomi.")
            print("\033[?25h", end="", flush=True)

        elif choice == "6":
            print("Goodbye!")
            running = False

        else:
            os.system("clear")
            print("\033[H", end="")
            dmaze_display(gen.canvas, theme)
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
