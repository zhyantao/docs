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

## 嵌套类

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

## 继承的特点及访问控制

### 特点

- 代码重用：子类可以直接使用父类的属性和方法。
- 多态性：通过虚函数实现不同类型的对象对同一消息作出响应的能力。
- 扩展性：可以轻松地添加新的子类来扩展系统的功能而不需要修改现有的代码。

### 访问控制

继承方式决定了基类成员在派生类中的访问级别：

- `public` 继承：基类的 `public` 成员仍是 `public`，`protected` 成员仍是 `protected`（最常见的继承方式，满足"is-a"关系）；
- `protected` 继承：基类的 `public` 和 `protected` 成员在派生类中都变为 `protected`；
- `private` 继承：基类的 `public` 和 `protected` 成员在派生类中都变为 `private`（派生类内部仍可访问，但进一步的派生类不可再访问）。

注意：无论哪种继承方式，基类的 `private` 成员都不能被派生类直接访问。

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

## 继承特例化的模板类

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

## `= delete` 与 `= default`

C++11 起，可以显式删除（`= delete`）或默认化（`= default`）特殊成员函数。

- `= delete` 禁止调用某个成员函数。常见用途：禁止拷贝构造和拷贝赋值（适用于管理独占资源的类）、禁止隐式类型转换。
- `= default` 显式要求编译器生成默认实现，通常用于析构函数或拷贝成员，明确表达"使用默认行为"的意图。

```cpp
#include <iostream>

using namespace std;

class IntMat {
    size_t rows;
    size_t cols;
    int* data;

public:
    IntMat(size_t rows, size_t cols) : rows(rows), cols(cols) {
        data = new int[rows * cols]{};
    }
    ~IntMat() { delete[] data; }

    // 禁止拷贝构造与拷贝赋值：对象独占 data 内存，拷贝会导致重复释放
    IntMat(const IntMat&)            = delete;
    IntMat& operator=(const IntMat&) = delete;

    int getElement(size_t r, size_t c);
    bool setElement(size_t r, size_t c, int value);
};

int IntMat::getElement(size_t r, size_t c) {
    if (r >= this->rows || c >= this->cols) {
        cerr << "Indices are out of range" << endl;
        return 0;
    }
    return data[this->cols * r + c];
}

bool IntMat::setElement(size_t r, size_t c, int value) {
    if (r >= this->rows || c >= this->cols) return false;

    data[this->cols * r + c] = value;
    return true;
}

int main() {
    IntMat imat(3, 4);
    imat.setElement(1, 2, 256);

    // IntMat imat2(imat); // error: 拷贝构造已被删除
    // IntMat imat3(2, 3);
    // imat3 = imat;       // error: 拷贝赋值已被删除

    cout << imat.getElement(1, 2) << endl;

    return 0;
}
```

对于只需要拷贝语义的类，也可以用 `= default` 显式保留默认实现：

```cpp
class Point {
public:
    double x, y;
    Point(double x, double y) : x(x), y(y) {}
    ~Point()                     = default; // 显式使用默认析构
    Point(const Point&)          = default; // 显式使用默认拷贝构造
    Point& operator=(const Point&) = default;
};
```
