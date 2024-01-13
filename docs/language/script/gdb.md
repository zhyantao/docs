# GDB

在跟踪源代码的过程中，学会使用 GDB 将会很大程度上提升你跟踪源代码的效率。

## 安装分屏工具 tmux

```{code-block} bash
sudo apt install tmux
```

更进一步地，我们需要掌握一些 [常用的 tmux 命令](https://quickref.me/tmux)：

```{code-block} text
# 创建 tmux 会话
tmux

# 纵向分屏
Ctrl + b, "

# 横向分屏
Ctrl + b, %

# 关闭当前分屏
Ctrl + b, x

# 切换分屏（按住 Ctrl + b 不放，再按方向键，可以调整窗口大小）
Ctrl + b, 方向键
```

接下来，你会学习关于 GDB 中常用的命令，但并不是全部，有兴趣的话请参考 [`man gdb`](https://www.kdocs.cn/l/cncEx5Kq8rkd)。

本文使用的书写格式为：`[c]ommand <required arg> (optional arg)`

(gdb_tips)=

## 运行和调试程序

```{code} bash
# 设置断点
[b]reak <函数名 or 函数名:行号 or *内存地址>

# 反汇编
disassemble <函数名>

# 查看断点编号
[i]nfo [b]reak

# 删除断点
[d]elete <断点编号>

# 在条件为真时停在断点处
[condition] <断点编号> <C 语言描述的条件>

# 列出参数列表
[i]nfo (about)
    (about) 可以是下面的任何一个：
    [f]rame     当前栈帧，上一个栈帧，寄存器地址，参数列表，局部变量
    [s]tack     栈轨迹，函数调用，参数列表
    [r]egisters 每一个寄存器都保存了什么值
    [b]reak     断点的编号的内存地址，断点位于什么函数内
    [fu]nctions 函数签名

# 将指定文件加载到 gdb 中
[file] <可执行的文件名>

# 执行已加载的可执行程序
[r]un (arg1 arg2 ... argn)

# 继续执行源代码，停在下一个断点处
[c]ontinue

# 执行一行源代码（会跳转到函数调用内部）
[s]tep

# 执行一条 x86 指令（会跳转到函数调用内部）
[s]tep[i]

# 执行一行源代码（不会跳转到函数调用内部）
[n]ext

# 执行一条 x86 指令（不会跳转到函数调用内部）
[n]ext[i]

# 终止当前调试会话
[k]ill

# 打印栈轨迹，打印每个函数和它们的参数
[b]ack[t]race
info stack
where

# 退出 GDB
[q]uit
```

## 进入交互模式

`layout` 命令允许我们调试源代码的同时，显示源代码。

```{code-block} bash
# 未处于调试模式，进入 TUI 模式
gdb tui

# 已处于调试模式，进入 TUI 模式
tui enable

# 已处于 TUI 模式，展示下一个子窗口
layout next

# 已处于 TUI 模式，展示上一个子窗口
layout prev

# 已处于 TUI 模式，展示源代码
layout src

# 已处于 TUI 模式，展示汇编代码
layout asm

# 已处于 TUI 模式，同时展示源代码和汇编代码
layout split

# 已处于 TUI 模式，在展示源代码的同时，展示寄存器中的值
layout reg

# 已处于 TUI 模式，聚焦于下一个子窗口
focus next

# 已处于 TUI 模式，聚焦于上一个子窗口
focus prev

# 已处于 TUI 模式，聚焦于源代码子窗口
focus src

# 已处于 TUI 模式，聚焦于汇编代码子窗口
focus asm

# 已处于 TUI 模式，聚焦于寄存器子窗口
focus reg

# 已处于 TUI 模式，聚焦于命令行子窗口
focus cmd

# 已处于 TUI 模式，退出 TUI 模式
tui disable

# 已处于 TUI 模式，重新加载 TUI 模式
Ctrl + l
```

## 监视变量、寄存器和内存

```{code-block} bash
# 打印表达式的值
[p]rint <表达式>
    表达式中可以包含变量名、*内存地址、$寄存器名、常量

# 打印表达式的值（16 进制表示）
[p]rint/x <表达式>

# 打印内存地址中的值
[x]/(number)(format)(unit_size) <内存地址>
    number      从指定内存地址开始，连续的几个单位
    format      打印格式，如果是 i 则不打印数字，而是打印指令
    unit_size   数据大小 [b]ytes, [h]alfwords, [w]ords, [g]iants

# 反汇编某个函数
disassemble <函数名>
```

## 小技巧

如果在调试过程中修改了源代码，在下次运行 GDB 时使用 `run (args)` 可以重新定位到上次离开的地方。

使用 `Ctrl + z` 可以暂时将 GDB 挂起，然后使用命令 `jobs` 查看后台进程，使用 `fg <编号>` 恢复。

[100 个 GDB 小技巧](https://wizardforcel.gitbooks.io/100-gdb-tips/content/index.html)。
