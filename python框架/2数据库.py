"""
sqlAlchemy特性：
1. 提供异步数据库连接池管理
2. 提供数据库模型定义
3. 支持多数据库连接，数据库大部分语法解耦

过程：
1.create_url 后创建 engine，一个数据库只创建一个engine单例模式，多数据库多engine
2.connection 连接数据库
ORM：对象关系映射

=======================
crud: 
core模式，
    Raw SQL
        直接运行sql, 不建议使用，有sql注入风险
        解决方案是：SQL 结构与数据分离。用 :参数名 作为占位符，通过字典传入值：
         result = await conn.execute(
            text("SELECT * FROM product WHERE name LIKE :keyword"),
            {"keyword": f"%{keyword}%"},
        )
    SQL表达式
ORM模式

"""


