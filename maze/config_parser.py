from typing import Any


def config_parser(filename: str) -> dict[str, Any]:
    raw: dict[str, str] = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    raw[key.strip().upper()] = value.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file '{filename}' not found!")
    except PermissionError:
        raise PermissionError(f"Permission denied reading '{filename}'!")

    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"]
    for key in mandatory:
        if key not in raw:
            raise KeyError(f"Mandatory key '{key}' is missing from config!")

    perfect_str = raw["PERFECT"].strip().title()
    if perfect_str not in ("True", "False"):
        val = raw["PERFECT"]
        raise ValueError(f"PERFECT must be 'True' or 'False', got '{val}'")
    perfect_bool: bool = perfect_str == "True"

    def parse_coords(raw_str: str, label: str) -> tuple[int, int]:
        try:
            parts = raw_str.split(",")
            if len(parts) != 2:
                raise ValueError
            return (int(parts[0].strip()), int(parts[1].strip()))
        except ValueError:
            raise ValueError(f"{label} must be 'x,y', got '{raw_str}'")

    entry: tuple[int, int] = parse_coords(raw["ENTRY"], "ENTRY")
    exit_pos: tuple[int, int] = parse_coords(raw["EXIT"], "EXIT")

    try:
        width: int = int(raw["WIDTH"])
        height: int = int(raw["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be integers")

    if width <= 0 or height <= 0:
        raise ValueError(f"WIDTH and HEIGHT must be > 0, got {width}x{height}")

    for label, (cx, cy) in [("ENTRY", entry), ("EXIT", exit_pos)]:
        if not (0 <= cx < width and 0 <= cy < height):
            raise ValueError(f"{label} ({cx},{cy}) outside {width}x{height}")

    if entry == exit_pos:
        raise ValueError("ENTRY and EXIT cannot be the same cell!")

    BLOCKED = [
        "config.txt", "README.md", "pyproject.toml", "setup.py",
        "a_maze_ing.py", "Makefile", ".gitignore"
    ]

    output_file = raw["OUTPUT_FILE"].strip()

    if output_file.startswith("/") or ".." in output_file:
        raise ValueError("Invalid OUTPUT_FILE: path traversal not allowed")

    if output_file in BLOCKED:
        raise ValueError(f"OUTPUT_FILE '{output_file}' is protected")

    settings: dict[str, Any] = {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry,
        "EXIT": exit_pos,
        "PERFECT": perfect_bool,
        "OUTPUT_FILE": raw["OUTPUT_FILE"],
    }

    if "SEED" in raw:
        try:
            settings["SEED"] = int(raw["SEED"])
        except ValueError:
            raise ValueError(f"SEED must be an integer, got '{raw['SEED']}'")

    return settings
