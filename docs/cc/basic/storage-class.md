# 存储类别与限定符

## extern

C++ 中的 `extern` 关键字用于说明一个变量或者函数是在其他地方定义的，而不是在当前文件中定义。它的作用是告诉编译器，某个变量或函数的定义在其他源文件中，并且在链接时会找到它的实际定义。

对于变量而言，`extern` 声明告诉编译器，该变量在其他地方定义，不要为它分配存储空间。在链接阶段，编译器会在其他文件中找到该变量的定义，确保所有文件中对该变量的引用都指向同一地址。

对于函数而言，`extern` 用于声明函数的原型，表示该函数的定义在其他地方。这样在编译时，编译器就知道函数的接口，而在链接时会找到实际的函数定义。

```cpp
// 在文件 A.cpp 中定义变量
int globalVar = 42;
```

```cpp
// 在文件 B.cpp 中使用 extern 声明该变量
extern int globalVar;

// 在文件C.cpp中使用该变量
#include <iostream>
int main() {
    std::cout << globalVar << std::endl;
    return 0;
}
```

在这个例子中，文件 `B.cpp` 使用 `extern` 声明了在文件 `A.cpp` 中定义的 `globalVar` 变量，确保在链接时能够正确找到它。

## static

在 C++ 中，关键字 `static` 具有多个用途。

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

2、**全局静态变量（Global Static Variables）：** 在全局范围内使用 `static` 关键字声明的变量具有内部链接（internal linkage），只能在当前源文件中访问，它们对其他源文件是不可见的。

```cpp
// File1.cpp
static int globalStaticVariable = 42;
```

```cpp
// File2.cpp
#include <iostream>

// 错误示例：static 全局变量具有内部链接，其他源文件无法通过 extern 访问，
// 下面的声明会导致链接错误（undefined reference）
// extern int globalStaticVariable;

int main() {
    // std::cout << globalStaticVariable << std::endl; // 无法访问
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

## const

`const` 是一种常见的类型保护机制，用法主要分为以下三类：

```cpp
const int& func(int& a);   // 修饰返回值
int& func(const int& a);   // 修饰变量
int& func(int& a) const {} // 修饰成员函数
```

- `const` 修饰返回值时，肯定修饰的是引用，表示返回值不可被修改。
- `const` 修饰参数时，通常也是引用，表示在函数内部我们不希望改变实参的值。
- `const` 修饰成员函数，表示在成员函数实现中，不可修改成员变量。

```{code-block} cpp
:emphasize-lines: 9, 20, 24, 39, 49

#include <iostream>
#include <cstring>

using namespace std;

class Student
{
private:
    const int BMI = 24;
    char *name;
    int born;
    bool male;

public:
    Student()
    {
        name = new char[1024]{0};
        born = 0;
        male = false;
        // BMI = 25; // error: const 成员只能在初始化列表初始化，不能在构造体内赋值
        cout << "Constructor: Person()" << endl;
    }

    Student(const char *name, int born, bool male)
    {
        this->name = new char[1024];
        setName(name);
        this->born = born;
        this->male = male;
        cout << "Constructor: Person(const char, int , bool)" << endl;
    }

    ~Student()
    {
        cout << "To destroy object: " << name << endl;
        delete[] name;
    }

    void setName(const char *name)
    {
        strncpy(this->name, name, 1024);
    }

    void setBorn(int born)
    {
        this->born = born;
    }

    int getBorn() const
    {
        // born++; // error: const 成员函数不能修改成员变量
        return born;
    }

    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};

void Student::setGender(bool isMale)
{
    male = isMale;
}

void Student::printInfo()
{
    std::cout << "Name: " << name << std::endl;
    std::cout << "Born in " << born << std::endl;
    std::cout << "Gender: " << (male ? "Male" : "Female") << std::endl;
}

int main()
{
    Student yu("Yu", 2000, true);
    cout << "yu.getBorn() = " << yu.getBorn() << endl;
    return 0;
}
```

## mutable

在编程中，**`mutable`** 是一个关键字，主要用于 **C++** 语言中，它的核心含义是 **“可变的”**。它有两个主要的使用场景：

### 1. 突破 `const` 成员函数的限制（最主要用途）

这是 `mutable` 最常见和核心的用途。它用于修饰类的**成员变量**。

- **背景**：在 C++ 中，被声明为 `const` 的成员函数，承诺不会修改该函数的**所属对象**的任何成员变量（即对象状态）。
- **矛盾**：但有时，我们有一个从逻辑上讲是“常量”的函数，却需要修改一些**与对象核心逻辑状态无关**的、用于“内部管理”的变量。例如：
  - 缓存（Memoization）计算结果
  - 访问计数
  - 调试日志
  - 互斥锁（mutex）的状态
- **解决**：将这些内部管理用的变量声明为 `mutable`，那么即使在 `const` 成员函数中，也可以合法地修改它们。

**示例：**

```cpp
class DatabaseCache {
private:
    // 核心数据（逻辑状态）
    std::string cachedData;
    // 内部管理用的变量，声明为 mutable
    mutable bool cacheValid{false};
    mutable std::chrono::system_clock::time_point lastFetchTime;

public:
    // 一个 const 成员函数，承诺不会改变对象的“逻辑状态”
    std::string getData() const {
        if (!cacheValid) {
            // 错误！不能在 const 函数中修改普通成员变量
            // cachedData = fetchFromDatabase();

            // 但是可以修改 mutable 成员
            lastFetchTime = std::chrono::system_clock::now();
            // 假设这里有一个线程安全的方式更新 cachedData
            cacheValid    = true;
        }
        return cachedData;
    }
};
```

### 2. 在 Lambda 表达式中（C++11 起）

在 Lambda 表达式中，`mutable` 用于允许按值捕获的变量在 Lambda 函数体内被修改。

- **默认情况**：Lambda 表达式按值捕获（`[=]` 或显式指定变量名）的变量在函数体内是**只读的**，因为编译器生成的函数调用运算符（`operator()`）默认是 `const` 的。
- **使用 `mutable`**：在 Lambda 后加上 `mutable` 关键字，会移除其 `operator()` 的 `const` 属性，从而允许修改按值捕获的变量（注意：修改的只是副本，不影响外部原变量）。

**示例：**

```cpp
int main() {
    int x        = 0;

    auto lambda1 = [x]() {
        // x = 5; // 错误！不能修改按值捕获的变量
        return x;
    };

    auto lambda2 = [x]() mutable {
        x = 5; // 正确！因为使用了 mutable，可以修改内部副本
        std::cout << "内部 x: " << x << std::endl; // 输出 5
        return x;
    };

    lambda2();
    std::cout << "外部 x: " << x << std::endl; // 输出 0，因为修改的是副本
}
```

### 其他语言

虽然 `mutable` 是 C++ 的关键字，但其概念在其他语言中以不同形式存在：

- **Rust**：有 `mut` 关键字，用于声明变量或引用是可变的，这是其所有权系统的核心。

  ```rust
  let mut x = 5; // 可变变量
  x = 10; // 允许
  ```

- **C#**：有 `mutable` 关键字，主要用于在 `struct`（结构体）的 `getter`（属性访问器）中修改字段，但使用场景相对较少。
- **Java / Python**：没有直接的 `mutable` 关键字。对象成员的可变性通常由设计决定（如使用 `final` 修饰符或属性设置器）。

### 总结

在 **C++** 中，`mutable` 主要是一个**例外说明符**，它：

1. **（主要用途）** 为 `const` 成员函数“开一个后门”，允许修改那些**不属于对象核心逻辑状态**的内部管理性成员变量。
2. **（Lambda 中）** 允许修改 Lambda 表达式内部按值捕获的变量的**副本**。

它的存在体现了 C++ 的设计哲学：在提供严格约束（如 `const` 正确性）的同时，也提供必要的灵活性以满足底层或性能优化需求。使用时需谨慎，避免滥用而破坏 `const` 承诺带来的语义安全。

## define

### 函数式宏

`#define` 支持定义形如函数的宏，例如：

```cpp
#define MAX(a, b) ((a) > (b) ? (a) : (b))
```

宏只是预处理阶段的**文本替换**，它完全合法，不会导致编译错误。但正因为是纯文本替换，
函数式宏存在两个经典问题：

1. **参数副作用**：`MAX(x++, y++)` 展开后 `x++`、`y++` 会被执行多次；
2. **运算符优先级**：如果参数本身是表达式（如 `MAX(a & 0xFF, b & 0xFF)`），
   不加括号的宏（如 `#define MAX(a, b) a > b ? a : b`）会因优先级产生错误结果，
   因此每个参数和整体都要加括号。

由于宏没有类型检查和参数求值顺序保证，现代 C++ 更推荐使用内联函数或模板代替函数式宏（见下文“inline 关键字”一节）。

### do { ... } while (0) 惯用法

当宏需要包含多条语句时，直接使用大括号会带来问题：`if (cond) MACRO();` 展开成
`if (cond) { ... };` 后，多出来的分号会把 `else` 断开。`do { ... } while (0)` 惯用法
可以让多条语句的宏表现得像一条语句：

```cpp
#define LOG(msg)                                     \
    do {                                             \
        printf("[%s:%d] ", __FILE__, __LINE__);      \
        printf("%s\n", msg);                         \
    } while (0)

if (error)
    LOG("failed");
else
    LOG("ok"); // 展开后语法正确
```

注意：`do { ... } while (0)` 包装的宏不是表达式，不能出现在赋值等需要值的上下文中；
也不能在其中使用 `return`，因为 `return` 会直接返回外层函数。

## inline 关键字

```cpp
#include <iostream>

using namespace std;

inline float max_function(float a, float b) {
    if (a > b)
        return a;
    else
        return b;
}

// #define MAX_MACRO(a, b) a > b ? a : b

#define MAX_MACRO(a, b) (a) > (b) ? (a) : (b)

int main() {
    int num1 = 20;
    int num2 = 30;
    int maxv = max_function(num1, num2);
    cout << maxv << endl;

    maxv = MAX_MACRO(num1, num2);
    cout << maxv << endl;

    maxv = MAX_MACRO(num1++, num2++);
    cout << maxv << endl;
    cout << "num1=" << num1 << endl;
    cout << "num2=" << num2 << endl;

    num1 = 0xAB09;
    num2 = 0xEF08;
    maxv = MAX_MACRO(num1 & 0xFF, num2 & 0xFF);
    cout << maxv << endl;

    return 0;
}
```

上面的例子中，`MAX_MACRO(num1++, num2++)` 展开后自增运算符被执行了多次，产生了副作用；
`MAX_MACRO(num1 & 0xFF, num2 & 0xFF)` 则演示了不加括号的宏在表达式参数上的优先级问题。
而 `inline` 函数在编译期做类型检查，参数只求值一次，因此更安全。
