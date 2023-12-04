import numpy as np
from itertools import permutations


def generate_templates():
    # Generate nested list of permutations of [0,1,2]
    PERMUTATIONS_012 = [list(perm) for perm in permutations(range(3))]
    for column_by_row in permutations(range(9)):
        box_by_row = [pos // 3 for pos in column_by_row]
        # Check column_by_row corresponds to a valid template
        if (
            (box_by_row[0:3] in PERMUTATIONS_012)
            and (box_by_row[3:6] in PERMUTATIONS_012)
            and (box_by_row[6:9] in PERMUTATIONS_012)
        ):
            # Yield corresponding template array
            template_grid = np.zeros((9, 9))
            for row_idx in range(9):
                template_grid[row_idx, column_by_row[row_idx]] = 1
            yield template_grid


def find_valid_templates(grid):
    # Create indicator arrays for each 3x3 box in the grid
    BOX_GRIDS = np.zeros((9, 9, 9))
    for grid_idx in range(9):
        BOX_GRIDS[
            grid_idx,
            3 * (grid_idx // 3) : 3 * (grid_idx // 3) + 3,
            3 * (grid_idx % 3) : 3 * (grid_idx % 3) + 3,
        ] = 1
    # Create a nested list of digits 1-9, each list has a unique digit removed
    OTHER_DIGITS = []
    for digit in range(1, 10):
        OTHER_DIGITS.append(list(range(1, digit)) + list(range(digit + 1, 10)))
    valid_templates_list = [[], [], [], [], [], [], [], [], []]
    for template_idx, template in enumerate(generate_templates()):
        for digit in range(1, 10):
            valid = True
            # Check that none of the template positions are in the same row,
            # column or box as one of the clues of `digit`, and that they
            # don't coincide with the position of a different digit.
            digit_grid = (grid == digit) + (template == 1)
            if (
                (np.sum(digit_grid, axis=0) > 1).any()
                or (np.sum(digit_grid, axis=1) > 1).any()
                or (np.sum(BOX_GRIDS * digit_grid, axis=(1, 2)) > 1).any()
                or (np.isin(grid, OTHER_DIGITS[digit - 1]) * template).any()
            ):
                valid = False
            if valid:
                valid_templates_list[digit - 1].append(template_idx)
    return valid_templates_list


def solve_backtrack(grid):
    return grid
