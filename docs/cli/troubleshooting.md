# Troubleshooting

```{admonition} 重要提示！
先在 tldr 上搜索：<https://tldr.inbrowser.app/>

- 内核与驱动开发：<https://bootlin.com/doc/training/linux-kernel/linux-kernel-slides.pdf>
- 调试技术：<https://bootlin.com/doc/training/debugging/debugging-slides.pdf>
- 音频模块：<https://bootlin.com/doc/training/audio/audio-slides.pdf>
- 抢占式实时 OS：<https://bootlin.com/doc/training/preempt-rt/preempt-rt-slides.pdf>
- 嵌入式 Linux：<https://bootlin.com/doc/training/embedded-linux/embedded-linux-slides.pdf>
- 图形与图像系统：<https://bootlin.com/doc/training/graphics/graphics-slides.pdf>
```

| 工具类别         | 工具名称     | 主要功能描述                                         |
| ---------------- | ------------ | ---------------------------------------------------- |
| **网络分析**     | `netstat`    | 显示网络连接、路由表、接口统计等信息                 |
|                  | `tcpdump`    | 网络抓包工具，用于分析网络流量                       |
|                  | `iperf`      | 网络带宽测试工具                                     |
| **文件分析**     | `lsof`       | 列出打开的文件和网络连接                             |
|                  | `file`       | 检测文件类型                                         |
|                  | `strings`    | 提取文件中的可打印字符串                             |
| **系统调用跟踪** | `strace`     | 跟踪程序执行时的系统调用和信号                       |
|                  | `ltrace`     | 跟踪程序执行时的库函数调用                           |
| **性能分析**     | `perf`       | Linux 性能分析工具，支持 CPU 性能分析、函数调用图等  |
|                  | `gprof`      | 分析程序的性能瓶颈，生成函数调用图和耗时统计         |
|                  | `vmstat`     | 报告虚拟内存、CPU、I/O 等系统状态                    |
|                  | `iostat`     | 监控系统I/O设备的使用情况                            |
|                  | `htop`       | 交互式进程查看器，实时监控系统资源使用情况           |
| **内存调试**     | `valgrind`   | 内存调试工具，检测内存泄漏、非法内存访问等问题       |
|                  | `gcov`       | 代码覆盖率测试工具                                   |
| **二进制分析**   | `objdump`    | 显示目标文件的详细信息，包括反汇编、段信息、符号表等 |
|                  | `readelf`    | 显示 ELF 文件的详细信息，如段头、符号表、动态段等    |
|                  | `nm`         | 显示目标文件的符号表                                 |
|                  | `addr2line`  | 将地址转换为文件名和行号                             |
|                  | `ldd`        | 列出可执行文件或共享库依赖的动态库                   |
| **内核调试**     | `dmesg`      | 查看内核日志，用于分析内核级别的错误                 |
|                  | `sysctl`     | 查看和修改内核参数                                   |
|                  | `procd`      | OpenWrt 进程管理工具                                 |
| **动态分析**     | `ld.so`      | 动态链接器，支持环境变量调试功能                     |
| **静态分析**     | `cppcheck`   | C/C++ 代码静态分析工具                               |
|                  | `clang-tidy` | Clang 的静态分析工具                                 |
|                  | `splint`     | C 代码的静态分析工具                                 |
| **进程管理**     | `ps`         | 查看当前运行的进程信息                               |
|                  | `top`        | 实时监控系统进程和资源使用情况                       |
|                  | `pidstat`    | 监控进程的 CPU、内存、I/O 等资源使用情况             |

## netstat

```bash
# 显示 gpsd 进程的所有网络资源（TCP/UDP/UNIX）
netstat -ap | grep gpsd
```

## tcpdump

```bash
# 捕获 53494 端口的流量
tcpdump -i any port 53494

# 显示时间戳和数据内容
tcpdump -i any port 53494 -tttt -A

# 保存原始数据包供后续分析
tcpdump -i any port 53494 -w save.pcap
```

## lsof

```bash
# 查看 gpsd 所有打开的文件
lsof | grep gpsd
```

## strace

```bash
# 附加到正在运行的 gpsd 进程上，跟踪所有网络相关的系统调用
strace -p 7497 -e trace=network -s 100
```

(gdb_tips)=

## gdb

| 类别               | 命令                 | 描述                       | 示例                   |
| ------------------ | -------------------- | -------------------------- | ---------------------- |
| **断点与执行控制** | `break <函数名>`     | 设置函数断点               | `break main`           |
|                    | `break <文件:行号>`  | 在指定文件的指定行设置断点 | `break main.c:10`      |
|                    | `info break`         | 查看所有断点               | `info break`           |
|                    | `delete <断点编号>`  | 删除断点                   | `delete 1`             |
|                    | `run <args>`         | 启动程序                   | `run arg1 arg2`        |
|                    | `continue`           | 继续执行                   | `continue`             |
|                    | `step`               | 单步进入函数               | `step`                 |
|                    | `next`               | 单步跳过函数               | `next`                 |
| **调用栈与上下文** | `backtrace`          | 打印调用栈                 | `backtrace`            |
|                    | `frame <编号>`       | 切换栈帧                   | `frame 2`              |
|                    | `info locals`        | 查看当前帧局部变量         | `info locals`          |
| **变量与内存查看** | `print <表达式>`     | 打印表达式的十进制值       | `print x`              |
|                    | `print /x <表达式>`  | 打印表达式的十六进制值     | `print /x x`           |
|                    | `x/<格式> <地址>`    | 检查内存                   | `x/4wx 0x7fffffffe000` |
|                    | `watch <表达式>`     | 设置数据观察点             | `watch *0x12345678`    |
| **寄存器与汇编**   | `info registers`     | 查看寄存器值               | `info registers`       |
|                    | `disassemble <函数>` | 反汇编函数                 | `disassemble main`     |
| **布局与界面**     | `layout src`         | 显示源代码窗口             | `layout src`           |
|                    | `layout asm`         | 显示汇编窗口               | `layout asm`           |
|                    | `layout split`       | 同时显示源码和汇编         | `layout split`         |
|                    | `layout regs`        | 显示寄存器窗口             | `layout regs`          |
|                    | `focus <窗口>`       | 切换焦点窗口               | `focus cmd`            |
|                    | `refresh`            | 刷新布局显示               | `refresh`              |
|                    | `tui reg <寄存器组>` | 显示特定寄存器组           | `tui reg general`      |

## grep

| 命令    | 等价形式  | 示例说明                                                           |
| ------- | --------- | ------------------------------------------------------------------ |
| `grep`  | -         | `grep "error" file.txt`（搜索文件中的 `"error"`）                  |
|         |           | `grep -i "hello" file.txt`（忽略大小写搜索 `"hello"`）             |
|         |           | `grep -r "pattern" /path/to/dir/`（递归搜索目录）                  |
| `egrep` | `grep -E` | `egrep "error\|warning" file.txt`（匹配 `"error"` 或 `"warning"`） |
|         |           | `egrep "[0-9]{3}" file.txt`（匹配 3 位数字）                       |
| `fgrep` | `grep -F` | `fgrep "$100" file.txt`（直接搜索 `"$100"`，避免 `$` 被当作正则）  |
|         |           | `fgrep "*.log" file.txt`（搜索字面值 `"*.log"`，不解析为通配符）   |

## sed

```bash
# 将 filename.txt 中的 abc def 替换为 def abc
sed -i 's@abc def@def abc@' filename.txt
```

注：`@` 可以是其他符号，它的主要作用在于区分需要替换的字符串和原始字符串。

## tee

`tee` 命令主要用于将一段文字写入文件。

```bash
cat <<EOF | tee ~/.config/pip/pip.conf
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
EOF
```

如果向文件中添加的内容包含特殊字符，比如 `$()`，我们发现 `$()` 消失不见了，解决方式如下：

```bash
cat <<\EOF | tee test.txt
CURR_DIR := $(shell pwd)
EOF
```

## tar

`tar` 命令主要用于打包文件和目录，并不直接进行压缩。

如果你希望在打包的同时也减小文件的大小，你需要在使用 `tar` 命令时结合一个压缩工具，如 `gzip`、`bzip2`、`xz` 等。例如：

- 使用 `gzip` 压缩：`tar czf archive_name.tar.gz file_or_directory_to_compress`
- 使用 `bzip2` 压缩：`tar cjf archive_name.tar.bz2 file_or_directory_to_compress`
- 使用 `xz` 压缩：`tar cJf archive_name.tar.xz file_or_directory_to_compress`

解压时，仍然需要跟上 `z`、`j` 或者 `J` 选项，才能正常解压。

## 快捷键

| 快捷键/命令       | 功能描述                                              |
| ----------------- | ----------------------------------------------------- |
| `Ctrl + s`        | 冻结窗口，用 `Ctrl + q` 或 `Ctrl + C` 退出            |
| `Ctrl + l`        | 清屏                                                  |
| `Ctrl + c`        | 终止程序运行                                          |
| `echo`            | 输出到屏幕                                            |
| `echo $PATH`      | 显示环境变量                                          |
| `echo $?`         | 显示上次命令是否运行成功（0 表示成功，非 0 表示失败） |
| `df`              | 查看内存和交换分区的使用情况                          |
| `df [-m\|-g\|-k]` | 以指定单位（M、G、K）显示内存和交换分区使用情况       |
| `shutdown`        | 关机                                                  |
| `reboot`          | 重启                                                  |
| `halt`            | 关机后关闭电源                                        |
