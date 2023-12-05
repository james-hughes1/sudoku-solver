import numpy as np
from sudokutools.solve import solve_backtrack

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


print(solve_backtrack(start_grid_minimal))
