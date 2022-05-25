import time
from utils import generate_items_in_file, get_items_from_file, build_matrix, clear_file, print_matrix_to_file, print_selected_items_to_file

items_file = "C:/Users/bodya/Desktop/Parallel/coursach/Parallel-Knapsack-Problem/src/items/items.csv"
resulting_file = "C:/Users/bodya/Desktop/Parallel/coursach/Parallel-Knapsack-Problem/src/items/result.txt"

def sequential_knapsack(max_capacity, generate_items):
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

    # for each item in matrix
    for item in range(1, rows):
        # for each capacity from 0 to max weigth
        for capacity in range(1, cols):
            # max value we can get without current item
            # guarantee to exist
            maxValWithoutCurr = matrix[item - 1][capacity]

            # initialize this value to 0
            maxValWithCurr = 0
            
            # depending of row above we get weight of current item
            weightOfCurr = items[item - 1][2]

            # check if there is knapsack capacity left
            if (capacity >= weightOfCurr):

                # maxValWithCurr is at least the value of the current item
                maxValWithCurr = items[item - 1][1]

                # remainingCapacity must be at least 0
                remainingCapacity = capacity - weightOfCurr

                # add the maximum value obtainable with the remaining capacity
                maxValWithCurr += matrix[item - 1][remainingCapacity]
            
            # pick larger of the two
            matrix[item][capacity] = max(maxValWithoutCurr, maxValWithCurr)
        #print("row {} done".format(item))
       
    
    
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


sequential_knapsack(2000, False)