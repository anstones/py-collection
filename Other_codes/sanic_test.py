#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
对我一个初学者来说，经常被各种async、asyncio、await、asyncpg、aiohttp、uvloop搞糊涂，谁是谁

1、以前的异步是多线程，涉及到锁的问题，非常难设计

2、现代大部分语言所实现的异步都是协程Coroutine（一个线程下运行），当然是有很多优点，才会这么火，async是异步的意思、
   coroutine是协程的意思，而asyncio是python的原生异步类库。

3、C#很早就有协程async/await实现

4、python从3.4开始原生支持asyncio，通过生成器和装饰器来实现。到了3.5也实现了async/await语法糖（代码中的一种漂亮的写法）。

5、现在java、nodejs、php、go、js都有一样的实现。php下最完善的async库是swoole。

6、在原生asyncio库的支持下，产生了一个aio系列的类库，包括aiohttp、aiopg、aiomysql、aioredis等等。这个系列的优势就是很完备。

7、python原生的pg数据库驱动是psycopg，除了aio实现的aiopg，另外还有asyncpg非常好用

8、gevent是基于greenlet协程库、基于libevent循环实现的异步事件框架，也算是很火的异步机制。

8、大名鼎鼎的uvloop。用cython编写的基于libuv循环的异步框架。这个uvloop号称就是比原生的快很多。写起来不用改变原生的语法。

9、Twisted是较早的使用异步和工厂的框架，后来都用tornado了，性能上tornado更好一点，flask也能使用类库实现异步协程。
   但是现在有了sanic，又一次超越了tornado。sanic号称python下效率最高的框架。

"""

from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.route("/")
async def test(request):
    return json({"hello": "world"})

app.run(host="0.0.0.0", port=8000)



import asyncio
import time

async def my_work():
    print("开始执行任务")
    time.sleep(5)
    print("任务完成")

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(my_work())
finally:
    loop.close()

