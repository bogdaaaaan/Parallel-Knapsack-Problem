import time
#from threading import Thread
from java.lang import Thread

def calc_result():
    c = 0
    while c < 10000000:
        c += 1

class TestThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        # arguments for the run method
        self.name = name

    def run(self):
        print(self.name)
        calc_result()

def main():
    start_time = time.time()
    threads_list = []

    for j in range(2):
        threads_list = []
        for i in range(100):
            thread = TestThread("{}-{}".format(j,i))
            threads_list.append(thread)

        for t in threads_list:
            t.start()
        
        for t in threads_list:
            t.join()        
    
    print("end time:", time.time() - start_time)

main()