# 从键盘获取一行输入文本

```{code-block} c
#include <stdio.h>

int main()
{
    char c;
    c = ' ';
    while (c != '\n')
    {
        c = getchar();
        printf("%c %5d \n", c, c);
    }

    return 0;
}
```
