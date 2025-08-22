# 智能指针

在 C++ 中，`std::unique_ptr`, `std::shared_ptr`, 和 `std::weak_ptr` 是智能指针类型，它们的设计目的是为了管理动态分配的内存资源并自动释放这些资源。这些智能指针有助于防止内存泄漏和悬挂指针的问题。

## std::unique_ptr

`std::unique_ptr` 是一种独占所有权的智能指针。这意味着它管理的对象只能由一个 `unique_ptr` 控制。一旦 `unique_ptr` 对象超出作用域或者被显式地重置，它所控制的对象就会被删除。

**特点：**

- 独占资源：一个对象只能被一个 `unique_ptr` 所拥有。
- 自动删除：当 `unique_ptr` 对象销毁时，它所拥有的对象会被自动删除。
- 不支持拷贝构造和赋值：不能创建 `unique_ptr` 的副本。
- 支持移动语义：可以通过移动构造和移动赋值将所有权从一个 `unique_ptr` 移动到另一个 `unique_ptr`。

**示例：**

```cpp
#include <memory>

int main() {
    std::unique_ptr<int> uptr(new int(42));
    // uptr 管理的 int 对象将在 uptr 超出作用域时被删除
    return 0;
}
```

## std::shared_ptr

`std::shared_ptr` 是一种共享所有权的智能指针。多个 `shared_ptr` 可以同时拥有同一个对象，它们共同维护一个引用计数器。当最后一个 `shared_ptr` 销毁或重置时，对象会被删除。

**特点：**

- 共享资源：多个 `shared_ptr` 可以共享同一对象的所有权。
- 引用计数：通过引用计数跟踪有多少个 `shared_ptr` 正在指向该对象。
- 自动删除：当引用计数降为零时，对象被删除。
- 支持拷贝构造和赋值：可以创建 `shared_ptr` 的副本。

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

`std::weak_ptr` 是一种不增加引用计数的智能指针。它通常与 `std::shared_ptr` 一起使用，以避免循环引用问题。`weak_ptr` 可以持有对 `shared_ptr` 所指向的对象的弱引用，但不会影响对象的生命周期。

**特点：**

- 不增加引用计数：`weak_ptr` 不会影响 `shared_ptr` 的引用计数。
- 用于避免循环引用：常用于解决两个 `shared_ptr` 互相引用的情况。
- lock 方法：可以将 `weak_ptr` 转换成 `shared_ptr`，但可能返回 `nullptr` 如果对象已被删除。
- expire 方法：判断 `weak_ptr` 是否已经过期（即所有 `shared_ptr` 已经销毁）。

**示例：**

```cpp
#include <memory>

int main() {
    auto sptr = std::make_shared<int>(42);
    auto wptr = std::weak_ptr<int>(sptr);
    // 如果 sptr 销毁后，wptr 将不再有效
    if (auto sptr2 = wptr.lock()) {
        // sptr2 现在是一个指向相同对象的 shared_ptr
    } else {
        // 对象已经被删除
    }
    return 0;
}
```

## 联系

- **共同目的**：它们都是智能指针，用于自动管理动态分配的内存。
- **RAII原则**：它们都遵循资源获取即初始化（RAII）的原则，确保资源在适当的时候被正确地分配和释放。
- **互操作性**：`std::unique_ptr` 可以通过 `.release()` 方法释放其所有权，从而可以转换为 `std::shared_ptr` 或者 `std::weak_ptr` 的原始指针形式。
- **所有权转移**：`std::unique_ptr` 和 `std::shared_ptr` 都可以通过移动语义来转移所有权。

## 总结

- `std::unique_ptr` 适用于单一所有权的情形，对象的生命周期完全由单个智能指针控制。
- `std::shared_ptr` 适用于需要共享所有权的情形，多个智能指针可以共享同一个对象的生命周期。
- `std::weak_ptr` 用于避免循环引用，并作为观察者模式的一种实现方式，它可以观察 `std::shared_ptr` 所管理的对象，但不会影响其生命周期。

在设计系统时，根据对象的生命周期和所有权需求选择合适的智能指针类型是非常重要的。

## shared_from_this

`shared_from_this` 是一个成员函数，它通常用于配合 `std::shared_ptr` 使用。这个成员函数允许一个类实例在内部持有对其自身的 `std::shared_ptr` 引用。这对于管理类的生命周期非常有用，特别是当类实例需要在外部被访问时。

**shared_from_this 的用法**

当你有一个类，它希望能够在内部生成一个指向自己的 `std::shared_ptr`，以便能够安全地将自己传递给其他对象或者在其他地方使用，这时就可以使用 `shared_from_this`。

_1. 类的定义_

首先，你的类需要从 `enable_shared_from_this` 模板类派生，或者直接包含 `enable_shared_from_this` 的模板特化。

```cpp
#include <memory>

class MyClass : public std::enable_shared_from_this<MyClass> {
public:
    // ...
    std::shared_ptr<MyClass> getSharedThis() { return shared_from_this(); }
};
```

这里的关键是 `std::enable_shared_from_this`。这个模板类提供了 `shared_from_this` 成员函数，该函数返回一个指向当前对象的 `std::shared_ptr`。

_2. 使用 shared_from_this_

接下来，你可以通过 `getSharedThis` 函数返回一个指向当前对象的 `std::shared_ptr`。

```cpp
std::shared_ptr<MyClass> createSharedPtr() {
    auto obj = std::make_shared<MyClass>();
    return obj->getSharedThis();
}
```

在这个例子中，`createSharedPtr` 函数返回一个指向 `MyClass` 的 `std::shared_ptr`。

_shared_from_this 的注意事项_

- **循环引用**：使用 `shared_from_this` 时要小心，因为它可能导致循环引用。如果一个对象持有指向自身的一个 `std::shared_ptr`，并且还有其他对象也持有指向该对象的 `std::shared_ptr`，那么这些对象可能会相互持有对方的 `shared_ptr`，导致引用计数永远不会下降到零，从而导致内存泄漏。
- **成员函数**：`shared_from_this` 必须在一个成员函数内部调用，不能在构造函数或析构函数中使用。
- **成员函数必须是 const**：如果希望在 const 成员函数中使用 `shared_from_this`，那么需要将 `enable_shared_from_this` 替换为 `enable_shared_from_this<T>` 的模板特化，其中 `T` 是类的类型。

**示例**

下面是一个完整的示例，展示了如何使用 `shared_from_this`。

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

void useSharedPtr(const std::shared_ptr<MyClass>& ptr) { ptr->printValue(); }

int main() {
    auto obj = std::make_shared<MyClass>(42);
    auto sharedObj = obj->getSharedThis();
    useSharedPtr(sharedObj);
    return 0;
}
```

在这个示例中，`MyClass` 从 `std::enable_shared_from_this<MyClass>` 派生，并提供了一个 `getSharedThis` 成员函数来返回一个指向自身的 `std::shared_ptr`。`useSharedPtr` 函数接受一个 `std::shared_ptr<MyClass>` 参数，并调用 `printValue` 方法来打印对象的值。

**总结**

- `shared_from_this` 是 `std::enable_shared_from_this` 模板类提供的成员函数，用于生成指向当前对象的 `std::shared_ptr`。
- 它通常用于在类的成员函数内部返回一个指向自身的 `std::shared_ptr`。
- 使用时需要注意避免循环引用的问题。
- `shared_from_this` 需要在类的成员函数中调用，不能在构造函数或析构函数中使用。
