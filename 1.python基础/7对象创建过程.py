"""
总结：
1. 不同的类创建不同的对象
2. 创建对象的过程：
    1. 调用 __new__ 创建实例
    2. 类型检查：只有 obj 是 cls 的实例（或其子类的实例）时才调用 __init__
    3. 返回对象
3. 判断对象是否可以调用, callable 判断对象里面是否包含 __call__ 方法就可以被调用
4. type.__call__ 过程：
    1. 调用 type.__new__ 创建类
    2. 调用 type.__init__ 初始化类
    3. 返回类
"""
def create_object(cls, *args, **kwargs):
    # 1. 调用 __new__ 创建实例
    obj = cls.__new__(cls, *args, **kwargs)
    # 2. 类型检查：只有 obj 是 cls 的实例（或其子类的实例）时才调用 __init__
    if isinstance(obj, cls):
        obj.__init__(*args, **kwargs)
    # 3. 返回对象
    return obj


# 测试
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print("I am a init")
    def __call__(self):
        print("I am a person")
    def sayHi(self):
        print(f"my name is {self.name}, I'm {self.age} years old")

p = create_object(Person, "shae", 5)
p.sayHi()

# 判断对象是否可以调用, 对象里面包含 __call__ 方法就可以被调用
print(callable(p.sayHi))
print(type(p.sayHi))
# print(Person(1,2))
class A:
    def __call__(self):
        print("A called")

class B(A):
    def __call__(self):
        print("B called")
        super().__call__()

b = B()
b()