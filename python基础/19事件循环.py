"""
python 事件循环
1.同步代码：I/O操作，input/output，网络，文件，控制台输入输出，ui界面交互事件，延迟操作
2.同步代码依次执行需要等待会阻塞，异步，多线程来解决阻塞解决方案：
运算密集型：多线程
I/O密集型：异步
3.事件循环时实现异步的基础手段 AbstractEventLoop类
"""
# 事件循环需要手动创建
import asyncio
# 创建一个新的事件循环对象
loop = asyncio.new_event_loop()
# 绑定事件循环到当前线程
asyncio.set_event_loop(loop)
# 获取当前线程的事件循环
current_loop = asyncio.get_event_loop()
print("当前事件循环:", current_loop)
# 移除事件循环绑定
asyncio.set_event_loop(None)
# 运行事件循环
# 陷入死循环，除非在循环中终止，否则后续代码永远无法得到运行
current_loop.run_forever()
# 停止事件循环
current_loop.stop()
"""
_run_once（） 方法核心调用事件循环中的队列，确保每次该方法运行，都能保证ready队列中的所有回调得到执行
1. 检查延时队列，加入ready,
2.计算等待时间timeout 
    a.ready有任务，timeout=0不等待 
    b.延时队列有任务时等待timeout = 延时队列队首-当前时间
    c.i/o,延时队列都没有任务时等待 timeout = None
3.用timeout的时间阻塞线程，等待I/O，期间有任何IO任务马上加入ready队列
4.复制ready队列中的所有任务，到执行队列中
"""