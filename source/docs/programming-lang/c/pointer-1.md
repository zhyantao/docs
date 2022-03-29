# 指向普通变量的指针

```{code-block} c
#include <stdio.h>

int main()
{
    float a, b;
    int x, *p;
    p = &a;
    b = *p;

    return 0;
}
```
