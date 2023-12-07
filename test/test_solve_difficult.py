import numpy as np
from src.sudokutools.solve import solve_backtrack

# Medium sudoku challenge, with solution
start_grid_medium = np.array(
    [
        [1, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 5, 0, 7, 0, 9, 0, 2, 0],
        [0, 0, 0, 0, 2, 0, 4, 0, 0],
        [2, 3, 0, 5, 0, 7, 0, 0, 1],
        [5, 0, 0, 0, 0, 0, 0, 0, 4],
        [8, 9, 0, 2, 0, 4, 0, 6, 7],
        [0, 0, 5, 0, 7, 0, 0, 0, 0],
        [0, 7, 0, 9, 1, 2, 0, 4, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 8],
    ]
)

solution_grid_expected_1 = np.array(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
)

# Example from
# https://en.wikipedia.org/wiki/Mathematics_of_Sudoku#Sudokus_with_Few_Clues
start_grid_minimal = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 3],
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0],
        [4, 0, 1, 6, 0, 0, 0, 0, 0],
        [0, 0, 7, 1, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 4, 0],
        [0, 3, 0, 9, 1, 0, 0, 0, 0],
    ]
)

solution_grid_expected_2 = np.array(
    [
        [7, 4, 5, 3, 6, 8, 9, 1, 2],
        [8, 1, 9, 5, 7, 2, 4, 6, 3],
        [3, 6, 2, 4, 9, 1, 8, 5, 7],
        [6, 9, 3, 8, 2, 4, 5, 7, 1],
        [4, 2, 1, 6, 5, 7, 3, 9, 8],
        [5, 8, 7, 1, 3, 9, 6, 2, 4],
        [1, 5, 8, 7, 4, 6, 2, 3, 9],
        [9, 7, 6, 2, 8, 3, 1, 4, 5],
        [2, 3, 4, 9, 1, 5, 7, 8, 6],
    ]
)

# Example from https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
start_grid_antagonist = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9],
    ]
)

solution_grid_expected_3 = np.array(
    [
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [2, 4, 6, 1, 7, 3, 9, 8, 5],
        [3, 5, 1, 9, 2, 8, 7, 4, 6],
        [1, 2, 8, 5, 3, 7, 6, 9, 4],
        [6, 3, 4, 8, 9, 2, 1, 5, 7],
        [7, 9, 5, 4, 6, 1, 8, 3, 2],
        [5, 1, 9, 2, 8, 6, 4, 7, 3],
        [4, 7, 2, 3, 1, 9, 5, 6, 8],
        [8, 6, 3, 7, 4, 5, 2, 1, 9],
    ]
)


def test_solve_backtrack_medium():
    solution_grid = solve_backtrack(start_grid_medium)
    assert (solution_grid == solution_grid_expected_1).all()


def test_solve_backtrack_minimal():
    solution_grid = solve_backtrack(start_grid_minimal)
    assert (solution_grid == solution_grid_expected_2).all()


def test_solve_backtrack_antagonist():
    solution_grid = solve_backtrack(start_grid_antagonist)
    assert (solution_grid == solution_grid_expected_3).all()
