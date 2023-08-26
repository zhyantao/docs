# 重载 int()、= 和 <<

main.cpp

```cpp
#include <iostream>
#include "time.hpp"

using namespace std;

int main()
{
    MyTime t1(1, 20);
    int minutes = t1; //implicit conversion
    float f = float(t1); //explicit conversion. 
    std::cout << "minutes = " << minutes << std::endl;
    std::cout << "minutes = " << f << std::endl;

    MyTime t2 = 70;
    std::cout << "t2 is " << t2 << std::endl;

    MyTime t3;
    t3 = 80;
    std::cout << "t3 is " << t3 << std::endl;

    return 0;

}
```

time.hpp

```cpp
#pragma once
#include <iostream>

class MyTime
{
    int hours;
    int minutes;
  public:
    MyTime(): hours(0), minutes(0)
    {
        std::cout << "Constructor MyTime()" << std::endl;
    }
    MyTime(int m): hours(0), minutes(m)
    {
        std::cout << "Constructor MyTime(int)" << std::endl;
        this->hours +=  this->minutes / 60;
        this->minutes %= 60;
    }
    MyTime(int h, int m): hours(h), minutes(m)
    {
        std::cout << "Constructor MyTime(int,int)" << std::endl;
    }
    
    //implicit conversion
    operator int() const
    {
        std::cout << "operator int()" << std::endl;
        return this->hours * 60 + this->minutes;
    }
    //explicit conversion
    explicit operator float() const
    {
        std::cout << "explicit operator float()" << std::endl;
        return float(this->hours * 60 + this->minutes);
    }

    MyTime & operator=(int m)
    {
        std::cout << "operator=(int)" << std::endl;
        this->hours = 0;
        this->minutes = m;
        this->hours =  this->minutes / 60;
        this->minutes %= 60;
        return *this;
    }

    friend std::ostream & operator<<(std::ostream & os, const MyTime & t)
    {
        std::string str = std::to_string(t.hours) + " hours and " 
                        + std::to_string(t.minutes) + " minutes.";
        os << str;
        return os;
    }
};
```