# class

## 嵌套类

```cpp
#include <iostream>

using namespace std;

class Storage {
public:
    class Fruit {
        string name;
        int weight;

    public:
        Fruit(string name = "", int weight = 0) : name(name), weight(weight) {
        }
        string getInfo() {
            return name + ", weight " + to_string(weight) + "kg.";
        }
    };

private:
    Fruit fruit;

public:
    Storage(Fruit f) {
        this->fruit = f;
    }
    void print() {
        cout << fruit.getInfo() << endl;
    }
};

int main() {
    Storage::Fruit apple("apple", 100);
    Storage mystorage(apple);
    mystorage.print();
    return 0;
}
```

## 构造函数

```cpp
#include <cstring>
#include <iostream>

using namespace std;

class Student {
private:
    char name[4];
    int born;
    bool male;

public:
    Student() {
        name[0] = 0;
        born = 0;
        male = false;
        cout << "Constructor: Person()" << endl;
    }

    Student(const char* initName) : born(0), male(true) {
        setName(initName);
        cout << "Constructor: Person(const char*)" << endl;
    }

    Student(const char* initName, int initBorn, bool isMale) {
        setName(initName);
        born = initBorn;
        male = isMale;
        cout << "Constructor: Person(const char, int , bool)" << endl;
    }

    void setName(const char* s) {
        strncpy(name, s, sizeof(name));
    }
    void setBorn(int b) {
        born = b;
    }
    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};

void Student::setGender(bool isMale) {
    male = isMale;
}

void Student::printInfo() {
    std::cout << "Name: " << name << std::endl;
    std::cout << "Born in " << born << std::endl;
    std::cout << "Gender: " << (male ? "Male" : "Female") << std::endl;
}

int main() {
    Student yu;
    yu.printInfo();

    yu.setName("Yu");
    yu.setBorn(2000);
    yu.setGender(true);
    yu.printInfo();

    Student li("li");
    li.printInfo();

    Student xue = Student("XueQikun", 1962, true);
    // a question: what will happen since "XueQikun" has 4+ characters?
    xue.printInfo();

    Student* zhou = new Student("Zhou", 1991, false);
    zhou->printInfo();
    delete zhou;

    return 0;
}
```

## 类外定义函数

```cpp
#include <cstring>
#include <iostream>

class Student {
private:
    char name[4];
    int born;
    bool male;

public:
    void setName(const char* s) {
        strncpy(name, s, sizeof(name));
    }

    void setBorn(int b) {
        born = b;
    }

    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};

void Student::setGender(bool isMale) {
    male = isMale;
}

void Student::printInfo() {
    std::cout << "Name: " << name << std::endl;
    std::cout << "Born in " << born << std::endl;
    std::cout << "Gender: " << (male ? "Male" : "Female") << std::endl;
}

int main() {
    Student yu;
    yu.setName("Yu");
    yu.setBorn(2000);
    yu.setGender(true);
    yu.printInfo();
    return 0;
}
```

## 访问控制

```cpp
#include <cstring>
#include <iostream>

class Student {
private:
    char name[4];
    int born;
    bool male;

public:
    void setName(const char* s) {
        strncpy(name, s, sizeof(name));
    }

    void setBorn(int b) {
        born = b;
    }

    void setGender(bool isMale) {
        male = isMale;
    }

    void printInfo() {
        std::cout << "Name: " << name << std::endl;
        std::cout << "Born in " << born << std::endl;
        std::cout << "Gender: " << (male ? "Male" : "Female") << std::endl;
    }
};

int main() {
    Student yu;
    yu.setName("Yu");
    yu.setBorn(2000);
    yu.setGender(true);
    yu.born = 2001; // you cannot access a private member
    yu.printInfo();
    return 0;
}
```

## 继承

```cpp
class Base {
protected:
    int n;

private:
    void foo1(Base& b) {
        n++;   // Okay
        b.n++; // Okay
    }
};

class Derived : public Base {
    void foo2(Base& b, Derived& d) {
        n++;       // Okay
        this->n++; // Okay
        // b.n++;      //Error. You cannot access a protected member through base
        d.n++; // Okay
    }
};

void compare(Base& b, Derived& d) // a non-member non-friend function
{
    // b.n++; // Error
    // d.n++; // Error
}
```

## 分文件编写

一个大的项目，通常把数据结构和算法实现分开放置：在 `hpp` 文件中声明类的结构，在 `cpp` 文件中对类中的成员函数做实现。因此，按照这种组织方式，我们有下面的代码示例：

```cpp
// base.hpp

class Base {
public:
    int a;
    int b;
    Base(int a = 0, int b = 0);
    ~Base();
    int product();
    friend std::ostream& operator<<(std::ostream& os, const Base& obj);
};
```

```cpp
// derive.hpp

class Derived : public Base {
public:
    int c;
    Derived(int c) : Base(c - 2, c - 1), c(c);
    ~Derived();
    int product();
    friend std::ostream& operator<<(std::ostream& os, const Derived& obj);
};
```

```cpp
// base.cpp

Base::Base(int a = 0, int b = 0) {
    this->a = a;
    this->b = b;
    cout << "Constructor Base::Base(" << a << ", " << b << ")" << endl;
}

Base::~Base() {
    cout << "Destructor Base::~Base()" << endl;
}

int Base::product() {
    return a * b;
}

friend std::ostream& Base::operator<<(std::ostream& os, const Base& obj) {
    os << "Base: a = " << obj.a << ", b = " << obj.b;
    return os;
}
```

```cpp
// derive.cpp

Derived::Derived(int c) : Base(c - 2, c - 1), c(c) {
    this->a += 3; // it can be changed after initialization
    cout << "Constructor Derived::Derived(" << c << ")" << endl;
}

Derived::~Derived() {
    cout << "Destructor Derived::~Derived()" << endl;
}

int Derived::product() {
    return Base::product() * c;
}

friend std::ostream& Derived::operator<<(std::ostream& os, const Derived& obj) {
    // call the friend function in Base class
    os << static_cast<const Base&>(obj) << endl;
    os << "Derived: c = " << obj.c;
    return os;
}
```

```cpp
// main.cpp

int main() {
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

## 继承特例化的模板类

在继承的时候，我们可能会见到类似下面的语法，不要被尖括号所迷惑，它是 **继承特例化的模板类** 的一种写法：

```cpp
#include <iostream>
#include <memory>

// 继承一个特例化的模板类
class SharedFromThis : public std::enable_shared_from_this<SharedFromThis> {
public:
    void doSomething() {
        std::shared_ptr<SharedFromThis> sharedPtr = shared_from_this();
        std::cout << "Shared pointer count: " << sharedPtr.use_count() << std::endl;
    }
};

int main() {
    std::shared_ptr<SharedFromThis> sharedPtr = std::make_shared<SharedFromThis>();
    sharedPtr->doSomething();

    return 0;
}
```
