# 硬拷贝

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

    MyString(const MyString& ms) {
        std::cout << "Constructor(MyString&)" << std::endl;
        this->buf_len = 0;
        this->characters = NULL;
        create(ms.buf_len, ms.characters);
    }

    ~MyString() {
        release();
    }

    MyString& operator=(const MyString& ms) {
        create(ms.buf_len, ms.characters);
        return *this;
    }

    bool create(int buf_len, const char* data) {
        release();

        this->buf_len = buf_len;

        if (this->buf_len != 0) {
            this->characters = new char[this->buf_len]{};
        }
        if (data)
            strncpy(this->characters, data, this->buf_len);

        return true;
    }

    bool release() {
        this->buf_len = 0;
        if (this->characters != NULL) {
            delete[] this->characters;
            this->characters = NULL;
        }
        return 0;
    }

    friend std::ostream& operator<<(std::ostream& os, const MyString& ms) {
        os << "buf_len = " << ms.buf_len;
        os << ", characters = " << static_cast<void*>(ms.characters);
        os << " [" << ms.characters << "]";
        return os;
    }
};
```
