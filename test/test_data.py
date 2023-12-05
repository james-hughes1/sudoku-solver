import numpy as np
import os

from src.sudokutools.data import read_grid, write_grid

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
    grid_actual = read_grid("test/test_files/test_grid_valid.txt")
    assert (grid_actual.shape[0] == grid_expected.shape[0]) and (
        grid_actual.shape[1] == grid_expected.shape[1]
    )
    assert (grid_actual == grid_expected).all()


def test_read_grid_accepted():
    grid_actual = read_grid("test/test_files/test_grid_acceptable.txt")
    assert (grid_actual.shape[0] == grid_expected.shape[0]) and (
        grid_actual.shape[1] == grid_expected.shape[1]
    )
    assert (grid_actual == grid_expected).all()


def test_read_grid_invalid_1(capfd):
    read_grid("test/test_files/test_grid_invalid_1.txt")
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid text file: must have exactly 9 digits per"
        " line.\n"
    )


def test_read_grid_invalid_2(capfd):
    read_grid("test/test_files/test_grid_invalid_2.txt")
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid text file: must have exactly 9 lines"
        " that contain digits.\n"
    )


def test_read_grid_non_txt(capfd):
    read_grid("test/test_files/test_grid_non_txt")
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid filepath: should end in .txt extension;"
        " file must be a text file.\n"
    )


def test_read_grid_non_existing(capfd):
    read_grid("test/test_files/test_grid_non_existing.txt")
    captured = capfd.readouterr()
    assert captured.out == "Invalid filepath: text file does not exist.\n"


def test_write_grid_terminal_valid(capfd):
    write_grid(grid_expected)
    captured = capfd.readouterr()
    assert captured.out == str_expected + "\n"


def test_write_grid_file_valid():
    write_grid(grid_expected, "test/test_files/test_write.txt")
    grid_actual = read_grid("test/test_files/test_write.txt")
    os.remove("test/test_files/test_write.txt")
    assert (grid_expected == grid_actual).all()


def test_write_grid_invalid_type(capfd):
    write_grid("hi")
    captured = capfd.readouterr()
    assert captured.out == "Invalid grid: must be a numpy.array."


def test_write_grid_invalid_shape(capfd):
    invalid_shape_grid = np.vstack([grid_expected, np.arange(9)])
    write_grid(invalid_shape_grid)
    captured = capfd.readouterr()
    assert captured.out == "Invalid grid: shape must be (9, 9)."


def test_write_grid_invalid_entries(capfd):
    invalid_entry_grid = 42 * np.ones((9, 9))
    write_grid(invalid_entry_grid)
    captured = capfd.readouterr()
    assert captured.out == "Invalid grid: entries must be integers [0-9]."
