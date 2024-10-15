# GDB

## 如何使用 GDB

首先，将程序编译并包含调试信息，然后在启动 GDB 时使用 `--args` 选项直接传递参数：

```bash
gdb --args myprogram arg1 arg2
```

进入 GDB 后，直接使用 `run` 命令即可。

(gdb_tips)=
## 设置断点、单步调试、打印调用栈

| 命令                          | 描述                                        | 示例                 |
| ----------------------------- | ------------------------------------------- | -------------------- |
| `break <函数名>`              | 设置断点                                    | `break main`         |
| `break <函数名:行号>`         | 在指定函数的指定行设置断点                  | `break main:10`      |
| `break <*内存地址>`           | 在指定内存地址设置断点                      | `break *0x4005a0`    |
| `disassemble <函数名>`        | 反汇编函数                                  | `disassemble main`   |
| `info break`                  | 查看断点编号                                | `info break`         |
| `delete <断点编号>`           | 删除断点                                    | `delete 1`           |
| `condition <断点编号> <条件>` | 在条件为真时停在断点处                      | `condition 1 x > 10` |
| `info <关于>`                 | 列出参数列表                                | `info frame`         |
| `file <可执行的文件名>`       | 将指定文件加载到 GDB 中                     | `file ./myprogram`   |
| `run (arg1 arg2 ... argn)`    | 执行已加载的可执行程序                      | `run arg1 arg2`      |
| `continue`                    | 继续执行源代码，停在下一个断点处            | `continue`           |
| `step`                        | 执行一行源代码（会跳转到函数调用内部）      | `step`               |
| `stepi`                       | 执行一条 x86 指令（会跳转到函数调用内部）   | `stepi`              |
| `next`                        | 执行一行源代码（不会跳转到函数调用内部）    | `next`               |
| `nexti`                       | 执行一条 x86 指令（不会跳转到函数调用内部） | `nexti`              |
| `kill`                        | 终止当前调试会话                            | `kill`               |
| `backtrace`                   | 打印栈轨迹，打印每个函数和它们的参数        | `backtrace`          |
| `info stack`                  | 打印栈轨迹                                  | `info stack`         |
| `where`                       | 打印当前调用栈                              | `where`              |
| `quit`                        | 退出 GDB                                    | `quit`               |

## 监视变量、寄存器和内存

| 命令                                       | 描述                          | 示例                   |
| ------------------------------------------ | ----------------------------- | ---------------------- |
| `print <表达式>`                           | 打印表达式的值                | `print x`              |
| `print/x <表达式>`                         | 打印表达式的值（16 进制表示） | `print/x x`            |
| `x/(number)(format)(unit_size) <内存地址>` | 打印内存地址中的值            | `x/4wx 0x7fffffffe000` |
| `disassemble <函数名>`                     | 反汇编某个函数                | `disassemble main`     |

## 调试过程中修改源代码

如果在调试过程中需要修改源代码，可以按照以下步骤操作：

1. 使用 `Ctrl+z` 暂时将 GDB 挂起；
2. 修改源代码；
3. 使用命令 `jobs` 查看后台进程；
4. 使用 `fg proc_num` 恢复；
5. 使用 `run (args)` 重新定位到上次离开的地方。

## 启用 TUI 增强调试体验

`layout` 命令允许我们在调试源代码的同时，显示源代码。

| 命令           | 描述                                 | 示例           |
| -------------- | ------------------------------------ | -------------- |
| `gdb tui`      | 未处于调试模式，进入 TUI 模式        | `gdb tui`      |
| `tui enable`   | 已处于调试模式，进入 TUI 模式        | `tui enable`   |
| `layout next`  | 展示下一个子窗口                     | `layout next`  |
| `layout prev`  | 展示上一个子窗口                     | `layout prev`  |
| `layout src`   | 展示源代码                           | `layout src`   |
| `layout asm`   | 展示汇编代码                         | `layout asm`   |
| `layout split` | 同时展示源代码和汇编代码             | `layout split` |
| `layout reg`   | 在展示源代码的同时，展示寄存器中的值 | `layout reg`   |
| `focus next`   | 聚焦于下一个子窗口                   | `focus next`   |
| `focus prev`   | 聚焦于上一个子窗口                   | `focus prev`   |
| `focus src`    | 聚焦于源代码子窗口                   | `focus src`    |
| `focus asm`    | 聚焦于汇编代码子窗口                 | `focus asm`    |
| `focus reg`    | 聚焦于寄存器子窗口                   | `focus reg`    |
| `focus cmd`    | 聚焦于命令行子窗口                   | `focus cmd`    |
| `tui disable`  | 退出 TUI 模式                        | `tui disable`  |
| `Ctrl + l`     | 重新加载 TUI 模式                    | `Ctrl + l`     |
