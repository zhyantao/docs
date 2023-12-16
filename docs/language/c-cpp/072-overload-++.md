# 重载 ++

```cpp
// main.cpp

#include <iostream>
#include "time.hpp"

using namespace std;

int main()
{
    MyTime t1(1, 59);
    MyTime t2 = t1++;
    MyTime t3 = ++t1;

    std::cout << "t1 is " << t1 << std::endl;
    std::cout << "t2 is " << t2 << std::endl;
    std::cout << "t3 is " << t3 << std::endl;

    return 0;
}
```

```cpp
// time.hpp

#pragma once
#include <iostream>

class MyTime
{
    int hours;
    int minutes;

public:
    MyTime() : hours(0), minutes(0)
    {
        std::cout << "Constructor MyTime()" << std::endl;
    }

    MyTime(int m) : hours(0), minutes(m)
    {
        std::cout << "Constructor MyTime(int)" << std::endl;
        this->hours += this->minutes / 60;
        this->minutes %= 60;
    }

    MyTime(int h, int m) : hours(h), minutes(m)
    {
        std::cout << "Constructor MyTime(int,int)" << std::endl;
    }

    // prefix increment
    MyTime &operator++()
    {
        this->minutes++;
        this->hours += this->minutes / 60;
        this->minutes = this->minutes % 60;
        return *this;
    }

    // postfix increment
    MyTime operator++(int)
    {
        MyTime old = *this; // keep the old value
        operator++();       // prefix increment
        return old;
    }

    friend std::ostream &operator<<(std::ostream &os, const MyTime &t)
    {
        std::string str = std::to_string(t.hours) + " hours and " + std::to_string(t.minutes) + " minutes.";
        os << str;
        return os;
    }
};
```