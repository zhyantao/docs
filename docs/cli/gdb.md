# GDB

## 1. 环境配置

### 1.1 权限与目录设置

```bash
# 创建 core 文件存储目录
mkdir -p /cache
chmod 777 /cache

# 允许 setuid 程序生成 core dump
echo 1 > /proc/sys/fs/suid_dumpable

# 临时禁用 SELinux 限制
setenforce 0
```

### 1.2 启用 Core Dump 功能

```bash
# 检查当前限制设置
ulimit -a

# 临时启用 core dump
ulimit -c unlimited

# 永久启用（添加到 shell 配置）
echo "ulimit -c unlimited" >> ~/.bashrc
source ~/.bashrc
```

### 1.3 配置 Core 文件路径

```bash
# 查看当前 core 文件路径
cat /proc/sys/kernel/core_pattern

# 设置自定义路径和命名格式
echo "/cache/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

# 永久生效配置
echo "kernel.core_pattern=/cache/core.%e.%p.%t" >> /etc/sysctl.conf
sysctl -p
```

```bash
# 命名格式说明：

# %% - 转义 % 字符    %p - 进程 ID          %u - 用户 ID
# %g - 组 ID          %s - 触发信号         %t - 时间戳（秒）
# %h - 主机名         %e - 可执行文件名
```

## 2. 核心概念解析

### 2.1 Segmentation Fault（段错误）

- **触发条件**：程序试图访问未被授权的内存区域
- **信号**：SIGSEGV (11)

```bash
$ kill -l

#  1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
#  6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
# 11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
# 16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
# 21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
# 26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
# 31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
# 38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
# 43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
# 48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
# 53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
# 58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
# 63) SIGRTMAX-1  64) SIGRTMAX
```

### 2.2 Core Dump（核心转储）

- **作用**：程序异常终止时的内存快照
- **内容**：崩溃时的完整状态（内存、寄存器、堆栈等）
- **用途**：事后分析程序崩溃原因

### 2.3 常见段错误原因

| 类别             | 具体问题                                        |
| ---------------- | ----------------------------------------------- |
| **内存访问错误** | 缓冲区溢出、空指针解引用、野指针访问            |
| **内存管理问题** | 重复释放、内存泄漏、访问越界、new/delete 不匹配 |
| **多线程问题**   | 线程不安全、竞态条件、死锁、未保护的共享数据    |
| **系统资源问题** | 栈溢出、内存碎片、文件描述符耗尽                |

## 3. Core 文件分析实战

```bash
# 加载 core 文件进行分析
gdb -c core.gpsd.7729.1764050460 --args /usr/bin/gpsd -n /dev/ttyS3

# 基本分析流程
(gdb) bt                    # 查看调用栈
(gdb) info registers        # 检查寄存器状态
(gdb) thread apply all bt   # 查看所有线程堆栈
(gdb) info proc mappings    # 查看内存映射
(gdb) info sharedlibrary    # 检查加载的共享库
```

## 4. 断点与执行控制

### 4.1 断点设置命令

| 命令                | 描述           | 示例               |
| ------------------- | -------------- | ------------------ |
| `break <function>`  | 函数断点       | `break main`       |
| `break <file:line>` | 文件行断点     | `break main.c:10`  |
| `break *<address>`  | 内存地址断点   | `break *0x4005a0`  |
| `tbreak`            | 临时断点       | `tbreak main.c:15` |
| `rbreak <regex>`    | 正则表达式断点 | `rbreak ^print_`   |
| `info break`        | 查看所有断点   | `info break`       |
| `delete <n>`        | 删除指定断点   | `delete 1`         |

### 4.2 执行控制命令

| 命令          | 描述               | 示例              |
| ------------- | ------------------ | ----------------- |
| `run <args>`  | 启动程序           | `run arg1 arg2`   |
| `start`       | 启动并在 main 暂停 | `start`           |
| `continue`    | 继续执行           | `continue`        |
| `step`        | 单步进入函数       | `step`            |
| `next`        | 单步跳过函数       | `next`            |
| `finish`      | 执行到函数返回     | `finish`          |
| `until <loc>` | 运行到指定位置     | `until main.c:20` |

## 5. 调用栈与上下文分析

| 命令             | 描述               | 示例          |
| ---------------- | ------------------ | ------------- |
| `backtrace`      | 打印调用栈         | `backtrace`   |
| `backtrace full` | 带局部变量的调用栈 | `bt full`     |
| `frame <n>`      | 切换栈帧           | `frame 2`     |
| `info frame`     | 当前帧详细信息     | `info frame`  |
| `info args`      | 查看函数参数       | `info args`   |
| `info locals`    | 查看局部变量       | `info locals` |

## 6. 寄存器深度分析

### 6.1 关键寄存器说明

- **PC (Program Counter)** - 下一条指令地址
- **SP (Stack Pointer)** - 当前栈顶位置
- **FP (Frame Pointer)** - 当前栈帧基址
- **通用寄存器** - 函数参数、临时变量存储

### 6.2 寄存器分析技巧

```bash
# 分析程序执行流
(gdb) info registers pc
(gdb) x/i $pc                    # 查看当前指令
(gdb) disas $pc-0x20, $pc+0x20   # 反汇编周边代码

# 检查栈状态
(gdb) info registers sp
(gdb) x/20xa $sp                 # 查看栈内存
(gdb) bt                         # 验证栈回溯

# 通用寄存器分析
(gdb) info registers
(gdb) x/x $rax                   # 检查指针有效性
```

### 6.3 常见错误模式识别

**空指针访问**

```bash
(gdb) p/x $rax
$1 = 0x0
(gdb) x/x $rax
Cannot access memory at address 0x0
```

**野指针访问**

```bash
(gdb) p/x $rbx
$2 = 0x12345678
(gdb) x/x $rbx
Cannot access memory at address 0x12345678
```

## 7. 变量与内存检查

### 7.1 变量查看命令

| 命令             | 描述         | 示例                   |
| ---------------- | ------------ | ---------------------- |
| `print <expr>`   | 打印表达式   | `print x`              |
| `print/x <expr>` | 十六进制格式 | `print/x &x`           |
| `x/<fmt> <addr>` | 检查内存     | `x/4wx 0x7fffffffe000` |
| `watch <expr>`   | 写观察点     | `watch *0x12345678`    |
| `display <expr>` | 自动显示     | `display x`            |
| `ptype <type>`   | 查看类型定义 | `ptype struct_name`    |

### 7.2 内存检查格式详解

```bash
# 基本语法：x/[数量][格式][单位] <地址>

# 格式字符：
# x - 十六进制   d - 十进制   u - 无符号十进制
# o - 八进制     t - 二进制   a - 地址
# c - 字符       s - 字符串   i - 指令

# 单位字符：
# b - 字节       h - 半字(2字节)
# w - 字(4字节)  g - 双字(8字节)

# 实用示例：
x/10xb buffer    # 16进制显示10字节
x/5i $pc         # 显示5条指令
x/20s string_ptr # 显示20个字符串
```

## 8. 多线程调试

| 命令                       | 描述             | 示例                       |
| -------------------------- | ---------------- | -------------------------- |
| `info threads`             | 查看所有线程     | `info threads`             |
| `thread <n>`               | 切换线程         | `thread 2`                 |
| `thread apply all <cmd>`   | 所有线程执行命令 | `thread apply all bt`      |
| `set scheduler-locking on` | 锁定其他线程     | `set scheduler-locking on` |
| `info locks`               | 检查锁状态       | `info locks`               |

## 9. TUI 图形模式

| 命令            | 描述          | 快捷键     |
| --------------- | ------------- | ---------- |
| `tui enable`    | 启用 TUI 模式 |            |
| `layout src`    | 源代码视图    |            |
| `layout asm`    | 汇编视图      |            |
| `layout split`  | 混合视图      |            |
| `layout reg`    | 寄存器视图    |            |
| `focus cmd/src` | 切换焦点      |            |
| `refresh`       | 刷新显示      |            |
| `tui disable`   | 退出 TUI      | `Ctrl+x+a` |

## 10. 实战调试案例

### 10.1 空指针解引用

```cpp
#include <stdio.h>

int main(void) {
    int* ptr = NULL;      // 空指针
    printf("%d\n", *ptr); // 解引用导致段错误
    return 0;
}
```

**调试分析**：

```bash
(gdb) bt
#0  0x000000000040053d in main () at segfault.c:4
(gdb) info registers
rax     0x0      0      # 空指针值
rip     0x40053d 0x40053d <main+13>  # 崩溃位置
```

### 10.2 栈溢出问题

```cpp
#include <stdio.h>

void recursive_function(int depth) {
    char buffer[1024]; // 每次递归消耗栈空间
    printf("Depth: %d\n", depth);
    recursive_function(depth + 1); // 无限递归导致栈溢出
}

int main() {
    recursive_function(1);
    return 0;
}
```

## 11. 高级调试技巧

### 11.1 实用命令汇总

| 命令                    | 描述            | 示例                  |
| ----------------------- | --------------- | --------------------- |
| `shell <cmd>`           | 执行 shell 命令 | `shell ls -la`        |
| `set logging on`        | 开启日志记录    | `set logging on`      |
| `info proc`             | 进程信息        | `info proc`           |
| `handle <sig> <action>` | 信号处理        | `handle SIGSEGV stop` |
| `generate-core-file`    | 生成 core 文件  | `generate-core-file`  |

### 11.2 优化代码调试

```bash
# 提升优化代码的可调试性
set print static-members on
set print vtbl on
set print asm-demangle on

# 处理内联函数
set print inline on
info address function_name
```

### 11.3 进程监控

```bash
# 查看进程线程信息
ps -T | grep gpsd

# 系统调用跟踪
strace -e trace=all -p <PID>
```

## 延伸阅读

- <https://sourceware.org/gdb/current/onlinedocs/gdb.html/>
