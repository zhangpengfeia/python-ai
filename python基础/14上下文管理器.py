"""
上下文管理：
1. 入口__enter__和出口__exit__
"""
# 文件操作 —— 自动关闭文件
with open("data.txt", "r") as f:
    content = f.read()
    # 离开 with 块时，文件自动关闭
# 等价于
f = open("data.txt", "r")
try:
    content = f.read()
except Exception as e:
    stopPropagation = f.__exit__(type(e), e, e.__traceback__)
    if not stopPropagation:
        raise
else:
    f.__exit__(None, None, None)
# 为什么不直接 f = open("file.txt", "r")，因为在with里，可以自动退出，入口__enter__和出口__exit__

# @contextmanager，可以把一个函数的返回结果变成上下文管理器
from contextlib import contextmanager
@contextmanager
def managed_resource(name):
    """用生成器实现上下文管理器"""
    print(f"获取资源: {name}")
    resource = {"name": name, "status": "active"}
    try:
        yield resource  # yield 之前的代码等价于 __enter__
    finally:
        print(f"释放资源: {name}")  # yield 之后的代码等价于 __exit__
# 使用
with managed_resource("database") as res:
    print(f"使用资源: {res}")
# 获取资源: database
# 使用资源: {'name': 'database', 'status': 'active'}
# 释放资源: database
