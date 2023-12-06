import sys
from sudokutools.solve import solve_backtrack
from sudokutools.data import read_grid, write_grid


def solve_sudoku():
    input_file = sys.argv[1]
    start_grid = read_grid(input_file)
    if not (start_grid == 0).all():
        solution_grid = solve_backtrack(start_grid)
        if not (solution_grid == 0).all():
            write_grid(solution_grid)


solve_sudoku()
