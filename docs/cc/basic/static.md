# static

在 C++ 中，关键字 `static` 具有多个用途，其中之一就是定义变量的作用域。

1、**局部静态变量（Local Static Variables）：** 在函数内部使用 `static` 关键字声明的变量被称为局部静态变量。这些变量只在函数首次调用时初始化，而不是每次函数被调用时都重新初始化。它们在整个程序运行期间保持其值，并且具有函数作用域，即只能在声明它们的函数内部访问。

```cpp
#include <iostream>

void exampleFunction() {
    static int staticVariable = 0;
    staticVariable++;
    std::cout << "Static Variable: " << staticVariable << std::endl;
}

int main() {
    exampleFunction();
    exampleFunction();
    return 0;
}
```

2、**全局静态变量（Global Static Variables）：** 在全局范围内使用 `static` 关键字声明的变量具有文件作用域，只能在当前源文件中访问。它们对其他源文件是不可见的。

```cpp
// File1.cpp
static int globalStaticVariable = 42;
```

```cpp
// File2.cpp
#include <iostream>

extern int globalStaticVariable; // 声明在其他源文件中定义的全局静态变量

int main() {
    std::cout << "Global Static Variable: " << globalStaticVariable << std::endl;
    return 0;
}
```

3、在类中使用 `static` 可以创建静态成员变量和静态成员函数。静态成员变量是类的所有实例共享的，而静态成员函数不属于任何实例，可以直接通过类名调用。

```cpp
class Example {
public:
    static int staticVariable;    // 静态成员变量
    static void staticFunction(); // 静态成员函数
};

// 静态成员变量的定义
int Example::staticVariable = 0;

// 静态成员函数的实现
void Example::staticFunction() {
    // 实现代码
}
```
