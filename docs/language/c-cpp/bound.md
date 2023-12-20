# 指针访问越界

```cpp
#include <iostream>

using namespace std;

int main()
{
    int a;
    int num = 0;
    int *p = &num;

    p[-1] = 2;    // out of bound
    p[0] = 3;     // okay
    *(p + 1) = 4; // out of bound

    cout << "num = " << num << endl;

    return 0;
}
```

## (ntdll.dll) 处有未经处理的异常: 堆已损坏

出现这个问题，我一开始一直以为是由于堆栈溢出，尝试修改 Visual Studio 的预留空间大小，无效。

后面又以为是因为指针引用错误，于是将一些变量的作用域稍微做了修改，无效。

堆栈溢出，内存不够用的思路一直在脑海中，其实起到了误导作用。
但是最终的结果确实是因为指针操作了非法空间，而造成这种结局的罪魁祸首：
不是因为在循环中大量重复引用相同的变量，而是由于没有给字符串添加结束符 `'\0'` 又使用了
`strlen()` 方法。

这个问题的调试，其实是挺难的。因为 Visual Studio
并没有在指定的出问题的行出发软中断，而是在其他位置，导致问题的定位很难。
