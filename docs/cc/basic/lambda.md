# Lambda

在 C++11 及之后的版本里，Lambda 表达式提供了一种便捷方式，让我们能够直接在需要调用函数的地方，或是将函数作为参数传递给其他函数时，定义一个没有名字的小型匿名函数。这种匿名函数，我们也叫它闭包，非常适合于用来封装那些打算用于算法或异步处理的简短代码片段。

下面是一个例子，展示了如何利用 Lambda 表达式来定制排序规则，依据元素的绝对值大小进行排序：

```cpp
#include <algorithm>
#include <cmath>

void sort_by_absolute_value(float* elements, size_t count) {
    std::sort(elements, elements + count,
              // 从这里开始是 Lambda 表达式
              [](float a, float b) -> bool { return std::abs(a) < std::abs(b); } // Lambda 表达式到此结束
    );
}
```

Lambda 表达式的结构可以分解为几个部分：

```{figure} ../../_static/images/lambdaexpsyntax.png
Lambda 语法解析
```

1. **捕获列表**（Capture List）：决定 Lambda 内部能否访问外边的变量，以及如何访问（比如是拷贝还是引用）。
2. **参数列表**：就像常规函数那样，列出 Lambda 接受的参数。
3. **`mutable` 关键字**（可选）：如果使用，允许 Lambda 修改通过值捕获的变量副本。
4. **异常规范**（可选）：指定 Lambda 抛出异常的规则。
5. **返回类型**（可选）：明确指出 Lambda 的返回类型，如果不写，编译器会自动推断。
6. **函数体**：Lambda 执行的实际代码。

当你在 Lambda 中通过引用捕获外部变量时，要注意几点：

- 引用捕获能直接修改外部变量，而值捕获则创建变量的副本，不能直接修改原变量。
- 外部变量的任何变化，引用捕获的 Lambda 都能看到，但值捕获的 Lambda 看到的是捕获时的变量副本，后续变化不影响它。
- 使用引用捕获可能会引发生命周期问题，尤其是在异步操作中，确保被引用的变量在 Lambda 执行期间依然有效。

接下来的代码示例，演示了如何在 Lambda 中利用变参模板（Variadic Templates）捕获任意数量的参数，并将它们传递给另一个函数：

```cpp
#include <iostream>

// 假设这是你实现的一个处理多种类型参数的函数
template <typename... Args> void processArguments(Args... args) {
    std::cout << "Processing arguments: ";
    (std::cout << ... << args) << std::endl; // 使用折叠表达式输出所有参数
}

// 使用 Lambda 表达式包装对 processArguments 的调用
template <typename... Args> void wrapperFunction(Args... args) {
    auto lambda = [&](/* 通过引用捕获外部变量 args */) {
        processArguments(args...); // 通过展开运算符传递参数
    };

    lambda(); // 执行Lambda
}

int main() {
    wrapperFunction(1, 2, "Example", 3.14);
    return 0;
}
```

在这个例子中，`wrapperFunction` 创建了一个 Lambda 表达式，该表达式通过引用捕获了所有传入的参数，并将它们转发给 `processArguments` 函数。这展示了 Lambda 表达式与变参模板结合使用的灵活性。
