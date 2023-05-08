"""
Questions:
1. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
    > This is IO bound because it is waiting for information from an API. It uses this information to display what we need from it.
2. Review dictionaries (see https://isaaccomputerscience.org/concepts/dsa_datastruct_dictionary). How could a dictionary be used on this assignment to improve performance?
    > Dictionaries could be used for this assignment because it is dealing with large amounts of data in a json file. These references in the 
    dictionary could help with the data we need. For example, the names of characters.
"""


from datetime import datetime, timedelta
import time
import requests
import json
import threading


# Const Values
TOP_API_URL = r"http://127.0.0.1:8790"

# Global Variables
call_count = 0

# Create the thread class
# class GetServer(threading.Thread):
#     def __init__(self, url):

#         threading.Thread.__init__(self)
#         self.response = requests.get(url)
#         self.data = None

#     def run(self):

#         # call the global count and add to it to keep track of calls
#         global call_count
#         call_count += 1

#         if self.response is not None and self.response.status_code == 200:
#             # we take the response from the URL
#             self.data = self.response.json()
class GetServer(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        global call_count
        call_count += 1
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


def print_film_details(film, chars, planets, starships, vehicles, species):
    """
    Print out the film details in a formatted way
    """

    def display_names(title, name_list):
        print("")
        print(f"{title}: {len(name_list)}")
        names = sorted([item["name"] for item in name_list])
        print(str(names)[1:-1].replace("'", ""))

    print("-" * 40)
    print(f'Title   : {film["title"]}')
    print(f'Director: {film["director"]}')
    print(f'Producer: {film["producer"]}')
    print(f'Released: {film["release_date"]}')

    display_names("Characters", chars)
    display_names("Planets", planets)
    display_names("Starships", starships)
    display_names("Vehicles", vehicles)
    display_names("Species", species)


def main():
    # Start a timer
    begin_time = time.perf_counter()

    print("Starting to retrieve data from the server")

    # create a thread to get all URLs from the API
    list_thread = GetServer(TOP_API_URL)
    list_thread.start()
    list_thread.join()

    # Another thread to get the URL for the 6th film
    film_six_url = f"{TOP_API_URL}/films/6"
    t2 = GetServer(film_six_url)
    t2.start()
    t2.join()

    # store the results from the thread to film_six list
    film_six = []
    film_six = t2.response

    # function helps to iterate through the categories using threads
    def iterate(thing: str):
        names = []
        threads = []

        # For each item in category, begin a thread and append it to a thread list
        for i in film_six[thing]:
            t = GetServer(i)
            threads.append(t)
            t.start()

        # Join threads in thread list
        for t in threads:
            t.join()
            data = t.response
            names.append(data)

        return names

    # Assigning variables for each of the category names
    characters = iterate("characters")
    planets = iterate("planets")
    starships = iterate("starships")
    vehicles = iterate("vehicles")
    species = iterate("species")

    # Call the display function
    print_film_details(film_six, characters, planets, starships, vehicles, species)

    print(f"There were {call_count} calls to the server")
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f"Total time = {total_time_str} sec")

    # If you do have a slow computer, then put a comment in your code about why you are changing
    # the total_time limit. Note: 90+ seconds means that you are not doing multithreading
    assert (
        total_time < 15
    ), "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."

    assert call_count == 94, "It should take exactly 94 threads to get all the data"


if __name__ == "__main__":
    main()
