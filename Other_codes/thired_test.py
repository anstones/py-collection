from concurrent.futures import ThreadPoolExecutor,as_completed
import time

"""
线程池
"""


def do_something(times):
    time.sleep(times)
    print("get page {}s finished".format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)
urls = [3, 2, 4]  # 并不是真的url
all_task = [executor.submit(do_something, url) for url in urls]

for future in as_completed(all_task):
    data = future.result()
    print("in main: get page {}s success".format(data))




