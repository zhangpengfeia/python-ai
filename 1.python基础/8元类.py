"""
metaclass: 元类
1.元类就是创建类的类，type是python中所有类的元类。
2.元类可以自定义,必须继承type
"""
# 1.
class Dog:
    pass
# 等于
class Dog(metaclass=type):
    pass
# 等于
Dog = type("Dog",(),{})
# 等于
Dog = type.__call__(type, "Dog",(),{})
d = Dog()
# 等于
d = type.__call__(Dog)

# 2.自定义元类
class MyMeta(type):
    # 控制类的创建 new 和 init
    def __new__(cls, name, bases, namespace):
        print("MyMeta new")
        return super().__new__(cls, name, bases, namespace)
    def __init__(self, name, bases, namespace):
        print("MyMeta init")
        super().__init__(name, bases, namespace)

    # 控制实例的创建
    def __call__(cls, *args, **kwargs):
        print("MyMeta call")
        return super().__call__(*args, **kwargs)

class Dog(metaclass=MyMeta):
    pass
Dog = type.__call__(MyMeta, "Dog",(),{})
d = MyMeta.__call__(Dog)