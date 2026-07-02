"""
Future类
类似于Promise，更加方便处理异步任务
1.每个 Future 都有两种状态，并且状态确定后不可修改：
    未完成：表示任务还在等待；
    已完成：表示任务已有结果，正常完成，错误情况，取消情况。
"""
# 通过事件循环创建Future
import asyncio
loop = asyncio.new_event_loop()
fut = loop.create_future()  # 通过事件循环对象创建Future
# print(fut.done())  # False，未完成
# print(fut.result())  # 引发InvalidStateError异常
# 让fut完成
# fut.set_result("result")  # 设置完成结果的值
# print(fut.done(), fut.result())  # 是否完成、完成结果，打印：True result

# 发生异常
# fut.set_exception(TypeError("类型异常"))  # 设置异常
# print(fut.done(), fut.exception())
# print(fut.result())  # 此时获取result会引发异常

# 取消
# fut.cancel("不等了")  # 取消future
# print(fut.done(), fut.cancelled())  # 已完成、已取消
# print(fut.result())  # 获取结果会引发CancelledError异常
# print(fut.exception())  # 获取异常结果同样会引发CancelledError异常

# 通过run方法创建Future
import asyncio
import socket
def run(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.call_soon(func)
    loop.run_forever()

# 封装异步网络请求
# 连接
def async_connect(host: str, port: int) -> asyncio.Future:
    loop = asyncio.get_running_loop()  # 获取当前的事件循环
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个socket
    sock.setblocking(False)  # 设置为非阻塞模式
    try:
        sock.connect((host, port))
    except BlockingIOError:
        pass
    fut = asyncio.Future()
    def on_writable() -> None:
        err = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) # 判断链接是否错误
        loop.remove_writer(sock) # 建立连接后，不需要监听，删除I/O队列任务
        if err == 0:
            fut.set_result(sock)
        else:
            fut.set_exception(ConnectionError(f"Connect failed: {err}"))

    # 监听文件描述符的可写事件，当socket连接成功时，文件描述符会变为可写
    loop.add_writer(sock, on_writable)
    return fut

# 请求
def async_read(sock: socket.socket, host: str, port: int, path: str) -> asyncio.Future:
    loop = asyncio.get_running_loop()
    fut = asyncio.Future()
    req = f"""GET {path} HTTP/1.1
    Host: {host}:{port}
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,ru;q=0.6
    Cache-Control: no-cache
    Connection: close
    Pragma: no-cache
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36
    """.replace("\n", "\r\n")
    sock.setblocking(False)
    sock.send(req.encode())
    data = b""
    def on_readable() -> None:
        nonlocal data
        try:
            chunk = sock.recv(4096)
            if chunk:
                data += chunk
            else:
                loop.remove_reader(sock)
                fut.set_result(data.decode())
        except BlockingIOError:
            pass

    loop.add_reader(sock, on_readable)
    return fut

def async_request(host: str, port: int, path: str) -> asyncio.Future:
    fut = asyncio.Future()
    def on_connected(f: asyncio.Future) -> None:
        try:
            sock = f.result()
            read_fut = async_read(sock, host, port, path)
            read_fut.add_done_callback(lambda rf: fut.set_result(rf.result()))
        except Exception as e:
            fut.set_exception(e)

    connect_fut = async_connect(host, port)
    connect_fut.add_done_callback(on_connected)
    return fut
