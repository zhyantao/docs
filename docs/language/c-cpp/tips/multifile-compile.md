# 多文件编译

## 创建三个文件

```cpp
// main.cpp

#include <iostream>
#include "mul.hpp"

using namespace std;

int main()
{
    int a, b;
    int result;

    cout << "Pick two integers:";
    cin >> a;
    cin >> b;

    result = mul(a, b);

    cout << "The result is " << result << endl;
    return 0;
}

```

```cpp
// mul.cpp

#include "mul.hpp"

int mul(int a, int b)
{
    return a * b;
}
```

```cpp
// mul.hpp

#pragma once

int mul(int a, int b);
```

## 编译

```shell
g++ -c main.cpp
g++ -c mul.cpp
```

## 链接

```shell
g++ -o mul main.o mul.o
```

## Q & A

**1、undefined reference to**

出现这个问题，一般有以下几个原因：

1. 链接时缺少相关的 `.o` 文件（目标文件）
2. 链接时缺少相关的 `.so` 文件（动态库）
3. 链接时缺少相关的 `.a` 文件（静态库）
4. 链接库文件时顺序错误
5. 在 C++ 代码中链接了 C 语言相关的库

针对前 3 个问题，只需要显式地给编译器指明去哪里找函数定义就可以了，具体做法就是在编译时增加编译选项 `-l<libname>` 和 `-L<libpath>`。

针对第 4 个问题，根据源代码的引用顺序调整库的链接顺序就可以了。

解决第 5 个问题，需要在 C++ 源代码的头文件中显示地声明引用的哪些头文件是用 C 语言写的，举例如下：

```cpp
#ifdef __cplusplus
extern "C"
{
#endif

// TODO: include C header files here

#ifdef __cplusplus
}
#endif
```

更多链接阶段出现的问题，可以参考 <https://www.cnblogs.com/schips/p/13728080.html>。

**2、DWARF error: could not find variable specification at offset**

出现这个问题，可能的原因有：（1）非 `static` 函数，调用了 `static` 函数。（2）忘记了在 Makefile 中链接 undefined reference 指向函数所在的文件。

**3、line 1: can't open: no such file**

出现这个错误，通常是因为使用的编译器和运行平台不匹配。可能是你用 GCC 编译了程序，但是却在开发板上运行了程序。

**4、line 2: syntax error: bad function name**

出现这个错误，通常是因为使用的编译器和运行平台不匹配。可能是你用 GCC 编译了程序，但是却在开发板上运行了程序。

**5、real-ld: cannot find crti.o: No such file or directory**

在编译时，明明使用 `-L` 指定了 `crti.o` 所在的路径，为什么还是会提示找不到这个文件呢？这种情况下，应该是忘记了在链接时指定 `--sysroot`。

**6、undefined reference to `rpl_malloc'**

这种错误多出现在交叉编译时，对 `rpl_malloc` 函数进行了重新定义，导致找不到原来的函数了。我们只需要注释掉重新定义的语句就可以了。

```cpp
// config.h

//#define malloc rpl_malloc
```

**7、静态库的链接问题**

如果静态库就在 gcc 的默认搜索路径下，可以直接使用下面的命令：

```bash
gcc your_program.c -lSDK
```

它会默认搜索名为 `libSDK.a` 这样的文件。

如果静态库没有在 gcc 的默认搜索路径下，需要人为指定搜索路径：

```bash
gcc your_program.c -Lpath/to/static/lib -lSDK
```

它会定位到 `path/to/static/lib/libSDK.a` 这个文件。

如果库文件名没有 `lib` 前缀，那么在链接的时候，需要在 `-l` 参数后面加个冒号，改为 `-l:`：

```bash
gcc your_program.c -l:SDK
```

它会定位到名为 `SDK.a` 这个静态库文件。

如果链接时报 skipping incompatible 错误，这主要是因为库版本和平台版本不一致：

- 查看平台版本：`readelf -h main.o | grep "Magic\|Machine"`
- 查看库版本：`readelf -h HD_CORS_SDK.a | grep "Magic\|Machine"`

```{note}
Magic 字段主要关注前 5 个字节，第 1 个字节都是以 `0x7f` 开头，第 2、3、4 个字节分别是字母 `E`、`L`、`F` 的 ASCII 码，第 5 个字节如果是 `0x01` 表示该文件适用于 32 位平台，如果是 `0x02` 表示适用于 64 位平台。

Machine 字段中的 ARM 表示最高支持到 ARMv7 或 Aarch32，ARM 64-bit architecture 表示最高可支持到 ARMv8 或 Aarch64。

注意：用正则表达式匹配字符的时候，不应该随便在 pattern 中加空格，如果写成 `"Magic \| Machine"` 就匹配不到 `Magic` 字段了。
```

参考：[ELF 文件解析 1-前述+文件头分析 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/380908650)
