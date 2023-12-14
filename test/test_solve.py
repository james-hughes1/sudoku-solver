import numpy as np

from src.sudokutools.solve import (
    check_grid_valid,
    generate_templates,
    find_valid_templates,
    refine_valid_templates,
    solve_backtrack,
)

# Initialise some basic sudoku grids, and a solution grid.
start_grid_easy = np.array(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 0],
        [4, 5, 6, 7, 0, 9, 1, 2, 3],
        [0, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 0, 7, 8, 9, 1],
        [0, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 0, 5, 6, 7],
        [0, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 0, 3, 4, 5],
        [9, 0, 2, 3, 4, 5, 6, 7, 8],
    ]
)

# This grid has the same solution as above
start_grid_refine_test = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 5, 6, 7, 0, 9, 1, 2, 3],
        [0, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 0, 7, 8, 9, 1],
        [0, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 0, 5, 6, 7],
        [0, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 0, 3, 4, 5],
        [9, 0, 2, 3, 4, 5, 6, 7, 8],
    ]
)

start_grid_invalid = start_grid_easy.copy()
start_grid_invalid[0, 0] = 2

solution_grid_expected = np.array(
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

start_grid_no_solution_1 = np.array(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
    ]
)

start_grid_no_solution_2 = np.array(
    [
        [1, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 2, 0],
        [0, 1, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 1, 0],
        [2, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)


def test_check_valid_true():
    assert check_grid_valid(start_grid_easy)


def test_check_valid_false():
    assert not check_grid_valid(start_grid_invalid)


def test_templates():
    # This test uses the fact that there are 46656 templates, and any given
    # cell on the grid is filled in 1 out of 9 of these templates, i.e.
    # 5184.
    count_array = np.zeros((9, 9))
    for template_array in generate_templates():
        count_array += template_array
    count_array_expected = 5184 * np.ones((9, 9))
    assert (count_array == count_array_expected).all()


def test_find_valid_templates():
    valid_templates_array = find_valid_templates(start_grid_easy)
    assert (np.sum(valid_templates_array, axis=1) == np.ones(9)).all()


def test_refine_valid_templates():
    # This test takes a starting grid which is almost trivial, such that
    # the grid should be completely `solved by refine_valid_templates`.
    valid_templates_array = find_valid_templates(start_grid_refine_test)
    solution_grid, refined_valid_templates_array = refine_valid_templates(
        start_grid_refine_test, valid_templates_array
    )
    assert (solution_grid == solution_grid_expected).all()
    assert (np.sum(valid_templates_array, axis=1) == np.ones(9)).all()


def test_solve_backtrack_easy():
    solution_grid = solve_backtrack(start_grid_easy)
    assert (solution_grid == solution_grid_expected).all()


def test_solve_backtrack_invalid(capfd):
    solve_backtrack(start_grid_invalid)
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid starting grid, each digit can only appear "
        "once in each row, column and 3x3 box.\n"
    )


def test_solve_backtrack_no_solution_1(capfd):
    solve_backtrack(start_grid_no_solution_1)
    captured = capfd.readouterr()
    assert (
        captured.out == "Unacceptable starting grid, this grid cannot be "
        "solved.\n"
    )


def test_solve_backtrack_no_solution_2(capfd):
    solve_backtrack(start_grid_no_solution_2)
    captured = capfd.readouterr()
    assert (
        captured.out == "Unacceptable starting grid, this grid cannot be "
        "solved.\n"
    )


def test_solve_backtrack_few_clues(capfd):
    start_grid = np.zeros((9, 9))
    start_grid[0, 0] = 1
    solution_grid = solve_backtrack(start_grid)
    assert (solution_grid != 0).all() and check_grid_valid(solution_grid)
