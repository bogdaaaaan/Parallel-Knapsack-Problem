import multiprocessing
import queue
import time

def test():
    print("qwerty")
    start_time = time.time()
    for i in range(5001):
        f(i)
    print(time.time() - start_time)
        


def main(_processes):
    if __name__ == '__main__':
        print("qwerty")
        start_time = time.time()
        #arr = list(range(5000))

        pool = multiprocessing.Pool(processes=_processes)
        res = []
        for i in range(5000):
            res.append(pool.map(f, [j for j in range(3000)]))
            #print("row {} done".format(i))
            
        pool.close()
        pool.join()

        print(time.time() - start_time)


def f(a):
    res = a
    res *= a
    #print(res)s
    return (a, res)

_processes = 5
main(_processes)
#test(_processes)