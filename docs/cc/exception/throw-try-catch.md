# throw-try-catch

## 被调用者捕获的异常

```cpp
#include <cfloat>
#include <cstdlib>
#include <iostream>

float ratio(float a, float b) {
    if (a < 0)
        throw 1;
    if (b < 0)
        throw 2;
    if (fabs(a + b) < FLT_EPSILON)
        throw "The sum of the two arguments is close to zero.";

    return (a - b) / (a + b);
}

float ratio_wrapper(float a, float b) {
    try {
        return ratio(a, b);
    } catch (int eid) {
        if (eid == 1)
            std::cerr << "Call ratio() failed: the 1st argument should be positive." << std::endl;
        else if (eid == 2)
            std::cerr << "Call ratio() failed: the 2nd argument should be positive." << std::endl;
        else
            std::cerr << "Call ratio() failed: unrecognized error code." << std::endl;
    }
    return 0;
}

int main() {
    float x = 0.f;
    float y = 0.f;
    float z = 0.f;

    std::cout << "Please input two numbers <q to quit>:";
    while (std::cin >> x >> y) {
        try {
            z = ratio_wrapper(x, y);
            std::cout << "ratio(" << x << ", " << y << ") = " << z << std::endl;
        } catch (const char* msg) {
            std::cerr << "Call ratio() failed: " << msg << std::endl;
            std::cerr << "I give you another chance." << std::endl;
        }

        std::cout << "Please input two numbers <q to quit>:";
    }
    std::cout << "Bye!" << std::endl;
    return 0;
}
```

## 被子类捕获的异常

```cpp
#include <iostream>

class Base {
public:
    Base() {
    }
};

class Derived : public Base {
public:
    Derived() {
    }
};

int main() {
    try {
        throw Derived();
    } catch (const Base& base) {
        std::cerr << "I caught Base." << std::endl;
    } catch (const Derived& derived) { // never reach here
        std::cerr << "I caught Derived." << std::endl;
    }

    return 0;
}
```

## catch(...)

```cpp
#include <iostream>
#include <stdexcept>

// 自定义异常类
class except1 : public std::exception {
public:
    const char* what() const noexcept override {
        return "Exception 1";
    }
};

class except2 : public std::exception {
public:
    const char* what() const noexcept override {
        return "Exception 2";
    }
};

void func(int arg) {
    try {
        if (arg == 1) {
            throw except1();
        } else if (arg == 2) {
            throw except2();
        } else {
            throw std::runtime_error("Unknown exception");
        }
    } catch (except1& e1) {
        std::cerr << "Caught exception: " << e1.what() << std::endl;
    } catch (except2& e2) {
        std::cerr << "Caught exception: " << e2.what() << std::endl;
    } catch (...) // 接受所有异常
    {
        std::cerr << "Caught unknown exception" << std::endl;
    }
}

int main() {
    try {
        func(1);
        func(2);
        func(3);
    } catch (const std::exception& e) {
        std::cerr << "Caught exception in main: " << e.what() << std::endl;
    }

    return 0;
}
```
