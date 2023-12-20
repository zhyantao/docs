# 空格不可作为 scanf 的结尾

```{code-block} c
#include <stdio.h>

int main()
{
    int a;
    scanf("%d ", &a); // 不要将空格作为scanf的结尾，会导致一些意想不到的效果。
    printf("%d\n", a);
    return 0;
}
```
