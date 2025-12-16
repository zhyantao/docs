# mutable

在编程中，**`mutable`** 是一个关键字，主要用于 **C++** 语言中，它的核心含义是 **“可变的”**。它有两个主要的使用场景：

## 1. 突破 `const` 成员函数的限制（最主要用途）

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
            cacheValid = true;
        }
        return cachedData;
    }
};
```

## 2. 在 Lambda 表达式中（C++11 起）

在 Lambda 表达式中，`mutable` 用于允许按值捕获的变量在 Lambda 函数体内被修改。

- **默认情况**：Lambda 表达式按值捕获（`[=]` 或显式指定变量名）的变量在函数体内是**只读的**，因为编译器生成的函数调用运算符（`operator()`）默认是 `const` 的。
- **使用 `mutable`**：在 Lambda 后加上 `mutable` 关键字，会移除其 `operator()` 的 `const` 属性，从而允许修改按值捕获的变量（注意：修改的只是副本，不影响外部原变量）。

**示例：**

```cpp
int main() {
    int x = 0;

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

## 其他语言

虽然 `mutable` 是 C++ 的关键字，但其概念在其他语言中以不同形式存在：

- **Rust**：有 `mut` 关键字，用于声明变量或引用是可变的，这是其所有权系统的核心。

  ```rust
  let mut x = 5; // 可变变量
  x = 10; // 允许
  ```

- **C#**：有 `mutable` 关键字，主要用于在 `struct`（结构体）的 `getter`（属性访问器）中修改字段，但使用场景相对较少。
- **Java / Python**：没有直接的 `mutable` 关键字。对象成员的可变性通常由设计决定（如使用 `final` 修饰符或属性设置器）。

## 总结

在 **C++** 中，`mutable` 主要是一个**例外说明符**，它：

1. **（主要用途）** 为 `const` 成员函数“开一个后门”，允许修改那些**不属于对象核心逻辑状态**的内部管理性成员变量。
2. **（Lambda 中）** 允许修改 Lambda 表达式内部按值捕获的变量的**副本**。

它的存在体现了 C++ 的设计哲学：在提供严格约束（如 `const` 正确性）的同时，也提供必要的灵活性以满足底层或性能优化需求。使用时需谨慎，避免滥用而破坏 `const` 承诺带来的语义安全。
