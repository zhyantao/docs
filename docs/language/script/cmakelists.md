# CMakeLists

## 使用方法

```bash
mkdir build
cd build && cmake ..
make
sudo make install
```

## 一个例子

```cpp
// main.cpp

#include "student.hpp"

int main()
{
    Student yu;
    yu.setName("Yu");
    yu.setBorn(2000);
    yu.setGender(true);
    yu.printInfo();
    return 0;
}
```

```cpp
// student.cpp

#include <iostream>
#include "student.hpp"

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
```

```cpp
// student.hpp

#pragma once

#include <cstring>
class Student
{
private:
    char name[4];
    int born;
    bool male;

public:
    void setName(const char *s)
    {
        strncpy(name, s, sizeof(name));
    }

    void setBorn(int b)
    {
        born = b;
    }

    // the declarations, the definitions are out of the class
    void setGender(bool isMale);
    void printInfo();
};
```

```cmake
# CMakeLists.txt

cmake_minimum_required(VERSION 3.12)

project(persondemo)

ADD_EXECUTABLE(persondemo main.cpp student.cpp)
```

---

1. 在 Linux 下使用 CMake 构建应用程序. <https://www.ibm.com/developerworks/cn/linux/l-cn-cmake/>
2. CMake 入门实战. <https://www.hahack.com/codes/cmake/>
3. Cmake 实战 <https://kdocs.cn/l/ch0JlSoQjQdm>
