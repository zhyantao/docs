# extern

```{code-block} c
#include <stdio.h>

extern int a;
void changea();

int main()
{
    changea();
    printf("%d\n", a);
    return 0;
}
```
