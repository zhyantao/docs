# GDB

## 1. 核心概念

### 1.1 Segmentation Fault（段错误）

- **定义**：程序访问了系统未分配给它的内存空间
- **触发条件**：
  - 访问**不允许访问**的内存
  - 以**错误方式**访问允许访问的内存
- **信号**：SIGSEGV

> 使用命令 `kill -l` 可以列出系统支持的所有信号，从编号 1 开始。

### 1.2 Core Dump（核心转储）

- **作用**：程序异常终止时的内存快照
- **内容**：崩溃时的完整状态（内存、寄存器、堆栈等）
- **文件名**：可通过模式自定义

## 2. 环境配置

### 2.1 启用 Core Dump

```bash
# 检查当前设置
ulimit -a

# 临时启用
ulimit -c unlimited

# 永久启用（添加到 ~/.bashrc 或 /etc/profile）
echo "ulimit -c unlimited" >> ~/.bashrc
source ~/.bashrc
```

### 2.2 配置 Core 文件路径

```bash
# 查看当前路径
cat /proc/sys/kernel/core_pattern

# 设置自定义路径和命名
echo "/var/log/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

# 永久配置
echo "kernel.core_pattern=/var/log/core.%e.%p.%t" >> /etc/sysctl.conf
sysctl -p
```

**命名格式说明**：

- `%%` - 单个 % 字符
- `%p` - 进程 ID
- `%u` - 用户 ID
- `%g` - 组 ID
- `%s` - 导致 core dump 的信号
- `%t` - 时间戳（秒数）
- `%h` - 主机名
- `%e` - 程序文件名

### 2.3 权限和目录设置

```bash
# 创建 core 文件目录
mkdir -p /cache
chmod 777 /cache

# 对于 setuid 程序
echo 1 > /proc/sys/fs/suid_dumpable

# 解除 SELinux 限制
setenforce 0
```

## 3. GDB 基本使用

```bash
# 启动 GDB
gdb <可执行文件>

# 带参数启动程序
gdb --args myprogram arg1 arg2

# 加载 core 文件分析
gdb <可执行文件> <core文件>
gdb -c <core文件> <可执行文件>

# 附加到运行中的进程
gdb -p <PID>
```

## 4. 断点与执行控制

| 命令                      | 描述                               | 示例                 |
| ------------------------- | ---------------------------------- | -------------------- |
| `break <函数名>`          | 设置函数断点                       | `break main`         |
| `break <文件:行号>`       | 在指定文件的指定行设置断点         | `break main.c:10`    |
| `break *<内存地址>`       | 在内存地址设置断点                 | `break *0x4005a0`    |
| `tbreak`                  | 设置临时断点（命中一次后自动删除） | `tbreak main.c:15`   |
| `rbreak <正则表达式>`     | 使用正则表达式设置断点             | `rbreak ^print_`     |
| `info break`              | 查看所有断点                       | `info break`         |
| `delete <断点编号>`       | 删除断点                           | `delete 1`           |
| `delete`                  | 删除所有断点                       | `delete`             |
| `enable <编号>`           | 启用断点                           | `enable 1`           |
| `disable <编号>`          | 禁用断点                           | `disable 1`          |
| `condition <编号> <条件>` | 设置条件断点                       | `condition 1 x > 10` |
| `ignore <编号> <次数>`    | 忽略断点指定次数                   | `ignore 1 5`         |
| `run <args>`              | 启动程序                           | `run arg1 arg2`      |
| `start`                   | 开始执行并在 main 函数处暂停       | `start`              |
| `continue`                | 继续执行                           | `continue`           |
| `step`                    | 单步进入函数                       | `step`               |
| `next`                    | 单步跳过函数                       | `next`               |
| `stepi`                   | 单步执行指令（进入函数）           | `stepi`              |
| `nexti`                   | 单步执行指令（跳过函数）           | `nexti`              |
| `finish`                  | 执行到当前函数返回                 | `finish`             |
| `until <位置>`            | 执行到指定位置                     | `until main.c:20`    |
| `kill`                    | 终止当前调试会话                   | `kill`               |

## 5. Core 文件分析

### 5.1 加载 Core 文件

```bash
# 基本语法
gdb <可执行文件> <core文件>

# 示例
gdb /cache/gpsd.elf /cache/core.gpsd.7729.1764050460

# 验证文件完整性
file /cache/core.gpsd.7729.1764050460
```

### 5.2 基本调试命令

```bash
# 查看调用栈
(gdb) bt
(gdb) backtrace

# 查看完整调用栈信息
(gdb) bt full

# 查看所有线程堆栈
(gdb) thread apply all bt

# 查看变量值
(gdb) print variable_name

# 反汇编当前代码
(gdb) disassemble
```

## 6. 调用栈与上下文分析

| 命令             | 描述                 | 示例          |
| ---------------- | -------------------- | ------------- |
| `backtrace`      | 打印调用栈           | `backtrace`   |
| `backtrace full` | 打印调用栈和局部变量 | `bt full`     |
| `frame <编号>`   | 切换栈帧             | `frame 2`     |
| `up <数字>`      | 向上移动栈帧         | `up 1`        |
| `down <数字>`    | 向下移动栈帧         | `down 1`      |
| `info frame`     | 查看当前帧信息       | `info frame`  |
| `info args`      | 查看当前帧参数       | `info args`   |
| `info locals`    | 查看当前帧局部变量   | `info locals` |
| `info catch`     | 查看当前异常处理     | `info catch`  |

### 7.1 关键寄存器说明

- **PC (Program Counter)** - 当前执行指令地址
- **SP (Stack Pointer)** - 栈顶位置
- **FP (Frame Pointer)** - 栈帧基地址
- **通用寄存器** - 函数参数、局部变量

### 7.2 寄存器分析方法

#### 分析程序计数器 (PC)

```bash
# 查看 PC 指向的代码
(gdb) info registers pc
(gdb) x/i $pc

# 反汇编当前指令区域
(gdb) disas $pc-0x20, $pc+0x20
```

#### 分析栈指针 (SP)

```bash
# 检查栈指针
(gdb) info registers sp

# 查看栈内存内容
(gdb) x/20xa $sp

# 检查栈回溯完整性
(gdb) bt
```

#### 分析通用寄存器

```bash
# 查看所有寄存器
(gdb) info registers

# 检查特定寄存器
(gdb) info registers rax rbx rcx rdx

# 验证指针有效性
(gdb) x/x $rax    # 查看内存内容
(gdb) x/s $rax    # 按字符串查看
```

### 7.3 寄存器命令速查

| 命令                  | 描述                       | 示例                        |
| --------------------- | -------------------------- | --------------------------- |
| `info registers`      | 查看所有寄存器值           | `info registers`            |
| `info registers <名>` | 查看特定寄存器             | `info registers rax`        |
| `disassemble <函数>`  | 反汇编函数                 | `disassemble main`          |
| `disassemble <地址>`  | 反汇编指定地址范围         | `disassemble 0x4000,0x4020` |
| `set $<reg>=<值>`     | 修改寄存器值               | `set $rax=0`                |
| `info all-registers`  | 查看所有寄存器（包括浮点） | `info all-registers`        |

### 7.4 常见错误模式识别

#### 空指针访问

```bash
(gdb) p/x $rax
$1 = 0x0
(gdb) x/x $rax
Cannot access memory at address 0x0
```

#### 野指针访问

```bash
(gdb) p/x $rbx
$2 = 0x12345678
(gdb) x/x $rbx
Cannot access memory at address 0x12345678
```

## 8. 变量与内存查看

| 命令                    | 描述                       | 示例                   |
| ----------------------- | -------------------------- | ---------------------- |
| `print <表达式>`        | 打印表达式值               | `print x`              |
| `print/x <表达式>`      | 十六进制格式打印           | `print/x &x`           |
| `print/d <表达式>`      | 十进制格式打印             | `print/d x`            |
| `print/t <表达式>`      | 二进制格式打印             | `print/t x`            |
| `print/c <表达式>`      | 字符格式打印               | `print/c x`            |
| `x/<格式> <地址>`       | 检查内存                   | `x/4wx 0x7fffffffe000` |
| `x/<长度><格式> <地址>` | 指定长度检查内存           | `x/10xb buffer`        |
| `watch <表达式>`        | 设置写观察点               | `watch *0x12345678`    |
| `rwatch <表达式>`       | 设置读观察点               | `rwatch variable`      |
| `awatch <表达式>`       | 设置读写观察点             | `awatch *ptr`          |
| `info watchpoints`      | 查看观察点                 | `info watchpoints`     |
| `display <表达式>`      | 每次暂停时自动打印         | `display x`            |
| `undisplay <编号>`      | 取消自动显示               | `undisplay 1`          |
| `info display`          | 查看自动显示表达式         | `info display`         |
| `set print pretty on`   | 结构体/类按缩进格式显示    | `set print pretty on`  |
| `set print array on`    | 数组显示时每元素单独一行   | `set print array on`   |
| `set print null-stop`   | 遇到 NULL 时停止打印字符串 | `set print null-stop`  |
| `set print object on`   | 显示对象的实际类型         | `set print object on`  |
| `ptype <变量/类型>`     | 查看类型定义               | `ptype struct_name`    |
| `whatis <表达式>`       | 查看表达式类型             | `whatis variable`      |

### 内存检查格式说明

```bash
# 基本格式：x/[长度][格式][单位] <地址>

# 格式字符：
# x - 十六进制
# d - 十进制
# u - 无符号十进制
# o - 八进制
# t - 二进制
# a - 地址
# c - 字符
# s - 字符串
# i - 指令

# 单位字符：
# b - 字节
# h - 半字（2字节）
# w - 字（4字节）
# g - 巨字（8字节）

# 示例：
x/10xb buffer    # 以16进制显示10个字节
x/5i $pc         # 显示5条指令
x/20s string_ptr # 显示20个字符串
```

## 9. 多线程程序调试

### 9.1 线程分析命令

```bash
# 查看所有线程状态
(gdb) info threads

# 查看所有线程堆栈
(gdb) thread apply all bt

# 切换到特定线程
(gdb) thread 2

# 检查线程寄存器
(gdb) thread apply all info registers

# 检查互斥锁状态
(gdb) info locks
(gdb) p mutex_variable
```

### 9.2 多线程调试命令速查

| 命令                       | 描述               | 示例                       |
| -------------------------- | ------------------ | -------------------------- |
| `info threads`             | 查看所有线程       | `info threads`             |
| `thread <编号>`            | 切换到指定线程     | `thread 2`                 |
| `thread apply <ID> <命令>` | 对指定线程执行命令 | `thread apply 2 bt`        |
| `thread apply all <命令>`  | 对所有线程执行命令 | `thread apply all bt`      |
| `set scheduler-locking on` | 锁定其他线程执行   | `set scheduler-locking on` |

## 10. TUI 模式

| 命令           | 描述               | 示例           |
| -------------- | ------------------ | -------------- |
| `tui enable`   | 启用 TUI 模式      | `tui enable`   |
| `layout src`   | 显示源代码窗口     | `layout src`   |
| `layout asm`   | 显示汇编窗口       | `layout asm`   |
| `layout split` | 显示源码和汇编     | `layout split` |
| `layout reg`   | 显示寄存器窗口     | `layout reg`   |
| `focus cmd`    | 焦点切换到命令窗口 | `focus cmd`    |
| `focus src`    | 焦点切换到源码窗口 | `focus src`    |
| `refresh`      | 刷新 TUI 显示      | `refresh`      |
| `tui disable`  | 退出 TUI 模式      | `tui disable`  |
| `Ctrl+x+a`     | TUI 模式切换快捷键 |                |

## 11. 高级调试技巧

### 11.1 使用 core 文件进行事后分析

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

### 11.2 条件调试

```bash
# 只在特定条件满足时中断
(gdb) break function_name if condition

# 观察点：当变量被修改时中断
(gdb) watch variable_name

# 捕获点：当系统调用发生时中断
(gdb) catch syscall read
```

### 11.3 脚本化调试

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

## 12. 实际调试案例

### 12.1 空指针解引用示例

```cpp
#include <stdio.h>

int main(void) {
    int* ptr = NULL;      // 创建空指针
    printf("%d\n", *ptr); // 解引用空指针，导致段错误
    return 0;
}
```

**调试分析**：

```bash
(gdb) bt
#0  0x000000000040053d in main () at segfault.c:4
(gdb) info registers
rax     0x0      0
rip     0x40053d 0x40053d <main+13>
```

### 12.2 栈溢出示例

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

## 13. 常见段错误原因

### 13.1 内存访问错误

- 缓冲区溢出
- 空悬指针/野指针
- 重复释放内存
- 内存泄漏
- 内存访问越界
- `new[]`/`delete` 不配对

### 13.2 多线程问题

- 线程不安全函数
- 未加锁保护的共享数据
- 死锁和竞争条件

### 13.3 系统资源问题

- 内存碎片
- 栈溢出
- 文件描述符耗尽

## 14. 其他实用命令

| 命令                      | 描述              | 示例                       |
| ------------------------- | ----------------- | -------------------------- |
| `shell <命令>`            | 执行 shell 命令   | `shell ls -la`             |
| `set logging on`          | 开启日志记录      | `set logging on`           |
| `set logging file <文件>` | 设置日志文件      | `set logging file gdb.log` |
| `show commands`           | 显示历史命令      | `show commands`            |
| `show version`            | 显示 GDB 版本信息 | `show version`             |
| `info proc`               | 显示进程信息      | `info proc`                |
| `info sharedlibrary`      | 显示加载的共享库  | `info sharedlibrary`       |
| `info signals`            | 显示信号处理信息  | `info signals`             |
| `handle <信号> <动作>`    | 设置信号处理方式  | `handle SIGSEGV stop`      |
| `generate-core-file`      | 生成 core 文件    | `generate-core-file`       |
| `quit`                    | 退出 GDB          | `quit`                     |

## 15. 调试最佳实践

1. **权限准备**：确保有足够的系统权限进行调试
2. **符号匹配**：使用与 core dump 完全一致的可执行文件版本
3. **系统监控**：结合 strace、ltrace 实时监控系统调用和库调用
4. **完整回溯**：使用 `bt full` 获取完整的调用栈信息
5. **多线程分析**：检查所有线程状态以排除并发问题
6. **寄存器分析**：重点关注 PC、SP 和包含指针值的通用寄存器
7. **内存验证**：对可疑指针使用 `x` 命令验证内存可访问性
8. **模式识别**：熟悉常见错误模式的寄存器特征

## 调试优化代码

```bash
# 禁用优化影响调试
set print static-members on
set print vtbl on
set print asm-demangle on

# 处理内联函数
set print inline on
info address function_name
```

## 16. 实用命令速查

```bash
# 实时监控
strace -p <PID>
ps aux | grep <进程名>

# Core 文件管理
ls -la /cache/core.*
file /cache/core.gpsd.7729.1764050460

# GDB 快速分析
gdb -c core.file program
(gdb) bt
(gdb) info registers
(gdb) thread apply all bt
(gdb) quit
```
