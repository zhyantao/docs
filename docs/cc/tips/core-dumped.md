# core dumped

## 什么是 Segmentation fault

Segmentation fault（段错误）指程序访问了系统未分配给该程序的内存空间，这部分内存空间可能不可访问、不存在或受系统保护。

SIGSEGV 是操作系统在用户态程序错误访问内存时的处理机制：

- 当用户态程序访问**不允许访问**的内存时，产生 SIGSEGV
- 当用户态程序以错误方式访问**允许访问**的内存时，同样产生 SIGSEGV

## 什么是 core

core 原指使用线圈制作的内存（core memory）。虽然现代已使用半导体内存，但核心转储文件仍沿用 "core" 这一名称。

## 什么是 core dump

当程序异常终止时，操作系统将程序当时的内存内容转储到文件中（通常命名为 core），这个过程称为 core dump。core 文件包含了程序崩溃时的完整状态，包括内存、寄存器、堆栈等信息。

## core 文件的存放路径

发生 core dump 时，生成的文件名格式可自定义，存放路径由以下配置指定：

```bash
# 查看 core 文件存放路径
cat /proc/sys/kernel/core_pattern

# 临时修改存放路径
echo "/var/log/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

# 永久修改存放路径
echo "kernel.core_pattern=/var/log/core.%e.%p.%t" >> /etc/sysctl.conf
sysctl -p
```

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

## core dump 配置检查

检查系统是否启用 core dump：

```bash
ulimit -a
```

重点关注 `core file size` 参数：

- 如果值不为 0，表示已启用 core dump
- 如果值为 0，需要启用 core dump 功能：

```bash
# 临时启用
ulimit -c unlimited

# 永久启用，添加到 ~/.bashrc 或 /etc/profile
echo "ulimit -c unlimited" >> ~/.bashrc
source ~/.bashrc
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

## 寄存器分析方法

### 关键寄存器的作用

在分析 core dump 时，以下寄存器尤为重要：

- **PC (Program Counter)**：指向当前执行的指令地址
- **SP (Stack Pointer)**：指向当前栈顶位置
- **FP (Frame Pointer)**：指向当前栈帧基地址
- **通用寄存器**：存储函数参数、局部变量等

### 定位问题寄存器的方法

#### 1. 分析程序计数器 (PC)

```bash
# 查看 PC 寄存器指向的代码
(gdb) info registers pc
(gdb) x/i $pc

# 反汇编当前指令区域
(gdb) disas $pc-0x20, $pc+0x20
```

PC 寄存器告诉程序崩溃时执行的具体指令。如果 PC 指向非法地址（如 0x0），通常是空指针调用。

#### 2. 分析栈指针 (SP) 和栈内存

```bash
# 检查栈指针
(gdb) info registers sp

# 查看栈内存内容
(gdb) x/20xa $sp

# 检查栈回溯的完整性
(gdb) bt
```

如果 SP 寄存器值异常，可能是栈溢出或栈被破坏。

#### 3. 分析通用寄存器中的指针值

```bash
# 查看所有寄存器
(gdb) info registers

# 检查寄存器中的地址是否有效
(gdb) info registers rax rbx rcx rdx

# 验证指针有效性
(gdb) x/x $rax  # 查看 rax 指向的内存
(gdb) x/s $rax  # 如果可能是字符串，按字符串查看
```

#### 4. 识别问题寄存器的模式

**空指针访问模式：**

```bash
# 如果寄存器值为 0 或很小
(gdb) p/x $rax
$1 = 0x0
(gdb) x/x $rax
Cannot access memory at address 0x0
```

**野指针访问模式：**

```bash
# 寄存器值看起来像随机地址
(gdb) p/x $rbx
$2 = 0x12345678
(gdb) x/x $rbx
Cannot access memory at address 0x12345678
```

**栈溢出模式：**

```bash
# SP 寄存器指向异常区域
(gdb) info registers sp
# sp     0x7fffffffe000  0x7fffffffe000
(gdb) x/x $sp
# Value can't be converted to integer
```

### 实际寄存器分析案例

```bash
# 案例：空指针解引用
(gdb) info registers
rax     0x0      0
rbx     0x7fffffffdd80   140737488346496
rcx     0x0      0
rdx     0x0      0
rsi     0x7ffff7fa44a0   140737353783456
rdi     0x1      1
rbp     0x7fffffffdb10   0x7fffffffdb10
rsp     0x7fffffffdb10   0x7fffffffdb10
r8      0x0      0
r9      0x7ffff7fb0500   140737353804032
r10     0x8      8
r11     0x246    582
r12     0x0      0
r13     0x7fffffffdc40   140737488346176
r14     0x0      0
r15     0x0      0
rip     0x400540 0x400540 <main+16>
...

(gdb) x/i $rip
=> 0x400540 <main+16>:    mov    (%rax),%edx  # 试图读取 rax 指向的内存
```

**分析过程：**

1. 发现 `rip` 指向 `mov (%rax),%edx` 指令
2. 检查 `rax` 寄存器值为 `0x0`
3. 确认是空指针解引用：试图读取地址 0x0 的内容

## 实际调试案例

### 环境准备

```bash
# 解除 SELinux 权限限制
setenforce 0

# 确认目标进程状态
ps aux | grep gpsd

# 实时跟踪系统调用
strace -p <PID>

# 检查核心转储设置
sysctl kernel.core_pattern
ulimit -c
```

### core dump 配置

```bash
# 启用 core dump
ulimit -c unlimited

# 设置 core 文件路径和命名格式
echo "/cache/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

# 确保目录有写权限
mkdir -p /cache
chmod 777 /cache

# 对于 setuid 程序，需要额外配置
echo 1 > /proc/sys/fs/suid_dumpable
```

### 文件验证

```bash
# 检查生成的 core 文件
ls -la /cache/core.*

# 验证 core 文件完整性
file /cache/core.gpsd.7729.1764050460
```

## 多线程程序调试技巧

对于多线程程序的 core dump，需要特别关注线程间交互：

```bash
# 查看所有线程状态
(gdb) thread apply all bt

# 切换到特定线程
(gdb) thread 2

# 检查线程局部存储
(gdb) info threads
(gdb) thread apply all info registers

# 检查互斥锁状态
(gdb) info locks
(gdb) p mutex_variable
```

## 产生段错误的常见原因

### 内存访问错误

- 缓冲区溢出（buffer overrun）
- 空悬指针 / 野指针
- 重复释放（double delete）
- 内存泄漏（memory leak）
- 不配对的 `new[]` / `delete`
- 内存访问越界

### 多线程问题

- 多线程程序使用了线程不安全的函数
- 多线程读写的数据未加锁保护
- 死锁（deadlock）或竞争条件（race condition）

### 系统资源问题

- 内存碎片（memory fragmentation）
- 栈溢出（stack overflow）
- 文件描述符耗尽

## 示例程序与调试

### 示例 1：空指针解引用

```cpp
#include <stdio.h>

int main(void) {
    int* ptr = NULL;      // 创建空指针
    printf("%d\n", *ptr); // 解引用空指针，导致段错误
    return 0;
}
```

**调试分析：**

```bash
(gdb) bt
#0  0x000000000040053d in main () at segfault.c:4
(gdb) info registers
rax     0x0      0
rip     0x40053d 0x40053d <main+13>
```

### 示例 2：栈溢出

```cpp
#include <stdio.h>

void recursive_function(int depth) {
    char buffer[1024]; // 大数组占用栈空间
    printf("Depth: %d\n", depth);
    recursive_function(depth + 1);
}

int main() {
    recursive_function(1);
    return 0;
}
```

## 高级调试技巧

### 1. 使用 core 文件进行事后分析

```bash
# 加载 core 文件
gdb -c core.file program

# 检查内存映射
(gdb) info proc mappings

# 查看共享库
(gdb) info sharedlibrary

# 检查信号信息
(gdb) info signals
```

### 2. 条件调试

```bash
# 只在特定条件满足时中断
(gdb) break function_name if condition

# 观察点：当变量被修改时中断
(gdb) watch variable_name

# 捕获点：当系统调用发生时中断
(gdb) catch syscall read
```

### 3. 脚本化调试

```bash
# 创建调试脚本
cat > debug_script.gdb << EOF
set pagination off
bt full
info registers
thread apply all bt
quit
EOF

# 批量分析多个 core 文件
for core in core.*; do
    echo "Analyzing $core"
    gdb -x debug_script.gdb program $core
done
```

## 调试技巧总结

1. **权限准备**：确保有足够的系统权限进行调试
2. **符号匹配**：使用与 core dump 完全一致的可执行文件版本
3. **系统监控**：结合 strace、ltrace 实时监控系统调用和库调用
4. **完整回溯**：使用 `bt full` 获取完整的调用栈信息
5. **多线程分析**：检查所有线程状态以排除并发问题
6. **寄存器分析**：重点关注 PC、SP 和包含指针值的通用寄存器
7. **内存验证**：对可疑指针使用 `x` 命令验证内存可访问性
8. **模式识别**：熟悉常见错误模式的寄存器特征

通过系统性的寄存器分析和调用栈检查，可以快速定位导致段错误的具体指令和根本原因，显著提高调试效率。
