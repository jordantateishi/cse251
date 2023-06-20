import sys
from termcolor import colored

# Size of the array (SIZE x SIZE)
SIZE = 10

# TODO write a recursive function that does the following:
# 1. Check if a house (row, col) in the neighborhood is your house (equals -2).
#    If it is, return True
# 2. Check if you have already checked this house (row, col); if True, return False
# 3  Add house to solution path
# 3. Recursively check the next column and current row if house (row, next_col) is even
# 4. Recursively check the current column and next row if house (next_row, col) is even
# 5. If the recursive call returns True, return True again to exit; else remove
#    house from solution path
# def deliver_presents_recursively(add arguments)

def deliver_presents_recursively(neighborhood, row, column, complete_path, solution_path):
    if neighborhood[row][column] == -2:
        return True
    if neighborhood[row][column] in complete_path:
        return False
    
    solution_path.append(neighborhood[row][column])
    complete_path.append(neighborhood[row][column])

    next_col = column + 1
    next_row = row + 1

    if neighborhood[row][next_col] % 2 == 0:
        if deliver_presents_recursively(neighborhood, row, next_col, complete_path, solution_path):
            return True
    else:
        solution_path.remove((row, next_col))

    if neighborhood[next_row][column] % 2 == 0:
        if deliver_presents_recursively(neighborhood, next_row, column, complete_path, solution_path):
            return True
    else:
        solution_path.remove((next_row, column))

def printNeighborhood(neighborhood, path=None):
    '''Print out the neighborhood. If a path is
       provided, then highlight it in red.
    '''

    for row in range(SIZE):
        for col in range(SIZE):
            alreadyPrintedValue = False
            if path != None:
                for r, c in path:
                    if r == row and c == col:
                        print(f"{colored(neighborhood[row][col], 'red')}\t", end="")
                        alreadyPrintedValue = True
            if not alreadyPrintedValue:
                print(f"{colored(neighborhood[row][col], 'white')}\t", end="")
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
    neighborhood[SIZE - 1][SIZE - 1] = -2

    printNeighborhood(neighborhood)

    # The solution path from the start to the end
    solution_path = []

    # The complete path, this is used to prevent
    # checking the same square more than once.
    complete_path = []

    # make the first call to the recursive function
    # deliver_presents_recursively(add arguments)

    deliver_presents_recursively(neighborhood, 0, 0, complete_path, solution_path)

    print(f'{solution_path=}')

    # print map and color the path
    printNeighborhood(neighborhood, solution_path)


def main():
    # stop execution if too many recursive calls have been made
    sys.setrecursionlimit(5000)
    find_path()


if __name__ == "__main__":
    main()
