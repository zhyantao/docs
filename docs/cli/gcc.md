# GCC

本文将详细介绍如何更优秀地使用 GCC 编译器生成高质量代码，包括编译优化、GDB 调试配合以及常见低级错误的检测和预防。

## 编译优化策略

### 优化级别选择

GCC 提供了多个优化级别，合理选择对代码性能至关重要：

```bash
# 开发调试阶段 - 不优化，便于调试（Debug Version）
gcc -O0 -g -o program program.c

# 发布版本 - 平衡优化（Release Version）
gcc -O2 -o program program.c

# 高性能需求 - 激进优化
gcc -O3 -march=native -o program program.c

# 空间优化 - 嵌入式系统等
gcc -Os -o program program.c
```

### 架构特定优化

```bash
# 为当前 CPU 架构优化
gcc -O2 -march=native -o program program.c

# 为特定架构优化
gcc -O2 -march=haswell -o program program.c

# 启用所有安全优化
gcc -O2 -mtune=native -o program program.c
```

### 链接时优化 (LTO)

```bash
# 启用链接时优化
gcc -flto -O2 -o program program1.c program2.c

# 并行 LTO 编译
gcc -flto=auto -O2 -o program program1.c program2.c
```

## 与 GDB 调试器配合使用

### 调试信息生成

```bash
# 生成完整调试信息
gcc -g3 -O0 -o program program.c

# 生成基础调试信息（推荐发布版本调试）
gcc -g -O2 -o program program.c

# 分离调试信息
gcc -g -O2 -o program program.c
objcopy --only-keep-debug program program.debug
strip --strip-debug program
```

### GDB 常用调试技巧

```bash
# 启动调试
gdb ./program

# 设置断点
(gdb) break main
(gdb) break filename.c:linenumber

# 查看变量
(gdb) print variable_name
(gdb) display variable_name

# 查看内存
(gdb) x/10x &array   # 查看 10 个十六进制内存单元
(gdb) x/20s pointer  # 查看 20 个字符串

# 回溯跟踪
(gdb) backtrace
(gdb) backtrace full  # 显示所有帧的局部变量

# 观察点
(gdb) watch variable           # 变量改变时中断
(gdb) watch *(int*)0x12345678  # 内存地址观察
```

### 调试优化代码

```bash
# 即使优化也保留部分调试信息
gcc -g -O2 -fno-omit-frame-pointer -o program program.c
```

## 检测和优化低级错误

### 警告选项配置

```bash
# 启用所有警告
gcc -Wall -Wextra -o program program.c

# 更严格的警告
gcc -Wall -Wextra -Wpedantic -o program program.c

# 将警告视为错误
gcc -Wall -Werror -o program program.c

# 特定警告控制
gcc -Wall -Wno-unused-parameter -o program program.c

# 作用域变量冲突检查
gcc -Wall -Wextra -Werror -Wconversion -Wshadow -o program program.c
```

### 静态分析工具

```bash
# 启用GCC静态分析
gcc -fanalyzer -o program program.c

# 使用额外静态分析工具
scan-build gcc -o program program.c
cppcheck --enable=all program.c
```

### 内存错误检测

```bash
# 地址消毒剂 (AddressSanitizer)
gcc -fsanitize=address -g -O1 -o program program.c

# 未定义行为检测
gcc -fsanitize=undefined -g -O1 -o program program.c

# 内存消毒剂
gcc -fsanitize=memory -g -O1 -o program program.c

# 线程错误检测
gcc -fsanitize=thread -g -O1 -o program program.c
```

### 代码保护技术

```bash
# 栈保护
gcc -fstack-protector-strong -o program program.c

# 缓冲区溢出保护
gcc -D_FORTIFY_SOURCE=2 -O2 -o program program.c

# 位置无关执行 (PIE)
gcc -fPIE -pie -o program program.c

# 立即绑定
gcc -Wl,-z,now -Wl,-z,relro -o program program.c
```

## 性能分析指导优化

### 性能分析选项

```bash
# 生成性能分析信息
gcc -pg -O2 -o program program.c

# 使用 gprof 分析
./program
gprof program gmon.out > analysis.txt

# 使用 perf 分析
perf record ./program
perf report
```

### 基于分析的反馈优化

```bash
# 生成分析数据
gcc -fprofile-generate -O2 -o program program.c
./program  # 运行生成分析数据

# 使用分析数据优化
gcc -fprofile-use -O2 -o program program.c
```

## 实用编译脚本示例

```bash
#!/bin/bash
# build_debug.sh - 开发调试版本
gcc -g3 -O0 -Wall -Wextra -fsanitize=address \
    -fno-omit-frame-pointer \
    -DDEBUG \
    -o program program.c

#!/bin/bash
# build_release.sh - 发布版本
gcc -O2 -flto=auto -march=native \
    -fstack-protector-strong -D_FORTIFY_SOURCE=2 \
    -s -Wl,--gc-sections \
    -o program program.c
```

## 常见编译问题解决

### 依赖管理

```bash
# 显示所有依赖（编译报错的时候可以追溯调用栈）
gcc -M program.c

# 生成依赖文件
gcc -MD -c program.c -o program.o

# 指定包含路径
gcc -I/usr/local/include -L/usr/local/lib -lname program.c
```

### 符号和调试

```bash
# 查看可执行文件符号
nm program

# 查看动态依赖
ldd program

# 去除调试符号（发布版本）
strip program

# 保留调试符号但减小体积
strip --strip-debug program
```
