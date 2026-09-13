# this

`this` 是指向当前对象的指针，在类的非静态成员函数内部都可以使用。它的典型用途有：

- **区分同名变量**：当成员函数参数与成员变量重名时，用 `this->member` 指代成员变量（见下方 `setBorn()`）；
- **返回对象自身**：链式调用（如 `obj.setA().setB()`）时 `return *this`；
- **在构造函数中调用其他成员函数**：明确表示"调用的是这个对象的成员"（见下方带参构造函数）。

注意：`this` 只在非静态成员函数中有效，静态成员函数没有 `this` 指针。

```cpp
#include <cstring>
#include <iostream>

using namespace std;

class Student {
private:
    char* name;
    int born;
    bool male;

public:
    Student() {
        name = new char[1024]{0};
        born = 0;
        male = false;
        cout << "Constructor: Person()" << endl;
    }

    Student(const char* name, int born, bool male) {
        this->name = new char[1024];
        this->setName(name);
        this->born = born;
        this->male = male;
        cout << "Constructor: Person(const char, int , bool)" << endl;
    }

    ~Student() {
        cout << "To destroy object: " << name << endl;
        delete[] name;
    }

    void setName(const char* name) { strncpy(this->name, name, 1024); }

    void setBorn(int born) { this->born = born; }

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
    Student* class1 = new Student[3]{
        {"Tom", 2000, true},
        {"Bob", 2001, true},
        {"Amy", 2002, false},
    };

    class1[1].printInfo();
    delete[] class1;

    return 0;
}
```
