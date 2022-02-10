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
  - 关系 $R$ 中的一个属性组，它不是 $R$ 的候选键，但它与另一个关系 $S$ 的候选键相对应，则称这个属性组为 $R$ 的外码或外键
* - 主属性与非主属性
  - 包含在任意一个候选键中的属性被称作主属性，而其他属性被称作非主属性
* - 实体完整性
  - 关系的主键中的属性值不能为空值
* - 参照完整性
  - 如果关系 $R_1$ 的外键 $F_k$ 与关系 $R_2$ 的主键 $P_k$ 相对应，则 $R_1$ 中的每一个元组的 $F_k$ 值或者等于 $R_2$ 中某个元组的 $P_k$ 值，或者为空值
* - 用户自定义的完整性
  - 用户针对具体的应用环境定义的完整性约束条件。如 $S\#$ 要求是 $10$ 位整数，其中前四位为年度，当前年度与他们的差必须在 $4$ 以内
* - 三级模式
  - 外模式 / 局部模式 / External Schema / **View**
    
    概念模式 / 全局模式 / 逻辑模式 / 模式 / **Schema** / Conceptual View
    
    内模式 / 存储模式 / 物理模式 / Internal Schema = Internal View
* - 两层映像
  - $\text{E-C}$ 映像（$\text{E-C Mapping}$）实现逻辑独立性
    
    $\text{C-I}$ 映像（$\text{C-I Mapping}$）实现物理独立性
* - 数据模型
  - 层次模型（一种用树形结构描述实体及其之间关系的数据模型）
    
    网状模型（允许一个结点可以同时拥有多个双亲结点和子节点）
    
    关系模型（采用二维表格结构表达实体类型及实体间联系的数据模型）
```

## 关系代数

操作符操作的内容是集合，得到的结果也是集合。

```{list-table}
:header-rows: 1
:name: 关系代数之元组操作
:widths: 20, 80

* - 元组操作
  - 元组语句
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

## 数据库设计

数据库设计是指根据数据库模型确定数据的组织方式 [^cite_ref-3]。{numref}`db-design` 展示了数据库设计的详细步骤：

```{figure} ../../_static/images/db-design.*
:name: db-design

数据库设计流程
```

一个设计良好的数据库，应该尽可能消除数据冗余，但是又不是完全严格地按照三大范式来约束。
因为在规范和性能之间，总会需要有一个取舍，如果数据严格满足规范，那么必然需要一些联表查询，进而导致性能下降。
因此，在数据库设计时，允许有一定的数据冗余，以保证性能。

另外一点，设计良好的数据库应当尽可能避免使用物理外键，也就是说，尽量不要在数据表中使用外键字段。
因为这会导致在后续业务中给维护表结构带来额外的负担。比如，有了外键后，删除和更新数据都会变得很麻烦。

## 后续阅读

[^cite_ref-4] [^cite_ref-5] [^cite_ref-6] [^cite_ref-7] [^cite_ref-8] [^cite_ref-9] [^cite_ref-10]

## 参考文献

[^cite_ref-1]: 关系数据库是什么 | Oracle 中国 <https://www.oracle.com/cn/database/what-is-a-relational-database/>
[^cite_ref-2]: NoSQL 是什么？ NoSQL 数据库详解 - MongoDB <https://www.mongodb.com/zh-cn/nosql-explained>
[^cite_ref-3]: Database design basics. (n.d.). Database design basics. Retrieved May 1, 2010, from <https://support.office.com/en-US/article/Database-design-basics-EB2159CF-1E30-401A-8084-BD4F9C9CA1F5>
[^cite_ref-4]: 数据库系统（上）模型与语言 <https://www.mubucm.com/doc/1TZV-8_G4Dk>
[^cite_ref-5]: 数据库系统（中）建模与设计 <https://www.mubucm.com/doc/666LyLPreVk>
[^cite_ref-6]: 数据库系统（下）管理与技术 <https://www.mubucm.com/doc/6BprZ8u4YSk>
[^cite_ref-7]: 数据库系统原理习题与解析 <https://kdocs.cn/l/cnw25Tq3UVuU>
[^cite_ref-8]: 数据库系统知识点整理 <https://www.mubucm.com/doc/6fdWgkSb_kA>
[^cite_ref-9]: 数据库系统原理（考研笔记） <https://kdocs.cn/l/cnWHWWKze7Af>
[^cite_ref-10]: 数据密集型应用系统设计 <https://www.mubucm.com/doc/4kP4oa6Hm4A>
