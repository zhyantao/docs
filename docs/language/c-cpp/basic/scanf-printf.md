# scanf-printf

## 输入和输出截断

```{code-block} c
#include <stdio.h>

int main()
{
    int a, b, c, x, y, z;
    int p, q, r;

    printf("Enter 3 1b number\n");
    scanf("%d %*d %d", &a, &b, &c);
    printf("%d %d %d \n\n", a, b, c);

    printf("Enter 2 4b number\n");
    scanf("%2d %4d", &x, &y);
    printf("%d %d\n\n", x, y);

    printf("Enter 2 2b number\n");
    scanf("%d %d", &a, &x);
    printf("%d %d \n\n", a, x);

    printf("Enter 1 9b number\n");
    scanf("%3d %4d %3d", &p, &q, &r);
    printf("%d %d %d \n\n", p, q, r);

    printf("Enter 2 3b number\n");
    scanf("%d %d", &x, &y);
    printf("%d %d \n\n", x, y);

    return 0;
}
```

## 空格不可作为 scanf 的结尾

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

## 输入格式控制

```{code-block} c
#include <stdio.h>

int main()
{
    int num1, num2, num3;
    scanf("%d %d %d", &num1, &num2, &num3);
    printf("Number 1 is %d\n", num1);
    printf("Number 2 is %d\n", num2);
    printf("Number 3 is %d\n", num3);
    return 0;
}
```

```{code-block} c
#include <stdio.h>

int main()
{
    char address[80];

    printf("Enter address \n");
    scanf("%[^\n]", address);
    printf("%-80s \n\n", address);
}
```

## 输出格式控制

## printf

```{code-block} c
#include <stdio.h>

int main()
{
    // 字符串
    char country[15] = "United Kingdom"; // 有效字符为 14 个（末尾 '\0' 也占一个字节）
    printf("%s\n", country);
    printf("%15s\n", country);    // 占宽 15，右对齐 (不再考虑末尾的 '\0')
    printf("%5s\n", country);     // 指定长度小于字符串长度，5 被忽略。
    printf("%15.6s\n", country);  // 占宽 15，显示 6 字符，右对齐
    printf("%-15.6s\n", country); // 左对齐（因为有 '-'）
    printf("%15.0s\n", country);  // 显示 0 字符
    printf("%.3s\n", country);    // 显示 3 个字符（没有占宽，默认左对齐）

    // 浮点数
    printf("%f\n", 13.0);
    printf("%lf\n", 13.0);
    printf("%10f\n", 13.0);

    // 整数和字符数组（示例程序）
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

## 格式化指示符

| 说明符     | 数据类型       | 描述                                                         |
| ---------- | -------------- | ------------------------------------------------------------ |
| `%d/%i`    | `int`          | 输出类型为有符号的十进制整数，`i` 是老式写法                 |
| `%o`       | `unsigned int` | 输出类型为无符号八进制整数（没有前导 `0`）                   |
| `%u`       | `unsigned int` | 输出类型为无符号十进制整数                                   |
| `%x`/`%X`  | `unsigned int` | 输出类型为无符号十六进制整数，`x` 对应的是 abcdef，`X` 对应的是 ABCDEF（没有前导 `0x` 或者 `0X`） |
| `%f`/`%lf` | `double`       | 输出类型为十进制表示的浮点数，默认精度为 6（`lf` 在 C99 开始加入标准，意思和 `f` 相同） |
| `%e`/`%E`  | `double`       | 输出类型为科学计数法表示的数，此处 `e` 的大小写代表在输出时用的 `e` 的大小写，默认浮点数精度为 6 |
| `%g`       | `double`       | 根据数值不同自动选择 `%f` 或 `%e`，`%e` 格式在指数小于 -4 或指数大于等于精度时用使用 |
| `%G`       | `double`       | 根据数值不同自动选择 `%f` 或 `%E`，`%E` 格式在指数小于 -4 或指数大于等于精度时用使用 |
| `%c`       | `char`         | 输出类型为字符型。可以把输入的数字按照 ASCII 码相应转换为对应的字符 |
| `%s`       | `char *`       | 输出类型为字符串。输出字符串中的字符直至遇到字符串中的空字符（字符串以 `\0` 结尾，这个 `\0` 即空字符）或者已打印了由精度指定的字符数 |
| `%p`       | `void *`       | 以 16 进制形式输出指针                                       |
| `%%`       | 不转换参数     | 不进行转换，输出字符 `%`（百分号）本身                       |
| `%n`       | `int *`        | 到此字符之前为止，一共输出的字符个数，不输出文本             |


## getchar()

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

    while (1)
    {
        /* 读取一行文本 */
        c = 0;
        while ((ctr = getchar()) != '\n')
            line[c++] = ctr;
        line[c] = '\0';

        /* 计算一行中的字数 */
        if (line[0] == '\0')
            break;
        else
        {
            words++;
            for (i = 0; line[i] != '\0'; i++)
                if (line[i] == ' ' || line[i] == '\t')
                    words++;
        }

        /* 计算行数和字符数 */
        lines = lines + 1;
        characters = characters + strlen(line);
    }

    printf("\n");
    printf("Number of lines = %d\n", lines);
    printf("Number of words = %d\n", words);
    printf("Number of characters = %d\n", characters);

    return 0;
}
```

## 从键盘获取一行输入文本

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
