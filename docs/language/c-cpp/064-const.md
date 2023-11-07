# const

`const` 是一种常见的类型保护机制，用法主要分为以下三类：

```cpp
const int &func(int &a);   // 修饰返回值
int &func(const int &a);   // 修饰变量
int &func(int &a) const {} // 修饰成员函数
```

- `const` 修饰返回值时，肯定修饰的是引用，表示返回值不可被修改。
- `const` 修饰参数时，通常也是引用，表示在函数内部我们不希望改变实参的值。
- `const` 修饰成员函数，表示在成员函数实现中，不可修改成员变量。

```{code-block} cpp
:emphasize-lines: 9, 20, 24, 39, 49

#include <iostream>
#include <cstring>

using namespace std;

class Student
{
private:
    const int BMI = 24;
    char *name;
    int born;
    bool male;

public:
    Student()
    {
        name = new char[1024]{0};
        born = 0;
        male = false;
        BMI = 25; // can it be modified?
        cout << "Constructor: Person()" << endl;
    }

    Student(const char *name, int born, bool male)
    {
        this->name = new char[1024];
        setName(name);
        this->born = born;
        this->male = male;
        cout << "Constructor: Person(const char, int , bool)" << endl;
    }

    ~Student()
    {
        cout << "To destroy object: " << name << endl;
        delete[] name;
    }

    void setName(const char *name)
    {
        strncpy(this->name, name, 1024);
    }

    void setBorn(int born)
    {
        this->born = born;
    }

    int getBorn() const
    {
        born++; // Can it be modified?
        return born;
    }

    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};

void Student::setGender(bool isMale)
{
    male = isMale;
}

void Student::printInfo()
{
    std::cout << "Name: " << name << std::endl;
    std::cout << "Born in " << born << std::endl;
    std::cout << "Gender: " << (male ? "Male" : "Female") << std::endl;
}

int main()
{
    Student yu("Yu", 2000, true);
    cout << "yu.getBorn() = " << yu.getBorn() << endl;
    return 0;
}
```
