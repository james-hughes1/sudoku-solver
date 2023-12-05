import numpy as np


def read_grid(filepath):
    with open(filepath, "r") as file:
        file_lines = file.readlines()
    file_digits = []
    for line in file_lines:
        line_digits = [int(char) for char in line if char.isdigit()]
        if line_digits:
            file_digits.append(line_digits)
    grid = np.array(file_digits)
    return grid


def write_grid(grid, filepath=None):
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
