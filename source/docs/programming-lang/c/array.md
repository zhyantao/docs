# 定义和使用二维数组

```{code-block} c
#include <stdio.h>

int main()
{
    char city[][10] = {    // 数组必须有第二个列数
        "Beijing",
        "Shenzhen",
        "Shanghai",
        "Guangzhou"
    };    // 不要忘记末尾的分号

    for(int i = 0; i < sizeof(city)/sizeof(city[0]); i++)
    {
        printf("%s\n", city[i]);
    }

    // 二维数组最后也是有0的。
    return 0;
}
```
