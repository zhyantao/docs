# Compile

## Makefile

### 使用方法

1、编写 Makefile

```bash
CXX := g++
CXXFLAGS := -c -Wall
LDFLAGS :=

TARGET := hello
SRCS := $(wildcard *.cpp)
OBJS := $(patsubst %.cpp, %.o, $(SRC))

# 声明 `all` 为伪目标，防止与系统中的同名目标冲突
.PHONY:
all: $(TARGET)

# 目标规则: 生成可执行文件
$(TARGET): $(OBJS)
    $(CXX) -o $@ $^ $(LDFLAGS)

# 编译规则: 生成目标文件
$(OBJS): %.o: %.cpp
    $(CXX) -o $@ -c $< $(CXXFLAGS)

.PHONY:
clean:
    rm -f *.o $(TARGET)
```

2、配置编译选项

```bash
cat <<EOF | tee config.site
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
EOF
```

3、开始编译

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

参考文档：<https://seisman.github.io/how-to-write-makefile>。

### 赋值操作

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

### 通配符

| 通配符 | 作用                                |
| ------ | ----------------------------------- |
| `$@`   | 代表目标文件，也就是 `:` 左侧的文件 |
| `$^`   | 代表依赖文件，也就是 `:` 右侧的文件 |
| `$<`   | 代表第一个依赖文件                  |
| `%`    | 匹配字符串中任意个字符              |

### 常用函数

| 函数                                   | 作用                                                    |
| -------------------------------------- | ------------------------------------------------------- |
| `$(subst from,to,text)`                | 将 `text` 中的 `from` 替换为 `to`                       |
| `$(patsubst pattern,replacement,text)` | 将 `text` 中符合格式 `pattern` 的字替换为 `replacement` |
| `$(strip string)`                      | 去掉前导和结尾空格，并将中间的多个空格压缩为单个空格    |
| `$(wildcard pattern)`                  | 匹配 `pattern`，文件名之间用一个空格隔开                |

## CMakeLists

使用 CMake 最大的优势在于跨平台，它会为我们生成一份 Makefile，然后就和 Makefile 的使用方法就一样了。

1、编写 CMakeLists

```cmake
# CMakeLists.txt

cmake_minimum_required(VERSION 3.12)

project(persondemo)

ADD_EXECUTABLE(persondemo main.cpp student.cpp)
```

2、开始编译

```bash
mkdir build
cd build && cmake ..
make
sudo make install
```

1. 在 Linux 下使用 CMake 构建应用程序. <https://www.ibm.com/developerworks/cn/linux/l-cn-cmake/>
2. CMake 入门实战. <https://www.hahack.com/codes/cmake/>
3. CMake 实战 <https://kdocs.cn/l/ch0JlSoQjQdm>

## Autoconf

```bash
cd /path/to/src && autoreconf -vi

cd /path/to/src && ./configure \
--build=i686-pc-linux-gnu \
--target=aarch64-linux \
--host=aarch64-linux \

make -C /path/to/src
make -C /path/to/src install
```

## Meson

```bash
cat <<EOF | tee /path/to/aarch64-linux.ini
[constants]
sdk_dir = '/path/to/sdk'
sysroot_dir = sdk_dir + '/sysroot'
toochain_dir = sysroot_dir + '/usr/bin'
crosstools_prefix = toolchain_dir + '/aarch64-linux-'

[binaries]
c = crosstools_prefix + 'gcc'
cpp = crosstools_prefix + 'g++'
strip = crosstools_prefix + 'strip'
pkgconfig = 'pkg-config'

[build-in options]
has_function_print = true
has_function_hfkerhisadf = false
allow_default_for_cross = true

[host_machine]
system = 'linux'
cpu_family = 'arm'
cpu = 'cortex-a9'
endian = 'little'

[build_machine]
system = 'linux'
cpu_family = 'x86_64'
cpu = 'i686'
EOF
```

```bash
export CMAKE := /path/to/bin/cmake

export PKG_CONFIG_PATH :=
export PKG_CONFIG_LIBDIR := /path/to/usr/lib/pkgconfig:/path/to/usr/share/pkgconfig
export PKG_CONFIG_SYSROOT_DIR := /path/to/sysroot

CURR_DIR := $(shell pwd)

meson build_dir \
--prefix=$(CURR_DIR) \
--build-type=plain \
--cross-file /path/to/aarch64-linux.ini

cd build_dir && meson compile -C output_dir

meson install -C output_dir
```
