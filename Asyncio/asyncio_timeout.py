#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import asyncio

#### timeout
async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print('yay!')

async def main():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# asyncio.run(main())    python3.7 才有，可直接用run方法调用async定义的协程函数执行
