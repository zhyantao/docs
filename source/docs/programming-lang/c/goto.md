# 避免使用 goto 语句

```{code-block} c
#include <stdio.h>
#include <math.h>

int main()
{
    double x, y;
read:
    scanf("%f", &x);
    if(x < 0)
        goto read;
    y = sqrt(x);
    printf("%lf %lf\n", x, y);
    goto read;

    return 0;
}
```
