"""
协程Coroutine：在一个线程里，类似多线程效果，可以解决异步的回调地狱
1.当一个函数使用async标记则是协程
2.调用协程函数时，会得到一个协程对象 class coroutine，底层生成器实现，但是没有__next__
3.协程是单线程由事件控制，而多线程是操作系统控制的。
4..send 驱动协程函数执行 ，或使用 asyncio.create_task(test()）循环驱动
5.asyncio.run(协程对象) api，自动开启事件循环，自动绑定循环回调，自动task()，返回result
6. await 可以等待一个协程对象，也可以等待一个task(Future)，实际等待的是awaitable协议__await__
"""
import asyncio
def async_delay(duration: int):
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    loop.call_later(duration, future.set_result, None)
    return future

from typing import Coroutine
def gather(*aws: Coroutine) -> asyncio.Future:
    # 1.获取任务数量 2.根据任务数量添加callback, 3.返回future
    future = asyncio.Future()
    count = 0 # 任务已完成数量
    taskslen = len(aws) # 任务数量
    contexts = [None] * taskslen  # 文本列表

    def on_done(f: asyncio.Future, idx: int):
        nonlocal count
        print(f.result())
        contexts[idx] = f.result()
        count += 1
        if count == taskslen:
            future.set_result(contexts)
    for (i, aw) in enumerate(aws):
        asyncio.create_task(aw).add_done_callback(lambda f, idx=i: on_done(f,idx))
    return future

async def coro(name: str, duration: int):
    await async_delay(duration)
    return f"{name} 完成"

import asyncio
class Event:
    def __init__(self):
        self.futures = None
    def set(self):
        if self.futures:
            self.futures.set_result(1)
    async def wait(self):
        loop = asyncio.get_running_loop()
        self.futures = loop.create_future()
        await self.futures

    pass
async def test():
    event = Event()
    async def waiter():
        print("waiter: 开始等待")
        await event.wait()
        print("waiter: 被唤醒")
    async def setter():
        print("setter: 1秒后设置事件")
        await async_delay(1)
        event.set()
        print("setter: 事件已设置")
    await gather(waiter(), setter())
asyncio.run(test())

# 预期结果：
""" 
waiter: 开始等待
setter: 1秒后设置事件
setter: 事件已设置
waiter: 被唤醒 
"""