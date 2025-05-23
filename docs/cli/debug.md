# debug

在 Linux 系统中，有许多常用的调试和分析工具，用于检查二进制文件、调试程序、分析性能等。以下是一些常见的工具及其用途：

## 二进制文件分析工具

| 工具      | 说明                                                   |
| --------- | ------------------------------------------------------ |
| `objdump` | 显示目标文件的详细信息，包括反汇编、段信息、符号表等。 |
| `readelf` | 显示 ELF 文件的详细信息，如段头、符号表、动态段等。    |
| `file`    | 检测文件类型（如可执行文件、共享库等）。               |
| `strings` | 提取文件中的可打印字符串。                             |
| `ldd`     | 列出可执行文件或共享库依赖的动态库。                   |

## 调试工具

| 工具        | 说明                                                                  |
| ----------- | --------------------------------------------------------------------- |
| `gdb`       | GNU 调试器，用于调试 C/C++ 程序，支持断点、单步执行、变量查看等功能。 |
| `strace`    | 跟踪程序执行时的系统调用和信号。                                      |
| `ltrace`    | 跟踪程序执行时的库函数调用。                                          |
| `valgrind`  | 内存调试工具，检测内存泄漏、非法内存访问等问题。                      |
| `addr2line` | 将地址转换为文件名和行号（用于调试崩溃问题）。                        |

## 性能分析工具

| 工具     | 说明                                                  |
| -------- | ----------------------------------------------------- |
| `perf`   | Linux 性能分析工具，支持 CPU 性能分析、函数调用图等。 |
| `gprof`  | 分析程序的性能瓶颈，生成函数调用图和耗时统计。        |
| `htop`   | 交互式进程查看器，实时监控系统资源使用情况。          |
| `vmstat` | 报告虚拟内存、CPU、I/O 等系统状态。                   |
| `iostat` | 监控系统 I/O 设备的使用情况。                         |

## 动态分析工具

| 工具      | 说明                                                                    |
| --------- | ----------------------------------------------------------------------- |
| `ld.so`   | 动态链接器，支持环境变量 `LD_PRELOAD` 和 `LD_LIBRARY_PATH` 等调试功能。 |
| `dmesg`   | 查看内核日志，用于分析内核级别的错误。                                  |
| `sysctl`  | 查看和修改内核参数。                                                    |
| `tcpdump` | 网络抓包工具，用于分析网络流量。                                        |

## 静态分析工具

| 工具         | 说明                                                   |
| ------------ | ------------------------------------------------------ |
| `cppcheck`   | C/C++ 代码静态分析工具，检测潜在的错误和代码风格问题。 |
| `clang-tidy` | Clang 的静态分析工具，支持代码风格检查和优化建议。     |
| `splint`     | C 代码的静态分析工具，检测潜在的错误和漏洞。           |

## 崩溃分析工具

| 工具       | 说明                                           |
| ---------- | ---------------------------------------------- |
| `coredump` | 分析程序崩溃时生成的核心转储文件。             |
| `gdb`      | 加载核心转储文件，分析崩溃时的堆栈和变量状态。 |
| `bt`       | 在 `gdb` 中查看崩溃时的堆栈回溯信息。          |

## 其他工具

| 工具      | 说明                                       |
| --------- | ------------------------------------------ |
| `ps`      | 查看当前运行的进程信息。                   |
| `top`     | 实时监控系统进程和资源使用情况。           |
| `lsof`    | 列出打开的文件和网络连接。                 |
| `netstat` | 查看网络连接、路由表、接口统计等信息。     |
| `pidstat` | 监控进程的 CPU、内存、I/O 等资源使用情况。 |

## 工具组合使用示例

### 调试崩溃问题

- 使用 `gdb` 加载核心转储文件：
  ```bash
  gdb ./my_program core
  ```
- 在 `gdb` 中使用 `bt` 查看堆栈回溯：
  ```bash
  (gdb) bt
  ```

### 查看目标文件的符号表

```bash
nm myfile.o
```

输出示例：

```
0000000000000000 T main
0000000000000000 D global_var
                 U printf
```

- `T main`：`main` 是一个在文本段中定义的函数。
- `D global_var`：`global_var` 是一个在已初始化数据段中定义的全局变量。
- `U printf`：`printf` 是一个未定义的符号，需要从外部链接。

### 查看共享库的动态符号表

```bash
nm -D libexample.so
```

输出示例：

```
00000000000005a0 T my_function
                 U malloc
```

- `T my_function`：`my_function` 是在共享库中定义的函数。
- `U malloc`：`malloc` 是一个未定义的符号，需要从外部链接。

### 解码 C++ 符号名称

```bash
nm -C myfile.o
```

输出示例：

```
0000000000000000 T main
0000000000000000 D global_var
                 U std::cout
```

- `std::cout` 是一个解码后的 C++ 符号名称。

### 显示符号大小

```bash
nm -S myfile.o
```

输出示例：

```
0000000000000000 0000000000000014 T main
0000000000000000 0000000000000004 D global_var
```

- `0000000000000014` 是 `main` 函数的大小（20 字节）。
- `0000000000000004` 是 `global_var` 变量的大小（4 字节）。

### 分析内存泄漏

- 使用 `valgrind` 检查内存泄漏：
  ```bash
  valgrind --leak-check=full ./my_program
  ```

### 分析系统调用

- 使用 `strace` 跟踪程序执行时的系统调用：
  ```bash
  strace ./my_program
  ```

### 分析性能瓶颈

- 使用 `perf` 分析程序的 CPU 性能：
  ```bash
  perf record ./my_program
  perf report
  ```

### 查看动态库依赖

- 使用 `ldd` 查看可执行文件的动态库依赖：
  ```bash
  ldd ./my_program
  ```

## 查看 gpio 占用情况

```bash
cat /sys/kernel/debug/gpio
```
