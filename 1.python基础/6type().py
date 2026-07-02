"""
⚠ 所有的对象都是通过类创建的，创建对象的类，称之为该对象的类型（也有所属类的说法）
1.所有函数的类型是function
2.所有类的类型是type
3.创建类的类，称之为元类（metaclass）
    因为type创建了class，所以type就是class的元类
"""

# type创建class 类名A, 父类名(), 属性名attr
A = type("A",(), {
    "attr": 1
})
a = A()
print(a)

class A:
    _a = 1  # 约定私有成员，外部仍然可以访问，大部分情况用它
    __a = 2  # 严格私有成员，外部无法直接访问__a
    __a__ = 3  # 有特殊作用的成员，往往是系统内置的
    @classmethod # 类方法，第一个参数是类本身，可以访问类属性
    def test(cls):
        print(cls._a, cls.__a, cls.__a__)  # 内部可以访问所有成员


# MRO
"""
类似于js原型继承，python是基于类的继承
"""
print(A.__mro__) # 继承链
print(A.mro()) # 继承链
