# 函数的数组传递

```{code-block} c
#include <stdio.h>

void findlargest(int arr[], int n)
{
    int max = arr[0];
    for(int i = 0; i < n; i++)
    {
        if(arr[i] > max)
            max = arr[i];
    }
    printf("The largest number is %d\n", max);
    return;
}

int main()
{
    int arr[] = {1, 120, 4, 2, 20, 99, 8, 3};
    findlargest(arr, sizeof(arr)/sizeof(arr[0]));
    return 0;
}
```
