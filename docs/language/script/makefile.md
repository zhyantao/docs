# Makefile

本文仅提供编写手动编写 Makefile 的简单示例，理解了本文就能够应付大部分的 Makefile 了，更加复杂的 Makefile 都是在这种简单规则上叠加的。但是只阅读本文是远远不够的，为了能够对 Makefile 有更加清晰的认识，我这里推荐另外一个文档：<https://seisman.github.io/how-to-write-makefile>。

```{note}
在实际工程中，虽然也有只用 Makefile 的项目，但是更为方便的方式是使用 CMakeList 来生成 Makefile。cmake 管理工程的最大优势在于跨平台，自己不用书写太复杂的脚本了，自己写一写配置文件，后面的工作就都是自动化的了。
```

## 使用方法

```bash
cat <<EOF | tee config.site
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
EOF
```

```bash
make clean

cd /path/to/src && ./configure \
--prefix=/path/to/install \
--build=i686-pc-linux-gnu \
--target=aarch64-linux \
--host=aarch64-linux \
--disable-test-modules \
--enable-optimizations \
--with-openssl=/path/to/sysroot/usr \
--with-openssl-rpath=auto \
--disable-ipv6 \
--with-config-site=CONFIG_SITE

make -C /path/to/src -j8
sudo make -C /path/to/src install
```

## 版本一

最简单的方式就是把文件一个一个手打出来进行编译。

```bash
# 基本格式：目标文件:依赖文件
hello: main.cpp printhello.cpp  factorial.cpp
    g++ -o hello main.cpp printhello.cpp  factorial.cpp
```

## 版本二

采用 Makefile 只会更新有变动的文件，在工程比较大的情况下可以节省很多时间。

```bash
CXX = g++
TARGET = hello
OBJ = main.o printhello.o factorial.o

$(TARGET): $(OBJ)
    $(CXX) -o $(TARGET) $(OBJ)

main.o: main.cpp
    $(CXX) -c main.cpp

printhello.o: printhello.cpp
    $(CXX) -c printhello.cpp

factorial.o: factorial.cpp
    $(CXX) -c factorial.cpp
```

## 版本三

```bash
CXX = g++
TARGET = hello
OBJ = main.o printhello.o factorial.o

CXXFLAGS = -c -Wall

$(TARGET): $(OBJ)
    $(CXX) -o $@ $^

%.o: %.cpp
    $(CXX) -o $@ -c $< $(CXXFLAGS)

# .PHONY 作用在于防止 clean 这个命令和系统中可能存在的 clean 命令冲突
.PHONY: clean
clean:
    rm -f *.o $(TARGET)
```

## 版本四

这是目前 Makefile 的主流编写方式。

```bash
# := 表示临时赋值
CXX := g++
TARGET := hello
SRCS := $(wildcard *.cpp)
OBJS := $(patsubst %.cpp, %.o, $(SRC))

CXXFLAGS := -c -Wall

$(TARGET): $(OBJS)
    $(CXX) -o $@ $^

%.o: %.cpp
    $(CXX) -o $@ -c $< $(CXXFLAGS)

.PHONY: clean
clean:
    rm -f *.o $(TARGET)
```

## 赋值操作

|运算符|行为描述|
|---|---|
|`=`|定义变量 |
|`:=`|重新定义变量，覆盖之前的值 |
|`?=`|如果变量未定义，则赋予默认值 |
|`+=`|在变量后追加值 |
```bash
var = "hello world"
$(info $(var))  # "hello world"

var ?= "update or not"
$(info $(var))  # "hello world"

var += "append"
$(info $(var))  # "hello world" "append"

var := "always update"
$(info $(var))  # "always update"

# 默认目标
all: 
	@echo "All done"  # All done

# 空目标，确保每个语句都会执行
.PHONY: all
```

## 通配符

| 通配符 | 作用                                |
| ------ | ----------------------------------- |
| `$@`   | 代表目标文件，也就是 `:` 左侧的文件 |
| `$^`   | 代表依赖文件，也就是 `:` 右侧的文件 |
| `$<`   | 代表第一个依赖文件                  |
| `%`    | 匹配字符串中任意个字符              |

## 常用函数

| 函数                                   | 作用                                                    |
| -------------------------------------- | ------------------------------------------------------- |
| `$(subst from,to,text)`                | 将 `text` 中的 `from` 替换为 `to`                       |
| `$(patsubst pattern,replacement,text)` | 将 `text` 中符合格式 `pattern` 的字替换为 `replacement` |
| `$(strip string)`                      | 去掉前导和结尾空格，并将中间的多个空格压缩为单个空格    |
| `$(wildcard pattern)`                  | 匹配 `pattern`，文件名之间用一个空格隔开                |
