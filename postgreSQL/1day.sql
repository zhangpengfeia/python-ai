-- ddl语音
-- 第一步：创建test模式
CREATE SCHEMA IF NOT EXISTS test;
-- 第二步：授权
GRANT ALL PRIVILEGES ON SCHEMA test TO admin;

-- 第三步：创建表
/*
-- 一般主键设置为 primary key
1.唯一性，不能重复
2.非空
*/
create table test.user(
    id int primary key,
    name varchar(255),
    age integer check ( age > 0 ),
    score numeric(5,2) default 0.0,
    email varchar(255) unique,
    created_at timestamp default current_timestamp
);


/*
表关系：1对1，1对多，多对多
1对1：
    任意一表中加入外键，指向另一表的主键
    外键约束后修改时会做外键检查，确保正确
    实现方式：
        为外键加上UNIQUE约束，确保唯一
        user_id integer unique not null
        foreign key (user_id) references test.user(id)
1对多：
    一个A可以有多个B，一个B只能对应一个A
    部门表，商品分类表，用户订单表
    实现方式：
        外键不能加UNIQUE
        foreign key (dept_id) references test.dept(id)
多对多：
    一个A对应多个B,一个B对应多个A
    学生选修课程，一个学生选修多门课程，一个课程多个学生选修
    实现方式：
        创建一张中间表
        primary key (stu_id, course_id),  联合主键
        foreign key (stu_id) references test.stu(id),
        foreign key (course_id) references test.course(id)
*/

/*
什么是外键？
一个字段引用了另一个表的字段
从表：包含外键
主表：被外键引用的表

外键约束：
foreign key (course_id) references test.course(id) no action
1.NO ACTION 外键字段不能为空
2.CASCADE 级联删除
3.SET NULL 设置为NULL
4.RESTRICT 同 NO ACTION, 不支持延迟检查
*/