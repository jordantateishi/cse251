import threading

# global sum
SUM = 0

def find_sum(num):
   global SUM
   SUM = sum(range(num))

def main():

    # use threading to find the sums of numbers up to 10, 13, and 17
    t1 = threading.Thread(target=find_sum, args=(10, ))
    t2 = threading.Thread(target=find_sum, args=(13, ))
    t3 = threading.Thread(target=find_sum, args=(17, ))

    t1.start()
    t1.join()
    assert SUM == 45, f'The sum should equal 45 but instead was {SUM}' 

    t2.start()
    t2.join()
    assert SUM == 78, f'The sum should equal 78 but instead was {SUM}'

    t3.start()
    t3.join()
    assert SUM == 136, f'The sum should equal 136 but instead was {SUM}' 



if __name__ == '__main__':
    main()
    print("DONE")
