# 一级指针和二级指针

```{code-block} c
#include <stdio.h>

int main()
{
    float a = 81.3;
    float *p = &a;
    float **q = &p;

    printf("%f %f\n", *p, **q);

    return 0;
}
```
