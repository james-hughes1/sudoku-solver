import numpy as np

from src.sudokutools.solve import (
    generate_templates,
    find_valid_templates,
    solve_backtrack,
)


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

start_grid_medium = np.array(
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

start_grid_hard = np.array(
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

solution_grid_expected_2 = np.array(
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


def test_templates():
    count_array = np.zeros((9, 9))
    for template_array in generate_templates():
        count_array += template_array
    count_array_expected = 5184 * np.ones((9, 9))
    assert (count_array == count_array_expected).all()


def test_valid_templates():
    valid_templates_list = find_valid_templates(start_grid_easy)
    for template_idx_list in valid_templates_list:
        assert len(template_idx_list) == 1


def test_solve_backtrack_easy():
    solution_grid = solve_backtrack(start_grid_easy)
    assert (solution_grid == solution_grid_expected_1).all()


def test_solve_backtrack_medium():
    solution_grid = solve_backtrack(start_grid_medium)
    assert (solution_grid == solution_grid_expected_1).all()


def test_solve_backtrack_hard():
    solution_grid = solve_backtrack(start_grid_hard)
    assert (solution_grid == solution_grid_expected_2).all()
