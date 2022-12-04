# 浮点数的精度问题

```{code-block} c
#include <stdio.h>

int main()
{
    float a = 1.0 / 3.0;
    float b = a * 3.0;
    printf("%d\n", b);    // 由于精度问题会导致得不到想要的结果
    return 0;
}
```
