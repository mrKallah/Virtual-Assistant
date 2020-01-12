import time
from multiprocessing import Value, Process



def a(x):
    while True:
        time.sleep(.5)
        with x.get_lock():
            x.value += 1
            print("x = {}".format(x.value))

def b(x, y):
    with y.get_lock():
        y.value = x.value
        y.value += 1
    print("y = {}".format(y.value))

if __name__ == "__main__":
    x = Value('i', 0)
    y = Value('i', 0)
    p = Process(target=a, args=(x, ))
    p.start()

    while True:
        time.sleep(2)
        p = Process(target=b, args=(x, y))
        p.start()
        p.join()