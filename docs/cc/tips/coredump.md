# Segmentation fault

## 什么是 Segmentation fault

Segmentation fault 就是指程序访问了系统未分配给这个程序的内存空间，这部分内存空间或者是不可访问，或者是是不存在的，又或者是受系统保护的。  

SIGSEGV 是一个用户态的概念，是操作系统在用户态程序错误访问内存时所做出的处理：

- 当用户态程序访问（访问表示读、写或执行）**不允许访问** 的内存时，产生 SIGSEGV；
- 当用户态程序以错误的方式访问 **允许访问** 的内存时，同样会产生SIGSEGV。

## 什么是 core

在使用半导体作为内存的材料前，人类是利用线圈当作内存的材料（发明者为王安），线圈就叫作 core ，用线圈做的内存就叫作 core memory。如今 ，半导体工业澎勃发展，已经没有人用 core memory 了，不过，在许多情况下，人们还是把记忆体叫作 core 。

## 什么是 core dump

我们在开发（或使用）一个程序时，最怕的就是程序莫明其妙地当掉。于是这时操作系统就会把程序当掉时的内存内容 dump 出来（现在通常是写在一个叫 core 的 file 里面），这个动作就叫作 core dump。

## core 文件的存放路径

发生 core dump 时，会生成文件名为诸如 `core.%e.%p.%t` 的文件，存放路径由下面的文件指定：

```bash
# 查看 core 文件的存放路径
cat /proc/sys/kernel/core_pattern

# 临时修改 core 文件的存放路径
echo "/var/log/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

# 永久修改 core 文件的存放路径
/sbin/sysctl -w kernel.core_pattern=/var/log/core.%e.%p.%t
```

````{dropdown}
```text
%%  单个 % 字符
%p  所 dump 进程的进程 ID
%u  所 dump 进程的实际用户 ID
%g  所 dump 进程的实际组 ID
%s  导致本次 core dump 的信号
%t  core dump 的时间 (由 1970 年 1 月 1 日计起的秒数)
%h  主机名
%e  程序文件名
```
````

如果在 `core_pattern` 指定目录下没有找到 core 文件，检查当前系统是否使能了 core dump 模式：

```bash
ulimit -a
```

````{dropdown}
```text
core file size (blocks)         (-c) 1024
data seg size (kb)              (-d) unlimited
scheduling priority             (-e) 0
file size (blocks)              (-f) unlimited
pending signals                 (-i) 2795
max locked memory (kb)          (-l) 64
max memory size (kb)            (-m) unlimited
open files                      (-n) 1024
POSIX message queues (bytes)    (-q) 819200
real-time priority              (-r) 0
stack size (kb)                 (-s) 8192
cpu time (seconds)              (-t) unlimited
max user processes              (-u) 2795
virtual memory (kb)             (-v) unlimited
file locks                      (-x) unlimited
```
````

如果 `core file size` 不等于 0，则说明已经使能了 core dump，无需额外的操作，只需要将发生 Segmentation fault 的程序再运行一遍就可以了，然后去 `core_pattern` 指定的目录下去找 core 文件。

如果 `core file size` 等于 0，发生 Segmentation fault 时是不显示 `(core dumped)` 这个字段的，你可以使用下面的命令使能 core dump：

```bash
ulimit -c 1024
```

接下来，再去运行发生 Segmentation fault 的程序，然后去指定目录下去找 core 文件。

## 如何分析 core 文件

首先，`cd` 到 core 文件所在的目录，然后运行下面的命令，将 core 文件与可执行程序关联起来：

```bash
gdb <exec_file> <core_dump_file>
```

接下来，第一条命令一般是设置断点，例如将断点打在第 10 行：

```bash
b 10
```

然后，开始运行程序：

```bash
r
```

参考 {ref}`gdb_tips`，完成接下来的调试步骤。

## 产生段错误的常见原因

- 缓冲区溢出（buffer overrun）
- 空悬指针 / 野指针
- 重复释放（double delete）
- 内存泄漏（memory leak）
- 不配对的 `new[]` / `delete`
- 内存碎片（memory fragmentation）
- 内存访问越界
- 多线程程序使用了线程不安全的函数
- 多线程读写的数据未加锁保护

## 示例程序

```c
#include <stdio.h>

int main(void)
{
    int *ptr = NULL;      // 创建一个空指针
    printf("%d\n", *ptr); // 尝试解引用空指针，这将导致段错误
    return 0;
}
```
