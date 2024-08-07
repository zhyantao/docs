# friend

在 C++ 中，友元（friend）是一个特殊的机制，它允许非成员函数或者另一个类的成员函数访问当前类的私有（private）和保护（protected）成员。友元可以是函数或者是另一个类。

友元机制在某些场景下非常有用，尤其是在需要提高程序效率或者实现某些特定功能的时候。然而，由于它破坏了封装性原则，所以在设计时需要权衡利弊。

## 友元函数

友元函数是指被声明为某个类的友元的函数。这类函数虽然不是该类的成员，但是它可以访问这个类的所有私有和保护成员。这在某些情况下很有用，比如当你需要一个函数能够直接操作一个类的内部数据时。

### 声明

- 在类定义中，通过使用 `friend` 关键字来声明友元函数。
- 友元函数的声明不需要函数体，它更像是一个声明而不是定义。

### 访问权限

- 友元函数可以访问该类的所有私有和保护成员。

### 作用域

- 友元函数不属于任何特定的对象实例，因此它不能直接访问类的成员变量，除非通过对象实例引用或指针。

### 实例

- 友元函数可以在类外定义，但必须在类内声明。

### 示例代码

假设我们有一个类 `Circle`，它有一个私有的半径成员 `radius`，并且我们想要创建一个友元函数 `printRadius` 来打印这个半径值。

```cpp
#include <iostream>

class Circle {
private:
    double radius;

public:
    Circle(double r) : radius(r) {
    }

    friend void printRadius(const Circle& c); // 声明友元函数
};

// 友元函数定义
void printRadius(const Circle& c) {
    std::cout << "Radius of the circle: " << c.radius << std::endl;
}

int main() {
    Circle c(5.0);
    printRadius(c); // 调用友元函数

    return 0;
}
```

在这个例子中，`printRadius` 函数被声明为 `Circle` 类的友元函数，因此它可以访问 `Circle` 类的私有成员 `radius`。

### 注意事项

- 友元函数不隐式地捕获类的对象；你需要明确地传递对象实例给友元函数。
- 友元函数不属于类的成员函数，所以它不能使用 `this` 指针。
- 友元关系不会自动传递，即如果 `A` 是 `B` 的友元，那么 `B` 不一定是 `A` 的友元，除非也显式声明。
- 友元函数可能会破坏封装性，因此应该谨慎使用。

## 友元类

在 C++中，友元类（friend class）是一种特殊的关系，它允许一个类访问另一个类的私有（private）和保护（protected）成员。这种机制可以用来增强类之间的合作，同时保持封装性。友元类的概念类似于友元函数，但这里整个类都被声明为另一个类的友元。

### 声明

- 在类定义中，使用 `friend` 关键字来声明友元类。
- 通常在类的定义中声明友元类，但不在友元类中定义任何成员。

### 访问权限

- 友元类中的成员函数可以访问被声明为友元的那个类的所有私有和保护成员。

### 作用域

- 友元类中的成员函数可以直接访问另一个类的私有和保护成员，就像它们是自己的成员一样。

### 实例

- 友元类可以在类外定义，但必须在类内声明。

### 示例代码

假设我们有两个类 `Account` 和 `BankManager`，其中 `Account` 有一个私有成员 `balance`，而 `BankManager` 需要访问这个成员以进行管理操作。

```cpp
#include <iostream>

class Account {
private:
    double balance;

public:
    Account(double initialBalance) : balance(initialBalance) {
    }

    friend class BankManager; // 声明 BankManager 为友元类
};

class BankManager {
public:
    void deposit(Account& acc, double amount) {
        acc.balance += amount;
        std::cout << "Deposited: " << amount << std::endl;
        std::cout << "New balance: " << acc.balance << std::endl;
    }
};

int main() {
    Account acc(1000.0);
    BankManager manager;

    manager.deposit(acc, 500.0); // 使用 BankManager 的 deposit 方法

    return 0;
}
```

在这个例子中，`BankManager` 类被声明为 `Account` 类的友元类，这意味着 `BankManager` 类中的成员函数可以直接访问 `Account` 类的私有成员 `balance`。

### 注意事项

- 友元关系是单向的，即如果 `A` 是 `B` 的友元，那么 `B` 不一定是 `A` 的友元，除非也显式声明。
- 友元类中的所有成员函数都可以访问另一个类的私有和保护成员。
- 友元类可能会破坏封装性，因此应该谨慎使用。

## 循环引用问题

循环引用通常发生在两个类互相依赖对方的成员函数的情况下。例如，类 `A` 的成员函数需要访问类 `B` 的私有成员，而类 `B` 的成员函数也需要访问类 `A` 的私有成员。如果没有适当的设计，这会导致编译错误，因为编译器不知道如何处理这种相互依赖。

### 使用友元解决循环引用

一种解决方法是将一个类声明为另一个类的友元。这允许其中一个类访问另一个类的私有成员，从而解决了循环引用的问题。但是，这通常意味着这两个类之间的耦合度非常高，可能需要重新考虑设计是否合理。

### 示例代码

```cpp
#include <iostream>

class A {
private:
    int dataA;

public:
    A(int d) : dataA(d) {
    }

    friend class B; // 声明 B 为友元类
};

class B {
private:
    int dataB;

public:
    B(int d) : dataB(d) {
    }

    void setAData(A& a, int value) {
        a.dataA = value; // 访问 A 的私有成员
        std::cout << "Set A's data to: " << value << std::endl;
    }

    friend class A; // 也可以声明 A 为友元类
};

int main() {
    A a(10);
    B b(20);

    b.setAData(a, 30); // 使用 B 的 setAData 方法

    return 0;
}
```

在这个例子中，`A` 和 `B` 相互声明为友元类，这样它们就可以访问对方的私有成员，从而解决了循环引用的问题。请注意，这种方式可能会导致封装性受损，因此需要根据具体情况判断是否使用这种方法。
