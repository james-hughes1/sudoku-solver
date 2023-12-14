"""!@file solve.py
    @brief Module containing tools to solve sudoku grids.
    @author Created by J. Hughes on 06/12/2023.
"""

from typing import Generator
import numpy as np
from itertools import permutations
from copy import deepcopy


def check_grid_valid(grid: np.ndarray) -> bool:
    """!@brief Checks if grid represents part of a valid solution to a sudoku
    puzzle.
    @details Returns a boolean value indicating whether or not the grid has
    repeated digits in each row, column and 3x3 box.
    @param grid Sudoku grid stored as a np.ndarray.
    @return valid True if grid is valid, False otherwise.
    """
    valid = True
    digit = 1
    while valid and digit < 10:
        digit_grid = grid == digit
        # Check row, column and box condition.
        if (
            (np.sum(digit_grid, axis=0) > 1).any()
            or (np.sum(digit_grid, axis=1) > 1).any()
            or (np.sum(BOX_GRIDS * digit_grid, axis=(1, 2)) > 1).any()
        ):
            valid = False
        digit += 1
    return valid


def generate_templates() -> Generator[np.ndarray, None, None]:
    """!@brief Generator for sudoku solution templates.
    @details This generator yields a 9x9 sudoku grid with just 9 non-zero
    entries, ones,  which represent a possible distribution of any fixed
    digit from 1 to 9 in the solution grid. Iterating through the generator
    produces all 46656 possible templates.
    @return template_grid Digit template generator.
    """
    # Generate nested list of permutations of [0,1,2].
    PERMUTATIONS_012 = [list(perm) for perm in permutations(range(3))]
    for column_by_row in permutations(range(9)):
        box_by_row = [pos // 3 for pos in column_by_row]
        # Check column_by_row corresponds to a valid template.
        if (
            (box_by_row[0:3] in PERMUTATIONS_012)
            and (box_by_row[3:6] in PERMUTATIONS_012)
            and (box_by_row[6:9] in PERMUTATIONS_012)
        ):
            # Yield corresponding template array.
            template_grid = np.zeros((9, 9))
            for row_idx in range(9):
                template_grid[row_idx, column_by_row[row_idx]] = 1
            yield template_grid


# Create helpful global variables to reduce processing times within routines.

# BOX_GRIDS is a 3D array; BOX_GRIDS[i,:,:] yields a grid with 1's indicating
# the cells all belonging to one box.
BOX_GRIDS = np.zeros((9, 9, 9))
for grid_idx in range(9):
    BOX_GRIDS[
        grid_idx,
        3 * (grid_idx // 3) : 3 * (grid_idx // 3) + 3,
        3 * (grid_idx % 3) : 3 * (grid_idx % 3) + 3,
    ] = 1

# OTHER_DIGITS[i] = [1, 2, ..., i-1, i+1, ..., 8, 9]
OTHER_DIGITS = []
for digit in range(1, 10):
    OTHER_DIGITS.append(list(range(1, digit)) + list(range(digit + 1, 10)))

# ALL_TEMPLATES[i] is 9x9 grid array representing the (i)th template.
ALL_TEMPLATES = np.array(list(generate_templates()))


def find_valid_templates(
    grid: np.ndarray, valid_templates_array: np.ndarray = None
) -> np.ndarray:
    """!@brief Produce a list of templates applicable to a sudoku grid.
    @details Given a starting grid of clues, this function iterates through
    all possible templates, and - for each digit - stores the subset of
    templates that are valid given the clues.
    @param grid Sudoku grid stored as a np.ndarray.
    @param valid_templates_array Optional, allows search through a subset of
    all possible templates.
    @return valid_templates_array The subsets of valid templates for each
    digit.
    """
    # If no previous valid templates have been found, simply mark all
    # templates as valid for all digits.
    if valid_templates_array is None:
        valid_templates_array = np.ones((9, 46656))
    for digit in range(1, 10):
        # Produce a bool array length 46656, checking which templates are
        # consistent with (i.e. are a 'superset' of) the clues for that digit.
        digit_grid = 1 * (grid == digit)
        digit_valid_grid = np.any(ALL_TEMPLATES - digit_grid < 0, axis=(1, 2))
        # Produce a similar array, checking which templates do not conflict
        # withany of the other digits currently on the grid.
        other_digit_grid = 1 * ((grid - (digit * digit_grid)) > 0)
        other_digit_valid_grid = np.any(
            ALL_TEMPLATES * other_digit_grid == 1, axis=(1, 2)
        )
        # From the current set of templates marked as valid for this digit,
        # Remove any that (a) aren't consistent with the digit, or (b) aren't
        # consistent with the other clues, or both.
        eliminate_array = (
            digit_valid_grid | other_digit_valid_grid
        ) * valid_templates_array[digit - 1, :]
        valid_templates_array[digit - 1, :] -= eliminate_array
    return valid_templates_array


def refine_valid_templates(
    grid: np.ndarray, valid_templates_array: np.ndarray
) -> np.ndarray:
    """!@brief Filters the array of valid templates given the grid of clues.
    @details Loops through the subset of valid templates for each digit,
    checking if there is a cell on the grid occupied in all templates, but
    not recorded on the grid of clues. If such a location is found, this cell
    is filled in with the digit, and the valid_templates_array regenerated; it
    will be smaller since the grid has fewer empty cells. Continues to loop
    until the valid_templates_array no longer changes.
    @param grid Sudoku grid stored as a np.ndarray.
    @param valid_templates_array Array of subsets of valid templates for each
    digit; an array of this format can be produced using @ref
    find_valid_templates.
    @return valid_templates_array Array of subsets of valid templates for each
    digit.
    """

    # Only run the function if all digits have at least one valid template.
    if not (np.sum(valid_templates_array, axis=1) == 0).any():
        # Loop until the set of valid templates no longer gets smaller.
        refined = False
        while not refined:
            refined = True
            for digit_idx in range(9):
                template_array_digit = ALL_TEMPLATES[
                    np.where(valid_templates_array[digit_idx, :] == 1)[0], :, :
                ]
                # Grid of booleans indicating digits that are fixed across all
                # templates.
                fixed_digits = np.prod(template_array_digit, axis=0, dtype=int)
                # If there is a fixed digit that is not already on the grid,
                # add it to the grid and refine the set of valid templates
                # for all digits.
                if np.sum(fixed_digits) > np.sum(grid == (digit_idx + 1)):
                    refined = False
                    grid += (digit_idx + 1) * (
                        1 * fixed_digits - 1 * (grid == (digit_idx + 1))
                    )
                    valid_templates_array = find_valid_templates(
                        grid, valid_templates_array
                    )
                    if (np.sum(valid_templates_array, axis=1) == 0).any():
                        refined = True
    return grid, valid_templates_array


def solve_backtrack(grid: np.ndarray) -> np.ndarray:
    """!@brief Solves a sudoku using the backtracking method, using templates
    to filter the possible values first.
    @param grid Sudoku grid of clues stored as a np.ndarray.
    @return grid Sudoku grid with all cells containing digits 1-9, so that
    all sudoku rules are satisfied.
    """
    # Check if the start grid clues are valid.
    if not check_grid_valid(grid):
        print(
            "Invalid starting grid, each digit can only appear "
            "once in each row, column and 3x3 box."
        )
        return np.zeros((9, 9)) - 1
    else:
        # Find set of valid templates and refine the set.
        valid_templates_array = find_valid_templates(grid)
        grid, valid_templates_array = refine_valid_templates(
            grid, valid_templates_array
        )
        if (np.sum(valid_templates_array, axis=1) == 0).any():
            print("Unacceptable starting grid, this grid cannot be " "solved.")
            return np.zeros((9, 9)) - 1
        else:
            # Create nested list for candidate digits for each cell, from valid
            # templates, as well as nested list of generators for the candidate
            # digits in each cell.
            possible_digits_array = np.zeros((9, 9, 9))
            possible_digits_list = [
                deepcopy([[].copy() for _ in range(9)]) for _ in range(9)
            ]
            possible_digits_gens = deepcopy(possible_digits_list)
            for digit_idx in range(9):
                template_array_digit = ALL_TEMPLATES[
                    np.where(valid_templates_array[digit_idx, :] == 1)[0], :, :
                ]
                possible_digits_array[digit_idx] += np.sum(
                    template_array_digit, axis=0
                )
            for row_idx in range(9):
                for col_idx in range(9):
                    # Add 1 to make the indices from np.where into digits.
                    possible_digits = (
                        np.where(
                            possible_digits_array[:, row_idx, col_idx] > 0
                        )[0]
                        + 1
                    ).tolist()
                    possible_digits_list[row_idx][col_idx] = possible_digits
                    # Add 0 to the generator; this last iterate indicates all
                    # possible values have been tried.
                    possible_digits_gens[row_idx][col_idx] = (
                        digit for digit in possible_digits + [0]
                    )
            search_positions = np.vstack(np.where(grid == 0))
            num_search_positions = search_positions.shape[1]
            # Don't search if the refinement of templates solves the sudoku,
            # which happens often.
            solved = num_search_positions == 0
            search_idx = 0
            while not solved:
                # Increment the current cell's value by 1.
                current_position = (
                    search_positions[0, search_idx],
                    search_positions[1, search_idx],
                )
                new_value = next(
                    possible_digits_gens[current_position[0]][
                        current_position[1]
                    ]
                )
                grid[current_position] = new_value
                # When you reach the maximum candidate digit, backtrack.
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
                    # If current solution is valid, advance the search to the
                    # next cell.
                    if check_grid_valid(grid):
                        if search_idx == num_search_positions - 1:
                            solved = True
                        else:
                            search_idx += 1
            return grid
