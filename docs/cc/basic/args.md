# 可变参数列表

## 可变参数宏

::::{tab-set}
:::{tab-item} `__VA_ARGS__`

`__VA_ARGS__` 原样替换传入的参数列表。

宏写法示例

```cpp
#define PRINTF(...) printf(__VA_ARGS__)
```

展开前调用

```cpp
PRINTF("a + b = %d", a + b);
```

宏展开结果

```cpp
printf("a + b = %d", a + b);
```

:::

:::{tab-item} `#__VA_ARGS__`

`#__VA_ARGS__` 将整个参数列表转换为字符串。注意参数本身也会被引号包裹。

宏写法示例

```cpp
#define PRINTF(...) printf(#__VA_ARGS__)
```

展开前调用

```cpp
PRINTF(1, "x", int);
```

宏展开结果

```cpp
printf("1, \"x\", int");
```

:::

:::{tab-item} `##__VA_ARGS__`

`##__VA_ARGS__` 如果没有额外参数，则会移除前面多余的逗号；有参数则保留。

宏写法示例

```cpp
#define PRINTF(fmt, ...) printf(fmt, ##__VA_ARGS__)
```

展开前调用

```cpp
PRINTF("a = %d", a);
```

宏展开结果

```cpp
printf("a = %d", a);
```

:::

:::{tab-item} `x...`

GCC 扩展语法（非标准），等同于 `__VA_ARGS__`，不推荐使用。

宏写法示例

```cpp
#define PRINTF(x...) printf(x)
```

展开前调用

```cpp
PRINTF("a + b = %d", a + b);
```

宏展开结果

```cpp
printf("a + b = %d", a + b);
```

:::
::::

实战案例：<https://gitee.com/zhyantao/misc/blob/master/leetcode/cpp/include/debug.h>

## 可变参数函数展开（C风格）

在上一节中，我们通过宏将可变参数直接传递给已有函数（如 `printf`）。这一节介绍如何在自定义函数中访问和处理可变参数列表。

**关键概念**

| 术语        | 含义                                                      |
| ----------- | --------------------------------------------------------- |
| `va_list`   | 类型，用于保存可变参数列表。                              |
| `va_start`  | 宏，初始化 `va_list`，使其指向第一个可变参数。            |
| `va_arg`    | 宏，从参数列表中提取下一个参数（需指定类型）。            |
| `va_end`    | 宏，清理 `va_list` 占用的资源。                           |
| `vsnprintf` | 函数，用于将格式化字符串写入缓冲区，支持 `va_list` 参数。 |

**示例 1：日志函数 `log`**

```cpp
#include <cstdarg>
#include <iostream>

void log(char* fmt, ...) {
    char buf[512] = {0};
    va_list ap;

    va_start(ap, fmt);                              // 初始化参数列表
    (void)vsnprintf(buf, sizeof(buf) - 2, fmt, ap); // 使用 vsnprintf 格式化输出
    va_end(ap);                                     // 清理参数列表

    printf("%s\n", buf);
}

int main() {
    log((char*)"%s, %d, %s", "hello", 100, "world");
}
```

**示例 2：求和函数 `sum`**

```cpp
#include <cstdarg>
#include <iostream>

double sum(int num, ...) {
    va_list ap; // 定义参数列表
    double ret = 0.0;

    va_start(ap, num); // 初始化参数列表

    for (int i = 0; i < num; i++) {
        ret += va_arg(ap, double); // 按类型依次取出参数
    }

    va_end(ap); // 清理参数列表

    return ret;
}

int main() {
    std::cout << "Sum of 2, 3 is " << sum(2, 2.0, 3.0) << std::endl;
    std::cout << "Sum of 2, 3, 4, 5 is " << sum(4, 2.0, 3.0, 4.0, 5.0) << std::endl;
}
```

## `getopt_long`

```cpp
#include <getopt.h>
#include <iostream>

using namespace std;

int main(int argc, char* argv[]) {
    /**
     * struct option
     * {
     *      const char * name;
     *      int          has_arg;
     *      int        * flag;
     *      int          val;
     * }
     */
    static struct option long_options[] = {
        {"reqarg", required_argument, NULL, 'r'},
        {"optarg", optional_argument, NULL, 'o'},
        {"noarg", no_argument, NULL, 'n'},
        {NULL, 0, NULL, 0},
    };

    while (1) {
        int option_index = 0, opt;

        /**
         * getopt_long 会遍历 argv 数组，在每次迭代中，它会返回下一个选项字符（如果有），
         * 然后，这个字符与长选项列表进行比较，如果匹配，则对应的操作会被执行，
         * 如果没有匹配，那么函数将返回 -1。
         * 只有一个字符，不带冒号，只表示选项，如 -c
         * 一个字符，后接一个冒号，表示选项后面带一个参数，如 -a 100
         * 一个字符，后接两个冒号——表示选项后面带一个可选参数，
         * 即参数可有可无，如果带参数，则选项与参数直接不能有空格，如 -b200
         */
        opt = getopt_long(argc, argv, "a::b:c:d", long_options, &option_index);

        if (opt == -1) // 选项遍历完毕，退出循环
            break;

        printf("opt = %c\t\t", opt);
        printf("optarg = %s\t\t", optarg);
        printf("optind = %d\t\t", optind);
        printf("argv[%d] = %s\t\t", optind, argv[optind]);
        printf("option_index = %d\n", option_index);
    }

    return 0;
}
```

这段代码是一个使用 `getopt_long` 函数进行命令行参数解析的例子，它演示了如何处理短选项（使用单个字符）和长选项（使用字符串）。

首先，代码定义了一个静态的 `struct option` 数组 `long_options`，用于描述长选项的信息。每个数组元素都是一个结构体，包含以下字段：

- `name`：选项的名称，字符串类型。
- `has_arg`：指定选项是否需要参数，有三个可能值：`no_argument`（0）表示不需要参数，`required_argument`（1）表示必须有参数，`optional_argument`（2）表示参数是可选的。
- `flag`：如果不为 `NULL`，则指向一个整数变量，用于存储选项的值（即 `val` 字段），而不是返回选项字符。如果为 `NULL`，则 `getopt_long` 函数将返回选项字符。
- `val`：选项的值，通常是一个字符。

在 `main` 函数中，使用一个 `while` 循环来遍历命令行参数。在循环中，调用 `getopt_long` 函数来获取下一个选项。`getopt_long` 的参数包括：

- `argc` 和 `argv`：分别是命令行参数的数量和数组。
- `"a::b:c:d"`：短选项的字符串表示，冒号表示需要参数的选项。
- `long_options`：长选项的数组。
- `option_index`：用于存储当前长选项在 `long_options` 数组中的索引。

在每次循环迭代中，打印出当前选项的相关信息，包括选项字符、选项参数、`optind` 的值、对应的参数值等。

```bash
g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out --reqarg 100 --optarg=200 --noarg
g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out –reqarg=100 --optarg=200 --noarg
g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out --reqarg 100 --optarg --noarg
```

这条指令表示使用 C++20 标准，进行优化，启用所有警告，使用多线程，编译 `main.cpp` 文件，然后运行生成的可执行文件 `a.out` 并传递一些命令行参数。

在不同的命令行调用中，通过使用 `--reqarg`、`--optarg`、`--noarg` 等选项来测试程序的输出。程序会解析这些选项，并打印相关的信息。

## `<typename... Args>`

在 C++ 中，你可以使用递归或者使用 C++17 引入的折叠表达式（fold expression）来访问可变参数列表中的每个参数。

::::{tab-set}
:::{tab-item} 递归方式（C++11 及以上）

```cpp
#include <iostream>

// 递归终止条件
void printArgs() {
    std::cout << std::endl;
}

// 递归步骤
template <typename T, typename... Args>
void printArgs(T first, Args... args) {
    std::cout << first << " ";
    printArgs(args...); // 递归调用
}

int main() {
    printArgs(1, "Hello", 3.14, 'A');
    return 0;
}
```

在这个例子中，`printArgs` 函数通过递归的方式遍历可变参数列表，打印每个参数的值。递归终止条件是一个没有参数的版本。
:::

:::{tab-item} 使用折叠表达式（C++17 及以上）

```cpp
#include <iostream>

template <typename... Args>
void printArgs(Args... args) {
    (std::cout << ... << args) << std::endl; // 折叠表达式
}

int main() {
    printArgs(1, "Hello", 3.14, 'A');
    return 0;
}
```

在这个例子中，使用了 C++17 引入的折叠表达式。`(std::cout << ... << args)` 表示将所有参数展开成一个表达式，然后通过 `<<` 运算符连接起来，最后加上 `std::endl` 进行换行。
:::
::::

这两种方法都允许你访问可变参数列表中的每个参数，具体选择取决于你的编译环境和代码的需求。折叠表达式提供了一种更简洁和直观的语法，但需要 C++17 及以上的编译器支持。

````{admonition} 包展开（args...）和模式（args）

*例 1：字面量作为实参*

```cpp
template <typename... Us>
void f(Us... pargs) {}

template <typename... Ts>
void g(Ts... args) {
    // &args... 是包展开
    // &args    是它的模式
    f(&args...);
}

int main() {
    // Ts... args   会展开成 int E1, double E2, const char* E3
    // &args...     会展开成 &E1, &E2, &E3
    // Us...        会展开成 int* E1, double* E2, const char** E3
    g(1, 0.2, "a");
}
```

*例 2：数组作为实参*

```cpp
// 接受任意数量的模板参数（用 Ts... 表示）
template <typename... Ts>
void f(Ts...) {}

// 接受一个模板参数包 Ts 和一个非类型参数包 N
// Ts (&...arr)[N] 表示 arr 是一个引用数组，数组元素的类型是 Ts
// 数组的大小是 N
template <typename... Ts, int... N>
void g(Ts (&... arr)[N]) {}

int main() {
    // Ts... 会展开成 void f(char, int)
    f('a', 1);

    // Ts... 会展开成 void f(double)
    f(0.1);

    // Ts (&...arr)[N] 会展开成 const char (&)[2], int (&)[1]
    // 模板参数 Ts 被展开为 const char
    // 非类型参数 N 被展开为数组大小，即 2 和 1
    int n[1];
    g<const char, int>("a", n);
}
```

*例 3：调整可变参数的位置*

```cpp
template <typename A, typename B, typename... C>
void func(A arg1, B arg2, C... arg3) {
    container<A, B, C...> t1; // 展开成 container<A, B, E1, E2, E3>
    container<C..., A, B> t2; // 展开成 container<E1, E2, E3, A, B>
    container<A, C..., B> t3; // 展开成 container<A, E1, E2, E3, B>
}
```
````
