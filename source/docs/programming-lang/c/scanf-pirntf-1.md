# 输出格式控制

```{code-block} c
#include <stdio.h>

int main()
{

    char country[15] = "United Kingdom";    // 14个字符（除末尾'\0'）
    printf("%s\n", country);                // 末尾有个'\0'没有显示
    printf("----------------\n");

    printf("%15s\n", country);              // 占宽15，右对齐 (不再考虑末尾的'\0')
    printf("%5s\n", country);               // 指定长度小于字符串长度，5 被忽略。
    printf("%15.6s\n", country);            // 占宽15，显示6字符，右对齐
    printf("%-15.6s\n", country);           // 左对齐（因为有'-'）
    printf("%15.0s\n", country);            // 显示0字符
    printf("%.3s\n", country);              // 显示3个字符（没有占宽，默认左对齐）

    return 0;
}
```

```{code-block} c
#include <stdio.h>

int main()
{
    printf("%f\n", 13.0);
    printf("%lf\n", 13.0);
    printf("%10f\n", 13.0);
    return 0;
}
```

```{code-block} c
#include <stdio.h>

int main()
{
    int no;
    char name1[15], name2[15], name3[15];

    printf("Enter no and name1:\n");
    scanf("%d %15c", &no, name1);
    printf("%d %15s \n\n", no, name1);

    printf("Enter no and name2:\n");
    scanf("%d %s", &no, name2);
    printf("%d %15s \n\n", no, name2);

    printf("Enter no and name3:\n");
    scanf("%d %15s", &no, name3);
    printf("%d %15s \n\n", no, name3);

    return 0;
}
```
