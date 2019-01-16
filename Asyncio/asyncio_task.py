#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import asyncio

#### Task
async def nested():
    await asyncio.sleep(2)
    print("等待2s")

# async def main(lp):
async def main():
    # 将协程包装成任务含有状态
    # task = asyncio.create_task(nested())   python3.7 才有
    # task = lp.create_task(nested())        通过loop.create_task  创建任务
    task = asyncio.ensure_future(nested())
    print(task)
    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task
    print(task)
    print(task.done())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        # loop.run_until_complete(main(loop))
        loop.run_until_complete(main())
    except KeyboardInterrupt as e:
        for task in asyncio.Task.all_tasks():
            print(task)
            task.cancel()
            print(task)
        loop.run_forever()  # restart loop
    finally:
        loop.close()

