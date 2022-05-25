from java.lang import Thread, InterruptedException
import time
from utils import generate_items_in_file, get_items_from_file, build_matrix, clear_file, print_matrix_to_file, print_selected_items_to_file, chunk_array

items_file = "C:/Users/bodya/Desktop/Parallel/coursach/Parallel-Knapsack-Problem/src/items/items.csv"
resulting_file = "C:/Users/bodya/Desktop/Parallel/coursach/Parallel-Knapsack-Problem/src/items/result.txt"

class KnapsackThread(Thread):
    def __init__(self, matrix, item, items, capacity_list):
        Thread.__init__(self)
        self.exit = False
        self.matrix = matrix
        self.item = item
        self.items = items
        self.capacity_list = capacity_list
        self.result = []

    def run(self):
        try:
            if not self.exit:
                for capacity in self.capacity_list:
                    # max value we can get without current item
                    # guarantee to exist
                    maxValWithoutCurr = self.matrix[self.item - 1][capacity]

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
                        maxValWithCurr += self.matrix[self.item - 1][remainingCapacity]
                    
                    # pick larger of the two
                    max_val = max(maxValWithoutCurr, maxValWithCurr)

                    # put results in list
                    self.result.append((self.item, capacity, max_val))
                self.end()
        except InterruptedException:
            print("exception")

    def get_result(self):
        return self.result

    def end(self):
        self.exit = True


def parallel_knapsack(max_capacity, generate_items, threads_count):
    # start counting time
    print("qwerty")
    start_time = time.time()

    # if random generation selected, generate random max_capacity of items 
    if (generate_items): generate_items_in_file(items_file, generate_items)

    # get items from file and get total number of items
    items = get_items_from_file(items_file)
    number = len(items)

    rows, cols = number + 1, max_capacity + 1

    # create matrix
    matrix = build_matrix(rows, cols)

    # get size of chunk that each thread will compute
    # create list which holds each thread capacity indexes
    # for example: 3 threads, 30 cols = 10 columns per thread
    # [[0,1,2,3,4,5,6,7,8,9],[10,11,12,13,14,15,16,17,18,19],[20,21,22,23,24,25,26,27,28,29]]
    capacity_list = chunk_array(list(range(1, cols)), threads_count)

    # for each row in matrix
    for item in range(1, rows):

        # create thread_list
        thread_list = []

        # for each thread
        for t in range(threads_count):
            # give info about matrix, current row,
            # all items and which capacity indexes this thread should cover
            thread = KnapsackThread(matrix, item, items, capacity_list[t])
            thread_list.append(thread)
            thread.start()
        
        # after threads created wait untill all finish work
        for t in thread_list:
            t.join()

        for t in thread_list:
            t.end()

        # collect results from each thread
        for t in thread_list:
            res = t.get_result()
            for val in res:
                matrix[val[0]][val[1]] = val[2]
        
        
    # start backtracking to get list of selected items

    # save result of max value
    max_value = matrix[number][max_capacity]

    print(max_value)

    # create temporary variable with max_capacity value
    temp_max_capacity = max_capacity

    # create selected items list
    selected_items = []

    # go from last item to first
    for i in range(number, 0, -1):
        if max_value <= 0:
            break

        # secure selecting last max_value
        if max_value == matrix[i - 1][temp_max_capacity]:
            continue
        else:
            # this item is included
            selected_items.append(items[i - 1])
            
            # since this weight is included its value is deducted
            max_value = max_value - items[i - 1][1]
            temp_max_capacity = temp_max_capacity - items[i - 1][2]

    # reverse items from start to end
    selected_items.reverse()
    
    print(time.time() - start_time)
    # pring result
    clear_file(resulting_file)
    print_matrix_to_file(matrix, resulting_file)
    print_selected_items_to_file(selected_items, resulting_file)


parallel_knapsack(2000, False, 4)