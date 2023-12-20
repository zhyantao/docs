# const_cast

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
