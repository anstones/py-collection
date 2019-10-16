import time
import threading
from queue import Queue
from random import random


q = Queue()


def double(n):
    return n*2


def producer():
    while 1:
        wt = random()
        time.sleep(wt)
        q.put((double, wt))

def comsumer():
    while 1:
        task, wt = q.get()
        print(wt, task(wt))
        q.task_done()


for target in (producer, comsumer):
    print(target)
    try:
        t = threading.Thread(target=target)
        t.start()
    except KeyboardInterrupt as e:
        break
