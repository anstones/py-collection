#!/usr/bin/env python
# -*- encoding: utf-8 -*-

### 绑定回调
import time
import asyncio
 
now = lambda : time.time()
 
async def do_some_work(x):
    print('Waiting: ', x)
    return 'Done after {}s'.format(x)
 
def callback(future):  # 回调函数
    print('Callback: ', future.result())
 
start = now()
 
coroutine = do_some_work(2)

loop = asyncio.get_event_loop()

task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)  # 添加回调函数

loop.run_until_complete(task)
 
print('TIME: ', now() - start)