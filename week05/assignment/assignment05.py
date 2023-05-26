'''
Questions:
1. How would you define a barrier in your own words?
   >
        A barrier is what we use to have the program wait for the other threads before proceeding.
   >
2. Why is a barrier necessary in this assignment?
   >
        A barrier was necessary for this because I ran into problems with the dealership class. I needed to break the loop but if I did
        so before the other threads could finish, it would fail. The barriers protected my program and prevented me from running
        into deadlocks.
   >
'''

from datetime import datetime, timedelta
import time
import threading
import random

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!


class Car():
    """ This is the Car class that will be created by the manufacturers """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round',
                  'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                  'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        self.display()

    def display(self):
        #print(f'{self.make} {self.model}, {self.year}')
        pass


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, manufacturer_id, sem_dealership, sem_manufacturer, car_queue, my_lock, barrier, manufacturer_stats, manufacturer_count, dealer_count):
        threading.Thread.__init__(self)

        self.cars_to_produce = random.randint(200, 300)
        self.manufacturer_id = manufacturer_id
        self.sem_dealership = sem_dealership
        self.sem_manufacturer = sem_manufacturer
        self.car_queue = car_queue
        self.my_lock = my_lock
        self.barrier = barrier
        self.manufacturer_stats = manufacturer_stats
        self.manufacturer_count = manufacturer_count
        self.dealer_count = dealer_count
        

    def run(self):
        # create cars to send to the dealership
        manufacturer_count = 0
        for i in range(self.cars_to_produce):
            self.sem_dealership.acquire()
            self.my_lock.acquire()
            car = Car()
            self.car_queue.put(car)

            manufacturer_count += 1

            self.sem_manufacturer.release()
            self.my_lock.release()

        # this is the count that we keep track of
        self.manufacturer_stats.append(manufacturer_count)

        # wait until all of the manufacturers are finished producing cars
        self.barrier.wait()

        # "Wake up/signal" the dealerships one more time.
        for i in range(self.dealer_count):
            if self.manufacturer_id == 0:       # only working with one thread so that we don't send multiple
                self.sem_dealership.acquire()
                self.my_lock.acquire()
                self.car_queue.put(None)    # send None to the queue for the dealership to handle
                self.my_lock.release()
                self.sem_manufacturer.release()
                self.sem_dealership.release()


class Dealership(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, dealership_id, sem_dealership, sem_manufacturer, car_queue, my_lock, barrier, dealer_stats, manufacturer_count, dealer_count):
        threading.Thread.__init__(self)

        self.dealership_id = dealership_id
        self.sem_dealership = sem_dealership
        self.sem_manufacturer = sem_manufacturer
        self.car_queue = car_queue
        self.my_lock = my_lock
        self.barrier = barrier
        self.dealer_stats = dealer_stats
        self.manufacturer_count = manufacturer_count
        self.dealer_count = dealer_count
        


    def run(self):

        dealer_count = 0
        while True:

            self.sem_manufacturer.acquire()

            self.my_lock.acquire()
            
            if self.car_queue.items[0] != None:
                self.car_queue.get()
                dealer_count += 1   # add to the counter

                self.sem_dealership.release()
                self.my_lock.release()

                time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

            else:
                # when we get None in our queue, we proceed with these
                self.sem_dealership.release()
                self.my_lock.release()

                self.dealer_stats.append(dealer_count)   # add the final counts to the list
                self.barrier.wait()     # wait for remaining threads
                break
            

                # Sleep a little - don't change.  This is the last line of the loop
                time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def run_production(manufacturer_count, dealer_count):
    """ This function will do a production run with the number of
        manufacturers and dealerships passed in as arguments.
    """

    # Start a timer
    begin_time = time.perf_counter()

    # Create semaphore(s)
    sem_dealership = threading.Semaphore(MAX_QUEUE_SIZE)
    sem_manufacturer = threading.Semaphore(0)

    # Create queue
    car_queue = QueueTwoFiftyOne()

    # Create lock(s)
    my_lock = threading.Lock()
    the_lock = threading.Lock()

    # Create barrier(s)
    manufact_barrier = threading.Barrier(manufacturer_count)
    dealer_barrier = threading.Barrier(dealer_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)
    manufacturer_stats = list([0] * manufacturer_count)

    manufacturer_threads = []
    for i in range(manufacturer_count):
        manufacturer_id = i
        i = Manufacturer(manufacturer_id, sem_dealership, sem_manufacturer, car_queue, my_lock, manufact_barrier, manufacturer_stats, manufacturer_count, dealer_count)
        manufacturer_threads.append(i)

    dealership_threads = []
    for i in range(dealer_count):
        dealership_id = i
        i = Dealership(dealership_id, sem_dealership, sem_manufacturer, car_queue, the_lock, dealer_barrier, dealer_stats, manufacturer_count, dealer_count)
        dealership_threads.append(i)

    for i in dealership_threads:
        i.start()

    for i in manufacturer_threads:
        i.start()

    for i in manufacturer_threads:
        i.join()
    for i in dealership_threads:
        i.join()

    run_time = time.perf_counter() - begin_time

    # This function must return the following - only change the variable names, if necessary.
    # manufacturer_stats: is a list of the number of cars produced by each manufacturer,
    #                collect this information after the manufacturers are finished.
    return (run_time, car_queue.get_max_size(), dealer_stats, manufacturer_stats)


def main():
    """ Main function """

    #runs = [(2, 2)]
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for manufacturers, dealerships in runs:
        run_time, max_queue_size, dealer_stats, manufacturer_stats = run_production(
            manufacturers, dealerships)

        print(f'Manufacturers       : {manufacturers}')
        print(f'Dealerships         : {dealerships}')
        print(f'Run Time            : {run_time:.2f} sec')
        print(f'Max queue size      : {max_queue_size}')
        print(f'Manufacturer Stats  : {manufacturer_stats}')
        print(f'Dealer Stats        : {dealer_stats}')
        print('')

        assert sum(dealer_stats) == sum(manufacturer_stats)


if __name__ == '__main__':
    main()
