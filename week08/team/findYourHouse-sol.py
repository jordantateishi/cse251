import random
import string
import sys
import time
from termcolor import colored

SIZE = 10


def deliver_presents_recursively(neighborhood, row, col, solution_path, complete_path: list):

    # Check if we have already checked this row and col
    if (row, col) in complete_path:
        return False
    complete_path.append((row, col))

    # Check if this row and col is the house
    if neighborhood[row][col] == -2:
        print('Santa found your house and will now deliver your presents!')
        return True

    # Create list to store any path that contains an even value
    even_paths = []

    # Move to the right, -1 indicates out of bounds
    next_col = col + 1 if col + 1 < SIZE else -1
    # Move down a row, -1 indicates out of bounds
    next_row = row + 1 if row + 1 < SIZE else -1

    # Is value in next column and current row even
    if next_col != -1 and neighborhood[row][next_col] % 2 == 0:
        #print(f'adding next_col: {row},{next_col}, value={map[row][next_col]}')
        even_paths.append((row, next_col))

    # Is value in current column and next row even
    if next_row != -1 and neighborhood[next_row][col] % 2 == 0:
        #print(f'adding next_row: {next_row},{col}, value={map[next_row][col]}')
        even_paths.append((next_row, col))

    for r, c in even_paths:

        # Add path before checking if r and c are on the solution path
        solution_path.append((r, c))

        # If this r and c are the house, then exit by returning
        if deliver_presents_recursively(neighborhood, r, c, solution_path, complete_path):
            return True
        # Since we returned False from recursive call, we can remove the
        # r and c from the solution path
        solution_path.remove((r, c))


def printNeighborhood(neighborhood, path=None):

    for row in range(SIZE):
        for col in range(SIZE):
            alreadyPrintedValue = False
            if path != None:
                for r, c in path:
                    if r == row and c == col:
                        print(f"{colored(neighborhood[row][col], 'red')} ", end="")
                        alreadyPrintedValue = True
            if not alreadyPrintedValue:
                print(f"{colored(neighborhood[row][col], 'white')} ", end="")
        print()


def find_path():

    # Create a SIZE x SIZE array (list of lists)
    neighborhood = [[0 for x in range(SIZE)] for y in range(SIZE)]

    # Fill in the neighborhoods with odd and even numbers.
    # The path to your house is along even numbers
    for row in range(1, SIZE):
        for col in range(1, SIZE):
            neighborhood[row][col] = (row * 2) // col

    # -2 is your house (bottom right corner)
    neighborhood[SIZE - 1][random.choice([0, 1, 4, 5, 6, 7, 8, 9])] = -2

    printNeighborhood(neighborhood)

    # The solution path from the start to the end
    solution_path = []

    # The complete path that each recursive call checks,
    # this is used to prevent checking the same square more
    # than once.
    complete_path = []

    solution_path.append((0, 0))
    deliver_presents_recursively(neighborhood, 0, 0, solution_path, complete_path)

    print(f'{solution_path=}')

    # print map and color the path
    printNeighborhood(neighborhood, solution_path)


def main():
    # stop execution if too many recursive calls have been made
    sys.setrecursionlimit(5000)
    find_path()


if __name__ == "__main__":
    main()
