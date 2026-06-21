line = input("请输入数字")
line2 = input("输入数字2")
print(f"{line}+{line2} = {int(line)+int(line2)}")

# if True:
#     print("true")

# 变量定义
# a = 10
# b = 3.5
# c = "Python"
# d = True
# e = None
#
# # 1. 数据类型与 type 函数
# print(type(a)) # int
# print(type(b)) # float
# print(type(c)) # str
# print(type(d)) # bool
# print(type(e)) # NoneType
# print(type(a) == int) # True
#
# # 2. 变量类型转换
# print(int(b)) # 3
# print(float(a)) # 10
# print(str(a) + c) # 10Python
# print(bool(0)) # False
# print(bool("")) # False
# print(bool("hello")) # True
#
# # 3. 算术运算符
# print(a + 5) # 15
# print(a / 4) # 2.5
# print(a // 4) # 2
# print(a % 4) # 2
# print(a ** 2) # 100
# print(c * 2) # PythonPython
#
# # 4. 字符串格式化（f-string）
# name = "Alice"
# age = 25
# print(f"姓名: {name}, 年龄: {age}") # 姓名: Alice, 年龄: 25
# print(f"明年{age + 1}岁") # 明年26岁
# print(f"{a} + {5} = {a + 5}") # 10 + 5 = 15
#
# # 5. 比较运算符与链式比较
# print(a > 5) # True
# print(a == 10) # True
# print(5 < a < 20) # True
# print(c == "python") # False
# print("A" < "a") # True
#
# # 6. 逻辑运算符
# print(True and False) #  False
# print(True or False) # True
# print(not d) # False
# print(0 and 5) # 0
# print(3 or 5) # 3
# print("" and "hello") # ""
# print("hi" or "hello") # "hi"
# print(not None) # True
#
# # 7. 三元运算符
# score = 85
# result = "及格" if score >= 60 else "不及格"
# print(result) # 及格
# level = "A" if score >= 90 else ("B" if score >= 80 else "C")
# print(level) # B
#
# # 8. 赋值运算符
# x = 10
# x += 5
# print(x) # 15
# x -= 3
# print(x) #12
# x *= 2
# print(x) # 24
# x /= 4
# print(x) #6
#
# s = "Hi"
# s += " Python"
# print(s) # Hi Python
# s *= 2
# print(s) # Hi PythonHi Python


# 1. while 循环 + if-else
# n = 1
# result = 0
# while n <= 5:
#     if n % 2 == 0:
#         result += n
#     else:
#         result -= n
#     n += 1
# print(result)
#
# # 2. continue 和 break
# num = 1
# while num <= 10:
#     if num == 3:
#         num += 1
#         continue
#     if num == 7:
#         break
#     print(num)
#     num += 1
#
# # 3. 循环 else 子句
# i = 0
# while i < 3:
#     print(i)
#     i += 1
# else:
#     print("end")
#
# # 4. 嵌套条件
# x = 15
# if x < 10:
#     print("A")
# elif x < 20:
#     if x % 2 == 0:
#         print("B")
#     else:
#         print("C")
# else:
#     print("D")
#
# # 5. 综合练习
# a = 1
# b = 0
# while a <= 5:
#     if a == 3:
#         b += 10
#     elif a % 2 == 0:
#         b += a * 2
#     else:
#         b += a
#     a += 1
# print(b)