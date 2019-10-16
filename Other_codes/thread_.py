import threading
import time


def peofile(func):
    def wapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print('COST: {}'.format(end - start))
    return wapper


def fib(n):
    if n <2:
        return 1
    return fib(n-1) + fib(n-2)


@peofile
def nothread():
    fib(35)
    fib(35)

@peofile
def hasthread():
    for i in range(2):
        t = threading.Thread(target=fib, args=(35,))
        t.start()

    main_thread = threading.currentThread()
    for i in threading.enumerate():
        if i is main_thread:
            continue
        i.join()


nothread()
hasthread() 

    