# MySQL 基础

## 什么是 MySQL

我们经常性地混淆数据库和数据库管理系统的概念，那么 MySQL 是一个数据库呢？还是一个数据库管理系统？

数据库是一个静态的资源，表示数据的集合，而 MySQL
本身并不代表数据，它是用于操作数据的软件，因此将它定位为数据库管理系统 [^cite_ref-1] 更为合适。

数据库、操作数据库的软件和终端应用三者一起，我们通常称之为数据库系统。

按照操作的数据模型的差异，数据库管理系统可以细分为关系型数据管理系统和非关系型数据库管理系统。
而 MySQL 可以作为关系型数据库管理系统的代表。

安装 MySQL 可能会遇到一点坑，不推荐用 Installer 安装，它会给你装很多不需要的环境。
推荐[下载 Zip](https://dev.mysql.com/downloads/mysql/5.7.html)，然后配一下环境变量就可以了。

## MySQL 的工作流程

{numref}`mysql-arch` 展示了当在客户端发出一条指令后，MySQL 将会做出的一系列的响应 [^cite_ref-2]。

```{figure} ../../_static/images/mysql-architecture.png
:name: mysql-arch

数据库管理系统结构
```

## CRUD 中的事务

数据库管理系统在操作数据库的过程中，终究不是原语操作，难免会导致数据发生不一致的现象，
而如何避免这些现象的产生或者当这些现象产生后，应该如何补救就成了我们研究的重点。

考虑数据存储的载体数量和位置。如果数量较少，只有一块硬盘，那么事务的实现其实就十分简单了，但是真实场景通常不会这样。
然后，对于几块数据盘，它们之间的通信是否流畅，是否会发生网络分区，也是应当着重考虑的问题。

如何保证事务？常用的手段就是日志，而日志的本质就是一个个存储在磁盘上的文件，
它们记录了你修改了哪些数据，改成了什么，原来是什么。

日志通常不只有一种，比如可以分为 Redo log、binlog、Undo log，在什么场合使用什么类型的 log
以及如何使用其中的某几种 log 来实现目标也是我们应该熟知的。

关于这部分知识的补充，我们应该进一步阅读和学习，具体可以参考 [^cite_ref-3] [^cite_ref-4]。

## 参考文献

[^cite_ref-1]: Database <https://en.wikipedia.org/wiki/Database>
[^cite_ref-2]: 基础架构：一条SQL查询语句是如何执行的？丁奇 <https://time.geekbang.org/column/article/68319>
[^cite_ref-3]: MySQL 实战 45 讲，丁奇 <https://time.geekbang.org/column/intro/139>
[^cite_ref-4]: 凤凰架构，周志华 <https://icyfenix.cn/>