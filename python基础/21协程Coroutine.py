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
def gather(*aws: Coroutine) -> asyncio.Future:
    # 你的代码
    pass
async def coro(name: str, duration: int):
    await async_delay(duration)
    return f"{name} 完成"
async def main():
    results = await gather(
        coro("A", 2),
        coro("B", 1),
        coro("C", 3),
    )
    print(results)  # 预期: ['A 完成', 'B 完成', 'C 完成']
asyncio.run(main())
