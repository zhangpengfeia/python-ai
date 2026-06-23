"""
描述符
1.描述符类，只要包含 __get__, __set__, -_delete__ 任意一个，即可称为描述符类
2.如果有set和delete任意一个，则叫数据描述符，如果只有get，则叫非数据描述符
3.访问类属性顺序：
    1.数据型描述符（类属性）
    2.实例属性（instance.__dict__）
    3.类属性（普通）
    4.父类...
应用场景：
"""
# 描述符类
class Descriptor:
    def __set_name__(self, owner, name): # py3.6新增的
        print(f"{name} is set")
    def __get__(self, instance):
        print("__get__")
    def __set__(self, instance, value): # self=Descriptor, instance=MyClass, value=10
        print(instance)
        print("__set__")
    def __delete__(self, instance):
        print("__delete__")

# 3.类属性访问
class MyClass:
    desc_attr = Descriptor() # 描述符对象，描述符，数据描述符
ins = MyClass()
print(ins.desc_attr)
MyClass.desc_attr=10 # 直接覆盖描述符对象，变成属性描述符

# 手写@property装饰符
import math

# class RadiusDecorator:
#     def __set__(self, instance, value):
#         if value < 0:
#             raise ValueError("半径不能是负数")
#         instance._radius = value

#     def __get__(self, instance, owner):
#         return instance._radius

#     def __delete__(self, instance):
#         raise AttributeError("不能删除半径属性")


class MyProperty:
    def __init__(self, get_func=None, set_func=None, delete_func=None):
        self.get_func = get_func
        self.set_func = set_func
        self.delete_func = delete_func

    def __get__(self, instance, owner):
        if self.get_func is None:
            raise AttributeError("属性不可读")
        return self.get_func(instance)

    def __set__(self, instance, value):
        if self.set_func is None:
            raise AttributeError("属性不可写")
        self.set_func(instance, value)

    def __delete__(self, instance):
        if self.delete_func is None:
            raise AttributeError("属性不可删除")
        self.delete_func(instance)

    def setter(self, func):
        self.set_func = func
        return self

    def deleter(self, func):
        self.delete_func = func
        return self


class Circle:

    @MyProperty
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能是负数")
        self._radius = value

    @radius.deleter
    def radius(self):
        raise AttributeError("不能删除半径属性")

    @MyProperty
    def area(self):
        return math.pi * self.radius**2

    @MyProperty
    def circumference(self):
        return 2 * math.pi * self.radius

    @MyProperty
    def diameter(self):
        return 2 * self.radius

    def __init__(self, radius=5):
        self.radius = radius


c = Circle(5)
print(c.radius, c.area, c.circumference, c.diameter)
c.radius = 10
print(c.radius, c.area, c.circumference, c.diameter)
# 装饰器(可调用对象) --> 返回任何东西

