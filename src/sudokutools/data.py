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


def write_grid(grid, filename=None):
    return 0
