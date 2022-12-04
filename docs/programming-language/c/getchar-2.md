# 处理键盘输入的一行文本

```{code-block} c
#include <stdio.h>
#include <string.h>

int main()
{
    char line[81], ctr;
    int i, c,
        characters = 0,
        words = 0,
        lines = 0;

    printf("Give one sapce after each word.\n");
    printf("When completed, press 'Enter'.\n\n");

    while(1)
    {
        /* 读取一行文本 */
        c = 0;
        while((ctr = getchar()) != '\n')
            line[c++] = ctr;
        line[c] = '\0';

        /* 计算一行中的字数 */
        if(line[0] == '\0')
            break;
        else
        {
            words++;
            for(i = 0; line[i] != '\0'; i++)
                if(line[i] == ' ' || line[i] == '\t')
                    words++;
        }

        /* 计算行数和字符数 */
        lines= lines + 1;
        characters = characters + strlen(line);
    }

    printf("\n");
    printf("Number of lines = %d\n", lines);
    printf("Number of words = %d\n", words);
    printf("Number of characters = %d\n", characters);

    return 0;
}
```
