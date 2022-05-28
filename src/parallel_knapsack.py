import time
from utils import generate_items_in_file, generate_items_in_array, get_items_from_file, build_matrix, clear_file, print_matrix_to_file, print_selected_items_to_file, chunk_array
from threading import Thread, Event
#from multiprocessing import Process

items_file = "C:/Users/bodya/Desktop/Parallel/coursach/Parallel-Knapsack-Problem/src/items/items.csv"
resulting_file = "C:/Users/bodya/Desktop/Parallel/coursach/Parallel-Knapsack-Problem/src/items/result.txt"

global pool 
pool = []

event1 = Event()
event2 = Event()

class KnapsackThread(Thread):
    def __init__(self, id, items, capacity_list):
        Thread.__init__(self)
        self.waiting = False
        self.threads_amount = 0
        self.id = id
        self.item = 0
        self.items = items
        self.capacity_list = capacity_list

    # def set_item(self, item):
    #     self.item = item

    def compute(self):
        for capacity in self.capacity_list:
            # max value we can get without current item
            # guarantee to exist
            maxValWithoutCurr = matrix[self.item - 1][capacity]

            # initialize this value to 0
            maxValWithCurr = 0
            
            # depending of row above we get weight of current item
            weightOfCurr = self.items[self.item - 1][2]

            # check if there is knapsack capacity left
            if (capacity >= weightOfCurr):

                # maxValWithCurr is at least the value of the current item
                maxValWithCurr = self.items[self.item - 1][1]

                # remainingCapacity must be at least 0
                remainingCapacity = capacity - weightOfCurr

                # add the maximum value obtainable with the remaining capacity
                maxValWithCurr += matrix[self.item - 1][remainingCapacity]
            
            # pick larger of the two
            max_val = max(maxValWithoutCurr, maxValWithCurr)

            matrix[self.item][capacity] = max_val
    
    def run(self):
        while self.item < len(self.items):
            print("Thread #{} started on row #{}".format(self.id, self.item + 1))
            print("event1: {}".format(event1.is_set()))
            print("event2: {}".format(event2.is_set()))
            
            # compute current row
            self.item += 1 
            self.compute()

            # remove thread id from pool of available threads
            pool.remove(self.id)

            # if pool has threads that currently working - wait
            if len(pool) > 0:
                self.waiting = True
                print("Thread #{} waiting".format(self.id))
                event1.wait()
                print("Thread #{} no more waiting".format(self.id))

            if not self.waiting:
                print("All waiting threads set free by Thread #{}".format(self.id))
                event1.set()

            self.waiting = False

            pool.append(self.id)
            print("Thread #{} added to pool {}".format(self.id, pool))

            if len(pool) != self.threads_amount:
                print("Thread #{}, Pool isn't full, wait".format(self.id))
                event2.wait()
            else:
                print("Pool full, goto next iteration")
                event2.set()
                event1.clear()
                event2.clear()
                continue
            


            # if not self.waiting:
            #     print("Thread #{} ended on row #{} last and gonna wait for others".format(self.id, self.item))
            #     event.set()
            #     event.wait()
            # else:
            #     print("Thread #{} ended on row #{}".format(self.id, self.item))
            #     self.waiting = False
            #     if len(pool) != self.threads_amount:
            #         event.wait()
            #     else:
            #         print("Thread #{} ended on row #{} and was last in queue".format(self.id, self.item))
            #         event.set()

            


def parallel_knapsack(max_capacity, generate_items, threads_amount):
    #total = time.time()
    print("Parallel knapsack, threads amount:", threads_amount)
    # if random generation selected, generate random max_capacity of items 
    if (generate_items): generate_items_in_file(items_file, generate_items)
    items = get_items_from_file(items_file)

    #if (generate_items): items = generate_items_in_array(generate_items)
    #else: items = get_items_from_file(items_file)
    
    number = len(items)
    rows, cols = number + 1, max_capacity + 1

    # get size of chunk that each thread will compute
    # create list which holds each thread capacity indexes
    # for example: 3 threads, 30 cols = 10 columns per thread
    # [[0,1,2,3,4,5,6,7,8,9],[10,11,12,13,14,15,16,17,18,19],[20,21,22,23,24,25,26,27,28,29]]
    capacity_list = chunk_array(list(range(1, cols)), threads_amount)
    
    # create thread_list
    thread_list = []

    # start counting time
    start_time = time.time()

    # for each thread
    for t in range(threads_amount):
        # give info about items and chunks
        thread = KnapsackThread(t, items, capacity_list[t])
        thread_list.append(thread)

        # track available thread in pool
        pool.append(t)

    for thread in thread_list:
        thread.threads_amount = len(pool)
    
    for thread in thread_list:
        thread.start()

    # # for each row in matrix
    # for item in range(1, rows):
    #     for thread in thread_list:
    #         thread.set_item(item)
            
    # after threads created wait untill all finish work
    for thread in thread_list:
        thread.join()
    
    # print time 
    print("time to compute:", time.time() - start_time)
    
    # start backtracking to get list of selected items
    # save result of max value
    max_value = matrix[number][max_capacity]

    print("max value is: ", max_value)

    # # create temporary variable with max_capacity value
    # temp_max_capacity = max_capacity

    # # create selected items list
    # selected_items = []

    # # go from last item to first
    # for i in range(number, 0, -1):
    #     if max_value <= 0:
    #         break

    #     # secure selecting last max_value
    #     if max_value == matrix[i - 1][temp_max_capacity]:
    #         continue
    #     else:
    #         # this item is included
    #         selected_items.append(items[i - 1])
            
    #         # since this weight is included its value is deducted
    #         max_value = max_value - items[i - 1][1]
    #         temp_max_capacity = temp_max_capacity - items[i - 1][2]

    # # reverse items from start to end
    # selected_items.reverse()
    
    # # pring result
    # clear_file(resulting_file)
    # print_matrix_to_file(matrix, resulting_file)
    # print_selected_items_to_file(selected_items, resulting_file)

    # print("Total time: {}".format(time.time() - total))


MAX_CAPACITY = 40
ITEMS = 10

global matrix
matrix = build_matrix(ITEMS + 1, MAX_CAPACITY + 1)

parallel_knapsack(MAX_CAPACITY, False, 4)