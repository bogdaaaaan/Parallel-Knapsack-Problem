import random


def generate_items_in_array(num_of_items):
    res = []
    for i in range(num_of_items):
        res.append((i, random.randint(1,20), random.randint(1,20)))
    return res

# generate items for problem
def generate_items_in_file(file_name, num_of_items):
    file = open(file_name, "w")
    file.write("Item,Value,Weight\n")
    for i in range(num_of_items):
        file.write("{},{},{}\n".format(i,random.randint(1, 20),random.randint(1, 20)))
    file.close()

# get item from file
def get_items_from_file(file_name):
    # create items list that will fill up with items from file 
    items = []
    file = open(file_name, "r")

    # check for header values
    header = True

    # add each item in items list
    for line in file.read().splitlines():
        if (header):
            header = False
        else:
            t = []
            
            # lines has next structure: item number, value, weight
            for num in line.split(','):
                t.append(int(num))
            items.append(t)
    
    # return items
    return items

# clear file before writing in it
def clear_file(file_name):
    file  = open(file_name, "w")
    file.close()

# create matrix with given rows and cols
def build_matrix(rows, cols):
    matrix = []
    for r in range(0, rows):
        matrix.append([0 for c in range(0, cols)])
    return matrix

# print matrix to a file 
def print_matrix_to_file(mat, file_name):
    file  = open(file_name, "a")
    for i in mat:
        for j in i:
            file.write(str(j) + '\t')
        file.write('\n')
    file.write("Max value: {}".format(mat[len(mat)-1][len(mat[len(mat)-1])-1]))
    file.close()

# print out items that were selected in knapsack algorithm into file
def print_selected_items_to_file(items, file_name):
    file  = open(file_name, "a")
    file.write('\nSelected items:\n#\tVal\tWt\n')
    for i in items:
        for j in i:
            file.write(str(j) + '\t')
        file.write('\n')
    file.close()

def chunk_array(a, n):
    k, m = divmod(len(a), n)
    return [a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]