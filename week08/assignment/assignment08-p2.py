'''
Requirements
1. Create a recursive, multithreaded program that finds the exit of each maze.
   
Questions:
1. It is not required to save the solution path of each maze, but what would
   be your strategy if you needed to do so?
   >
        I would do something similar to what I did in the first assignment. I would add each move of the path to the list and remove it if it
        ends up not being the correct path. However, I am not sure how successful this would be because we are dealing with multiple threads in this
        assignment.
   >
2. Is using threads to solve the maze a depth-first search (DFS) or breadth-first search (BFS)?
   Which search is "better" in your opinion? You might need to define better. 
   (see https://stackoverflow.com/questions/20192445/which-procedure-we-can-use-for-maze-exploration-bfs-or-dfs)
   >
        I think that using threads to solve a maze is a BFS. This is because we do not backtrack as we did in the first assignment. We are creating a new
        thread for each time we encounter a fork in the maze. In my opinion, a BFS is "better" if we define better as faster. I believe that because it allows us to spread out
        through the maze much faster than going through each path and backtracking.
   >
'''

import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False


def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze,row,col,color):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them

    global stop
    global thread_count

    #color = get_color()

    # this will stop the threads from running once the end is found
    if maze.at_end(row, col):
        stop = True
        return

    moves = maze.get_possible_moves(row, col)   # list of moves that are possible from the current location

    if len(moves) > 1:  # if it is greater than 1, that means it is a fork with multiple possible moves. That means we have to use threads
        threads = []
        for r, c in moves:
            if maze.can_move_here(r, c) and not stop:
                color = get_color()     # change the color so we can see the change in thread
                maze.move(r, c, color)
                t = threading.Thread(target=solve_find_end, args=(maze,r,c,color))
                t.start()
                threads.append(t)
                thread_count += 1

        for t in threads:
            t.join()

    else:  # this is for when there is only one possible move the path may take
        for r, c in moves:
            if maze.can_move_here(r, c) and not stop:
                maze.move(r, c, color)
                solve_find_end(maze,r,c,color)     # recursion

def find_end(filename, delay):

    global thread_count
    global stop
    stop = False
    thread_count = 0

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)


    position = maze.get_start_pos() # start position returns a pair (row, col)
    row = position[0]
    col = position[1]

    color = get_color()

    solve_find_end(maze,row,col, color)

    print(f'Number of drawing commands = {screen.get_command_count()}')
    print(f'Number of threads created  = {thread_count}')

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


def find_ends():
    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    print('*' * 40)
    print('Part 2')
    for filename, delay in files:
        print()
        print(f'File: {filename}')
        find_end(filename, delay)
    print('*' * 40)


def main():
    # prevent crashing in case of infinite recursion
    sys.setrecursionlimit(5000)
    find_ends()


if __name__ == "__main__":
    main()
