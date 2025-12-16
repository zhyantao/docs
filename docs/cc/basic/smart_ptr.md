# 智能指针

在 C++ 中，`std::unique_ptr`、`std::shared_ptr` 和 `std::weak_ptr` 是智能指针类型，它们的设计目的是管理动态分配的内存资源并自动释放这些资源，有助于防止内存泄漏和悬挂指针问题。

## std::unique_ptr

`std::unique_ptr` 是一种独占所有权的智能指针，其管理的对象只能由一个 `unique_ptr` 控制。

**特点：**

- 独占资源：一个对象只能被一个 `unique_ptr` 拥有
- 自动删除：当 `unique_ptr` 销毁时，它所拥有的对象会被自动删除
- 不支持拷贝构造和赋值：不能创建副本
- 支持移动语义：可以通过移动构造和移动赋值转移所有权

**示例：**

```cpp
#include <memory>
int main() {
    std::unique_ptr<int> uptr(new int(42));
    // uptr 管理的 int 对象将在 uptr 超出作用域时被删除
    return 0;
}
```

## scoped_ptr

`scoped_ptr`（如 `boost::scoped_ptr`）是一个早期的、非标准智能指针，实现了独占所有权的概念，与 `std::unique_ptr` 类似，但限制更严格。

**特点：**

- 独占所有权：独占其管理的对象
- 自动删除：超出作用域时自动删除其管理的对象
- 禁止拷贝和移动：既不能拷贝也不能移动，强调资源的局部作用域性
- 轻量级：通常比 `std::unique_ptr` 更轻量（尤其在旧的或受限的编译环境中）
- 非标准：属于 Boost 库，新代码中应优先使用 `std::unique_ptr`

**示例：**

```cpp
#include <boost/scoped_ptr.hpp>
int main() {
    boost::scoped_ptr<int> sptr(new int(42));
    // sptr 管理的 int 对象将在 sptr 超出作用域时被删除
    // boost::scoped_ptr<int> sptr2 = sptr; // 错误！禁止拷贝
    return 0;
}
```

## std::shared_ptr

`std::shared_ptr` 是一种共享所有权的智能指针，多个 `shared_ptr` 可以同时拥有同一个对象，共同维护一个引用计数器。

**特点：**

- 共享资源：多个 `shared_ptr` 可以共享同一对象的所有权
- 引用计数：通过引用计数跟踪有多少个 `shared_ptr` 指向该对象
- 自动删除：当引用计数降为零时，对象被删除
- 支持拷贝构造和赋值：可以创建副本

**示例：**

```cpp
#include <memory>
int main() {
    auto sptr = std::make_shared<int>(42);
    auto sptr2 = sptr; // sptr2 也指向同一个 int 对象
    // 当 sptr 和 sptr2 都销毁时，int 对象才会被删除
    return 0;
}
```

## std::weak_ptr

`std::weak_ptr` 是一种不增加引用计数的智能指针，通常与 `std::shared_ptr` 一起使用，以避免循环引用问题。

**特点：**

- 不增加引用计数：不影响对象的生命周期
- 用于避免循环引用：解决两个 `shared_ptr` 互相引用的情况
- lock 方法：可将 `weak_ptr` 转换成 `shared_ptr`，如果对象已被删除则返回 `nullptr`
- expire 方法：判断 `weak_ptr` 是否已经过期（即所有 `shared_ptr` 已经销毁）

**示例：**

```cpp
#include <memory>
int main() {
    auto sptr = std::make_shared<int>(42);
    auto wptr = std::weak_ptr<int>(sptr);
    if (auto sptr2 = wptr.lock()) {
        // sptr2 现在是一个指向相同对象的 shared_ptr
    } else {
        // 对象已经被删除
    }
    return 0;
}
```

## shared_from_this

`shared_from_this` 是一个成员函数，通常用于配合 `std::shared_ptr` 使用，允许一个类实例在内部持有对其自身的 `std::shared_ptr` 引用。

### 用法

类需要从 `std::enable_shared_from_this` 模板类派生。

```cpp
#include <memory>
class MyClass : public std::enable_shared_from_this<MyClass> {
public:
    std::shared_ptr<MyClass> getSharedThis() { return shared_from_this(); }
};
```

### 注意事项

- **循环引用**：可能导致循环引用，造成内存泄漏
- **调用限制**：必须在成员函数内部调用，不能在构造函数或析构函数中使用
- **对象管理**：对象必须已被 `shared_ptr` 管理

### 示例

```cpp
#include <iostream>
#include <memory>
class MyClass : public std::enable_shared_from_this<MyClass> {
public:
    MyClass(int value) : value_(value) {}
    void printValue() const { std::cout << "Value: " << value_ << std::endl; }
    std::shared_ptr<MyClass> getSharedThis() const { return shared_from_this(); }
private:
    int value_;
};

void useSharedPtr(const std::shared_ptr<MyClass>& ptr) {
    ptr->printValue();
}

int main() {
    auto obj = std::make_shared<MyClass>(42);
    auto sharedObj = obj->getSharedThis();
    useSharedPtr(sharedObj);
    return 0;
}
```

## 智能指针对比

| 特性             | `std::unique_ptr`                | `boost::scoped_ptr`                       | `std::shared_ptr`                    | `std::weak_ptr`                    |
| ---------------- | -------------------------------- | ----------------------------------------- | ------------------------------------ | ---------------------------------- |
| **所属库**       | C++标准库                        | Boost 库                                  | C++标准库                            | C++标准库                          |
| **所有权模型**   | 独占所有权                       | 独占所有权                                | 共享所有权                           | 弱引用（不拥有所有权）             |
| **所有权转移**   | 支持移动语义                     | **禁止**拷贝和移动                        | 支持拷贝构造和赋值                   | 从`shared_ptr`构造                 |
| **引用计数**     | 无                               | 无                                        | 有，影响对象生命周期                 | 有，但不增加引用计数               |
| **主要用途**     | 单一所有权场景                   | 严格的局部作用域资源管理                  | 多指针共享同一对象的场景             | 解决循环引用，观察`shared_ptr`对象 |
| **自动删除**     | 是（析构时自动删除）             | 是（析构时自动删除）                      | 是（引用计数为 0 时删除）            | 否（不管理对象生命周期）           |
| **互操作性**     | 可通过`.release()`转换为原始指针 | 封闭，不与其他智能指针交互                | 可与`weak_ptr`配合使用               | 通过`.lock()`转换为`shared_ptr`    |
| **现代 C++推荐** | ✅ 推荐使用                      | ❌ 旧代码中使用，新项目用`unique_ptr`替代 | ✅ 推荐使用                          | ✅ 推荐使用                        |
| **循环引用处理** | 不涉及                           | 不涉及                                    | 可能导致循环引用（需配合`weak_ptr`） | 专门用于解决循环引用               |

### shared_from_this 摘要

| 方面         | 说明                                                                                         |
| ------------ | -------------------------------------------------------------------------------------------- |
| **作用**     | 允许类实例内部获取指向自身的`shared_ptr`                                                     |
| **实现方式** | 类需继承`std::enable_shared_from_this<T>`                                                    |
| **使用场景** | 类需要安全地将自身传递给其他对象时                                                           |
| **限制**     | 1. 不能在构造函数/析构函数中调用<br>2. 对象必须已被`shared_ptr`管理<br>3. 需注意避免循环引用 |
| **替代方案** | 手动传递`shared_ptr`参数或使用回调机制                                                       |

## 选择指南

| 场景                               | 推荐智能指针        | 理由                           |
| ---------------------------------- | ------------------- | ------------------------------ |
| 单一所有权，明确的生命周期         | `std::unique_ptr`   | 轻量、高效、支持所有权转移     |
| 旧代码维护（Boost 环境）           | `boost::scoped_ptr` | 严格的局部作用域管理           |
| 共享所有权，多个对象需访问同一资源 | `std::shared_ptr`   | 引用计数自动管理生命周期       |
| 观察共享资源，避免循环引用         | `std::weak_ptr`     | 不影响引用计数，安全观察       |
| 类需要返回自身的共享指针           | `shared_from_this`  | 安全获取指向自身的`shared_ptr` |

## 注意事项

1. **性能考虑**：`shared_ptr` 有引用计数开销，`unique_ptr` 更轻量
2. **循环引用**：`shared_ptr` 相互引用会导致内存泄漏，需用 `weak_ptr` 打破循环
3. **所有权设计**：优先考虑 `unique_ptr`，只在需要共享所有权时使用 `shared_ptr`
4. **现代 C++**：新项目应优先使用标准库智能指针（`unique_ptr`、`shared_ptr`、`weak_ptr`）
