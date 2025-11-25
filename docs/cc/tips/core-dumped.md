# core dumped

## 什么是 Segmentation fault

Segmentation fault 指程序访问了系统未分配给该程序的内存空间，这部分内存空间可能不可访问、不存在或受系统保护。

SIGSEGV 是操作系统在用户态程序错误访问内存时的处理机制：

- 当用户态程序访问**不允许访问**的内存时，产生 SIGSEGV
- 当用户态程序以错误方式访问**允许访问**的内存时，同样产生 SIGSEGV

## 什么是 core

core 原指使用线圈制作的内存（core memory）。虽然现代已使用半导体内存，但核心转储文件仍沿用 "core" 这一名称。

## 什么是 core dump

当程序异常终止时，操作系统将程序当时的内存内容转储到文件中（通常命名为 core），这个过程称为 core dump。

## core 文件的存放路径

发生 core dump 时，生成的文件名格式为 `core.%e.%p.%t`，存放路径由以下配置指定：

```bash
# 查看 core 文件存放路径
cat /proc/sys/kernel/core_pattern

# 临时修改存放路径
echo "/var/log/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

# 永久修改存放路径
/sbin/sysctl -w kernel.core_pattern=/var/log/core.%e.%p.%t
```

````{dropdown} 文件名格式说明
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

## core dump 配置检查

检查系统是否启用 core dump：

```bash
ulimit -a
```

重点关注 `core file size` 参数：
- 如果值不为 0，表示已启用 core dump
- 如果值为 0，需要启用 core dump 功能：

```bash
ulimit -c unlimited
```

## 如何分析 core 文件

### 基本分析方法

```bash
# 进入 core 文件所在目录
cd /cache

# 将 core 文件与可执行程序关联
gdb /cache/gpsd.elf /cache/core.gpsd.7729.1764050460
```

### 关键调试命令

在 gdb 环境中执行：

```bash
# 查看调用栈回溯
(gdb) bt

# 查看完整调用栈信息
(gdb) bt full

# 查看所有线程堆栈
(gdb) thread apply all bt

# 查看寄存器状态
(gdb) info registers

# 查看变量值
(gdb) print variable_name

# 反汇编当前执行代码
(gdb) disassemble
```

## 实际调试案例

### 环境准备

```bash
# 解除 SELinux 权限限制
setenforce 0

# 确认目标进程状态
ps | grep gpsd

# 实时跟踪系统调用
strace -p <PID>
```

### core dump 配置

```bash
# 启用 core dump
ulimit -c unlimited

# 设置 core 文件路径和命名格式
echo "/cache/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

# 触发异常条件（可选）
ifconfig lo down
```

### 文件验证

```bash
# 检查生成的 core 文件
ls /cache/core.*
```

## 产生段错误的常见原因

- 缓冲区溢出（buffer overrun）
- 空悬指针 / 野指针
- 重复释放（double delete）
- 内存泄漏（memory leak）
- 不配对的 `new[]` / `delete`
- 内存访问越界
- 多线程程序使用了线程不安全的函数
- 多线程读写的数据未加锁保护
- 内存碎片（memory fragmentation）

## 示例程序

```cpp
#include <stdio.h>

int main(void) {
    int* ptr = NULL;      // 创建空指针
    printf("%d\n", *ptr); // 解引用空指针，导致段错误
    return 0;
}
```

## 调试技巧总结

1. **权限准备**：确保有足够的系统权限进行调试
2. **符号匹配**：使用与 core dump 完全一致的可执行文件版本
3. **系统监控**：结合 strace 实时监控系统调用
4. **完整回溯**：使用 `bt full` 获取完整的调用栈信息
5. **多线程分析**：检查所有线程状态以排除并发问题
