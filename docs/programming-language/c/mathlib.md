# 数学函数库的使用

```{code-block} c
#include <stdio.h>
#include <math.h>
#define LAMDA 0.001

/******************* Notice **************/
/*               gcc 4_13.c -lm          */
/* lm means linked with /usr/lib/libm.so */
/*****************************************/

int main()
{
    double    t;
    float    r;
    int    i, R;

    for(i = 1; i <= 27; i ++)
        printf("--");
    printf("\n");

    for(t = 0; t <= 3000; t += 150)
    {
        r = exp(-LAMDA * t);
        R = (int)(50 * r + 0.5);

        printf(" | ");
        for(i = 1; i <= R; i++)
            printf("*");
        printf("#\n");
    }

    for(i = 1; i < 3; i++)
        printf(" |\n");

    return 0;
}
```
