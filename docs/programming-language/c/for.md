# 使用逗号运算符的 for 循环

```{code-block} c
#include <stdio.h>

int main()
{
    for(int n = 10, m = 20; n <= m; ++n, --m)
    {
        printf("%d ", n);
    }
    printf("\n");
    return 0;
}
```
