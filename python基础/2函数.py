
def add(a,b):
    print(a+b)

def sum_all(*args):
    print(type(args))

sum_all(1,2,3,4,5)

def print_name(**kwargs):
    """
    参数:
        kwargs
    文档注释
    """
    print(type(kwargs))


print_name(name="Alice", age=25)