# core dumped 调试指南

## 基本使用方法

### 什么是 Segmentation fault

Segmentation fault（段错误）指程序访问了系统未分配给该程序的内存空间，这部分内存空间可能不可访问、不存在或受系统保护。

SIGSEGV 是操作系统在用户态程序错误访问内存时的处理机制：

- 当用户态程序访问**不允许访问**的内存时，产生 SIGSEGV
- 当用户态程序以错误方式访问**允许访问**的内存时，同样产生 SIGSEGV

### 什么是 core dump

当程序异常终止时，操作系统将程序当时的内存内容转储到文件中（通常命名为 core），这个过程称为 core dump。core 文件包含了程序崩溃时的完整状态，包括内存、寄存器、堆栈等信息。

> core 原指使用线圈制作的内存（core memory），虽然现代已使用半导体内存，但核心转储文件仍沿用 "core" 这一名称。

### 启用 core dump

**检查是否启用：**

```bash
ulimit -a
```

重点关注 `file size` 参数：

- 如果值不为 0，表示已启用 dump
- 如果值为 0，需要启用 dump 功能：

```bash
# 临时启用
ulimit -c unlimited

# 永久启用，添加到 ~/.bashrc 或 /etc/profile
echo "ulimit -c unlimited" >> ~/.bashrc
source ~/.bashrc
```

**配置 core 文件存放路径：**

```bash
# 查看当前路径
cat /proc/sys/kernel/core_pattern

# 临时修改
echo "/tmp/%e.%t.%p.%s.core" > /proc/sys/kernel/core_pattern

# 永久修改
echo "kernel.core_pattern=/tmp/%e.%t.%p.%s.core" >> /etc/sysctl.conf
sysctl -p
```

命名参数说明：

```text
%%  单个 % 字符
%p  进程 ID
%u  实际用户 ID
%g  实际组 ID
%s  导致 core dump 的信号
%t  core dump 的时间戳
%h  主机名
%e  程序文件名
```

### 调试方法

#### 基本分析流程

```bash
# 将 core 文件与可执行程序关联
gdb /path/to/program /path/to/core.file
```

**常用 gdb 命令：**

```bash
(gdb) bt                    # 查看调用栈回溯
(gdb) bt full               # 查看完整调用栈信息
(gdb) thread apply all bt   # 查看所有线程堆栈
(gdb) info registers        # 查看寄存器状态
(gdb) print variable_name   # 查看变量值
(gdb) disassemble           # 反汇编当前执行代码
```

#### 寄存器分析

**关键寄存器：**

- **PC (Program Counter)**：指向当前执行的指令地址
- **SP (Stack Pointer)**：指向当前栈顶位置
- **FP (Frame Pointer)**：指向当前栈帧基地址

**分析命令：**

```bash
(gdb) info registers pc          # 查看 PC 寄存器
(gdb) x/i $pc                    # 查看 PC 指向的指令
(gdb) disas $pc-0x20, $pc+0x20   # 反汇编当前指令区域
(gdb) info registers sp          # 检查栈指针
(gdb) x/20xa $sp                 # 查看栈内存内容
```

**常见错误模式识别：**

| 错误类型   | 寄存器特征         | 验证命令                |
| ---------- | ------------------ | ----------------------- |
| 空指针访问 | 寄存器值为 0       | `x/x $rax` 提示无法访问 |
| 野指针访问 | 寄存器值为随机地址 | `x/x $rbx` 提示无法访问 |
| 栈溢出     | SP 指向异常区域    | `x/x $sp` 无法转换      |

**分析案例：**

```bash
(gdb) info registers
rax     0x0      0
rip     0x400540 0x400540 <main+16>

(gdb) x/i $rip
=> 0x400540 <main+16>:    mov    (%rax),%edx  # 试图读取 rax 指向的内存
```

分析结论：`rip` 指向 `mov (%rax),%edx` 指令，而 `rax` 值为 `0x0`，确认为空指针解引用。

### 调试技巧总结

1. **权限准备**：确保有足够的系统权限进行调试
2. **符号匹配**：使用与 core dump 完全一致的可执行文件版本
3. **完整回溯**：使用 `bt full` 获取完整的调用栈信息
4. **多线程分析**：检查所有线程状态以排除并发问题
5. **寄存器分析**：重点关注 PC、SP 和包含指针值的通用寄存器
6. **内存验证**：对可疑指针使用 `x` 命令验证内存可访问性
7. **模式识别**：熟悉常见错误模式的寄存器特征

---

## 高级特性

### 多线程程序调试

对于多线程程序的 core dump，需要特别关注线程间交互：

```bash
(gdb) info threads                     # 查看所有线程
(gdb) thread 2                         # 切换到特定线程
(gdb) thread apply all bt              # 所有线程的调用栈
(gdb) thread apply all info registers  # 所有线程的寄存器状态
(gdb) info locks                       # 检查互斥锁状态
```

### 产生段错误的常见原因

**内存访问错误：**

- 缓冲区溢出（buffer overrun）
- 空悬指针 / 野指针
- 重复释放（double delete）
- 不配对的 `new[]` / `delete`
- 内存访问越界

**多线程问题：**

- 使用了线程不安全的函数
- 共享数据未加锁保护
- 死锁或竞争条件

**系统资源问题：**

- 栈溢出（stack overflow）
- 文件描述符耗尽

### 示例程序

**示例 1：空指针解引用**

```cpp
#include <stdio.h>

int main(void) {
    int* ptr = NULL;
    printf("%d\n", *ptr); // 段错误
    return 0;
}
```

**示例 2：栈溢出**

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

### 高级调试技巧

#### 1. 事后分析

```bash
gdb -c core.file program          # 直接加载 core 文件
(gdb) info proc mappings          # 检查内存映射
(gdb) info sharedlibrary          # 查看共享库
(gdb) info signals                # 检查信号信息
```

#### 2. 条件调试

```bash
(gdb) break function_name if condition   # 条件断点
(gdb) watch variable_name                # 观察点
(gdb) catch syscall read                 # 捕获系统调用
```

#### 3. 脚本化批量调试

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

#### 4. 完整环境配置

```bash
# 启用 core dump
ulimit -c unlimited

# 设置 core 文件路径
echo "/tmp/%e.%t.%p.%s.core" > /proc/sys/kernel/core_pattern

# setuid 程序额外配置
echo 1 > /proc/sys/fs/suid_dumpable

# 结合 strace 实时跟踪
strace -p <PID>
```
