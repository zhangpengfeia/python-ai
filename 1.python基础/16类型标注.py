"""
类型标注
"""
# 声明变量的类型
# 声明变量的类型
name: str = "Alice"
age: int = 25
pi: float = 3.14
is_active: bool = True
# 没有初始值
value: int
value = 10
# Python 是动态语言，类型标注不会强制约束
x: int = "hello"  # 不会报错，但类型检查工具会提示

def greet(name: str, age: int) -> str:
    """函数参数和返回值的类型标注"""
    return f"{name} 今年 {age} 岁"
# 调用
greet("Alice", 25)        # 正确
greet("Alice", "25")      # 运行不会报错，但类型检查会警告

from typing import Optional, Union
# Optional：值可以是某个类型，也可以是 None
def find_user(user_id: int) -> Optional[str]:
    """返回用户名，找不到时返回 None"""
    if user_id <= 0:
        return None
    return f"User_{user_id}"
# Union：值可以是多种类型之一
def parse_value(value: str) -> Union[int, float, str]:
    """尝试将字符串转换为数字，失败则返回原字符串"""
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
from typing import Any, TypeAlias


# Any：任意类型，相当于没有类型约束
def log_data(data: Any) -> None:
    print(f"数据: {data}")


# 类型别名，让复杂类型更易读
Vector: TypeAlias = List[float]
Matrix: TypeAlias = List[List[float]]

def dot_product(v1: Vector, v2: Vector) -> float:
    """计算两个向量的点积"""
    return sum(a * b for a, b in zip(v1, v2))