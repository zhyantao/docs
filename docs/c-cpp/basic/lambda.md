# Lambda

在 C++ 11 和更高版本中，Lambda 表达式（通常称为 Lambda）是一种在 **被调用的位置** 或 **作为参数传递给函数的位置** 定义匿名函数对象（闭包）的简便方法。Lambda 通常用于封装传递给算法或异步函数的少量代码行。 

```cpp
#include <algorithm>
#include <cmath>

void abssort(float *x, unsigned n)
{
    std::sort(x, x + n,
              // Lambda expression begins
              [](float a, float b)
              {
                  return (std::abs(a) < std::abs(b));
              } // end of lambda expression
    );
}
```

下图显示了 lambda 语法的各个部分：

```{figure} ../../_static/images/lambdaexpsyntax.png
Lambda 语法解析
```

1. capture 子句（在 C++ 规范中也称为 Lambda 引导。）
2. 参数列表（可选）。 （也称为 Lambda 声明符）
3. mutable 规范（可选）。
4. exception-specification（可选）。
5. trailing-return-type（可选）。
6. Lambda 体。

在使用 capture 子句时，建议你记住以下几点（尤其是使用采取多线程的 Lambda 时）：

- 引用捕获可用于修改外部变量，而值捕获却不能实现此操作。（mutable 允许修改副本，而不能修改原始项）
- 引用捕获会反映外部变量的更新，而值捕获不会。
- 引用捕获引入生存期依赖项，而值捕获却没有生存期依赖项。当 Lambda 以异步方式运行时，这一点尤其重要。如果在异步 Lambda 中通过引用捕获局部变量，该局部变量将很容易在 Lambda 运行时消失。代码可能会导致在运行时发生访问冲突。

更多细节参考：<https://learn.microsoft.com/zh-cn/cpp/cpp/lambda-expressions-in-cpp>

## Lambda 引用捕获

这段代码使用了 C++11 引入的变参模板（Variadic Templates）和 Lambda 表达式的特性。

```cpp
#include <iostream>

// 示例函数 g，你需要根据你的需求实现这个函数
template <typename... Args>
void g(Args... args)
{
    // 实现 g 函数的逻辑
    std::cout << "g called with arguments: ";
    ((std::cout << args << " "), ...); // 折叠表达式，输出参数
    std::cout << std::endl;
}

// 函数模板 f
template <class... Args>
void f(Args... args)
{
    auto lm = [&, args...] { // Lambda 表达式捕获 args
        g(args...);          // 调用函数 g
    };

    lm(); // 调用 Lambda 表达式
}

int main()
{
    // 调用 f 函数
    f(1, 2, "Hello", 3.14);

    return 0;
}
```

这段代码定义了两个函数模板：

1. `g` 函数：这是一个示例函数，用于演示如何使用折叠表达式输出可变参数列表中的参数。

2. `f` 函数：这个函数使用 Lambda 表达式，并捕获了可变参数 `args`，然后调用了 `g` 函数。Lambda 表达式被赋值给 `lm` 变量，并通过 `lm()` 调用。在 Lambda 表达式中使用了 `args...` 来展开可变参数列表。

在 `main` 函数中，调用了 `f` 函数，传递了一些参数。这些参数被捕获并传递给 `g` 函数，然后 `g` 函数使用折叠表达式输出了这些参数。

请注意，你需要根据你的具体需求实现 `g` 函数的逻辑，这里的示例只是输出参数值。