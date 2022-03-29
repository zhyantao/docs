# 自动类型转换

```{code-block} c
#include <stdio.h>

int main()
{
    int         i, x;
    float       f;
    double      d;
    long int    l;

    i = 10;
    f = 3.0;
    d = 20.0;
    l = 20;
    x = 1 / l + i * f - d;
    printf("%d", sizeof(x));

    return 0;
}
```
