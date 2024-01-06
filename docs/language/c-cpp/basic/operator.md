# operator

## operator+ 和 operator+=

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

## operator++

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

## operator+int

```cpp
// main.cpp

#include <iostream>
#include "time.hpp"

using namespace std;

int main()
{
    MyTime t1(2, 40);
    std::cout << (30 + t1).getTime() << std::endl;

    std::cout << t1 << std::endl;
    std::cout << "Please input two integers:" << std::endl;
    std::cin >> t1;
    std::cout << t1 << std::endl;

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

    friend MyTime operator+(int m, const MyTime &t)
    {
        return t + m;
    }

    std::string getTime() const
    {
        return std::to_string(this->hours) + " hours and " + std::to_string(this->minutes) + " minutes.";
    }

    friend std::ostream &operator<<(std::ostream &os, const MyTime &t)
    {
        std::string str = std::to_string(t.hours) + " hours and " + std::to_string(t.minutes) + " minutes.";
        os << str;
        return os;
    }

    friend std::istream &operator>>(std::istream &is, MyTime &t)
    {
        is >> t.hours >> t.minutes;
        t.hours += t.minutes / 60;
        t.minutes %= 60;
        return is;
    }
};
```

## operator+std::string

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

## operator int() 和 operator<<

```cpp
// main.cpp

#include <iostream>
#include "time.hpp"

using namespace std;

int main()
{
    MyTime t1(1, 20);
    int minutes = t1;    // implicit conversion
    float f = float(t1); // explicit conversion.
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

    // implicit conversion
    operator int() const
    {
        std::cout << "operator int()" << std::endl;
        return this->hours * 60 + this->minutes;
    }

    // explicit conversion
    explicit operator float() const
    {
        std::cout << "explicit operator float()" << std::endl;
        return float(this->hours * 60 + this->minutes);
    }

    MyTime &operator=(int m)
    {
        std::cout << "operator=(int)" << std::endl;
        this->hours = 0;
        this->minutes = m;
        this->hours = this->minutes / 60;
        this->minutes %= 60;
        return *this;
    }

    friend std::ostream &operator<<(std::ostream &os, const MyTime &t)
    {
        std::string str = std::to_string(t.hours) + " hours and " + std::to_string(t.minutes) + " minutes.";
        os << str;
        return os;
    }
};
```
