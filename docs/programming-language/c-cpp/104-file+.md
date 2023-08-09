# 从指定位置读写文件

```{code-block} c
#include <stdio.h>

int main()
{
    char c;
    FILE *fp = NULL;

    // 读文件
    fp = fopen("INPUT", "r");

    int ret = fseek(fp, 28, 0);    // 把文件指针放到指定位置
    printf("Return value of fseek(): %d\nPosition of pointer* fp: %d\n\n", ret, ftell(fp));

    while((c = getc(fp)) != EOF)
    {
        printf("%c", c);
    }
    fclose(fp);
    printf("\n");

    return 0;
}
```
