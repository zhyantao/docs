# 重载 + 和 +=

```cpp
// main.cpp

#include <iostream>
#include "time.hpp"

using namespace std;

int main()
{
    MyTime t1(2, 40);
    MyTime t2(1, 20);
    std::cout << (t1 + t2).getTime() << std::endl;

    t1 += t2;          // operator
    t1.operator+=(t2); // function

    std::cout << t1.getTime() << endl;

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

    std::string getTime() const
    {
        return std::to_string(this->hours) + " hours and " + std::to_string(this->minutes) + " minutes.";
    }
};
```