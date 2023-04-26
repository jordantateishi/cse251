import threading

class GetSum(threading.Thread):

    def __init__(self, number):
        threading.Thread.__init__(self)
        self.number = number
        self.sum = None

    def run(self):
        self.sum = sum(range(1, self.number))

def main():
    
    # Instantiate your thread class and pass in 10.
    t1 = GetSum(10)
    t1.start()
    
    # Repeat, passing in 13
    t2 = GetSum(13)
    t2.start()
    
    # Repeat, passing in 17
    t3 = GetSum(17)
    t3.start()

    # join all threads
    t1.join()
    t2.join()
    t3.join()
    
    assert t1.sum == 45, f'The sum should equal 45 but instead was {t1.sum}'
    assert t2.sum == 78, f'The sum should equal 78 but instead was {t2.sum}'
    assert t3.sum == 136, f'The sum should equal 136 but instead was {t3.sum}'

if __name__ == '__main__':
    main()
    assert threading.active_count() == 1
    print("DONE")
