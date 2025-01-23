# Makefile

## 使用方法

| 描述                                 | 参考链接                                                                                                    |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| 针对多个独立 `.cc` 文件编写 Makefile | {download}`查看 Makefile 示例 <https://github.com/zhyantao/makefile/blob/master/tests/Makefile>`            |
| 对 `.tar.gz` 文件编写 Makefile       | {download}`查看 Makefile 示例 <https://github.com/zhyantao/makefile/blob/master/gptp/Makefile>`             |
| 使用一条命令编译多个子目录           | {download}`查看 Makefile 示例 <https://github.com/zhyantao/makefile/blob/master/Makefile>`                  |
| 配置交叉编译环境                     | {download}`查看 sdk.mk 示例 <https://github.com/zhyantao/makefile/blob/master/gptp/sdk.mk>`                 |
| 使用 buildroot 构建 toolchain        | {download}`查看 Makefile 示例 <https://github.com/zhyantao/makefile/blob/master/buildroot/Makefile>`        |
| 使用 yocto 构建 toolchain            | {download}`查看 Makefile 示例 <https://github.com/zhyantao/makefile/blob/master/yocto/Makefile>`            |
| 使用 `bitbake` 编译和打包模块        | {download}`查看 Makefile 示例 <https://github.com/zhyantao/makefile/blob/master/yocto/bitbake/Makefile.in>` |

出于跨平台的目的，你可能会用到一些比 Makefile 更自动化的构建工具，比如 CMake、Autoconf、Meson 等等。为此，我们不得不做一些相关的配置信息，如下所示：

::::{tab-set}
:::{tab-item} configure

```bash
cat <<EOF | tee config.site
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
EOF

cd $(SRC_DIR) && ./configure \
--prefix=$(DESTDIR) \
--build=i686-pc-linux-gnu \
--host=aarch64-linux \
--target=aarch64-linux \
--disable-test-modules \
--enable-optimizations \
--with-openssl=$(SYSROOT_DIR)/usr \
--with-openssl-rpath=auto \
--disable-ipv6 \
--with-config-site=CONFIG_SITE

# {x86,amd64,arm32,arm64,ppc32,ppc64le,ppc64be,s390x,mips32,mips64}-linux,
# {arm32,arm64,x86,mips32}-android, {x86,amd64}-solaris,
# {x86,amd64,arm64}-FreeBSD and {x86,amd64}-darwin
```

:::
:::{tab-item} CMakeLists

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
--build=x86_64-pc-linux-gnu \
--host=aarch64-linux \
--target=aarch64-linux
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

## 赋值操作

| 运算符 | 行为描述                     |
| ------ | ---------------------------- |
| `=`    | 定义变量                     |
| `:=`   | 重新定义变量，覆盖之前的值   |
| `?=`   | 如果变量未定义，则赋予默认值 |
| `+=`   | 在变量后追加值               |

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
