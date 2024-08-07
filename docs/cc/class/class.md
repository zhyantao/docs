# class

## 构造函数

### 定义

构造函数是一种特殊的成员函数，它在创建对象时被自动调用，用于初始化对象的状态。构造函数的名字与类名相同，并且没有返回类型（即使是 `void` 也不行）。

### 注意事项

- 默认构造函数：如果没有显式定义任何构造函数，编译器会自动提供一个默认构造函数。
- 显式构造函数：可以通过使用 `explicit` 关键字来防止隐式类型转换。
- 拷贝构造函数：当需要通过已存在的对象来初始化新对象时，需要使用拷贝构造函数。
- 移动构造函数：用于从临时对象或者右值引用中初始化新对象，以支持高效的资源转移。
- 初始化列表：建议使用初始化列表来初始化成员变量，尤其是当成员是引用或常量时，它优先于构造函数体内的赋值操作。
- 构造顺序：如果一个类包含其他类的对象作为成员，则基类和成员对象的构造顺序需要特别注意。
- 异常安全：在构造过程中要确保异常安全，尤其是在初始化列表中抛出异常时。

### 示例

```cpp
#include <iostream>

class Point {
public:
    double x, y;

    // 默认构造函数
    Point() : x(0), y(0) {}

    // 显式构造函数
    explicit Point(double x, double y) : x(x), y(y) {}

    // 拷贝构造函数
    Point(const Point& other) : x(other.x), y(other.y) {}

    // 移动构造函数
    Point(Point&& other) noexcept : x(std::move(other.x)), y(std::move(other.y)) {}
};

int main() {
    Point p1;                 // 调用默认构造函数
    Point p2(1.0, 2.0);       // 调用显式构造函数
    Point p3(p2);             // 调用拷贝构造函数
    Point p4 = std::move(p3); // 调用移动构造函数
    return 0;
}
```

## 2. 嵌套类

### 定义

嵌套类是指在一个类的内部定义的另一个类。它可以是匿名的（即没有名字），也可以是有名字的。

### 使用场景

- 封装：将相关的类组织在一起，提高代码的可读性和可维护性。
- 命名空间：避免名称冲突，为类提供更具体的上下文。
- 访问控制：嵌套类可以访问外部类的私有成员，这有助于实现更紧密的耦合。

### 示例

```cpp
#include <iostream>

class OuterClass {
public:
    class InnerClass {
    public:
        void print() const { std::cout << "InnerClass\n"; }
    };

    void createInner() {
        InnerClass inner;
        inner.print();
    }
};

int main() {
    OuterClass outer;
    outer.createInner();

    // 外部访问
    OuterClass::InnerClass inner;
    inner.print();
    return 0;
}
```

## 3. 继承的特点及访问控制

### 特点

- 代码重用：子类可以直接使用父类的属性和方法。
- 多态性：通过虚函数实现不同类型的对象对同一消息作出响应的能力。
- 扩展性：可以轻松地添加新的子类来扩展系统的功能而不需要修改现有的代码。

### 访问控制

- `public`：继承的所有成员都可被访问。
- `protected`：继承的成员对子类可见，但对外部不可见。
- `private`：继承的成员只在派生类中可见，对外部和子类都不可见。

### 示例

```cpp
#include <iostream>

class Base {
protected:
    int data;

public:
    Base(int d) : data(d) {}

    virtual void print() const { std::cout << "Base: " << data << '\n'; }
};

class Derived : public Base {
public:
    Derived(int d) : Base(d) {}

    void print() const override { std::cout << "Derived: " << data << '\n'; }
};

int main() {
    Derived d(42);
    d.print();
    return 0;
}
```

## 4. 继承特例化的模板类

### 示例

假设我们有一个模板类 `BaseTemplate` 和一个特例化版本 `BaseTemplate<int>`，并且想要从它们派生一个新的类 `DerivedTemplate`。

```cpp
#include <iostream>

template <typename T>
class BaseTemplate {
public:
    T data;
    BaseTemplate(T d) : data(d) {}
};

// Specialization for int
template <>
class BaseTemplate<int> {
public:
    int data;
    BaseTemplate(int d) : data(d * 2) {} // 注意这里特例化了构造函数
};

// Derived from the general template
template <typename T>
class DerivedTemplate : public BaseTemplate<T> {
public:
    DerivedTemplate(T d) : BaseTemplate<T>(d) {}
};

// Derived from the specialized template
class DerivedFromSpecialized : public BaseTemplate<int> {
public:
    DerivedFromSpecialized(int d) : BaseTemplate<int>(d) {}
};

int main() {
    DerivedTemplate<double> dt(5.0);
    std::cout << "Data in DerivedTemplate: " << dt.data << std::endl;

    DerivedFromSpecialized dfs(5);
    std::cout << "Data in DerivedFromSpecialized: " << dfs.data << std::endl;

    return 0;
}
```

在这个例子中：

- `BaseTemplate<T>` 是一个通用模板类。
- `BaseTemplate<int>` 是 `BaseTemplate` 的特例化版本。
- `DerivedFromSpecialized` 继承自 `BaseTemplate<int>`。
- `DerivedTemplate<T>` 继承自 `BaseTemplate<T>`。
