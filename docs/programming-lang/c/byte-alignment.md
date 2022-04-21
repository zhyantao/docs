# 结构体和字节对齐

```{code-block} c
#include <stdio.h>

struct book_bank
{
    char title[15];
    char author[20];
    int paper;
    float price;
};

int main()
{
    // 字节对齐，结果为 4 的倍数
    // 因为 C 语言默认是以 16 个二进制位存储一个数据
    // 字节对齐可能会导致空间浪费问题，可以通过设置位域来解决
    printf("%d\n", sizeof(struct book_bank));    // 44
    return 0;
}
```
