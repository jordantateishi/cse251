'''
Requirements
1. Write a multithreaded/multiprocessing program that counts the number of prime numbers 
   contained within a data file.
2. Create one thread to read each number from the data file and put the number on the queue.
3. Create n number of processes, where n is equal to the number of cpu/cores on your computer.
4. The processes will pop each number off of the queue and check if it is prime. If it is
   prime increment a "counter" (use an appropriate multiprocessing data structure).
5. Assert that the number of prime numbers found is correct.

Questions to consider with your Team:
1. Does increasing the number of processes beyond your cpu count decrease the time it takes
   to find the prime numbers? Why or why not?
2. What are some of the advantages and disadvantages of using processes over threads?
'''


import multiprocessing as mp
import threading
import time


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
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


def read_thread(filename, data_queue):
    with open(filename) as f:
        for line in f:
            data_queue.put(line.strip())
    print("Finished reading the file")


def prime_process(data, primes, lock):
    while True:
        try:
            num = data.get(timeout=1)  # Wait for 1 second to get data
        except mp.queues.Empty:
            print("Data queue timeout. Possible deadlock.")
            break
        
        if num is None:
            break
        if is_prime(int(num)):
            with lock:
                primes.append(num)
                print(f"Processed number: {num}")


def main():
    filename = 'data.txt'
    begin_time = time.perf_counter()
    cpu_count = mp.cpu_count()

    data_queue = mp.Queue(maxsize=1000)
    primes = mp.Manager().list([0] * cpu_count)

    t1 = threading.Thread(target=read_thread, args=(filename, data_queue))

    processes = []
    lock = mp.Lock()
    for _ in range(cpu_count):
        p = mp.Process(target=prime_process, args=(data_queue, primes, lock))
        processes.append(p)
    t1.start()
    for p in processes:
        p.start()

    t1.join()
    for p in processes:
        p.join()

    primes = list(primes)

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

    assert len(primes) == 321, f"You should find exactly 321 prime numbers {len(primes)}"


if __name__ == '__main__':
    main()






# import multiprocessing as mp
# import threading
# import time

# def is_prime(n: int) -> bool:
#     """Primality test using 6k+-1 optimization.
#     From: https://en.wikipedia.org/wiki/Primality_test
#     """
#     if n <= 3:
#         return n > 1
#     if n % 2 == 0 or n % 3 == 0:
#         return False
#     i = 5
#     while i ** 2 <= n:
#         if n % i == 0 or n % (i + 2) == 0:
#             return False
#         i += 6
#     return True

# # TODO create read_thread function
# def read_thread(filename, data_queue):
#     with open(filename) as f:
#         for line in f:
#             data_queue.put(line.strip())


# # TODO create prime_process function
# def prime_process(data, primes):
#     num = data.get()
#     if is_prime(int(num)):
#         primes.append(num)
    


# def main():
#     """ Main function """

#     filename = 'data.txt'

#     # Start a timer
#     begin_time = time.perf_counter()
    
#     # Get number of processes to create based on cpu count
#     cpu_count = mp.cpu_count()

#     # TODO Create shared data structures
    
#     #data_queue = mp.Queue()
#     with mp.Manager() as manager:
#         data_queue = mp.Queue()
#         primes = manager.list([0] * cpu_count)


#     # TODO create reading thread
#         t1 = threading.Thread(target=read_thread, args=(filename, data_queue))


#     # TODO create prime processes
#     # with mp.Pool(cpu_count) as p:
#     #     p.map(is_prime, data)
#         processes = []
#         for _ in range(cpu_count):
#             p = mp.Process(target=prime_process, args=(data_queue, primes ))
#             processes.append(p)

#     # TODO Start them all
#         t1.start()
#         for i in processes:
#             i.start()
    
    

#     # TODO wait for them to complete
#         t1.join()
#         for i in processes:
#             i.join()
    
#         primes = list(primes)

#     total_time = "{:.2f}".format(time.perf_counter() - begin_time)
#     print(f'Total time = {total_time} sec')

#     # Assert the correct amount of primes were found.
#     assert len(primes) == 321, f"You should find exactly 321 prime numbers {len(primes)}"

# if __name__ == '__main__':
#     main()

