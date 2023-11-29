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


def solve_backtrack(grid):
    return grid
