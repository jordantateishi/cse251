'''
Requirements
1. Create a recursive program that finds the solution path for each of the provided mazes.
'''

import math
from screen import Screen
from maze import Maze
import cv2
import sys

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


def path(maze, solution_path, row, col, color):
    # Check if we have reached the end of the maze using the function from the Maze class
    if maze.at_end(row, col):
        return True
    
    # Use the function from Maze to put all possible moves into a list
    moves = maze.get_possible_moves(row, col)

    # go through each of the row/column pairs in the list of moves
    for r, c in moves:
        # if it is a possible move, then we move and append it to the solution_path
        if maze.can_move_here(r, c):
            maze.move(r, c, color)
            solution_path.append((r,c))

            # if it reaches the end, then we return True
            if path(maze, solution_path, r, c, color):
                return True
            
            # else we use the restore function to show that we have been there and get rid of this chosen path
            maze.restore(r,c)
            solution_path.remove((r,c))

def solve(maze):
    """ Solve the maze. The path object should be a list (x, y) of the positions 
        that solves the maze, from the start position to the end position. """

    solution_path = [] 

    position = maze.get_start_pos() # start position returns a pair (row, col)
    row = position[0]
    col = position[1]
    
    maze.move(row, col, COLOR)  # change the color of the start position square
    solution_path.append((row,col)) # add it to the solution path since it always has to start here

    # use the recursive function created to find the solution_path
    path(maze, solution_path, row, col, COLOR)

    return solution_path


def get_solution_path(filename):
    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    solution_path = solve(maze)

    print(f'Number of drawing commands for = {screen.get_command_count()}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True

    return solution_path


def find_paths():
    files = ('verysmall.bmp', 'verysmall-loops.bmp',
             'small.bmp', 'small-loops.bmp',
             'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    print('*' * 40)
    print('Part 1')
    for filename in files:
        print()
        print(f'File: {filename}')
        solution_path = get_solution_path(filename)
        print(f'Found path has length          = {len(solution_path)}')
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_paths()


if __name__ == "__main__":
    main()
