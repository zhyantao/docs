# 运行时类型识别（RTTI）

RTTI（Run-Time Type Identification）允许程序在运行时获取对象的类型信息，主要包括 `typeid` 运算符和 `dynamic_cast` 运算符。

```{note}
注意：本站的 [C/C++ 代码风格](../index) 参考 Google 风格约定**禁止使用 RTTI**（`dynamic_cast` 有一定运行时开销，
大量使用通常意味着设计上的多态使用不当），本页仅作学习参考。
```

## typeid

```cpp
#include <iostream>
#include <typeinfo>

using namespace std;

class Person {
protected:
    string name;

public:
    Person(string name = "") : name(name) {};
    virtual ~Person() {}
    string getInfo() { return name; }
};

class Student : public Person {
    string studentid;

public:
    Student(string name = "", string sid = "") : Person(name), studentid(sid) {};
    string getInfo() { return name + ":" + studentid; }
};

int main() {
    string s("hello");

    cout << "typeid.name of s           is " << typeid(s).name() << endl;
    cout << "typeid.name of std::string is " << typeid(std::string).name() << endl;
    cout << "typeid.name of Student     is " << typeid(Student).name() << endl;

    if (typeid(std::string) == typeid(s)) cout << "s is a std::string object." << endl;

    return 0;
}
```

## 多态与类型转换的陷阱

下面的例子演示了 C 风格强制转换的危险性：把基类对象强行转换成派生类指针后调用虚函数，会产生未定义行为。
安全的做法是使用 `dynamic_cast`（配合虚函数）进行向下转换。

```cpp
#include <iostream>

using namespace std;

class Person {
protected:
    string name;

public:
    Person(string name = "") : name(name) {};
    virtual ~Person() {}
    string getInfo() { return name; }
};

class Student : public Person {
    string studentid;

public:
    Student(string name = "", string sid = "") : Person(name), studentid(sid) {};
    string getInfo() { return name + ":(" + studentid + ")"; }
};

int main() {
    Person person("Yu");
    Student student("Sam", "20210212");
    Person* pp  = &student;
    Person& rp  = student;
    Student* ps = (Student*)&person; // danger!
    cout << "person.getInfo():" << person.getInfo() << endl;
    cout << "pp->getInfo():" << pp->getInfo() << endl;
    cout << "rp.getInfo():" << rp.getInfo() << endl;
    cout << "ps->getInfo():" << ps->getInfo() << endl; // danger if getInfo is not virtual

    char* p = (char*)100;
    // ps = dynamic_cast<Student*>(&person);
    // printf("address = %p\n", ps);
    // pp = dynamic_cast<Person*>(&student);
    // printf("address = %p\n", pp);
    return 0;
}
```

`dynamic_cast` 只能用于含虚函数的类层次，转换失败时：
- 指针版本返回 `nullptr`；
- 引用版本抛出 `std::bad_cast` 异常。
