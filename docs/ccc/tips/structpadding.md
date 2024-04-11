# 字节对齐

```cpp
#include <iostream>

using namespace std;

struct Student1
{
    int id;
    bool male;
    char label;
    float weight;
};

struct Student2
{
    int id;
    bool male;
    float weight;
    char label;
};

int main()
{
    cout << "Size of Student1: " << sizeof(Student1) << endl;
    cout << "Size of Student2: " << sizeof(Student2) << endl;
    return 0;
}
```


```c
#include <stdio.h>

struct book_bank
{
    char title[15];  // 16
    char author[20]; // 20
    int paper;       // 4
    float price;     // 4
};

int main()
{
    // 字节对齐，结果为 4 的倍数
    // 因为 C 语言默认是以 16 个二进制位存储一个数据
    // 字节对齐可能会导致空间浪费问题，可以通过设置位域来解决
    printf("%d\n", sizeof(struct book_bank)); // 44
    return 0;
}
```
