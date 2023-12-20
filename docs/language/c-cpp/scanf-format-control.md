# 输入格式控制

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
