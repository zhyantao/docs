# 字符的大小写转换

```{code-block} c
#include <stdio.h>

int main()
{
    char c;
    c = getchar();
    if(islower(c))
        putchar(toupper(c));
    else
        putchar(tolower(c));
    putchar('\n');

    return 0;
}
```
