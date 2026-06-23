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