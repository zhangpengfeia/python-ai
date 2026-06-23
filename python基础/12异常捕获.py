"""
异常捕获
异常类型：
BaseException
 ├── SystemExit          # sys.exit() 引发
 ├── KeyboardInterrupt   # Ctrl+C 引发
 └── Exception           # 常规异常的基类
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      └── ...
"""
try:
    number = int("abc")
except ValueError as e:
    print(f"数值错误: {e}")
except TypeError as e:
    print(f"类型错误: {e}")
else:
    print("没有异常时执行")
finally:
    print("始终会执行")