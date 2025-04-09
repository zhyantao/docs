# 多文件编译

## 指定链接时 `.a` 文件的搜索路径

静态链接库的默认搜索行为和动态链接库是一样的。

如果静态库就在 GCC 的默认搜索路径下，可以直接使用下面的命令：

```bash
gcc your_program.c -lSDK
```

它会默认搜索名为 `libSDK.a` 的文件。

如果静态库没有在 GCC 的默认搜索路径下，需要人为指定搜索路径：

```bash
gcc your_program.c -Lpath/to/static/lib -lSDK
```

它会定位到名为 `path/to/static/lib/libSDK.a` 的文件。

如果库文件名没有 `lib` 前缀，那么在链接的时候，需要在 `-l` 参数后面加个冒号，改为 `-l:`：

```bash
gcc your_program.c -l:SDK
```

它会定位到名为 `SDK.a` 的文件。

## 指定运行时 `.so` 文件的搜索路径

增加编译选项：`rpath`

```bash
# 让程序在当前路径下搜索 so 文件
LDFLAGS += -Wl,--hash-style=sysv,-Bsymbolic,-rpath=.
```

## undefined reference to

出现这个问题，一般有以下几个原因：

1. 链接时缺少相关的 `.o` 文件（目标文件）
2. 链接时缺少相关的 `.so` 文件（动态库）
3. 链接时缺少相关的 `.a` 文件（静态库）
4. 链接了错误的 `.so` 或者 `.a` 文件
5. 在 C++ 代码中链接了 C 语言相关的库
6. 函数模板的定义写在了 `.cpp` 文件中

问题 3：只需要显式地给编译器指明去哪里找函数定义就可以了，具体做法就是在编译时增加编译选项 `-l<libname>` 和 `-L<libpath>`。

问题 4：这种情况发生在有多个重名的库文件，链接的时候找到第一个库文件后，便不再继续往后找了，很可能第一个库文件中不包含函数定义。因此，这种情况下，需要按顺序检查执行 `make` 命令时，`--sysroot` 和 `-L` 提示的包含路径。找到库文件后，使用下面的命令检查库文件中是否含有目标函数：

```bash
# 查看库中定义了哪些函数和变量
nm -D libpthread.so.0

# 查看库是如何与其它库交互的
readelf -d libpthread.so.0
```

问题 5：需要在 C++ 源代码的头文件中显示地声明引用的哪些头文件是用 C 语言写的，举例如下：

```cpp
#ifdef __cplusplus
extern "C" {
#endif

// TODO: include C header files here

#ifdef __cplusplus
}
#endif
```

问题 6：函数模板的定义需要写在 `.h` 文件中。

## DWARF error: could not find variable specification at offset

这是因为在 C++ 源代码文件中引用了 C 头文件，需要在 C 头文件中添加 `extern "C"`。

```cpp
#ifdef __cplusplus
extern "C" {
#endif

// TODO: include C header files here

#ifdef __cplusplus
}
#endif
```

## line 1: can't open: no such file

出现这个错误，通常是因为使用的编译器和运行平台不匹配。可能是你用 GCC 编译了程序，但是却在开发板上运行了程序。

## line 2: syntax error: bad function name

出现这个错误，通常是因为使用的编译器和运行平台不匹配。可能是你用 GCC 编译了程序，但是却在开发板上运行了程序。

## real-ld: cannot find crti.o: No such file or directory

在编译时，明明使用 `-L` 指定了 `crti.o` 所在的路径，为什么还是会提示找不到这个文件呢？这种情况下，应该是忘记了在链接时指定 `--sysroot`。

## undefined reference to `rpl_malloc'

这种错误多出现在交叉编译时，对 `rpl_malloc` 函数进行了重新定义，导致找不到原来的函数了。我们只需要注释掉重新定义的语句就可以了。

```cpp
// config.h

// #define malloc rpl_malloc
```

## skipping incompatible

如果链接时报 skipping incompatible 错误，这主要是因为库版本和平台版本不一致：

- 查看平台版本：`readelf -h main.o | grep -E "Magic|Machine"`
- 查看库版本：`readelf -h HD_CORS_SDK.a | grep -E "Magic|Machine"`

注意：用正则表达式匹配字符的时候，不应该随便在 Pattern 中加空格，如果写成 `"Magic | Machine"` 就匹配不到 `Magic` 字段了。

```{note}
Magic 字段主要关注前 5 个字节，第 1 个字节都是以 `0x7f` 开头，第 2、3、4 个字节分别是字母 `E`、`L`、`F` 的 ASCII 码，第 5 个字节如果是 `0x01` 表示该文件适用于 32 位平台，如果是 `0x02` 表示适用于 64 位平台。

Machine 字段中的 ARM 表示最高支持到 ARMv7 或 Aarch32，ARM 64-bit architecture 表示最高可支持到 ARMv8 或 Aarch64。

参考：[ELF 文件解析 1-前述+文件头分析 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/380908650)
```

## error: storage size of 'xxx' isn't known

一个可能的原因是 `$SYSROOT/usr/include` 目录下头文件和当前项目所用的同名头文件内容不一致。

## error: XXX uses VFP register arguments, output does not

这是因为你正在使用的交叉编译链不支持硬件浮点运算，需要更换支持硬件浮点运算的工具链：

```bash
sudo apt-get update
sudo apt-get install gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf
```

注：`gnueabi` 不支持硬件浮点运算，`gnueabihf` 是支持的。
