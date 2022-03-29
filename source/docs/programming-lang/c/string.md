# 字符串结束符的处理方式

```{code-block} c
#include <stdio.h>
#include <string.h>

int main()
{
    char str1[] = "math";
    char str2[] = "english";

    strncpy(str1, str2, 5);
    str1[5] = '\0';    // 手动加结束符，否则乱码。

    printf("%s\n", str1);

    return 0;
}
```
