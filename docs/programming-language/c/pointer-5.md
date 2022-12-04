# 获取变量的物理地址

```{code-block} c
#include <stdio.h>

void main()
{
    char a;
    int x;
    float p, q;

    a = 'A';
    x = 125;
    p = 10.25, q = 18.76;

    printf("%p\n", &a);
    printf("%p\n", &x);
    printf("%p\n", &p);
    printf("%p\n", &q);

    return ;
}
```
