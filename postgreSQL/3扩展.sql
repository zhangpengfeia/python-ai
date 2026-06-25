
/*
postgres其它能力：
1.备份与恢复
2.锁
3.视图
4.物化识图
5.存储过程
6.触发器
7.CTE表达式
8.全文检索
  比 like 更高效精准，适合复杂丰富条件查询，默认支支持英文，安装插件支持中文
9.GIN索引
    加速全文检索查询
10.BRIN 索引，轻量级索引，按数据在磁盘上的物理块范围建立索引，占用空间小
11.FDW外部表
   可以在postygresql里直接查询另一个数据库，甚至CSV文件
12.JSON,JSONB
    postgreSQL默认支持JSON，JSONB是JSON的二进制格式，性能更高，支持检索

数据库分类：
1.关系型数据库(主流)：MySQL,PostgreSQL,Oracle,SQL Server,DB2,MariaDB,SQLite
2. 文档型数据库(主流)：MongoDB,CouchDB,Couchbase,Redis,ElasticSearch,DynamoDB
3. 键值对数据库(主流)：Redis,DynamoDB,Leveldb
4. 列族数据库：HBase
5. 图数据库：Neo4j,OrientDB,Titan

数据库设计三范式：
1.第一范式：列不可再分，每列都是原子值，一个格子只存一个值，不存数组或复合数据
2.第二范式：满足第一范式 + 非主键列完全依赖主键（消除部分依赖）
3.第三范式：满足第二范式 + 不能直接依赖非主键列
*/