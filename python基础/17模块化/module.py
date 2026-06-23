
"""
除了私有变量，python会默认导出所有函数和变量
"""
__all__: list[str] = ["PI", "add"]  # 只导出 PI 和 add

PI: float = 3.14159
E: float = 2.71828  # 没有在 __all__ 中，from import * 不会导入
def add(a: int, b: int) -> int:
    return a + b
def subtract(a: int, b: int) -> int:  # 不在 __all__ 中
    return a - b
# 私有变量
_private_add: int = 42
def _internal_helper(a: int) -> int:  # "私有"——约定外部不应使用
    return a * 2
print(__name__)
