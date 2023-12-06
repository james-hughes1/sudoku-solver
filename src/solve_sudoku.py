"""!@mainpage Sudoku Solver Package
    @brief Package which provides tools for solving sudoku grids, and dealing
    with I/O via .txt files.
    @section Terminology
    With the aim of consistent documentation, there are a few terms that I
    define here that are relevant to sudoku and are used throughout the
    documentation; these terms are by no means conventional within the study
    of sudoku:
    - Grid: The 9x9 orthogonal board on which the sudoku game is played.
    - Cell: The individual squares on the grid where the numbers are written.
    - Box: One of the nine mutually exclusive square subsets of the grid, each
    consisting of nine cells in a 3x3 arrangement.
    - Valid: Refers to a grid whose cells contain numbers satisfying the rules
    of sudoku, namely:
        - All cells are either empty (represented by 0 in the code) or contain
        exactly one of the digits 1-9.
        - Every digit 1-9 appears at most in each row.
        - Every digit 1-9 appears at most in each column.
        - Every digit 1-9 appears at most in each box.
    In other words, any valid grid can be made from a solved grid, with any
    number of cells made empty.
    - Solved: Refers to a valid grid with no empty cells.
    The last two terms relate to the solving algorithm and come from
    https://en.wikipedia.org/wiki/Sudoku_solving_algorithms.
    - Template: A possible arrangement of nine copies of a chosen digit across
    the board, which is valid.
    - Backtracking: A brute-force solving approach which involves filling in
    each grid cell iteratively, looping through the possible values for the
    latest cell:
        - When all possible values have been tried, we return to the previous
        cell.
        - When a possible value leads to a valid grid, we advance to the next
        cell.
        - We stop when we reach a solved grid.
    @section Modules
    @subsection Solve
    This module provides the backend for finding the solution to the starting
    grid of clues. There are three functions that deal with generating the
    valid templates for each digit given the clues provided. The @ref
    check_grid_valid function is a useful helper function which is used in
    multiple other routines. The main function here is the @ref
    solve_backtrack function which generates the valid templates for each
    digit, and then searches for the valid solution with the backtracking
    approach.
    @subsection Data
    This module enables convenient switching between the text file or string
    representation of the grid, and the np.ndarray type representation which
    is used in the solve module.
    @author Created by J. Hughes on 06/12/2023.
"""


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
