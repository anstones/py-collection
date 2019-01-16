#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import asyncio

#### 并发的执行任务
async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        if number == 2:
            1 / 0
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def main():
    # Schedule three calls *concurrently*:
    res = await asyncio.gather(
        *[factorial("A", 2),
          factorial("B", 3),
          factorial("C", 4)]
        , return_exceptions=True) # return_exceptions=True来保证了如果其中一个任务出现异常，其他任务不会受其影响会执行到结束。
    for item in res:
        print(item)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt as e:
        for task in asyncio.Task.all_tasks():
            print(task)
            task.cancel()
            print(task)
        loop.run_forever()  # restart loop
    finally:
        loop.close()
