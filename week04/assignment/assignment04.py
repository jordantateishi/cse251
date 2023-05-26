'''
Questions:
1. Do you need to use locks around accessing the queue object when using multiple threads? 
   Why or why not?
   >
        Yes, because we don't want multiple threads accessing the same queue at the same time as each other.
   >
2. How would you define a semaphore in your own words?
   >
        I would define it as something that prevents something from exceeding the allowed sapce for the program. It makes sure to
        block until space is available.
   >
3. Read https://stackoverflow.com/questions/2407589/what-does-the-term-blocking-mean-in-programming.
   What does it mean that the "join" function is a blocking function? Why do we want to block?
   >
        It means that it will wait until the task is completed. We want to block because we wouldn't want to receive incomplete data.
        This is especially true when dealing with threads because we are waiting for the function to finish.
   >
'''

from datetime import datetime
import time
import threading
import random
# DO NOT import queue

from plots import Plots

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

#########################
# NO GLOBAL VARIABLES!
#########################


class Car():
    """ This is the Car class that will be created by the factories """

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

        # Display the car that has just be created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, CARS_TO_PRODUCE, sem_dealership, sem_manufacturer, car_queue, my_lock, queue_stats):

        # call the super class's constructor
        threading.Thread.__init__(self)

        self.car_count = CARS_TO_PRODUCE
        self.sem_dealership = sem_dealership
        self.sem_manufacturer = sem_manufacturer
        self.car_queue = car_queue
        self.my_lock = my_lock
        self.queue_stats = queue_stats

    def run(self):
        """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
        """

        for i in range(self.car_count):
            # acquire the semaphore for the dealership
            self.sem_dealership.acquire()

            # lock before dealing with the queue
            self.my_lock.acquire()

            car = Car()
            self.car_queue.put(car)
            #self.queue_stats[(self.car_queue.size()) - 1] += 1

            self.my_lock.release()
            
            # release the manufacturer to let the dealership know there is a car in queue
            self.sem_manufacturer.release()

        # signal the dealer that there there are no more cars
        self.sem_dealership.acquire()
        self.car_queue.put(None)
        self.sem_manufacturer.release()


class Dealership(threading.Thread):
    """ This is a dealership that receives cars """

    def __init__(self, sem_dealership, sem_manufacturer, car_queue, my_lock, queue_stats):

        # call the super class's constructor
        threading.Thread.__init__(self)

        self.sem_dealership = sem_dealership
        self.sem_manufacturer = sem_manufacturer
        self.car_queue = car_queue
        self.my_lock = my_lock
        self.queue_stats = queue_stats

    def run(self):
        """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
        """

        while True:

            # acquire semaphore and lock
            self.sem_manufacturer.acquire()

            self.my_lock.acquire()

            car = self.car_queue.get()
            if car == None:
                break

            self.queue_stats[(self.car_queue.size())] += 1

            self.my_lock.release()

            # release the dealership semaphore so the manufacturer knows it can take another car
            self.sem_dealership.release()

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def main():
    # Start a timer
    begin_time = time.perf_counter()

    # random amount of cars to produce
    CARS_TO_PRODUCE = random.randint(500, 600)

    # Create semaphores
    sem_dealership = threading.Semaphore(MAX_QUEUE_SIZE)
    sem_manufacturer = threading.Semaphore(0)

    # Create queue (ONLY use class QueueTwoFiftyOne)
    car_queue = QueueTwoFiftyOne()

    # Create lock
    my_lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership,
    # the index of the list is the size of the queue. Update this list each time the
    # dealership receives a car (i.e., increment the integer at the index using the
    # queue size).
    queue_stats = [0] * MAX_QUEUE_SIZE

    # create your one manufacturer
    manufacturer = Manufacturer(CARS_TO_PRODUCE, sem_dealership, sem_manufacturer, car_queue, my_lock, queue_stats)

    # create your one dealership
    dealership = Dealership(sem_dealership, sem_manufacturer, car_queue, my_lock, queue_stats)

    # Start manufacturer and dealership
    manufacturer.start()
    dealership.start()

    # Wait for manufacturer and dealership to complete
    manufacturer.join()
    dealership.join()

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

    # Plot car count vs queue size
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats,
             title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')


if __name__ == '__main__':
    main()
