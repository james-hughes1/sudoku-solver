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


def test_solve_backtrack_invalid(capfd):
    start_grid_invalid = start_grid_easy.copy()
    start_grid_invalid[0, 0] = 2
    solve_backtrack(start_grid_invalid)
    captured = capfd.readouterr()
    assert (
        captured.out == "Invalid starting grid, each digit can only appear "
        "once in each row, column and 3x3 box."
    )


def test_solve_backtrack_few_clues(capfd):
    start_grid = np.zeros((9, 9))
    start_grid[0, 0] = 1
    solution_grid = solve_backtrack(start_grid)
    # Check that the solution is valid
    solve = True
    for element_idx in range(9):
        _, counts = np.unique(
            solution_grid[element_idx, :], return_counts=True
        )
        if (counts[1:] > 1).any():
            solve = False
        _, counts = np.unique(
            solution_grid[:, element_idx], return_counts=True
        )
        if (counts[1:] > 1).any():
            solve = False
        _, counts = np.unique(
            solution_grid[
                3 * (element_idx // 3) : 3 * (element_idx // 3) + 3,
                3 * (element_idx % 3) : 3 * (element_idx % 3) + 3,
            ],
            return_counts=True,
        )
        if (counts[1:] > 1).any():
            solve = False
    if (solution_grid == 0).any():
        solve = False
    assert solve
