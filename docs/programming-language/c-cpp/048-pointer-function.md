# 指向函数的指针

```c
#include <stdio.h>

void f2(void (*f1)(), int n)
{
    (*f1)(n);
    return ;
}

void f3(int n)
{
    for(int i = 0; i <= n; ++i)
    {
        printf("I love China.\n");
    }
    return ;
}

int main()
{
    f2(f3, 10);
    return 0;
}
```
