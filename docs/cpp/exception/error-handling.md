# 错误处理方式

处理程序中可能出现的错误，C/C++ 有多种方式可选，各有适用场景：

- **`assert`**：仅用于调试期检查，帮助尽早暴露逻辑错误；
- **错误码（返回值）**：调用方根据返回值判断是否出错；
- **`abort` / `exit`**：出现无法恢复的错误时直接终止程序；
- **异常（exception）**：通过 `throw`/`try-catch` 传递错误（见 [throw-try-catch](throw-try-catch)）；
- **`stderr` 输出**：向标准错误流输出诊断信息（错误码与 stderr 输出常配合使用）。

下面用同一个 `ratio()` 例子对比其中几种方式。

## assert

`assert` 在调试阶段检查条件，条件为假时终止程序。**注意**：定义 `NDEBUG` 后（发布版本），`assert` 会被完全移除，因此不能把必要的运行期检查写进 `assert`。

```cpp
#include <cassert>
#include <iostream>

int main(int argc, char** argv) {
    assert(argc == 2);
    std::cout << "This is an assert example." << std::endl;
    return 0;
}
```

## abort

`abort` 直接杀死程序（不会调用局部对象的析构函数），适用于无法继续执行的致命错误。

```cpp
#include <cfloat>
#include <cstdlib>
#include <iostream>

float ratio(float a, float b) {
    if (fabs(a + b) < FLT_EPSILON) {
        std::cerr << "The sum of the two arguments is close to zero." << std::endl;
        std::abort();
    }
    return (a - b) / (a + b);
    // return int(a - b) / int(a + b);// divided by zero behavior differently for int and float
}

int main() {
    float x = 0.f;
    float y = 0.f;
    float z = 0.f;

    std::cout << "Please input two numbers <q to quit>:";
    while (std::cin >> x >> y) {
        z = ratio(x, y);
        std::cout << "ratio(" << x << ", " << y << ") = " << z << std::endl;
        std::cout << "Please input two numbers <q to quit>:";
    }
    std::cout << "Bye!" << std::endl;
    return 0;
}
```

## 返回错误码

调用方通过返回值判断是否出错，错误信息则通过 `std::cerr` 输出。

```cpp
#include <cfloat>
#include <cstdlib>
#include <iostream>

bool ratio(float a, float b, float& c) {
    if (fabs(a + b) < FLT_EPSILON) {
        std::cerr << "The sum of the two arguments is close to zero." << std::endl;
        return false;
    }
    c = (a - b) / (a + b);
    return true;
}

int main() {
    float x = 0.f;
    float y = 0.f;
    float z = 0.f;

    std::cout << "Please input two numbers <q to quit>:";
    while (std::cin >> x >> y) {
        bool ret = ratio(x, y, z);
        if (ret)
            std::cout << "ratio(" << x << ", " << y << ") = " << z << std::endl;
        else
            std::cerr << "ratio(" << x << ", " << y << ") failed." << std::endl;

        std::cout << "Please input two numbers <q to quit>:";
    }
    std::cout << "Bye!" << std::endl;
    return 0;
}
```

## new 失败时的处理：异常 vs nothrow

默认情况下，`new` 分配失败时抛出 `std::bad_alloc` 异常；使用 `new(std::nothrow)` 时则返回空指针，不抛异常。

```cpp
#include <cstdlib>
#include <iostream>

using namespace std;

int main() {
    size_t length = 80000000000L;
    int* p        = NULL;

    try {
        cout << "Trying to allocate a big block of memory" << endl;
        p = new int[length];
        // p = new(std::nothrow) int[length];
        cout << "No exception." << endl;
    } catch (std::bad_alloc& ba) {
        cout << "bad_alloc exception!" << endl;
        cout << ba.what() << endl;
    }

    if (p)
        cout << "Memory successfully allocated." << endl;
    else
        cout << "So bad, null pointer." << endl;

    // for(size_t i = 0; i < length; i++)
    //     p[i] = i;
    // size_t sum;
    // for(size_t i = 0; i < length; i++)
    //     sum += p[i];
    // cout << "Sum = " << sum << endl;
    if (p) delete[] p;
    return 0;
}
```

## 标准错误输出 stderr / std::cerr

C 语言使用 `fprintf(stderr, ...)` 输出错误信息：

```cpp
#include <stdio.h>

void div(int n) {
    if (n % 2 != 0) {
        fprintf(stderr, "Error: The input must be an even number. Here it's %d\n", n);
    } else {
        int result = n / 2;
        fprintf(stdout, "Info: The result is %d\n", result);
    }
    return;
}

int main() {
    for (int n = -5; n <= 5; n++)
        div(n);
    return 0;
}
```

将正常输出（stdout）与错误输出（stderr）分开重定向，是排查问题时的重要技巧：

```bash
./a.out | less

# 将正常日志打印到 output.log 中，将错误日志打印到屏幕上
./a.out > output.log
./a.out 1> output.log
./a.out >> output.log

# 将正常日志打印到黑洞文件，将错误日志打印到屏幕上
./a.out > /dev/null

# 将错误日志打印到 error.log 中，将正常日志打印到屏幕上
./a.out 2> error.log

# 将正常日志打印到 output.log 中，将错误日志打印到 error.log
./a.out > output.log 2> error.log

# 后台运行，将所有日志（包括错误日志）打印到 all.log 中
./a.out &> all.log

# 前台运行，将所有日志（包括错误日志）打印到 all.log 中
./a.out > all.log 2>&1
```
