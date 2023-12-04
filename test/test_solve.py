import numpy as np

from src.sudokutools.solve import (
    generate_templates,
    solve_backtrack,
    find_valid_templates,
)


def test_templates():
    count_array = np.zeros((9, 9))
    for template_array in generate_templates():
        count_array += template_array
    count_array_expected = 5184 * np.ones((9, 9))
    assert (count_array == count_array_expected).all()


def test_valid_templates():
    start_grid = np.array(
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
    valid_templates_list = find_valid_templates(start_grid)
    for template_idx_list in valid_templates_list:
        assert len(template_idx_list) == 1


def test_solve_backtrack_valid():
    start_grid = np.array(
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 0],
            [4, 5, 6, 7, 8, 9, 1, 0, 3],
            [7, 8, 9, 1, 2, 3, 0, 5, 6],
            [2, 3, 4, 5, 6, 0, 8, 9, 1],
            [5, 6, 7, 8, 0, 1, 2, 3, 4],
            [8, 9, 1, 0, 3, 4, 5, 6, 7],
            [3, 4, 0, 6, 7, 8, 9, 1, 2],
            [6, 0, 8, 9, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
        ]
    )
    solution_grid = solve_backtrack(start_grid)
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
    assert (solution_grid == solution_grid_expected).all()
