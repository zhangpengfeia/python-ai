"""
模块化：
包：目录，模块：python文件，成员：全局定义的东西
1. import 关键词导入
2. 导入模块有缓存机制，多次导入缓存
3. python 有内置模块
    sys，fs等
from module import * 导入全部，会造成变量冲突
相对导入符号：
. —— 当前包
.. —— 父包
... —— 祖父包
"""
from module import add,PI
print(add(1,2))
print(PI)
print(__name__)