"""!@file data.py
    @brief Module containing tools to read .txt files as sudoku grids stored
    as np.ndarray, and conversely output stored sudoku grids as .txt files.
    @author Created by J. Hughes on 06/12/2023.
"""


import numpy as np


def read_grid(filepath: str) -> np.ndarray:
    """!@brief Read in a sudoku grid from a .txt file.
    @details Converts the given .txt file contents to a np.ndarray which
    represents the 9x9 sudoku grid. Expects a file in which exactly 9 of
    the lines contain exactly 9 digit characters each, with no digits on
    other lines.
    @param filepath Specified filepath. Must end with .txt.
    @returns grid Sudoku grid stored as a np.ndarray.
    """
    if filepath[-4:] != ".txt":
        print(
            "Invalid filepath: should end in .txt extension;"
            " file must be a text file."
        )
        return np.zeros((9, 9)) - 1
    else:
        try:
            with open(filepath, "r") as file:
                file_lines = file.readlines()
        except FileNotFoundError:
            print("Invalid filepath: text file does not exist.")
            return np.zeros((9, 9)) - 1
        # If filepath exists and points to .txt file, create a nested list of
        # the digits in each line.
        else:
            file_digits = []
            for line in file_lines:
                line_digits = [int(char) for char in line if char.isdigit()]
                if line_digits:
                    file_digits.append(line_digits)
            # Check that there are 9 rows of 9 digits.
            if len(file_digits) != 9:
                print(
                    "Invalid text file: must have exactly 9 lines that "
                    "contain digits."
                )
                return np.zeros((9, 9)) - 1
            elif [len(digits_list) for digits_list in file_digits] != [9] * 9:
                print(
                    "Invalid text file: must have exactly 9 digits per "
                    "line."
                )
                return np.zeros((9, 9)) - 1
            else:
                grid = np.array(file_digits)
                return grid


def write_grid(grid: np.ndarray, filepath: str = None):
    """!@brief Write a sudoku grid out to the terminal or to a specified text
    file.
    @details Converts the np.ndarray to a representative string with added
    symbols for readability. If no filepath specified the string is
    outputted to the terminal, otherwise it is stored in the specified
    .txt file location.
    @param grid Sudoku grid stored as a np.ndarray.
    """
    # Check grid is a numpy array shape (9, 9), with only single digit integer
    # entries.
    if not isinstance(grid, np.ndarray):
        print("Invalid grid: must be a numpy.array.")
    elif grid.shape != (9, 9):
        print("Invalid grid: shape must be (9, 9).")
    elif not (np.isin(grid, np.arange(10))).all():
        print("Invalid grid: entries must be integers [0-9].")
    else:
        # Create the string representing the grid, and output.
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
