from typing import Any


def write_output(
    settings: dict[str, Any],
    logic: list[list[int]],
    path: list[tuple[int, int]],
) -> None:
    output_path: str = settings["OUTPUT_FILE"]
    entry: tuple[int, int] = settings["ENTRY"]
    exit_: tuple[int, int] = settings["EXIT"]

    try:
        with open(output_path, "w") as f:
            for row in logic:
                for cell in row:
                    f.write(hex(cell)[2].upper())
                f.write("\n")

            f.write(f"\n{entry[0]},{entry[1]}\n")
            f.write(f"{exit_[0]},{exit_[1]}\n")

            for i in range(len(path) - 1):
                x, y = path[i]
                nx, ny = path[i + 1]
                dx: int = nx - x
                dy: int = ny - y
                if dx == 1:
                    f.write("E")
                elif dx == -1:
                    f.write("W")
                elif dy == 1:
                    f.write("S")
                elif dy == -1:
                    f.write("N")
            f.write("\n")
    except PermissionError:
        raise PermissionError(f"Permission denied writing to '{output_path}'!")
