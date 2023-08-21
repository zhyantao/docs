# 多维数组

```cpp
#include <iostream>
using namespace std;

// You must tell the function the bound of an array,
// otherwise, elements cannot be accessed
// if the array is a variable-length one, it may be difficult to know the bound
void init_2d_array(float mat[][4], //error, arrays of unknown bound
                    size_t rows, size_t cols)
{
    for (int r = 0; r < rows; r++)
        for(int c = 0; c < cols; c++)
            mat[r][c] =  r * c;
}

int main()
{
    int mat1[2][3] = {
        {11,12,13},
        {14,15,16}
    };

    int rows = 5;
    int cols = 4;
    //float mat2[rows][cols]; //uninitialized array
    float mat2[rows][4]; //uninitialized array

    //init_2d_array(mat2, rows, cols);

    for (int r = 0; r < rows; r++)
        for(int c = 0; c < cols; c++)
            mat2[r][c] =  r * c;


    for (int r = 0; r < rows; r++)
    {
        for(int c = 0; c < cols; c++)
            cout << mat2[r][c] << " ";
        cout << endl;
    }
    return 0;
}
```


```c
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