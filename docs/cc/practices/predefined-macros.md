# C++ 预定义宏完全指南：从基础到高级应用

## 引言

在 C++ 开发中，预定义宏是一组由编译器提供的特殊标识符，它们包含了编译环境、代码位置和语言标准等重要信息。这些宏在调试、日志记录、条件编译等场景中发挥着关键作用。本文将深入解析 C++ 中的预定义宏，帮助开发者更好地理解和利用它们。

## 核心预定义宏详解

### 1. 语言版本标识

```cpp
// 检查 C++ 标准版本
#if __cplusplus >= 202002L
// C++20 或更高版本的代码
#elif __cplusplus >= 201703L
// C++17 的代码
#endif
```

**版本对应关系：**

- C++98/03: `199711L`
- C++11: `201103L`
- C++14: `201402L`
- C++17: `201703L`
- C++20: `202002L`
- C++23: `202302L`

### 2. 文件与行号信息

```cpp
// 用于调试和日志记录
void logError(const char* message) {
    std::cerr << "[" << __FILE__ << ":" << __LINE__ << "] " << message << std::endl;
}

// 自定义错误宏
#define ASSERT(condition)                                                          \
    if (!(condition)) {                                                            \
        std::cerr << "Assertion failed at " << __FILE__ << ":" << __LINE__ << " (" \
                  << #condition << ")" << std::endl;                               \
        std::terminate();                                                          \
    }
```

### 3. 编译时间戳

```cpp
// 显示编译信息
void showBuildInfo() {
    std::cout << "Build date: " << __DATE__ << std::endl;
    std::cout << "Build time: " << __TIME__ << std::endl;
}
```

### 4. 环境检测

```cpp
// 检测运行环境
#if __STDC_HOSTED__
// 在有操作系统的环境下运行
#include <iostream>
#else
// 独立环境（如嵌入式系统）
// 使用自定义 IO 函数
#endif
```

## C++17/23 新增宏

### 内存对齐

```cpp
// C++17: 默认 new 操作符的对齐保证
constexpr size_t default_alignment = __STDCPP_DEFAULT_NEW_ALIGNMENT__;

// 检查是否需要特殊对齐
template <typename T>
void* allocate() {
    if (alignof(T) > __STDCPP_DEFAULT_NEW_ALIGNMENT__) {
        return ::operator new(sizeof(T), std::align_val_t{alignof(T)});
    }
    return ::operator new(sizeof(T));
}
```

### 扩展浮点类型支持

```cpp
// C++23: 检查浮点类型支持
#ifdef __STDCPP_FLOAT16_T__
using float16_t = _Float16;
#endif

#ifdef __STDCPP_BFLOAT16_T__
using bfloat16_t = __bf16;
#endif
```

## 实现定义宏

### 线程支持检测

```cpp
#if __STDCPP_THREADS__
// 支持多线程编程
#include <thread>
#include <mutex>
#endif
```

### 字符编码信息

```cpp
// 检查 wchar_t 是否使用 Unicode
#ifdef __STDCPP_ISO_10646__
// wchar_t 基于 Unicode
static_assert(sizeof(wchar_t) >= 2, "wchar_t too small for Unicode");
#endif

// 检查基本字符集一致性
#if __STDCPP_MB_MIGHT_NEQ_WC__
// 在 EBCDIC 系统上需要特殊处理
char narrow = 'A';
wchar_t wide = L'A';
// narrow == wide 可能为 false
#endif
```

## 重要注意事项

### 1. 宏的不可变性

```cpp
// 错误示例 - 会导致未定义行为
#define __LINE__ 100 // 错误！
#undef __cplusplus   // 错误！

// 正确用法：只读取，不修改
int currentLine = __LINE__;
```

### 2. 与 \_\_func\_\_ 的区别

```cpp
// __func__ 是函数局部变量，不是宏
void exampleFunction() {
    // 用于调试信息
    std::cout << "Function: " << __func__ << " in " << __FILE__ << " at line " << __LINE__
              << std::endl;
}
```

## 实用技巧和最佳实践

### 1. 版本兼容性处理

```cpp
// 安全的版本检查方式
#ifndef __cplusplus
#error "This is a C++ compiler only"
#endif

// 渐进增强的代码组织
#if __cplusplus >= 201703L
#define NODISCARD [[nodiscard]]
#else
#define NODISCARD
#endif

NODISCARD int computeValue();
```

### 2. 调试辅助宏

```cpp
// 条件调试输出
#ifdef DEBUG
#define DEBUG_LOG(msg) std::cout << __FILE__ << ":" << __LINE__ << " " << msg << std::endl
#else
#define DEBUG_LOG(msg)
#endif

// 使用示例
DEBUG_LOG("Entering function: " << __func__);
```

### 3. 平台特定代码

```cpp
// 结合其他宏进行平台检测
#if defined(_WIN32) && __STDC_HOSTED__
// Windows 特定代码
#elif defined(__linux__) && __STDC_HOSTED__
// Linux 特定代码
#else
// 独立环境或未知平台
#endif
```

## 常见问题解答

**Q: 为什么不能重定义预定义宏？**

A: 这些宏由编译器内部使用，重定义会导致编译器行为不一致和未定义行为。

**Q: `__FILE__` 会展开为绝对路径还是相对路径？**

A: 这取决于编译器实现，通常是编译命令中指定的路径。

**Q: 如何在编译时获取这些宏的值？**

A: 可以使用预处理命令：`g++ -E -dM - < /dev/null`（GCC/Clang）。

## 总结

C++ 预定义宏提供了强大的编译时信息获取能力，合理使用可以：

1. 编写可移植的跨版本代码
2. 实现详细的调试和日志功能
3. 根据环境条件优化代码路径
4. 确保代码的平台兼容性

记住始终遵循只读原则，不要尝试修改这些宏的值。随着 C++ 标准的演进，新的预定义宏会继续增加，保持对最新标准的关注将帮助你编写更健壮、更高效的代码。
