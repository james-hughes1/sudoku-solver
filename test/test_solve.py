import numpy as np

from src.sudokutools.solve import (
    generate_templates,
    solve_backtrack,
)


def test_templates():
    count_array = np.zeros((9, 9))
    for template_array in generate_templates():
        count_array += template_array
    count_array_expected = 5184 * np.ones((9, 9))
    assert (count_array == count_array_expected).all()


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
