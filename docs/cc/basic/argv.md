# argv

## 指定形参默认值

在 C++ 中，你可以为函数的形参指定默认值。这样，当你调用该函数时，如果没有提供对应的实参或者提供了少于形参的数量，则会使用这些默认值。默认值应该从右到左依次指定，因为你可以在一个参数列表中同时指定多个默认值。

这里是一个简单的示例，展示了如何使用默认参数：

```cpp
#include <iostream>

// 函数声明
void printInfo(std::string name, int age = 30, std::string city = "Unknown");

int main() {
    // 调用函数，只提供第一个参数
    printInfo("Alice");

    // 调用函数，提供前两个参数
    printInfo("Bob", 25);

    // 调用函数，提供所有参数
    printInfo("Charlie", 40, "New York");

    return 0;
}

// 函数定义
void printInfo(std::string name, int age, std::string city) {
    std::cout << "Name: " << name << ", Age: " << age << ", City: " << city << std::endl;
}
```

在这个例子中，`printInfo` 函数有三个形参：`name`, `age`, 和 `city`。我们分别为 `age` 和 `city` 指定了默认值。当我们调用 `printInfo` 函数时，可以只提供 `name` 参数，或者提供 `name` 和 `age` 参数，或者提供全部参数。

注意以下几点：

1. 默认参数必须按照从右向左的顺序进行定义。也就是说，在给定默认值之后，所有的参数都必须有默认值。
2. 默认参数可以是任何合法的表达式，包括常量、其他参数等。
3. 如果你希望在参数列表中为中间的一个参数指定默认值，那么在其右边的所有参数也必须有默认值。

## 指针/引用作为参数

在 C++ 中，函数参数可以使用指针或引用传递。这两种方式都允许函数修改传入的值。下面分别介绍指针和引用作为函数参数的区别。

### 指针作为函数参数

当使用指针作为函数参数时，你可以修改指针指向的数据，但不会改变原始变量的地址。如果函数内部重新分配了指针，那么原始变量的指针将不再指向新分配的内存。

```cpp
#include <iostream>

void swapPtr(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 10;
    int y = 20;

    std::cout << "Before swap: x = " << x << ", y = " << y << std::endl;
    swapPtr(&x, &y);
    std::cout << "After swap: x = " << x << ", y = " << y << std::endl;

    return 0;
}
```

### 引用作为函数参数

当使用引用作为函数参数时，实际上是创建了一个别名来直接访问原始变量。这意味着你可以在函数内部修改原始数据。但是，如果函数尝试重新绑定引用（例如通过 `a = b;`），则会导致编译错误。

```cpp
#include <iostream>

void swapRef(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 10;
    int y = 20;

    std::cout << "Before swap: x = " << x << ", y = " << y << std::endl;
    swapRef(x, y);
    std::cout << "After swap: x = " << x << ", y = " << y << std::endl;

    return 0;
}
```

### 比较

- **性能**：传递引用通常比传递指针更高效，因为不需要额外的间接寻址。
- **安全性**：使用引用可以避免空指针问题，因为引用必须初始化并且不能是 `null`。
- **可读性**：引用通常被认为更容易理解，因为它们更接近自然语言中的概念（如“别名”）。

### 注意事项

- 如果函数需要修改传入的值，使用引用通常更好。
- 如果需要传递较大的对象，比如类实例，使用引用（尤其是常量引用）可以避免复制开销。
- 指针可以用于处理空值，而引用不可以。

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

## `va_list` 和 `va_arg`

```cpp
#include <cstdarg>
#include <iostream>

void log(char* fmt, ...) {
    char buf[512] = {0};
    va_list ap;

    va_start(ap, fmt);
    (void)vsnprintf(buf, sizeof(buf) - 2, fmt, ap);
    va_end(ap);

    printf("%s\n", buf);
}

int main() {
    log((char*)"%s, %d, %s", "hello", 100, "world");
}
```

```cpp
#include <cstdarg>
#include <iostream>

double sum(int num, ...) {
    va_list valist; // 创建参数列表
    double ret = 0.0;

    va_start(valist, num); // 初始化参数列表

    for (int i = 0; i < num; i++) {
        ret += va_arg(valist, double); // 访问参数列表中的项
    }

    va_end(valist); // 清理参数列表占用的内存

    return ret;
}

int main() {
    std::cout << "Sum of 2, 3 is " << sum(2, 2.0, 3.0) << std::endl;
    std::cout << "Sum of 2, 3, 4, 5 is " << sum(4, 2.0, 3.0, 4.0, 5.0) << std::endl;
}
```

- `sum` 函数接受一个整数参数 `num`，表示后面可变参数的数量。
- `va_list` 是用于存储可变参数的类型，它是一个指向参数列表的对象。
- `va_start` 宏用于初始化 `valist`，将其指向参数列表的起始位置。
- 使用 `va_arg` 宏可以依次访问参数列表中的项，本例中假设参数都是 `double` 类型。
- `va_end` 宏用于清理参数列表占用的内存。

在 `main` 函数中分别调用了 `sum` 函数两次，每次传递不同数量的参数。这展示了可变参数函数的灵活性。

当程序运行时，`sum` 函数通过可变参数的方式计算传递给它的数字的总和，然后 `printf` 语句输出这个总和。在第一个调用中，传递了两个参数（2 和 3），在第二个调用中，传递了四个参数（2、3、4、5）。

使用 C 风格的可变参数函数，需要在运行时做类型转换，可能存在类型安全的隐患。

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
