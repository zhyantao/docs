(db_principles)=
# 数据库系统原理

## 基本介绍

平常我们经常提及的数据库指的是存储数据的仓库，其物理体现就是一个个的文件，实质是一个个的表（DB tables）。
这些表的维护由一个叫做数据库管理系统（DBMS）来完成，它保证了数据库的安全性和完整性，并为我们提供了 CRUD 接口。
底层由 DBMS 支持，借助 DBMS 提供的事务管理和 CRUD 接口，上层应用的具体业务实现则需要我们编写 SQL 语句手工实现。
{numref}`db-overview` 展示了数据库软件的交互过程。

```{figure} ../../_static/images/db-overview.*
:name: db-overview

数据库软件交互过程
```

按照数据库类型进行分类，我们可以将其分为关系型和非关系型两大类：

关系数据库是一种用于存储相互关联的数据点并提供数据点访问的数据库。
它采用关系模型，直接、直观地在表中展示数据。
在关系数据库中，表中的每一行都代表一条记录，每条记录都具有一个唯一的ID（又被称为键），而表中的列则用于存储数据的属性。
每条记录的每一个属性通常都有一个值。籍此，用户可以轻松在数据点之间建立关联 [^cite_ref-1]。

NoSQL 数据库（意即"不仅仅是SQL"）并非表格格式，其存储数据的方式与关系表不同。
NoSQL 数据库的类型因数据模型而异。 主要类型包括文档、键值、宽列和图形。
它们提供了灵活的模式，可以随大量数据和高用户负载而轻松扩展 [^cite_ref-2]。
如果对非关系型数据库进行细分，按照存储的数据的格式来看，又可以分为面向对象数据库和 XML 数据库。

关系型数据库的代表有：MySQL、Oracle、SQL Server、SQL Lite。

非关系型数据库的代表有：Redis、MongoDB、对象存储。

## 专业术语扫盲

```{list-table}
:header-rows: 1
:name: 数据库常见术语
:widths: 30, 70

* - 名词
  - 备注
* - 列 / 字段 / 属性 / 数据项
  - column / field / attribute / data item
* - 行 / 元组 / 记录
  - row / tuple / record
* - (关系) 模式 = 表名 + 表头
  - 关系模式是关系的结构
* - 关系 / 表 = 模式 + 表内容
  - 关系是关系模式在某一时刻的数据
* - 超键（super key）
  - 在关系中能唯一标识元组的**属性集**称为关系模式的超键
* - 候选键（candidate key）
  - 不含有多余属性的**超键**称为候选键，同一个元组可能有多个候选键
* - 主键（primary key）/ 主码
  - 用户挑选出来的用于标识元组的一个**候选键**称为主键。
    需要注意的是，这种描述在数据库原理课本上是适用的，但是理论并不是完全照搬地应用于实践，
    在数据库设计时，通常增加一个 `id` 列作为主键，而不是挑选候选键
* - 外键（foreign key）/ 外码
  - 关系 $R$ 中的一个属性组，它不是 $R$ 的候选键，但它与另一个关系 $S$ 
    的候选键相对应，则称这个属性组为 $R$ 的外码或外键
* - 主属性与非主属性
  - 包含在任意一个候选键中的属性被称作主属性，而其他属性被称作非主属性
* - 实体完整性
  - 关系的主键中的属性值不能为空值
* - 参照完整性
  - 如果关系 $R_1$ 的外键 $F_k$ 与关系 $R_2$ 的主键 $P_k$ 相对应，则 $R_1$ 中的每一个元组的 $F_k$
    值或者等于 $R_2$ 中某个元组的 $P_k$ 值，或者为空值
* - 用户自定义的完整性
  - 用户针对具体的应用环境定义的完整性约束条件。如 $S\#$ 要求是 $10$ 
    位整数，其中前四位为年度，当前年度与他们的差必须在 $4$ 以内
* - 三级模式 [^cite_ref-8]
  - 外模式 / 局部模式 / External Schema / **View**
    
    概念模式 / 全局模式 / 逻辑模式 / 模式 / **Schema** / Conceptual View
    
    内模式 / 存储模式 / 物理模式 / Internal Schema = Internal View
* - 两层映像
  - $\text{E-C}$ 映像（$\text{E-C Mapping}$）实现逻辑独立性
    
    $\text{C-I}$ 映像（$\text{C-I Mapping}$）实现物理独立性
* - 四种 SQL 语言 [^cite_ref-4]
  - 数据库定义语言（DDL，Data Defination Language）定义 SQL 模式、基本表、视图、索引等。
    `CREATE`、`ALTER`、`DROP`、`TRUNCATE`、`COMMENT`、`RENAME`。
    
    数据库操纵语言（DML，Data Manipulation Language）由 DBMS 
    提供。`SELECT`、`INSERT`、`UPDATE`、`DELETE`、`MERGE`、`CALL`、`EXPLAIN PLAN`、`LOCK TABLE`。

    数据库控制语言（DCL，Data Control Language）授权、角色控制等。`GRANT`、`REVOKE`。

    事务控制语言（TCL，Tranction Control Language）设置保存点、回滚等。`SAVEPOINT`、`ROLLBACK`、`SET TRANSACTION`。
* - 数据模型
  - 层次模型（一种用树形结构描述实体及其之间关系的数据模型）
    
    网状模型（允许一个结点可以同时拥有多个双亲结点和子节点）
    
    关系模型（采用二维表格结构表达实体类型及实体间联系的数据模型）
```

## 关系代数

一个完备的数据库语言，应当同时具备三种运算能力：关系代数、关系演算（包括元组演算和域演算）。

- 关系代数：以集合为对象进行操作，由集合到集合的变换。
- 元组演算：以元组为对象进行操作，取出表中的每一个元组进行验证（有多个元组变量需要多个循环）。
- 域演算：以域变量为对象进行操作，取出域的每一个变量进行验证看其是否满足条件。

对比这三种运算，域演算的非过程性最好，元组演算次之，关系代数最差。
从安全性上考虑，关系代数是一种安全的集合运算，而关系演算不一定是安全的。

```{list-table}
:header-rows: 1
:name: 关系代数之元组操作
:widths: 20, 80

* - 操作名称
  - 操作语句
* - 并
  - $R \cup S = \{ t | t \in R \vee t \in S \}$
* - 差
  - $R - S = \{ t | t \in R \wedge t \notin S \}$
* - 积
  - $R \times S = S \times R$

    $R \times S$ 表示 $R$ 中的每一个元组和 $S$ 中的所有元组串接，$S \times R$ 表示 $S$ 中的每一个元组和 $R$ 中的所有元组串接。
    因此，它们的结果相同，列的顺序不影响结果
* - 选择
  - $\sigma_{con}(R) = \{ t | t \in R \wedge con(t) = true \}$
* - 投影
  - $\Pi_{A_{i1}, A_{i2}, \dots, A_{ik}}(R) = \{ < t[A_{i1}], t[A_{i2}], \dots, t[A_{ik}] > | t \in R \}$

    投影可将列属性重新排列
* - 更名（针对列）
  - $\rho_{\text{new_column_name}}(\text{old_column_name})$

    当一个表需要和其自身进行连接运算时，通常要使用更名操作
* - 交
  - $R \cap S = \{ t | t \in R \wedge t \in S \} = R - (R - S) = S - (S - R)$
  
    注意，差运算的括号不能去
* - 自然连接
  - $R \bowtie S = \sigma_{t[B]=s[B]}(R \times S)$
  
    自然连接会筛选出两个表相同属性组上值相等的元组
* - 内连接（$\theta$-连接）
  - $R \mathop{\bowtie}\limits_{A \theta B}^{} S = \sigma_{t[A]\ \theta\ s[B]}(R \times S)$
    
    内连接是自然连接更一般的情况
* - 外连接
  - 左外连接 $R ⟕ S$，右外连接 $R ⟖ S$，全外连接 $R ⟗ S$

    外连接 = 自然连接或 $\theta$-连接 + 失配的元组与全空元组形成的连接
* - 除
  - $R \div S = \Pi_{R-S}(R)-\Pi_{R-S}((\Pi_{R-S}(R) \times S)-R)$

    注意，这里 $R - S$ 指的是属性做差，前面讲的是元组做差。除法比较难理解，从结果往回看比较好理解。
    结果的表头是 $R$ 的表头的一部分，但不在 $S$ 的表头中，结果与 $S$ 做笛卡尔积又都在 $R$ 中。
    除法经常用于求解 "查询 ... 全部的 / 所有的 ..." 问题
```

## SQL-DDL 基本语句

```{code-block} mysql
-- 创建数据库
create database `数据库名`;

-- 打开或关闭数据库
use `数据库名`;
close `数据库名`;

-- 创建基本表（概念模式的数据）
create table if not exists ​`表名`(
  `列名1` 数据类型 primary key unique not null auto_increment, 
  `列名2` 数据类型 not null
);

-- 创建视图（外模式的数据）
create view `视图名`
as 子查询
with check option;

-- 修改表结构
alter table `表名`
add `列名1` 数据类型, `列名2` 数据类型
modify `列名1` 数据类型, `列名2` 数据类型
add constraint 完整性约束条件
drop 完整性约束条件;

-- 删除基本表
drop table `表名`;

-- 删除数据库
drop database `数据库名`;
```

## SQL-DML 基本语句

```{code-block} mysql
-- 单一元组新增（列名可省略不写）
insert into `表名` (`列名1`, `列名2`)
  values(值1, 值2);

-- 批元组新增
insert into `表名` (`列名1`, `列名2`)
values(值1, 值2);

-- 单表查询
select distinct `列名1`, `列名2`
from `表名`
where 检索条件
group by 分组条件
having 分组过滤条件
order by `列名1` desc  -- 默认升序
not like 正则表达式;

-- 多表联合查询（笛卡尔积）
select `列名1` as `列别名1`, `列名2`
from `表名1` inner join `表名2` as `表别名2`  -- as 可以省略
             right outer join `表名3`
             on `表名3`.`列名3` = `表名1`.`列名1`
where `表名1`.`列别名1` = `表别名2`.`列名2`;  -- theta-连接，等值连接

-- 元组更新
update `表名`
set `列名1` = 表达式或子查询, `列名2` = 表达式或子查询
where 检索条件;

-- 元组删除
delete from `表名`
where 检索条件; -- 如果 where 条件省略，则删除所有元组
```

## 复杂查询和视图

复杂查询会使用到子查询，子查询是指 `where` 子句中的 `select` 语句。

使用复杂查询，我们能够实现的业务有（因为都是判断条件，返回值为 `true` 或 `false`）：

- 判断某一元素是否是某一个集合的成员（`[not] in (子查询)`）
- 判断某一个集合是否包含另一个集合（`表达式 [`$\theta$ `some |` $\theta$ `all] (子查询)`）
- 判断集合是否为空（`[not] exists (子查询)`）
- 判断集合是否存在重复元组（`[not] exists (子查询)`）

为了实现上述目标，我们可以将子查询分三种类型：IN-子查询、$\theta$-SOME / $\theta$-ALL
子查询、EXISTS-子查询。

注意，`in` 判断的是集合中是否包含某一个元素，而 `exists` 判断的是集合是否为空，它们是不一样的。

$\theta$ 表示的是比较符，可以是 `<`，`>`，`<=`，`>=`，`=`，`<>` 中的任意一个。
$\theta$ some 如果有一个值满足 $\theta$ 关系，返回值就是真，$\theta$ all 所有的值都满足 $\theta$
关系，返回值才为真。

按照层次结构划分，子查询分为外层和内层查询。
如果内层查询需要用到外层查询的变量，那么这种查询方式叫 **相关子查询**。
另一种方式则是内外层相互独立的查询，不涉及相关参数的传递，那么这种方式称为 **非相关子查询**。
根据 **变量的作用域原则**，子查询用到的变量可以是父查询传递过来的，反过来则不行。

例题（**难点**）求 *至少* 使用了工程 S1 供应的 *全部* 零件的工程号 [^cite_ref-5]。

要想回答这个问题，如果我们直接用正常的思路，将很难理解解题过程。
根据语义的转化，我们可以描述为：在 S1 生产的 *全部零件* 中，**不存在有一个** 零件它 **不** 使用。
因为这个语义中，含有两个否定，因此，需要两个 `not exist` 来完成从自然语言到 SQL 语言的转化。

```{code-block} mysql
select distinct 工程号
from SPJ SPJZ
where not exists (        -- 4. 它不使用
  select *                -- 1. 在 S1 生产的全部零件中，
  from SPJ SPJX
  where SNO = 'S1'
  and not exists (        -- 2. 不存在
    select *              -- 3. 有一个零件
    from SPJ SPJY
    where SPJY.零件号 = SPJX.零件号 and SPJY.工程号 = SPJZ.工程号
  )
);
```

这个题，看过好几遍了，每次看都不是很理解，**现在也不是很理解**，所以说，`exists` 可真是个难点。

## SQL-DCL 基本语句

数据库控制语言将为数据库的 **完整性** 和 **安全性** 保驾护航。

- 完整性：指的是 DBMS 保证在任何情况下的 DB 都是正确的、有效的、一致的。
- 安全性：访问规则、权利和授权。

SQL 语言支持度完整性约束包括：静态约束（列完整性和表完整性）和动态约束（触发器）。

不知道你注意到没有，我们在创建表的时候，其实是有完整性约束的，从关键字上的体现就是
`primary key`、`not null`、`unique`。他们保证了列完整性约束（或域完整性）。

当然，MySQL 还为我们提供了更多用于列完整性约束的关键字，比如
`constraint`，`check()`（保证条件为真），`references`，`on delete {cascade | set null}`。

表完整性约束和列完整性约束的关键字是一样的，可以把列完整性约束看做是表完整性约束的特例。
列完整性约束作用于某一个列上，而表完整性约束可以指定多个列服从某个约束，比如 `unique(列名1, 列名2)`。

trigger（触发器）是一种过程完整性约束（相比之下，create table 中定义的都是非过程性约束）。
触发器是一段程序，该程序可以在特定的时刻被自动触发执行，比如一次更新操作之前或之后。

```{code-block} mysql
create trigger `触发器名` before   -- 也可以是 after
update of `列名`                   -- 也可以是 insert delete
on `表名`
referencing 程序段中的变量声明
for each row                      -- 对更新操作的每一条结果检查约束，也可以对整个更新操作检查
when (检查条件)                  -- 检查条件如果满足，就执行下面的程序
  -- 单行程序直接写在这里
  -- 多行程序要用下面的方式
  begin atomic
    -- 程序段代码语句 1;
    -- 程序段代码语句 2;
  end
```

在安全控制方面，我们可以通过在数据字典或系统目录中保存存取规则，限制用户对 DB 的访问权利。
当用户量大时，可以按用户组建立访问规则。

- 访问的粒度：字段、元组、关系、数据库。
- 访问的权利：增、删、查、改。
- 访问的谓词：拥有权利需要满足的条件。

视图是安全控制的重要手段，如下所示。

```{code-block} mysql
create EmpView1 as select * from Employee -- 通过视图，限制用户对关系中某些数据项的存取
create EmpView2 as select * from Employee where P#=:UserId -- 视图与谓词结合，限制访问
```

从安全控制的角度来看，我们通常把用户分成三种类型：普通用户、程序员用户、DBA。

- 普通用户：具备 `select` 数据库、表、元组、字段的能力。
- 程序员用户：具备 `insert`、`update`、`delete` 元组的能力。
- DBA：具备 `create`、`alter`、`drop` 表空间、模式、表、索引、视图的能力。

```{code-block} mysql
-- 授权命令
grant all privileges      -- 或者是 select insert update delete
on `表名`                 -- 或者是 视图名
to `用户账户ID1`, `ID2`;  -- 或者是 public
with grant option         -- 默认是不应该授予普通用户 grant 权限的

-- 收回授权
revoke all privileges
on `表名`
from `用户账户ID1`, `ID2`;
```

## 数据库设计

数据库设计是指根据数据库模型确定数据的组织方式 [^cite_ref-3]。{numref}`db-design` 展示了数据库设计的详细步骤：

```{figure} ../../_static/images/db-design.*
:name: db-design

数据库设计流程 [^cite_ref-7]
```

一个设计良好的数据库，应该尽可能消除数据冗余，但是又不是完全严格地按照三大范式来约束。
因为在规范和性能之间，总会需要有一个取舍，如果数据严格满足规范，那么必然需要一些联表查询，进而导致性能下降。
因此，在数据库设计时，允许有一定的数据冗余，以保证性能。

另外一点，设计良好的数据库应当尽可能避免使用物理外键，也就是说，尽量不要在数据表中使用外键字段。
因为这会导致在后续业务中给维护表结构带来额外的负担。比如，有了外键后，删除和更新数据都会变得很麻烦。

不同类型的数据应当放在不同的数据库中，比如结构化数据放在 MySQL 中，视频流放在 MongoDB 中，评论放在
Redis 中。

数据库设计中需要用到的数据类型：

```{code-block} text
数值：tinyint     smallint    mediumint     int         bigint    float     double     decimal
       1字节      2字节       3字节         4字节        8字节                          金融常用

字符串：char      varchar     tinytext      text
        0-255     0-65536     2^8-1         2^16-1

时间日期：date    time        datetime      timestamp     year

空值      null
```

数据规范：每个表中都应该包含以下 5 个字段。

```{code-block} text
id      version    is_delete     gmt_create     gmt_update
主键    乐观锁      伪删除        创建时间        修改时间
```

## 函数依赖定理

[^cite_ref-7]

## 范式分解理论

[^cite_ref-7]

使用模式分解理论要解决的问题是：数据冗余、不一致性、插入异常、删除异常。

## 物理存储

[^cite_ref-6]

## 查询的实现

[^cite_ref-6]

## 查询的优化

[^cite_ref-6]

在数据库的查询优化中，有三条启发式的优化原则：

- 尽可能早地做选择
- 尽可能早地做投影
- 尽可能早地做选择和投影的合并

索引的分类有：

1. 主键索引 primary key 只能有一个列作为主键，不可重复
2. 唯一索引 unique key 可以有多个列声明为唯一索引，可以重复，这里的可以重复指的是什么可以重复？
3. 常规索引 key / index
4. 全文索引 FullText index

索引的数据结构？

分页和排序：limit / order by 分页可缓解数据库压力（案例：抖音瀑布流）

## 事务处理

事务处理包含并发控制和故障恢复。

为什么需要事务？在一个能够提供服务的程序中，可能会由于 CPU 调度，执行到一半被抢占了
CPU，或由于断电、系统崩溃了。

事务的隔离性是指多个进程拥有各自的空间，不受干扰。

[^cite_ref-6]

## 数据库转储

如果我们在 Windows 上安装了 MySQL 数据库的话，在 ``D:\Program Files\mysql-5.7.37-winx64\data``
目录下，如果使用 MyISM 引擎，应该是可以找见 ``.frm``\ （表结构），``.MYD``\ （数据文件），\
``.MYI``\ （索引文件）文件。如果使用 InnoDB 引擎，应该可以找见 ``.frm`` 和 ``ibdata`` 文件夹。

因此，其中一种转储方式就是直接复制这些文件。另一种方式就是使用 ``mysqldump`` 命令。

---

[^cite_ref-1]: 关系数据库是什么 | Oracle 中国 <https://www.oracle.com/cn/database/what-is-a-relational-database/>
[^cite_ref-2]: NoSQL 是什么 - MongoDB <https://www.mongodb.com/zh-cn/nosql-explained>
[^cite_ref-3]: Database design basics. (n.d.). Database design basics. Retrieved May 1, 2010, from
<https://support.office.com/en-US/article/Database-design-basics-EB2159CF-1E30-401A-8084-BD4F9C9CA1F5>
[^cite_ref-4]: SQL 四种语言 <https://www.cnblogs.com/henryhappier/archive/2010/07/05/1771295.html>
[^cite_ref-5]: 王珊, 张俊. 数据库系统概论 (第5版) 习题解析与实验指导[M]. 高等教育出版社, 2015.
[^cite_ref-6]: 数据库系统（下）管理与技术 <https://www.mubucm.com/doc/6BprZ8u4YSk>
[^cite_ref-7]: 数据库系统原理习题与解析 <https://kdocs.cn/l/cnw25Tq3UVuU>
[^cite_ref-8]: 如何理解数据库的三级模式 <https://www.zhihu.com/question/38737183/answer/93294527>
