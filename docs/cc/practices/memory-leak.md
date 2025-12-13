# 内存泄漏

造成内存泄漏的原因本质上只有一个：手动申请的内存没有释放。体现在代码中，可以细分为下面几条：

1. 使用了 `malloc` 函数，忘记了 `free`。
2. 使用了 `new` 函数，忘记了 `delete`。
3. 用一个指针指向了手动申请的一块内存，但是后面修改了指针的指向，导致找不到原来指向的内存空间，无法释放那块内存。

---

```cpp
#include <stdio.h>
#include <stdlib.h>

void foo() {
    int* p = (int*)malloc(sizeof(int));
    return;
} // memory leak

int main() {
    int* p = NULL;

    p = (int*)malloc(4 * sizeof(int));
    // some statements
    p = (int*)malloc(8 * sizeof(int));
    // some statements
    free(p);
    // the first memory will not be freed

    for (int i = 0; i < 1024; i++) {
        p = (int*)malloc(1024 * 1024 * 1024);
    }
    printf("End\n");

    return 0;
}
```

---

```cpp
// main.cpp

#include "mystring.hpp"
#include <iostream>

using namespace std;

// Why memory leak and memory double free?
int main() {
    MyString str1(10, "Shenzhen");
    cout << "str1: " << str1 << endl;

    MyString str2 = str1;
    cout << "str2: " << str2 << endl;

    MyString str3;
    cout << "str3: " << str3 << endl;
    str3 = str1;
    cout << "str3: " << str3 << endl;

    return 0;
}
```

```cpp
// mystring.hpp

#pragma once

#include <cstring>
#include <iostream>

class MyString {
private:
    int buf_len;
    char* characters;

public:
    MyString(int buf_len = 64, const char* data = NULL) {
        std::cout << "Constructor(int, char*)" << std::endl;
        this->buf_len = 0;
        this->characters = NULL;
        create(buf_len, data);
    }

    ~MyString() { delete[] this->characters; }

    bool create(int buf_len, const char* data) {
        this->buf_len = buf_len;

        if (this->buf_len != 0) {
            this->characters = new char[this->buf_len]{};
            if (data) strncpy(this->characters, data, this->buf_len);
        }

        return true;
    }

    friend std::ostream& operator<<(std::ostream& os, const MyString& ms) {
        os << "buf_len = " << ms.buf_len;
        os << ", characters = " << static_cast<void*>(ms.characters);
        os << " [" << ms.characters << "]";
        return os;
    }
};
```
