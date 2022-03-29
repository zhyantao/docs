# 函数的值传递

```{code-block} c
#include <stdio.h>

void sum(int a, int b)
{
    int s = a + b;
    printf("sum = %d\n", s);
    return;
}

int main(int argc, char* argv[])
{
    sum(1.0, 2.5);
    return 0;
}
```
