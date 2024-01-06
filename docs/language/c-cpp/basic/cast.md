# cast

## 普通类型转换

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

## const_cast

C 语言中的强制类型转化，在编译器看来，这并没有什么问题，也不会去做检查。这样的话，会产生问题，举个例子来讲：在强制类型转换之前，允许操作的空间是 4 个字节，在强制类型转换之后，它允许操作的空间是 8 字节，那么这样的话，就操作了不应该操作的空间。

为此，C++ 引入了更加安全的类型转换运算符，分别是 `const_cast`、`static_cast`、`reinterpret_cast` 等。

```cpp
#include <iostream>

using namespace std;

int main()
{
    int value1 = 100;
    const int value2 = 200;
    cout << "value1 = " << value1 << endl;
    cout << "value2 = " << value2 << endl;

    // int *pv1 = &value1;
    int *pv1 = const_cast<int *>(&value1);
    // int *pv2 = &value2; // error
    int *pv2 = const_cast<int *>(&value2);

    (*pv1)++;
    (*pv2)++; // 允许编译通过，但是 value2 并没有自增

    cout << "value1 = " << (*pv1) << endl;
    cout << "value2 = " << (value2) << endl;

    // int &v2 = value2; // error
    int &v2 = const_cast<int &>(value2);
    v2++;
    cout << "value2 = " << value2 << endl;

    cout << "*pv2 = " << (*pv2) << endl;
    cout << "v2 = " << v2 << endl;

    return 0;
}
```

## reinterpret_cast

```cpp
#include <iostream>

using namespace std;

int main()
{
    int i = 18;
    float *p1 = reinterpret_cast<float *>(i); // static_cast will fail
    int *p2 = reinterpret_cast<int *>(p1);

    printf("p1=%p\n", p1);
    printf("p2=%p\n", p2);

    return 0;
}
```