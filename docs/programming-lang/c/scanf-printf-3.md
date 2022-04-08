# 输入和输出截断

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
