'''
Requirements:
1. Write a function that takes a number and computes the sum of all numbers between
   one and that number (exclusive). This will be the target of your thread.
2. Create a thread to run this function.
3. Assert that your sums are correct for the given number.
   
Psuedocode:
1. Create either a global SUM or create a list object in main.
2a. If using a global, then inside of your function, set the global equal to the sum.
2b. If using a list object, set the appropriate index position equal to the sum.
3. In main, create a thread to call the sum function using 10.
4. Using assert, check the expected result (see main)
5. Repeat steps 3 and 4, but use 13.
6. Repeat steps 3 and 4, but use 17.

Things to consider:
a. If using a global, what is the correct syntax for creating a thread with one argument?
   (see https://stackoverflow.com/questions/3221655/python-threading-string-arguments)
b. How do you start a thread? (see this week's reading) 
c. How will you wait until the thread is done? (see this week's reading)
d. Do threads (including the main thread) share global variables? (see https://superfastpython.com/thread-share-variables/)
e. If you use a global, how will you ensure that one thread doesn't change the value of
   your global while another thread is using it too? (We haven't learned about locks yet, so you
   won't be able to run your threads simultaneously)
f. How do you modify the value of a global variable (see https://stackoverflow.com/questions/10588317/python-function-global-variables)
g. If using a list object, how to you instantiate it with the correct number of indexes? (see https://stackoverflow.com/questions/8528178/list-of-zeros-in-python)
'''
import threading

# global sum
SUM = 0

def main():

    # If not using a global, use this list to store your results
    results = [0] * 3
    
    # If using a global, place these asserts after the call to your summing function 
    # to check that your code is working correctly
    #assert SUM == 45, f'The sum should equal 45 but instead was {SUM}'  
    #assert SUM == 78, f'The sum should equal 78 but instead was {SUM}'    
    #assert SUM == 136, f'The sum should equal 136 but instead was {SUM}'
    
    # If using a list object, place these asserts after the call to your summing function
    # to check that your code is working correctly
    #assert results[0] == 45, f'The sum should equal 45 but instead was {results[0]}'  
    #assert results[1] == 78, f'The sum should equal 78 but instead was {results[1]}'    
    #assert results[2] == 136, f'The sum should equal 136 but instead was {results[2]}'


if __name__ == '__main__':
    main()
    print("DONE")
