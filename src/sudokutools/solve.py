"""!@file solve.py
@brief Module containing tools to solve sudoku grids.

@author Created by J. hughes on 06/12/2023.
"""

from typing import Generator
import numpy as np
from itertools import permutations
from copy import deepcopy


def generate_templates() -> Generator[np.ndarray, None, None]:
    """!@brief Generator for sudoku solution templates.
    @details This generator yields a 9x9 sudoku grid with just 9 non-zero
    entries, ones,  which represent a possible distribution of any fixed
    digit from 1 to 9 in the solution grid. Iterating through the generator
    produces all 46656 possible templates.
    @return template_grid Digit template generator.
    """
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


def find_valid_templates(grid: np.ndarray) -> list[list[int]]:
    """!@brief Produce a list of templates applicable to a sudoku grid.
    @details Given a starting grid of clues, this function iterates through
    all possible templates, and - for each digit - stores the subset of
    templates that are valid given the clues.
    @param grid Sudoku grid stored as a np.ndarray.
    @return valid_templates_list The subsets of valid templates for each digit.
    """
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


def refine_valid_templates(
    grid: np.ndarray, valid_templates_list: list[list[int]]
) -> list[list[int]]:
    """!@brief Filters the list of valid templates given the grid of clues.
    @details Loops through the subset of valid templates for each digit,
    checking if there is a cell on the grid occupied in all templates, but
    not recorded on the grid of clues. If such a location is found, this cell
    is filled in with the digit, and the valid_templates_list regenerated; it
    will be smaller since the grid has fewer empty cells. Continues to loop
    until the valid_templates_list no longer changes.
    @param grid Sudoku grid stored as a np.ndarray.
    @param valid_templates_list List of subsets of valid templates for each
    digit; a list of this format can be produced using @ref
    find_valid_templates.
    @return valid_templates_list List of subsets of valid templates for each
    digit.
    """

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


def check_grid_valid(grid: np.ndarray) -> bool:
    """!@brief Checks if grid represents part of a valid solution to a sudoku
    puzzle.
    @details Returns a boolean value indicating whether or not the grid has
    repeated digits in each row, column and 3x3 box.
    @param grid Sudoku grid stored as a np.ndarray.
    @return valid True if grid is valid, False otherwise.
    """
    valid = True
    for element_idx in range(9):
        _, counts = np.unique(grid[element_idx, :], return_counts=True)
        if (counts[1:] > 1).any():
            valid = False
        _, counts = np.unique(grid[:, element_idx], return_counts=True)
        if (counts[1:] > 1).any():
            valid = False
        _, counts = np.unique(
            grid[
                3 * (element_idx // 3) : 3 * (element_idx // 3) + 3,
                3 * (element_idx % 3) : 3 * (element_idx % 3) + 3,
            ],
            return_counts=True,
        )
        if (counts[1:] > 1).any():
            valid = False
    return valid


def solve_backtrack(grid: np.ndarray) -> np.ndarray:
    """!@brief Solves a sudoku using the backtracking method, using templates
    to filter the possible values first.
    @param grid Sudoku grid of clues stored as a np.ndarray.
    @return grid Sudoku grid with all cells containing digits 1-9, so that
    all sudoku rules are satisfied.
    """
    # Check if the start grid clues are valid
    if not check_grid_valid(grid):
        print(
            "Invalid starting grid, each digit can only appear "
            "once in each row, column and 3x3 box."
        )
        return np.zeros((9, 9))
    else:
        # Find set of valid templates and refine the set
        valid_templates_list = find_valid_templates(grid)
        grid, valid_templates_list = refine_valid_templates(
            grid, valid_templates_list
        )
        all_templates = list(generate_templates())
        solved = False
        # Create nested list for candidate digits for each cell, from valid
        # templates
        possible_digits_array = np.zeros((9, 9, 9))
        possible_digits_list = [
            deepcopy([[].copy() for _ in range(9)]) for _ in range(9)
        ]
        for digit_idx in range(9):
            for template_idx in valid_templates_list[digit_idx]:
                possible_digits_array[digit_idx] += all_templates[template_idx]
            for row_idx in range(9):
                for col_idx in range(9):
                    if possible_digits_array[digit_idx][row_idx][col_idx] > 0:
                        possible_digits_list[row_idx][col_idx].append(
                            digit_idx + 1
                        )
        possible_digits_gens = [
            [
                (
                    possible_digits
                    for possible_digits in possible_digits_list[row_idx][
                        col_idx
                    ]
                    + [0]
                )
                for col_idx in range(9)
            ]
            for row_idx in range(9)
        ]
        search_positions = np.vstack(np.where(grid == 0))
        num_search_positions = search_positions.shape[1]
        # Don't search if the refinement of templates solves the sudoku, which
        # happens often
        if num_search_positions == 0:
            solved = True
        search_idx = 0
        while not solved:
            current_position = (
                search_positions[0, search_idx],
                search_positions[1, search_idx],
            )
            new_value = next(
                possible_digits_gens[current_position[0]][current_position[1]]
            )
            grid[current_position] = new_value
            # When you reach the maximum candidate digit, backtrack
            if new_value == 0:
                possible_digits_gens[current_position[0]][
                    current_position[1]
                ] = (
                    possible_digits
                    for possible_digits in possible_digits_list[
                        current_position[0]
                    ][current_position[1]]
                    + [0]
                )
                search_idx -= 1
                assert search_idx >= 0
            else:
                # If current solution is valid, advance the search to the next
                # cell
                if check_grid_valid(grid):
                    if search_idx == num_search_positions - 1:
                        solved = True
                    else:
                        search_idx += 1
        return grid
