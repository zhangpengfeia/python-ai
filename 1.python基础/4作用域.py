# 局部作用域 Local
# 全局作用域 Global
# 外部作用域 Enclosing
# 内置作用域 Built-in
# x = 1 # 全局作用域
# def m():
#     x = 2 # 局部作用域
#     print(x)
# m()
#
# # 函数在编译时，默认值default使用的是同一个
# def a(item, default=[]): # 可以使用 default=None解决
#     default.append(item)
#     return default
# print(a(1)) # [1]
# print(a(2)) # [1, 2]

# def make_multiplier(x):
#     def fun(n):
#         return x * n
#     return fun
# tri = make_multiplier(3)
# print(tri(3))
# print(tri(10))
# tri = make_multiplier(2)
# print(tri(2))
# print(tri(10))

def create_account(x):
    num = x
    def deposit(y):
        nonlocal num
        num += y
        return num
    def withdraw(a):
        nonlocal num
        num -= a
        return num
    return deposit, withdraw

deposit, withdraw = create_account(100)
print(deposit(10))
print(deposit(20))