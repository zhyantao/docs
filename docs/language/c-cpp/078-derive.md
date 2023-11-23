# 继承

一个大的项目，通常把数据结构和算法实现分开放置：在 `hpp` 文件中声明类的结构，在 `cpp` 文件中对类中的成员函数做实现。因此，按照这种组织方式，我们有下面的代码示例：

```cpp
// base.hpp

class Base
{
public:
    int a;
    int b;
    Base(int a = 0, int b = 0);
    ~Base();
    int product();
    friend std::ostream &operator<<(std::ostream &os, const Base &obj);
};
```

```cpp
// derive.hpp

class Derived : public Base
{
public:
    int c;
    Derived(int c) : Base(c - 2, c - 1), c(c);
    ~Derived();
    int product();
    friend std::ostream &operator<<(std::ostream &os, const Derived &obj);
};
```

```cpp
// base.cpp

Base::Base(int a = 0, int b = 0)
{
    this->a = a;
    this->b = b;
    cout << "Constructor Base::Base(" << a << ", " << b << ")" << endl;
}

Base::~Base()
{
    cout << "Destructor Base::~Base()" << endl;
}

int Base::product()
{
    return a * b;
}

friend std::ostream &Base::operator<<(std::ostream &os, const Base &obj)
{
    os << "Base: a = " << obj.a << ", b = " << obj.b;
    return os;
}
```

```cpp
// derive.cpp

Derived::Derived(int c) : Base(c - 2, c - 1), c(c)
{
    this->a += 3; // it can be changed after initialization
    cout << "Constructor Derived::Derived(" << c << ")" << endl;
}

Derived::~Derived()
{
    cout << "Destructor Derived::~Derived()" << endl;
}

int Derived::product()
{
    return Base::product() * c;
}

friend std::ostream &Derived::operator<<(std::ostream &os, const Derived &obj)
{
    // call the friend function in Base class
    os << static_cast<const Base &>(obj) << endl;
    os << "Derived: c = " << obj.c;
    return os;
}
```

```cpp
// main.cpp

int main()
{
    {
        Base base(1, 2);
        cout << "Product = " << base.product() << endl;
        cout << base << endl;
    }
    cout << "----------------------" << endl;
    {
        Derived derived(5);
        cout << derived << endl;
        cout << "Product = " << derived.product() << endl;
    }
    return 0;
}
```

在继承的时候，我们可能会见到类似下面的语法，不要被尖括号所迷惑，它是 **继承特例化的模板类** 的一种写法：

```cpp
#include <iostream>
#include <memory>

// 继承一个特例化的模板类
class SharedFromThis : public std::enable_shared_from_this<SharedFromThis>
{
public:
    void doSomething()
    {
        std::shared_ptr<SharedFromThis> sharedPtr = shared_from_this();
        std::cout << "Shared pointer count: " << sharedPtr.use_count() << std::endl;
    }
};

int main()
{
    std::shared_ptr<SharedFromThis> sharedPtr = std::make_shared<SharedFromThis>();
    sharedPtr->doSomething();

    return 0;
}
```
