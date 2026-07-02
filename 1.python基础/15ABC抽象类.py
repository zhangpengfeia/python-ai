"""
抽象类：
1.只要继承 ABC 的类就是抽象类，抽象类不可实例化
2.子类必须实现父类方法
"""
from abc import ABC, abstractmethod
class Animal(ABC):
    @abstractmethod
    def eat(self):
        pass
class Dog(Animal):
    def eat(self):
        print("吃吃吃")
dog = Dog()
dog.eat()


from abc import ABC, abstractmethod

class Cache(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass
# 实现 MemoryCache（使用字典存储）
class MemoryCache(Cache):
    def __init__(self):
        self._cache = {}
    def get(self, key):
        print(f"从内存中获取数据: {key}")
        return self._cache.get(key)
    def set(self, key, value):
        self._cache[key] = value
        print(f"将数据保存到内存: {key}, {value}")
    def delete(self, key):
        del self._cache[key]
        print(f"从内存中删除数据: {key}")

# 实现 FileCache（使用文件存储）


from abc import ABC, abstractmethod

class A(ABC):
    @abstractmethod
    def foo(self):
        print("A.foo")
        pass

    def bar(self):
        print("A.bar")

class B(A):
    def foo(self):
        print("B.foo")

class C(B):
    pass
