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

def retrieve_thread(data_queue):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        if data_queue.get() == NO_MORE_VALUES:
            break

        # TODO process the value retrieved from the queue
        value = data_queue.get()

        # TODO make Internet call to get characters name and print it out
        response = requests.get(value)
        if response.status_code == 200:
            data = response.json()
        else:
            print('RESPONSE = ', response.status_code)
        char_name = data["name"]
        print(char_name)



def file_reader(data_queue): # TODO add arguments
    """ This thread reads the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open(r"urls.txt") as f:
        for line in f:
            data_queue.put(line.strip())

    # TODO signal the retrieve threads one more time that there are "no more values"
    for _ in range(RETRIEVE_THREADS):
        data_queue.put(NO_MORE_VALUES)



def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()
    
    # TODO create queue (if you use the queue module, then you won't need semaphores/locks)
    data_queue = queue.Queue()
    
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread needed to do their jobs
    reader = threading.Thread(target=file_reader, args=(data_queue,))
    threads = []
    for i in range(RETRIEVE_THREADS):
        i = threading.Thread(target=retrieve_thread, args=(data_queue,))
        threads.append(i)

    # TODO Get them going
    reader.start()
    for i in threads:
        i.start()

    # TODO Wait for them to finish
    for i in threads:
        i.join()
    reader.join()

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time to process all URLS = {total_time} sec')


if __name__ == '__main__':
    main()




