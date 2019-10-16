import time
import threading
from threading import Lock

value = 0
lock = Lock()

def getlock():
    global value
    with lock:  # with lock的作用相当于自动获取和释放锁(资源)
        new  = value +1
        time.sleep(0.001)
        value = new

threads = []

for i in range(100):
    t = threading.Thread(target=getlock)  # 锁定期间，其他线程不可以干活
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(value)