# 函数的址传递

```{code-block} c
#include <stdio.h>

void sort(int arr[], int n);
void printarr(int arr[], int n);

int main()
{
    int arr[] = {10, 39, 48, 23, 88, 0, -1, 38, -39};
    sort(arr, sizeof(arr)/sizeof(arr[0]));
    return 0;
}

void sort(int arr[], int n)
{
    for(int i = n - 1; i > 0; --i)        // 固定最后一个元素，最后元素始终保留最大的数字
        for(int j = 0; j < i; j++)    // 如果他前面的元素比它大，则交换元素
        {
            if(arr[i] < arr[j])
            {
                int tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
            }
        }
    printarr(arr, n);
    return ;
}

void printarr(int arr[], int n)
{
    printf("冒泡排序：\n");
    for(int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
    return ;
}
```
