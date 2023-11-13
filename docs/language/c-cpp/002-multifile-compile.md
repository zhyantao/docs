# 多文件编译

## 创建三个文件

main.cpp

```cpp
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

mul.cpp

```cpp
#include "mul.hpp"

int mul(int a, int b)
{
    return a * b;
}
```

mul.hpp

```cpp
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

## 常见的链接错误

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

#include "head_file_c.h"
...

#ifdef __cplusplus
}
#endif
```

更多链接阶段出现的问题，可以参考 <https://www.cnblogs.com/schips/p/13728080.html>。

**2、DWARF error: could not find variable specification at offset**

这个错误和 `-g` 参数有关。报这个错误有可能是因为函数签名用了 `static`，但是在函数体内部，却调用了非 `static` 函数。这种情况下，因为 `static` 函数在链接时就会去找函数实现，但是非 `static` 函数在运行时才会加载到内存，才会出现找不到引用的故障。
