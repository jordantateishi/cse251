'''
Questions:
1. Why can you not use the same pipe object for all the processes (i.e., why 
   do you need to create three different pipes)?
   >
        Because there are multiple pipes needed for this. There would be problems if multiple processes were waiting on the same pipe. Therefore, we created three different
        pipes to avoid any problems.
   >
2. Compare and contrast pipes with queues (i.e., how are the similar or different)?
   >
        Pipes and queues are similar in that they share data between processes. A queue shares a queue and a pipe shares messages. Both are useful when working with
        multiprocessing.
   >
'''

import datetime
import json
import multiprocessing as mp
import os
import random
import time

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables


class Bag():
    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ['Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green']

    def __init__(self, conn, MARBLE_COUNT, CREATOR_DELAY):
        mp.Process.__init__(self)
        self.conn = conn
        self.marble_count = MARBLE_COUNT
        self.creator_delay = CREATOR_DELAY

    def run(self):
        
        for _ in range(int(self.marble_count)):     # create a marble for the amount of marble_count within the 'settings.txt' file
            marble = random.choice(Marble_Creator.colors)
            self.conn.send(marble)      # send it to the bagger
            time.sleep(int(self.creator_delay))
        self.conn.send(None)    # done


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self, conn, conn2, BAG_COUNT, BAGGER_DELAY):
        mp.Process.__init__(self)
        self.conn = conn
        self.conn2 = conn2
        self.bag_count = BAG_COUNT
        self.bagger_delay = BAGGER_DELAY

    def run(self):
        
        bag = Bag()
        while True:
            received = self.conn.recv()     # first receive from the marble creator
            if received is None:    # break if no marbles left
                break
            bag.add(received)   # add it to the Bag() class and use the fucntions within the class to create the bag
            if bag.get_size() == self.bag_count:
                self.conn2.send(str(bag))
                time.sleep(int(self.bagger_delay))
                bag = Bag()

        self.conn2.send(None)   # done


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, conn, conn2, ASSEMBLER_DELAY):
        mp.Process.__init__(self)
        self.conn = conn
        self.conn2 = conn2
        self.assembler_delay = ASSEMBLER_DELAY

    def run(self):
       
        while True:
            received = self.conn.recv()     # receive from the bagger
            if received is None:    # similar to prior, if None then we break
                break
            gift = Gift(random.choice(Assembler.marble_names), received)    # add a random large marble and the smaller from the bagger using the Gift class
            self.conn2.send(str(gift))
            time.sleep(int(self.assembler_delay))

        self.conn2.send(None)   # done


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """

    def __init__(self, conn, WRAPPER_DELAY):
        mp.Process.__init__(self)
        self.conn = conn
        self.wrapper_delay = WRAPPER_DELAY

    def run(self):
       
        with open(BOXES_FILENAME, "w") as f:    # open the file 'boxes.txt'
            while True:
                received = self.conn.recv()     # receive from the assembler 
                if received is None:
                    break
                now = datetime.datetime.now()
                f.writelines(f"Created - {now}: {received}\n")  # add to a new line the information
                time.sleep(int(self.wrapper_delay)) 


def display_final_boxes(filename):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        print(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                print(line.strip())
    else:
        print(
            f'ERROR: The file {filename} doesn\'t exist.  No boxes were created.')


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        print(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    print(f'Marble count                = {settings[MARBLE_COUNT]}')
    print(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    print(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    print(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    print(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    print(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # created separate Pipes between creator -> bagger -> assembler -> wrapper
    creator_conn, bagger_conn = mp.Pipe()
    bagger_conn2, assembler_conn = mp.Pipe()
    assembler_conn2, wrapper_conn = mp.Pipe()

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    print('Create the processes')

    # Create the processes (ie., classes above)
    p1 = Marble_Creator(bagger_conn, settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    p2 = Bagger(creator_conn, bagger_conn2, settings[BAG_COUNT], settings[BAGGER_DELAY])
    p3 = Assembler(assembler_conn, assembler_conn2, settings[ASSEMBLER_DELAY])
    p4 = Wrapper(wrapper_conn, settings[WRAPPER_DELAY])

    print('Starting the processes')
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    print('Waiting for processes to finish')
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    display_final_boxes(BOXES_FILENAME)

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

if __name__ == '__main__':
    main()
