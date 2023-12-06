import numpy as np


def read_grid(filepath: str) -> np.ndarray:
    if filepath[-4:] != ".txt":
        print(
            "Invalid filepath: should end in .txt extension;"
            " file must be a text file."
        )
        return np.zeros((9, 9))
    else:
        try:
            with open(filepath, "r") as file:
                file_lines = file.readlines()
        except FileNotFoundError:
            print("Invalid filepath: text file does not exist.")
            return np.zeros((9, 9))
        else:
            file_digits = []
            for line in file_lines:
                line_digits = [int(char) for char in line if char.isdigit()]
                if line_digits:
                    file_digits.append(line_digits)
            if len(file_digits) != 9:
                print(
                    "Invalid text file: must have exactly 9 lines that "
                    "contain digits."
                )
                return np.zeros((9, 9))
            elif [len(digits_list) for digits_list in file_digits] != [9] * 9:
                print(
                    "Invalid text file: must have exactly 9 digits per "
                    "line."
                )
                return np.zeros((9, 9))
            else:
                grid = np.array(file_digits)
                return grid


def write_grid(grid: np.ndarray, filepath: str = None):
    if not isinstance(grid, np.ndarray):
        print("Invalid grid: must be a numpy.array.")
    elif grid.shape != (9, 9):
        print("Invalid grid: shape must be (9, 9).")
    elif not (np.isin(grid, np.arange(10))).all():
        print("Invalid grid: entries must be integers [0-9].")
    else:
        grid_str = ""
        for row_idx in range(9):
            row_str = ""
            for col_idx in range(9):
                row_str += str(grid[row_idx][col_idx])
                if col_idx in [2, 5]:
                    row_str += "|"
            row_str += "\n"
            grid_str += row_str
            if row_idx in [2, 5]:
                grid_str += "---+---+---\n"
        if filepath is None:
            print(grid_str)
        else:
            with open(filepath, "w") as file:
                file.write(grid_str)
