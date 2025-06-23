# GDB 调试指南

(gdb_tips)=

## 基本使用

```bash
gdb --args myprogram arg1 arg2
```

## 断点与执行控制

| 命令                      | 描述                       | 示例                 |
| ------------------------- | -------------------------- | -------------------- |
| `break <函数名>`          | 设置函数断点               | `break main`         |
| `break <文件:行号>`       | 在指定文件的指定行设置断点 | `break main.c:10`    |
| `break *<内存地址>`       | 在内存地址设置断点         | `break *0x4005a0`    |
| `info break`              | 查看所有断点               | `info break`         |
| `delete <断点编号>`       | 删除断点                   | `delete 1`           |
| `condition <编号> <条件>` | 设置条件断点               | `condition 1 x > 10` |
| `run <args>`              | 启动程序                   | `run arg1 arg2`      |
| `continue`                | 继续执行                   | `continue`           |
| `step`                    | 单步进入函数               | `step`               |
| `next`                    | 单步跳过函数               | `next`               |
| `stepi`                   | 单步执行指令（进入函数）   | `stepi`              |
| `nexti`                   | 单步执行指令（跳过函数）   | `nexti`              |
| `finish`                  | 执行到当前函数返回         | `finish`             |
| `kill`                    | 终止当前调试会话           | `kill`               |

## 调用栈与上下文

| 命令           | 描述               | 示例          |
| -------------- | ------------------ | ------------- |
| `backtrace`    | 打印调用栈         | `backtrace`   |
| `frame <编号>` | 切换栈帧           | `frame 2`     |
| `info frame`   | 查看当前帧信息     | `info frame`  |
| `info args`    | 查看当前帧参数     | `info args`   |
| `info locals`  | 查看当前帧局部变量 | `info locals` |

## 变量与内存查看

| 命令                  | 描述                       | 示例                   |
| --------------------- | -------------------------- | ---------------------- |
| `print <表达式>`      | 打印表达式值               | `print x`              |
| `print/x <表达式>`    | 十六进制格式打印           | `print/x &x`           |
| `x/<格式> <地址>`     | 检查内存                   | `x/4wx 0x7fffffffe000` |
| `watch <表达式>`      | 设置数据观察点             | `watch *0x12345678`    |
| `info watchpoints`    | 查看观察点                 | `info watchpoints`     |
| `display <表达式>`    | 每次暂停时自动打印         | `display x`            |
| `info display`        | 查看自动显示表达式         | `info display`         |
| `set print pretty on` | 结构体/类按缩进格式显示    | `set print pretty on`  |
| `set print array on`  | 数组显示时每元素单独一行   | `set print array on`   |
| `set print null-stop` | 遇到 NULL 时停止打印字符串 | `set print null-stop`  |

## 寄存器与汇编

| 命令                 | 描述         | 示例               |
| -------------------- | ------------ | ------------------ |
| `info registers`     | 查看寄存器值 | `info registers`   |
| `disassemble <函数>` | 反汇编函数   | `disassemble main` |
| `set $<reg>=<值>`    | 修改寄存器值 | `set $rax=0`       |

## TUI 模式

| 命令           | 描述           | 示例           |
| -------------- | -------------- | -------------- |
| `tui enable`   | 启用 TUI 模式  | `tui enable`   |
| `layout src`   | 显示源代码窗口 | `layout src`   |
| `layout asm`   | 显示汇编窗口   | `layout asm`   |
| `layout split` | 显示源码和汇编 | `layout split` |
| `layout reg`   | 显示寄存器窗口 | `layout reg`   |
| `tui disable`  | 退出 TUI 模式  | `tui disable`  |

## 其他实用命令

| 命令             | 描述            |
| ---------------- | --------------- |
| `shell <命令>`   | 执行 shell 命令 |
| `set logging on` | 开启日志记录    |
| `show commands`  | 显示历史命令    |
| `quit`           | 退出 GDB        |
