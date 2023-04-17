"""
Course: CSE 251
Lesson Week: 05
File: team05.py
Author: Brother Comeau (modified by Brother Foushee)

Purpose: Team Activity

Instructions:

- See in Canvas

"""

import threading
import queue
import time
import requests
import json

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread():  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue

        # TODO process the value retrieved from the queue

        # TODO make Internet call to get characters name and print it out
        pass



def file_reader(): # TODO add arguments
    """ This thread reads the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue

    # TODO signal the retrieve threads one more time that there are "no more values"



def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()
    
    # TODO create queue (if you use the queue module, then you won't need semaphores/locks)
    
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread needed to do their jobs

    # TODO Get them going

    # TODO Wait for them to finish

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time to process all URLS = {total_time} sec')


if __name__ == '__main__':
    main()




