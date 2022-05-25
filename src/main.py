import time
from sequential_knapsack import sequential_knapsack
from parallel_knapsack import parallel_knapsack
from test import test

# set main variables
max_capacity = 5000
items_count = 5
processes = 4
    
if __name__ == "__main__":
    start_time = time.time()
    #sequential_knapsack(max_capacity, False)
    #parallel_knapsack(max_capacity, False, processes)
    test(processes)

    print(time.time() - start_time)