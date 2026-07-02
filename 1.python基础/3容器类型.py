# 列表，内部使用动态数组
list1 = [1, 2, 3, 4, 5]
# print(list1[::4]) # 步长
# print(list1[::-2]) # 倒步长
# print(list1[:4])

# 元组，列表一旦创建，就不能修改，内部使用静态数组
tuple1 = (1, 2, 3, 4, 5)
x, *y = tuple1 # 元组解包
# print(x)
# print(tuple1[0])      # 1
# print(tuple1[-1])     # 5
# # 查询（不能修改）
# print(tuple1.index(2))    # 1
# print(tuple1.count(3))    # 2
# print(6 in tuple1)        # True

# 字典，键值对
dict1 = {"name": "Alice", "age": 25, "city": "New York"}
print(dict1["name"])
print(dict1.get("gender"))  # 安全访问 None（不报错）
# 批量更新
dict1.update({"phone": "123456", "age": 27})
# 删除
del dict1["phone"]          # 删除键值对
value = dict1.pop("age")    # 删除并返回值
last = dict1.popitem()      # 删除并返回最后插入的键值对（Python 3.7+）
dict1.clear()               # 清空

# set集合，内部使用hashSet，不允许重复
set1 = {1, 2, 3, 4, 5}
# 添加/删除
set1.add(4)          # {1, 2, 3, 4}
set1.remove(2)       # {1, 3, 4} —— 不存在会报错
set1.discard(10)     # 不报错，即使不存在
set1.pop()           # 随机删除并返回一个元素
set1.clear()         # set()
# 去重利器
nums = [1, 2, 2, 3, 3, 3]
unique = list(set(nums))   # [1, 2, 3]（顺序可能不同）

# str，可重复
str1 = "hello world"
# str1[0] = '2' # ❌

# 通用操作函数
# len() —— 获取元素个数
len([1, 2, 3])       # 3
len((1, 2, 3))       # 3
len({"a": 1, "b": 2}) # 2（键值对数量）
len("hello")         # 5
# max() / min() —— 最大/最小值
max([3, 1, 4, 1, 5])  # 5
min((3, 1, 4))        # 1
max("hello")          # 'o'（按字符编码）
# sum() —— 求和（元素必须是数字）
sum([1, 2, 3, 4])     # 10
sum((1, 2, 3))        # 6
# sorted() —— 排序，返回新列表
sorted([3, 1, 2])           # [1, 2, 3]
sorted((3, 1, 2))           # [1, 2, 3] —— 返回列表
sorted("cba")               # ['a', 'b', 'c']
sorted([3, 1, 2], reverse=True)  # [3, 2, 1]
# reversed() —— 反转，返回迭代器
list(reversed([1, 2, 3]))   # [3, 2, 1]
list(reversed("abc"))       # ['c', 'b', 'a']

# True
a = 1
b = 1.0
print(a == b) # ❗ python中==不比较内存地址
a = [1,2,{"a":1}]
b = [1,2,{"a":1}]
print(a is b) # ✔ False

# 遍历for,
# enumerate() —— 索引迭代
# zip() —— 组合迭代
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["北京", "上海", "广州"]
for name, age, city in zip(names, ages, cities):
    print(f"{name} 今年 {age} 岁，住在 {city}")

