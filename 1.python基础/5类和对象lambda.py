# lambda 和 函数区别
"""
1. lambda 没有函数名字
2. lambda 只能包含一个表达式
3. lambda 自动返回不用return
4. 适用临时简单逻辑
"""

# class定义
class Dog:
    species = "Canis familiaris" # 类属性
    # 构造器
    def __init__(self, name, age):
        self.name = name # 实例属性
        self.age = age
    # 自定义方法，第一个参数必须是self，如果不传则默认self
    def bark(self):
        return "Woof!"
    # 静态方法，没有self，只是一个普通函数，但属于类
    @staticmethod
    def static_method():
        return "This is a static method"

my_dog = Dog("小白", 3)
# print(my_dog.species) # 实例可以直接访问类属性
print(Dog.bark(my_dog))

# class单继承
class GoldenRetriever(Dog):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    def bark(self):
        return "Woof! Woof!"
print(Dog.__base__)
print(GoldenRetriever.__bases__)

# class多继承
"""
    多继承时，如果多个父类有同名方法，则优先继承参数的第一个父类的方法
    Animal > Dog > Duck
"""
class Duck:
    def __init__(self):
        print("Duck init")
class Animal(Dog,Duck):
    def __init__(self, name):
        self.name = name
        super().__init__() # 调用Dog的初始化方法
print(Animal.__bases__)


