# sizeof

```cpp
#include <iostream>

using namespace std;

int main() {
    int i = 0;
    short s = 0;
    cout << "sizeof(int)=" << sizeof(int) << endl;
    cout << "sizeof(i)=" << sizeof(i) << endl;
    cout << "sizeof(short)=" << sizeof(s) << endl;
    cout << "sizeof(long)=" << sizeof(long) << endl;
    cout << "sizeof(size_t)=" << sizeof(size_t) << endl;
    return 0;
}
```

## sizeof...

`sizeof...` 是 C++11 引入的一种运算符，用于计算模板参数包中的元素数量。

```cpp
#include <iostream>

// 定义模板结构体 count
template <class... Types>
struct count {
    static const std::size_t value = sizeof...(Types);
};

int main() {
    // 使用 count 结构体计算不同类型的数量
    std::cout << "Number of types: " << count<int, double, char>::value << std::endl;

    return 0;
}
```

- `count` 是一个模板结构体，它接受任意数量的类型参数 (`Types...`)。
- 语句使用 `sizeof...` 操作符来计算模板参数包中类型的数量，并将结果保存在 `value` 成员中。

在 `main` 函数中，我们使用了 `count` 结构体来计算不同类型的数量。在这个例子中，我们传递了 `int`、`double` 和 `char` 三个类型，然后输出了它们的数量。
