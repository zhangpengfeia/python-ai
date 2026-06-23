"""
装饰器
1. 接收一个可调用对象，返回一个可调用对象
2. 多个装饰器叠加执行顺序从上到下
"""

def my_decorator(func):
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

# 下面的代码
def say_hello():
    print("Hello!")
say_hello = my_decorator(say_hello)

# 等效于
@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# 输出：
# 函数执行前
# Hello!
# 函数执行后

# @decorator_a
# @decorator_b
# def func():
#     pass

# 等效于：
# func = decorator_a(decorator_b(func))

def cache(func):
    _cache = {}

    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
        return _cache[key]

    return wrapper


@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
print(fibonacci(60))  # 应该快速返回结果，输出: 9227465
