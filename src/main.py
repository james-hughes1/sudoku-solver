import numpy as np
from sudokutools.solve import (
    refine_valid_templates,
    find_valid_templates,
)

grid = np.array(
    [
        [1, 0, 3, 4, 5, 6, 7, 8, 0],
        [4, 5, 6, 0, 0, 9, 1, 2, 3],
        [0, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 0, 5, 0, 7, 8, 9, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 9, 1, 2, 3, 0, 5, 0, 7],
        [0, 4, 0, 6, 7, 8, 9, 1, 0],
        [6, 7, 8, 9, 1, 0, 0, 4, 5],
        [9, 0, 2, 3, 4, 5, 6, 7, 8],
    ]
)

print(find_valid_templates(grid))
print(refine_valid_templates(grid, find_valid_templates(grid)))
