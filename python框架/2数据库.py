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
crud: create read update delete
core模式：
    RawSQL
        直接运行sql, 不建议使用，有sql注入风险
        解决方案是：SQL 结构与数据分离。用 :参数名 作为占位符，通过字典传入值：
         result = await conn.execute(
            text("SELECT * FROM product WHERE name LIKE :keyword"),
            {"keyword": f"%{keyword}%"},
        )
    SQL表达式
        基于代码格式的sql表达式，先编译再执行不会产生注入攻击，次要选择
        ins = insert(Product).values(name="test", price=100)
        await conn.execute(ins)
ORM模式：
    会话：和orm对接，和数据库连接语法类似
    session_factory = async_sessionmaker(engine) # 创建会话工厂
        async with session_factory() as session: # 创建会话
            await session.execute(ins) # 执行sql语句
            await session.commit() # 提交事务
            await session.rollback() # 回滚事务

        # 最常见的情况是，会话工厂创建会话，会话上下文管理事务
        async with session_factory.begin() as session: # 开启事务上下文管理
            await session.execute(ins) # 执行sql语句
    session会跟踪模型对象的变化
        1. 修改，新增自动记录操作
        2. 退出上下文管理时，会自动提交，查询记录的操作，交给方言转为sql语句执行
        3. 提交事务
    
    session.flush() 手动将session中pending的操作 flush到数据库，再执行传入的sql
    session.refresh() 手动同步模型对象，不提交
   """


"""
数据迁移：alembic
 禁区：1.不许手动修改数据库。2.不许修改已执行过的迁移3.迁移脚本时常量，不允许变更
1.改模型
2.生产迁移文件
3.升级数据库
"""