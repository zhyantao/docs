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
