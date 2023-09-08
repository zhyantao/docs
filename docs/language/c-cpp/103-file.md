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

## fstream 无法使用相对路径

尝试修改 Visual Stuido 中项目的 >> `属性` >> `调试` >> `工作目录`。
