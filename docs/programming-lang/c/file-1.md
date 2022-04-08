# 普通文件读写

```{code-block} c
#include <stdio.h>

int main()
{
    char c;
    FILE *fp = NULL;
    
    // 写文件
    fp = fopen("INPUT", "w");
    while((c = getchar()) != '\n')
    {
        putc(c, fp);
    }
    fclose(fp);

    // 读文件
    fp = fopen("INPUT", "r");
    while((c = getc(fp)) != EOF)
    {
        printf("%c", c);
    }
    fclose(fp);
    printf("\n");

    return 0;
}
```
