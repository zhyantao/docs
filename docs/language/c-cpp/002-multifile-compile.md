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

在链接阶段，一个常见的错误是 `collect2: ld returned 1 exit status`，这通常是因为编译器找不到函数定义。因此，解决方法就是我们需要显式地给编译器说，去哪里找函数定义，也就是增加编译选项，如 `-lpthread` 就是告诉编译器我们在代码中使用到了多线程编程方法，要去 `thread` 库中去找函数定义。

更多链接问题，可以参考 <https://www.cnblogs.com/schips/p/13728080.html>。
