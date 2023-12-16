# 支持 MyTime + string 运算

```cpp
// main.cpp

#include <iostream>
#include "time.hpp"

using namespace std;

int main()
{
    MyTime t1(2, 40);
    std::cout << (t1 + 30).getTime() << std::endl;

    t1 += 30;          // operator
    t1.operator+=(30); // function

    std::cout << t1.getTime() << endl;

    std::cout << (t1 + "one hour").getTime() << std::endl;
    std::cout << (t1 + "two hour").getTime() << std::endl;

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
    MyTime() : hours(0), minutes(0) {}
    MyTime(int h, int m) : hours(h), minutes(m) {}

    MyTime operator+(const MyTime &t) const
    {
        MyTime sum;
        sum.minutes = this->minutes + t.minutes;
        sum.hours = this->hours + t.hours;

        sum.hours += sum.minutes / 60;
        sum.minutes %= 60;

        return sum;
    }

    MyTime &operator+=(const MyTime &t)
    {
        this->minutes += t.minutes;
        this->hours += t.hours;

        this->hours += this->minutes / 60;
        this->minutes %= 60;

        return *this;
    }

    MyTime operator+(int m) const
    {
        MyTime sum;
        sum.minutes = this->minutes + m;
        sum.hours = this->hours;
        sum.hours += sum.minutes / 60;
        sum.minutes %= 60;
        return sum;
    }

    MyTime &operator+=(int m)
    {
        this->minutes += m;
        this->hours += this->minutes / 60;
        this->minutes %= 60;
        return *this;
    }

    MyTime operator+(const std::string str) const
    {
        MyTime sum = *this;
        if (str == "one hour")
            sum.hours = this->hours + 1;
        else
            std::cerr << "Only \"one hour\" is supported." << std::endl;
        return sum;
    }

    std::string getTime() const
    {
        return std::to_string(this->hours) + " hours and " + std::to_string(this->minutes) + " minutes.";
    }
};
```