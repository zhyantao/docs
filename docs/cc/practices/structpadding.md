# 字节对齐

```cpp
#include <iostream>

using namespace std;

struct Student1 {
    int id;
    bool male;
    char label;
    float weight;
};

struct Student2 {
    int id;
    bool male;
    float weight;
    char label;
};

int main() {
    cout << "Size of Student1: " << sizeof(Student1) << endl;
    cout << "Size of Student2: " << sizeof(Student2) << endl;
    return 0;
}
```

```cpp
#include <stdio.h>

struct book_bank {
    char title[15];  // 16
    char author[20]; // 20
    int paper;       // 4
    float price;     // 4
};

int main() {
    // 结构体成员按照各自类型的自然对齐要求排列：
    // char 数组共占 15 + 20 = 35 字节，int 和 float 各占 4 字节；
    // 结构体总大小需要对齐到最大成员的对齐值（4 字节）的整数倍，
    // 因此 43 字节会被填充到 44 字节
    // 字节对齐可能会导致空间浪费问题，可以通过设置位域来解决
    printf("%d\n", sizeof(struct book_bank)); // 44
    return 0;
}
```
