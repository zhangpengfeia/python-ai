"""
上下文管理：
1. 入口__enter__和出口__exit__
"""
# 文件操作 —— 自动关闭文件
# with open("data.txt", "r") as f:
#     content = f.read()
#     # 离开 with 块时，文件自动关闭
# # 等价于
# f = open("data.txt", "r")
# try:
#     content = f.read()
# except Exception as e:
#     stopPropagation = f.__exit__(type(e), e, e.__traceback__)
#     if not stopPropagation:
#         raise
# else:
#     f.__exit__(None, None, None)
# # 为什么不直接 f = open("file.txt", "r")，因为在with里，可以自动退出，入口__enter__和出口__exit__
#
# # @contextmanager，可以把一个函数的返回结果变成上下文管理器
# from contextlib import contextmanager
# @contextmanager
# def managed_resource(name):
#     """用生成器实现上下文管理器"""
#     print(f"获取资源: {name}")
#     resource = {"name": name, "status": "active"}
#     try:
#         yield resource  # yield 之前的代码等价于 __enter__
#     finally:
#         print(f"释放资源: {name}")  # yield 之后的代码等价于 __exit__
# # 使用
# with managed_resource("database") as res:
#     print(f"使用资源: {res}")
# # 获取资源: database
# # 使用资源: {'name': 'database', 'status': 'active'}
# # 释放资源: database
#

from contextlib import contextmanager
import time

# @contextmanager
# def timer(task_name: str):
#     start = time.perf_counter()
#     yield
#     end = time.perf_counter()
#     cost = end - start
#     print(f"{task_name} 耗时: {cost:.4f} 秒")
# # 使用示例
# if __name__ == "__main__":
#     with timer("数据处理"):
#         time.sleep(1)
#         print("处理完成")
import tempfile
import shutil

# @contextmanager
# def TempDirectory():
#     tmp_dir = tempfile.mkdtemp()
#     try:
#         yield tmp_dir
#     finally:
#         shutil.rmtree(tmp_dir)
#
# with TempDirectory() as tmp_dir:
#     print(f"临时目录: {tmp_dir}")
#     # 可以在这个目录中创建文件
#     # 离开 with 块时，目录及其内容自动删除
#
# print("临时目录已清理")

@contextmanager
def demo():
    print("进入")
    try:
        yield
    except Exception as e:
        print(f"捕获异常: {e}")
    finally:
        print("清理")


with demo():
    print("执行中")
    raise ValueError("出错了")
