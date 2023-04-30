from datetime import datetime, timedelta
import math
import threading
import time

# Global count of the number of primes found
prime_count = 0

# Global count of the numbers examined
numbers_processed = 0

NUMBER_THREADS = 10

def primes(start, end):
    global prime_count
    global numbers_processed

    for i in range(start, end):
        numbers_processed += 1

        # Check if the numbers within the range are prime
        if is_prime(i):
            prime_count += 1

def partition(NUMBER_THREADS: int, start: int, num_range: int):
    # Calculate the partitions by dividing. The last partition will take the remainder
    num_partition = num_range // NUMBER_THREADS
    last_num_partition = num_range % NUMBER_THREADS

    list_partition = []
    count = 0
    for i in range(NUMBER_THREADS):
        if count < last_num_partition:
            count += 1
            end = start + num_partition + 1
        else:
            end = start + num_partition
        list_partition.append((start, end))
        start = end
    # return a list will all the partitioned numbers
    return list_partition

def is_prime(n: int):
    """
    Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test

    Parameters
    ----------
    ``n`` : int
        Number to determine if prime

    Returns
    -------
    bool
        True if ``n`` is prime.
    """

    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

if __name__ == '__main__':
    # Start a timer
    begin_time = time.perf_counter()

    # TODO write code here
    start = 10000000000
    num_range = 110003

    list_partition = partition(NUMBER_THREADS, start, num_range)

    # Create a list to store the threads
    threads=[]

    for i in list_partition:
        t = threading.Thread(target=primes, args=i)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Use the below code to check and print your results
    assert numbers_processed == 110_003, f"Should check exactly 110,003 numbers but checked {numbers_processed}"
    assert prime_count == 4764, f"Should find exactly 4764 primes but found {prime_count}"

    print(f'Numbers processed = {numbers_processed}')
    print(f'Primes found = {prime_count}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')
