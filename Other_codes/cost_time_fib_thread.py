import threading
import time

lock = threading.Lock()


def lock_holder(lock):
    print('Starting')
    while True:
        lock.acquire()
        print('Holding')
        time.sleep(100)
        print('Sleep done')


def lock_release(lock):
    time.sleep(1)  # 保证顺序
    lock.release()
    print('Release it')


# holder = threading.Thread(target=lock_holder, args=(lock,), name='LockHolder')
# holder.setDaemon(True)
# holder.start()
#
# # lock_release(lock)
# release = threading.Thread(target=lock_release, args=(lock,), name='release')
# release.start()
#
# holder = threading.Thread(target=lock_holder, args=(lock,), name='LockHolder')
# holder.setDaemon(True)
# holder.start()


import time
import threading


def profile(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print('COST: {}'.format(end - start))

    return wrapper


def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


@profile
def nothread():
    fib(35)
    fib(35)


@profile
def hasthread():
    for i in range(2):
        t = threading.Thread(target=fib, args=(35,))
        t.start()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

""" 测试斐波拉契用时 """
nothread()
hasthread()


import re
mys = u'hi新手oh上o路hea多ooo多oo指教98' #提取其中的中文字符串
p = re.compile(str('[\u4e00-\u9fa5]'))
res = re.findall(p, mys)
result = ''.join(res)
print(result)