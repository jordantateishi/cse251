import json
import os
import sys
import threading
from queue import Queue
import time

import matplotlib.pyplot as plt
import requests
from matplotlib import artist

RETRIEVE_THREADS = 16       # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue


def retrieve_thread(data_queue: Queue, thread_name):
    while True:
        url = data_queue.get()
        if (url == NO_MORE_VALUES):
            break

        # make Internet call to get characters name and log it
        req = requests.get(url)
        data = req.json()
        name = data['name']
        print(thread_name + ': ' + name)


def file_reader(data_queue: Queue):

    # Open the data file "urls.txt" and place items into a queue
    with open("urls.txt") as f:
        for line in f:
            data_queue.put(line.strip())

    # signal the retrieve threads one more time that there are "no more values"
    for i in range(RETRIEVE_THREADS):
        data_queue.put(NO_MORE_VALUES)


def main():
    
    # list to hold the 
    queue_stats = []

    # loop from 1 to the number of retrieve threads
    for thread_count in range(1, RETRIEVE_THREADS + 1, 3):
        threadBegin = time.time()
        # create queue
        data_queue = Queue()

        # create the threads
        reader_thread = threading.Thread(
            target=file_reader, args=(data_queue,))

        threads = []
        for i in range(thread_count):
            name = "Thread_" + str(i)
            threads.append(threading.Thread(
                target=retrieve_thread, args=(data_queue, name)))

        # Get them going - start the retrieve_threads first, then file_reader
        for i in range(thread_count):
            threads[i].start()

        reader_thread.start()

        # Wait for them to finish - The order doesn't matter
        for i in range(thread_count):
            threads[i].join()

        reader_thread.join()

        queue_stats.append(time.time() - threadBegin)

    xaxis = [i for i in range(1, RETRIEVE_THREADS + 1, 3)]
    print(f'xaxis={xaxis}')
    print(f'queue_stats={queue_stats}')
    plt.plot(xaxis, queue_stats)

    plt.title('Time VS Thread Count')
    plt.xlabel('Threads')
    plt.ylabel('Seconds')

    plt.tight_layout()
    plt.savefig('threads.png')
    plt.show()


if __name__ == '__main__':
    main()
