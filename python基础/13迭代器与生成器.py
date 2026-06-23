"""
Iterator: 迭代器
yield：生成器
1. 实现了 __iter__ 和 __next__ 方法，就是迭代器
2. 只要一个对象实现了 __iter__() 方法，并返回了迭代器，那它就是可迭代对象
3. 生成器本身就是个迭代器，类似 es6 的 generator
"""
class MyIterator:
    def __iter__(self):
        return self # 必须返回迭代器，99%都是返回自身
    def __next__(self):
        pass # 返回下一个元素

class CountdownInterator:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current < 0:
            raise StopIteration
        self.current -= 1
        return self.current

class Countdown:
    def __init__(self, start):
        self.start = start
    def __iter__(self):
        return CountdownInterator(self.start) # 返回新的迭代器

c1 = iter(Countdown(10)) # 创建迭代器
for i in c1: # 消费者
    print(i)
print(3 in Countdown(2))
print(any(Countdown(2)))
c2 = iter(Countdown(10))

# 列表推导式
print([i for i in range(10) if i % 2 == 0])
# 嵌套推导式
matrix = [[1,2,3],[4,5,6],[7,8,9]]
print([x for row in matrix for x in row])
# 字典推导式
print({x: x**2 for x in range(5)})
# 集合推导式
print({x for x in range(5)})
# 元组没有推导式

# 生成器函数
def simple_generator():
    print("开始执行")
    yield 1
    print("继续执行")
    yield 2
    print("结束执行")
    yield 3
for i in simple_generator():
    print(i)
# 生成器表达式
squares_gen = (x**2 for x in range(1000000))

def paginated_query(total_items, page_size):
    for i in range(0, total_items, page_size):
        end = min(i+page_size, total_items)
        yield list(range(i, end))
    pass


for page in paginated_query(25, 10):
    print(page)