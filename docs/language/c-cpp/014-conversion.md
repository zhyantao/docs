# 类型转换

```cpp
#include <iostream>

using namespace std;

int main()
{
    int num_int1 = 9;        // assigning an int value to num_int1
    int num_int2 = 'C';      // implicit conversion
    int num_int3 = (int)'C'; // explicit conversion, C-style
    int num_int4 = int('C'); // explicit conversion, function style
    int num_int5 = 2.8;      // implicit conversion
    float num_float = 2.3;   // implicit conversion from double to float, may loss precision
    short num_short = 650000;

    cout << "num_short = " << num_short << endl;

    return 0;
}
```

```c
#include <stdio.h>

int main()
{
    int i, x;
    float f;
    double d;
    long int l;

    i = 10;
    f = 3.0;
    d = 20.0;
    l = 20;
    x = 1 / l + i * f - d;
    printf("%d", sizeof(x));

    return 0;
}
```