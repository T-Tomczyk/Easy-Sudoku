import copy
import sudoku_patterns
import random

# Validates if given value may be legally inserted somewhere in the row.
# Required for the solve_grid function.
def value_valid_in_row(checked_value, row_index, grid):
    for value in grid[row_index]:
        if value == checked_value:
            return False
    return True
    
# Validates if given value may be legally inserted somewhere in the column.
# Required for the solve_grid function.
def value_valid_in_col(checked_value, col_index, grid):
    # Create a temporary list containing all values from selected column.
    column = []
    for i in range(9):
        column.append(grid[i][col_index])

    # Check if check_value is already in the list or not. Return accordingly.
    for value in column:
        if value == checked_value:
            return False
    return True

# Validates if given value may be legally inserted somewhere in the region
# (any 1 of 9 internal 3x3 grids).
# Required for the solve_grid function.
def value_valid_in_region(checked_value, row_index, col_index, grid):
    # Find region_index based on row_index and col_index.
    if row_index < 3:
        if col_index < 3:
            region_index = 0
        elif col_index < 6:
            region_index = 1
        else:
            region_index = 2
    elif row_index < 6:
        if col_index < 3:
            region_index = 3
        elif col_index < 6:
            region_index = 4
        else:
            region_index = 5
    else:
        if col_index < 3:
            region_index = 6
        elif col_index < 6:
            region_index = 7
        else:
            region_index = 8

    # Create a temporary list containing all values from selected region.
    region = []
    for i1 in range(3):
        for i2 in range(3):
            region.append(grid[region_index//3*3+i1][region_index%3*3+i2])

    # Check if checked_value is already in the list or not. Return accordingly.
    for value in region:
        if value == checked_value:
            return False
    return True

# Return a solved sudoku grid. Only works with easy sudokus (solvable without using
# advanced techniques).
def solve_grid(grid):
    grid = copy.deepcopy(grid)

    # Loop as long as sudoku is not solved.
    sudoku_solved = False
    while not sudoku_solved:

        # Convert every empty square in a grid to a list of
        # all legal values that may be entered in this square.
        # 1. Loop through every square of the grid.
        for row_index in range(9):
            for col_index in range(9):

                # 2. Check if square is empty.
                if grid[row_index][col_index] == 0:

                    # 3. If so, change it to a list of all potential solutions.
                    grid[row_index][col_index] = []
                    for potential_solution in range(1, 10):
                        if (
                            value_valid_in_row(potential_solution, row_index, grid) and
                            value_valid_in_col(potential_solution, col_index, grid) and
                            value_valid_in_region(potential_solution, row_index, col_index, grid)
                        ):
                            grid[row_index][col_index].append(potential_solution)

        # Change every single-element list to a single integer (the correct solution)
        # and every multiple-element list back to 0.
        for row_index in range(9):
            for col_index in range(9):
                if type(grid[row_index][col_index]) == list:
                    if len(grid[row_index][col_index]) == 1:
                        grid[row_index][col_index] = grid[row_index][col_index][0]
                    else:
                        grid[row_index][col_index] = 0

        # 1. Assume sudoku is solved.
        # 2. Check if there are any empty squares left.
        # 3. If so, break assumption and continue the loop.
        sudoku_solved = True
        for row in grid:
            for value in row:
                if value == 0:
                    sudoku_solved = False
    return grid

# Generates a random sudoku puzzle using sudoku patterns from the sudoku_patterns.py file.
# Increases all given numbers by a random value from 0 to 8 (where e.g. 9+1 produces 1, 8+4=3 etc.),
# and rotates entire grid by 0, 90, 180 or 270 degrees.
# Only generates easy sudokus (solvable without using advanced techniques).
def generate_grid():
    # Select random pattern from suudoku_patterns file.
    pattern_index = random.randrange(len(sudoku_patterns.patterns))

    # Assign this pattern to the grid variable.
    grid = sudoku_patterns.patterns[pattern_index]

    # Select number by which all numbers in the grid will be shifted.
    delta = random.randrange(9)

    # Modify the grid according to delta.
    for row_index in range(9):
        for col_index in range(9):
            if grid[row_index][col_index] != 0:
                grid[row_index][col_index] += delta
                if grid[row_index][col_index] > 9:
                    grid[row_index][col_index] -= 9
    return grid
    
# Returns given grid in a form of a human-readable string.
def pretty_print(grid):
    result = ''

    def print_3_rows(start, stop):
        nonlocal result

        for row_index in range(start,stop):
            for col_index in range(0,9,3):
                result += str(grid[row_index][col_index]) + ' '
                result += str(grid[row_index][col_index+1]) + ' '
                result += str(grid[row_index][col_index+2]) + '  '
            if row_index != 8:
                result += '\n'
        if stop != 9:
            result += '\n'

    print_3_rows(0,3)
    print_3_rows(3,6)
    print_3_rows(6,9)

    return result

# Returns the given grid in a form of a list of exactly 81 elements.
# Each element is an integer from 1-9 (value in a square) or 0 (no value)
def to_list(grid):
    puzzle_list = []
    for row in grid:
        for value in row:
            puzzle_list.append(value)
    return puzzle_list