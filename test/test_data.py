"""!@file test_data.py
@brief Module containing unit tests to validate the functionality of @ref
data.py
@author Created by J. Hughes on 14/12/2023.
"""

import numpy as np
import os

from src.sudokutools.data import read_grid, write_grid

# Initalise an array and string representing the same grid.
grid_expected = np.array(
    [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]
)

str_expected = (
    "000|007|000\n000|009|504\n000|050|169\n---+---+---\n"
    "080|000|305\n075|000|290\n406|000|080\n---+---+---\n"
    "762|080|000\n103|900|000\n000|600|000\n"
)


def test_read_grid_valid():
    """!@brief Check that @ref sudokutools.data.read_grid correctly
    transforms a text file that contains data in the correct format
    into a numpy array of the correct format.
    """
    grid_actual = read_grid("test/test_files/test_grid_valid.txt")
    assert (grid_actual.shape[0] == grid_expected.shape[0]) and (
        grid_actual.shape[1] == grid_expected.shape[1]
    )
    assert (grid_actual == grid_expected).all()


def test_read_grid_accepted():
    """!@brief Check that @ref sudokutools.data.read_grid correctly
    transforms a text file that contains data in an unexpected format
    (but which still uniquely determines a sudoku grid) into a numpy
    array of the correct format.
    """
    grid_actual = read_grid("test/test_files/test_grid_acceptable.txt")
    assert (grid_actual.shape[0] == grid_expected.shape[0]) and (
        grid_actual.shape[1] == grid_expected.shape[1]
    )
    assert (grid_actual == grid_expected).all()


def test_read_grid_invalid_1(capfd):
    """!@brief Check that @ref sudokutools.data.read_grid outputs an
    appropriate error message when one of the text file lines has 10
    digits.
    """
    read_grid("test/test_files/test_grid_invalid_1.txt")
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid text file: must have exactly 9 digits per"
        " line.\n"
    )


def test_read_grid_invalid_2(capfd):
    """!@brief Check that @ref sudokutools.data.read_grid outputs an
    appropriate error message when the text file has 10 lines of
    digits.
    """
    read_grid("test/test_files/test_grid_invalid_2.txt")
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid text file: must have exactly 9 lines"
        " that contain digits.\n"
    )


def test_read_grid_non_txt(capfd):
    """!@brief Check that @ref sudokutools.data.read_grid outputs an
    appropriate error message when the filepath passed does not point
    to a .txt file.
    """
    read_grid("test/test_files/test_grid_non_txt")
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid filepath: should end in .txt extension;"
        " file must be a text file.\n"
    )


def test_read_grid_non_existing(capfd):
    """!@brief Check that @ref sudokutools.data.read_grid outputs an
    appropriate error message when the filepath specified does not
    exist.
    """
    read_grid("test/test_files/test_grid_non_existing.txt")
    captured = capfd.readouterr()
    assert captured.out == "Invalid filepath: text file does not exist.\n"


def test_write_grid_terminal_valid(capfd):
    """!@brief Check that @ref sudokutools.data.write_grid prints the
    correct string when passed a grid array of the correct format and
    datatype.
    """
    write_grid(grid_expected)
    captured = capfd.readouterr()
    assert captured.out == str_expected + "\n"


def test_write_grid_file_valid():
    """!@brief Check that @ref sudokutools.data.write_grid correctly
    writes the grid to a text file when passed a grid array of the
    correct format and datatype.
    @details Note that this relies on @ref sudokutools.data.read_grid
    so therefore, if any of the tests for that function fail, this test
    should be considered failed also.
    """
    write_grid(grid_expected, "test/test_files/test_write.txt")
    grid_actual = read_grid("test/test_files/test_write.txt")
    os.remove("test/test_files/test_write.txt")
    assert (grid_expected == grid_actual).all()


def test_write_grid_invalid_type(capfd):
    """!@brief Check that @ref sudokutools.data.write_grid outputs an
    appropriate error message when the passed grid is not a numpy
    array.
    """
    write_grid("hi")
    captured = capfd.readouterr()
    assert captured.out == "Invalid grid: must be a numpy.array.\n"


def test_write_grid_invalid_shape(capfd):
    """!@brief Check that @ref sudokutools.data.write_grid outputs an
    appropriate error message when the passed grid is a numpy array of
    the wrong shape.
    """
    invalid_shape_grid = np.vstack([grid_expected, np.arange(9)])
    write_grid(invalid_shape_grid)
    captured = capfd.readouterr()
    assert captured.out == "Invalid grid: shape must be (9, 9).\n"


def test_write_grid_invalid_entries(capfd):
    """!@brief Check that @ref sudokutools.data.write_grid outputs an
    appropriate error message when the passed grid is a numpy array
    with entries not in {0, 1, ..., 9}.
    """
    invalid_entry_grid = 42 * np.ones((9, 9))
    write_grid(invalid_entry_grid)
    captured = capfd.readouterr()
    assert captured.out == "Invalid grid: entries must be integers [0-9].\n"
