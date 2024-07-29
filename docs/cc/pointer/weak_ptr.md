# weak_ptr

`weak_ptr` 是一种用于解决 `shared_ptr` 相互引用时产生死锁问题的智能指针。如果有两个 `shared_ptr` 相互引用，那么这两个 `shared_ptr` 指针的引用计数永远不会下降为 0，资源永远不会释放。 `weak_ptr` 是对对象的一种弱引用，它不会增加对象的 `use_count`，`weak_ptr` 和 `shared_ptr` 可以相互转化， `shared_ptr` 可以直接赋值给 `weak_ptr` ，`weak_ptr` 也可以通过调用 `lock` 函数来获得 `shared_ptr`。

`weak_ptr` 指针通常不单独使用，只能和 `shared_ptr` 类型指针搭配使用。将一个 `weak_ptr` 绑定到一个 `shared_ptr` 不会改变 `shared_ptr` 的引用计数。一旦最后一个指向对象的 `shared_ptr` 被销毁，对象就会被释放。即使有 `weak_ptr` 指向对象，对象也还是会被释放。

`weak_ptr` 并没有重载 `operator->` 和 `operator *` 操作符，因此不可直接通过 `weak_ptr` 使用对象，典型的用法是调用其 `lock` 函数来获得 `shared_ptr` 示例，进而访问原始对象。

为了理解 [std::shared_from_this()](https://en.cppreference.com/w/cpp/memory/enable_shared_from_this/shared_from_this) 方法，我们可以参考官方给的示例：

```cpp
#include <iostream>
#include <memory>

struct Foo : public std::enable_shared_from_this<Foo> {
    Foo() {
        std::cout << "Foo::Foo\n";
    }
    ~Foo() {
        std::cout << "Foo::~Foo\n";
    }
    std::shared_ptr<Foo> getFoo() {
        return shared_from_this();
    }
};

int main() {
    Foo* f = new Foo;
    std::shared_ptr<Foo> pf1;

    {
        std::shared_ptr<Foo> pf2(f); // pf2 指向了 Foo 对象
        pf1 = pf2->getFoo();         // pf1 获得了与 pf2 共享的指针，也指向了 Foo 对象
    }

    std::cout << "pf2 is gone\n";
}
```
