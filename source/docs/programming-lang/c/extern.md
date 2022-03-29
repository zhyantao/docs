# 外部变量和全局函数

```{code-block} c
#include <stdio.h>

extern int a;
void changea();

int main()
{
    changea();
    printf("%d\n", a);
    return 0;
}
```
