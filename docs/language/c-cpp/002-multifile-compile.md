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
g++ main.o mul.o -o mul
```

链接阶段的常见的错误是 `collect2: ld returned 1 exit status` 和 ``undefined reference to `main'``，这是因为编译器无法找到函数定义。对应的解决方法就是我们需要 **显式地给编译器指明去哪里找函数定义**，做法就是增加编译选项。

举例来讲，如果代码中使用了 `pthread_create()` 这个函数，就需要引用 `libpthread.so` 这个动态链接库。具体的做法就是去掉库文件名中的 `lib` 和 `.so`，在库名前面加上 `-l`，因此，最后的结果就是 `-lpthread`，这里的 `-l` 是 `link` 的意思。这样 GCC 编译期就知道要去 `libpthread.so` 这个库中去找函数定义了。

在链接时，编译期会在当前目录下已经编译生成的 `.o` 文件和编译选项中指定的 `.so` 文件中去找函数定义。记住这一点很重要，会帮助我们解决很多 `undefined reference` 问题。

如果出现 `DWARF error: could not find variable specification at offset xxxx`，这个错误和 `-g` 参数有关。报这个错误有可能是因为函数签名用了 `static`，但是在函数体内部，却调用了非 `static` 函数。这种情况下，因为 `static` 函数在链接时就会去找函数实现，但是非 `static` 函数在运行时才会加载到内存，才会出现找不到引用的故障。

更多链接阶段出现的问题，可以参考 <https://www.cnblogs.com/schips/p/13728080.html>。
