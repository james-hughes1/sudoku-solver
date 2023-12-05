import numpy as np
from itertools import permutations, product


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


def refine_valid_templates(grid, valid_templates_list):
    all_templates = list(generate_templates())
    # Loop until the set of valid templates no longer gets smaller
    refined = False
    while not refined:
        refined = True
        for digit_idx in range(9):
            num_valid_templates_digit = len(valid_templates_list[digit_idx])
            template_list_digit = [
                all_templates[template_idx]
                for template_idx in valid_templates_list[digit_idx]
            ]
            # Grid of booleans indicating digits that are fixed across all
            # templates
            fixed_digits = (
                np.sum(template_list_digit, axis=0)
                == num_valid_templates_digit
            )
            # If there is a fixed digit that is not already on the board, add
            # it to the board and refine the set of valid templates for all
            # digits
            if np.sum(fixed_digits) > np.sum(grid == (digit_idx + 1)):
                refined = False
                grid += (digit_idx + 1) * (
                    1 * fixed_digits - 1 * (grid == (digit_idx + 1))
                )
                valid_templates_list = find_valid_templates(grid)
    return grid, valid_templates_list


def solve_backtrack(grid):
    valid_templates_list = find_valid_templates(grid)
    all_templates = list(generate_templates())
    found = False
    valid_template_idx_gen = product(*valid_templates_list)
    while not found:
        template_idx_tuple = next(valid_template_idx_gen)
        template_list = [
            all_templates[template_idx] for template_idx in template_idx_tuple
        ]
        if (np.sum(template_list, axis=0) == 1).all():
            found = True
    solution_templates = np.stack(template_list)
    solution_grid = np.sum(
        np.arange(1, 10).reshape((-1, 1, 1)) * solution_templates, axis=0
    )
    return solution_grid
