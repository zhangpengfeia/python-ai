"""
魔术方法
1. 在特点场景自动触发就是魔术方法，比如 class中 __new__ __init__
2. 一般 __xx__ 都是魔术方法
常用魔术方法速查
类别	方法	触发场景
构造	__init__	创建对象后初始化
构造	__new__	创建对象（已讲过）
字符串	__str__	print()、str()
字符串	__repr__	repr()、交互式显示
比较	__eq__	==
比较	__lt__	<
比较	__gt__	>
比较	__le__	<=
比较	__ge__	>=
比较	__ne__	!=
算术	__add__	+
算术	__sub__	-
算术	__mul__	*
算术	__truediv__	/
容器	__len__	len()
容器	__getitem__	obj[key]
容器	__setitem__	obj[key] = value
容器	__delitem__	del obj[key]
容器	__contains__	in
容器	__iter__	for...in
转换	__int__	int()
转换	__float__	float()
转换	__bool__	bool()
可调用	__call__	obj()
属性	__getattr__	访问不存在的属性
属性	__getattribute__	访问任意属性
属性	__setattr__	设置属性
属性	__delattr__	删除属性
生命周期	__del__	对象销毁
"""
