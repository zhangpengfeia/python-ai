/*
事务：Transaction
1.一个连接只能创建一个事务，不同连接的事务有可能会相互影响
2.一般不会再sql里写事务，直接在代码里控制

核心特性 ACID:
1.原子性：事务中的所有操作都成功，或者都失败
2.一致性：事务开始之前和事务结束之后，数据库必须满足所有约束和规则
3.隔离性：多个事务并发执行时，彼此之间应该互不影响
4.持久性：事务一旦提交，结果就是永久的，系统崩溃也不会丢失

并行问题：
1.脏读：一个事务读到了另一个事物的提交的数据，postGreSQL不会出现脏读，其它数据库会。
2.不可重复读：一个事务正在读取数据，另一个事务正在更新数据，那么第一个事务读取的数据，在第二个事务更新完成之后，可能会被更新。
3.幻读：一个事务正在读取数据，另一个事务正在插入数据，那么第一个事务读取的数据，在第二个事务插入完成之后，可能会被插入。
4.更新丢失：两个事务同时读取同一数据并修改，后提交覆盖前的数据。

事务隔离级别：
设置隔离级别：set transaction isolation level [level];
1.READ_COMMITTED：可能：不可重复读，幻读，更新丢失
2.REPEATABLE READ ：可能：更新丢失
3.SERIALIZABLE：都不可能
*/
-- 查看数据库最大连接数量 show max_connections;
SELECT pg_backend_pid();
-- 开始事务
begin;
update user set age = age + 1 where id = 1;
update user set age = age + 1 where id = 2;
-- 提交事务
commit;
-- 回滚事务
rollback;
-- 在事务内设置保存点
savepoint sp1;
-- 回滚保存点
rollback to sp1;

/*
索引：
1.数据量大时，字段查询频繁，命中结果少适合使用索引，一般不轻易使用索引
2.FK 和 UK 会自动建立索引

CREATE INDEX idx_order_created_at ON orders (created_at);
*/