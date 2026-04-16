import random
import sys


def main() -> None:
    """CLI entry point for the maze-run command."""
    if len(sys.argv) < 2:
        print("Usage: maze-run <config_file>")
        sys.exit(1)

    from .config_parser import config_parser
    from .generator import MazeGenerator
    from .solver import bfs_solve
    from .display import dmaze_display, THEMES
    from .writer import write_output

    config_file = sys.argv[1]

    try:
        settings = config_parser(config_file)
    except (FileNotFoundError, KeyError, ValueError) as err:
        print(f"Config error: {err}")
        sys.exit(1)

    gen = MazeGenerator(settings)
    gen.generate()
    path = bfs_solve(gen.logic, settings)
    write_output(settings, gen.logic, path)
    theme = random.randint(0, len(THEMES) - 1)
    dmaze_display(gen.canvas, theme)


if __name__ == "__main__":
    main()
