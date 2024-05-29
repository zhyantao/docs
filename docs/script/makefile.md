# Makefile

## 使用方法

1、编写 Makefile

```makefile
CXX := g++
CXXFLAGS := -c -Wall
LDFLAGS :=

TARGET := hello
SRCS := $(wildcard *.cpp)
OBJS := $(patsubst %.cpp, %.o, $(SRCS))

# 声明 `all` 为伪目标，防止与系统中的同名目标冲突
.PHONY: all
all: $(TARGET)

# 目标规则: 生成可执行文件
$(TARGET): $(OBJS)
	$(CXX) -o $@ $^ $(LDFLAGS)

# 编译规则: 生成目标文件
$(OBJS): %.o: %.cpp
	$(CXX) -o $@ -c $< $(CXXFLAGS)

.PHONY: clean
clean:
	rm -f *.o $(TARGET)
```

2、配置编译选项

```bash
cat <<EOF | tee config.site
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
EOF

cat <<EOF | tee sdk.mk
CURR_DIR := $(shell pwd)

SYSROOT_DIR := $(CURR_DIR)/../../arm-buildroot-linux-gnueabihf_sdk-buildroot
TOOLCHAIN_DIR := $(SYSROOT_DIR)/usr/bin
export PATH := $(addsuffix :$(TOOLCHAIN_DIR), $(PATH))

# cross compile options
export ARCH := arm
export CROSS_COMPILE := arm-buildroot-linux-gnueabihf-

export CC := $(CROSS_COMPILE)gcc
export CXX := $(CROSS_COMPILE)g++
# export CPP := $(CROSS_COMPILE)gcc -E
export AS := $(CROSS_COMPILE)as
export LD := $(CROSS_COMPILE)ld
export STRIP := $(CROSS_COMPILE)strip
export RANLIB := $(CROSS_COMPILE)ranlib
export OBJCOPY := $(CROSS_COMPILE)objcopy
export OBJDUMP := $(CROSS_COMPILE)objdump
export AR := $(CROSS_COMPILE)ar
export NM := $(CROSS_COMPILE)nm

export CCFLAGS := --sysroot=$(SYSROOT_DIR) -I$(SYSROOT_DIR)/usr/include -g -Wall
export LDFLAGS := -L$(SYSROOT_DIR)/lib -L$(SYSROOT_DIR)/usr/lib

export PKG_CONFIG_DIR := "$(SYSROOT_DIR)/usr/lib/pkgconfig"
export PKG_CONFIG_PATH := "$(PKG_CONFIG_DIR):$(SYSROOT_DIR)/usr/share/pkgconfig"
export PKG_CONFIG_LIBDIR := "$(PKG_CONFIG_DIR)"
export PKG_CONFIG_SYSROOT_DIR := "$(SYSROOT_DIR)"
export PKG_CONFIG_DISABLE_UNINSTALLED := "yes"
EOF
```

3、开始编译

出于跨平台的目的，你可能会用到一些比 Makefile 更自动化的构建工具，比如 CMake、Autoconf、Meson 等等。为此，我们不得不做一些相关的配置信息，如下所示：

::::{tab-set}
:::{tab-item} CMakelists
```bash
cat <<EOF | tee CMakeLists.txt
cmake_minimum_required(VERSION 3.12)
project(persondemo)
ADD_EXECUTABLE(persondemo main.cpp student.cpp)
EOF

mkdir $(SRC_DIR)/build
cd build && cmake ..
make
make install
```
:::
:::{tab-item} Autoconf
```bash
cd $(SRC_DIR) && autoreconf -vi
cd $(SRC_DIR) && ./configure \
--build=i686-pc-linux-gnu \
--target=aarch64-linux \
--host=aarch64-linux
make -C $(SRC_DIR)
make -C $(SRC_DIR) install
```
:::
:::{tab-item} Meson
```bash
cat <<EOF | tee aarch64-linux.ini
[constants]
sysroot_dir = '/arm-buildroot-linux-gnueabihf_sdk-buildroot/sysroot'
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

meson build_dir \
--prefix=$(CURR_DIR) \
--build-type=plain \
--cross-file $(CURR_DIR)/aarch64-linux.ini
cd build_dir && meson compile -C output_dir
meson install -C output_dir
```
:::
::::

这些工具本质上还是会生成 Makefile，因此，不管你用的什么构建工具，下面的步骤是通用的：

```makefile
CURR_DIR := $(shell pwd)
-include sdk.mk

# where is source code?
PROJECT_NAME := valgrind
VERSION := 3.23.0
TAR_BALL := $(PROJECT_NAME)-$(VERSION).tar.bz2
SRC_DIR := $(CURR_DIR)/$(PROJECT_NAME)-$(VERSION)

# where is the build results?
export DESTDIR := $(CURR_DIR)/build

# make
.PHONY: all
all:
	@cd $(SRC_DIR) && ./configure \
	--prefix=$(DESTDIR) \
	--build=i686-pc-linux-gnu \
	--target=aarch64-linux \
	--host=aarch64-linux \
	--disable-test-modules \
	--enable-optimizations \
	--with-openssl=$(SYSROOT_DIR)/usr \
	--with-openssl-rpath=auto \
	--disable-ipv6 \
	--with-config-site=CONFIG_SITE
	# {x86,amd64,arm32,arm64,ppc32,ppc64le,ppc64be,s390x,mips32,mips64}-linux, 
	# {arm32,arm64,x86,mips32}-android, {x86,amd64}-solaris, 
	# {x86,amd64,arm64}-FreeBSD and {x86,amd64}-darwin
	@cd $(SRC_DIR) && make -C $(SRC_DIR) -j8
	@cd $(SRC_DIR) && make -C $(SRC_DIR) install

# make clean
.PHONY: clean
clean:
	rm -rf $(SRC_DIR)
	rm -rf $(DESTDIR)

# make patch
.PHONY: patch
patch:
	tar xf $(TAR_BALL)
	@if [ ! -d "patches" ]; then mkdir -p $(CURR_DIR)/patches; fi
	@rm -rf $(DESTDIR) && mkdir -p $(DESTDIR)

# make repo
.PHONY: repo
repo:
	@cd $(SRC_DIR) && if [ ! -d ".git" ]; then git init; fi
	@cd $(SRC_DIR) && git config --add core.filemode false
	@cd $(SRC_DIR) && git config --global core.autocrlf false
	@cd $(SRC_DIR) && git add .
	@cd $(SRC_DIR) && git commit -m "commit before make patch"
	@echo "$(SRC_DIR) is already up to date"

# make diff
.PHONY: diff
diff:
	@cd $(SRC_DIR) && git config --add core.filemode false
	@cd $(SRC_DIR) && git config --global core.autocrlf false
	@cd $(SRC_DIR) && git add .
	@cd $(SRC_DIR) && git diff --cached > $(CURR_DIR)/patches/0000-undefined.patch
	@echo "patch file is saved to $(CURR_DIR)/patches/0000-undefined.patch"

# make help
.PHONY: help
help:
	@echo ""
	@echo -e "Step 1:\033[35m make patch \033[0m  Apply patches"
	@echo -e "Step 2:\033[35m make repo  \033[0m  Initilize git repository and commit"
	@echo -e "Step 3:\033[35m make       \033[0m  Check if the modifications are valid"
	@echo -e "Step 4:\033[35m TODO: edit \033[0m  Create, edit and save modifications"
	@echo -e "Step 5:\033[35m make diff  \033[0m  Generate a patch file"
	@echo ""
```

参考文档：<https://seisman.github.io/how-to-write-makefile>。

## 赋值操作

|运算符|行为描述|
|---|---|
|`=`|定义变量 |
|`:=`|重新定义变量，覆盖之前的值 |
|`?=`|如果变量未定义，则赋予默认值 |
|`+=`|在变量后追加值 |

```makefile
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
