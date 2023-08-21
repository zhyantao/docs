# Lambda

在 C++ 11 和更高版本中，Lambda 表达式（通常称为 Lambda）是一种在 **被调用的位置** 或 **作为参数传递给函数的位置** 定义匿名函数对象（闭包）的简便方法。

Lambda 通常用于封装传递给算法或异步函数的 **少量代码行**。 

```cpp
#include <algorithm>
#include <cmath>

void abssort(float* x, unsigned n) {
    std::sort(x, x + n,
        // Lambda expression begins
        [](float a, float b) {
            return (std::abs(a) < std::abs(b));
        } // end of lambda expression
    );
}
```

下图显示了 lambda 语法的各个部分：

```{figure} ../_static/images/lambdaexpsyntax.png
:caption: Lambda 语法解析
```

1. capture 子句（在 C++ 规范中也称为 Lambda 引导。）
2. 参数列表（可选）。 （也称为 Lambda 声明符）
3. mutable 规范（可选）。
4. exception-specification（可选）。
5. trailing-return-type（可选）。
6. Lambda 体。

更多细节参考：<https://learn.microsoft.com/zh-cn/cpp/cpp/lambda-expressions-in-cpp>
