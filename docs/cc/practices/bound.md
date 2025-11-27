# 指针访问越界

```cpp
#include <iostream>

using namespace std;

int main() {
    int a;
    int num = 0;
    int* p = &num;

    p[-1] = 2;    // out of bound
    p[0] = 3;     // okay
    *(p + 1) = 4; // out of bound

    cout << "num = " << num << endl;

    return 0;
}
```

## ntdll.dll 处有未经处理的异常: 堆已损坏

这是一个运行时错误，编译通过完全没问题，而且 Visual Studio 运行崩溃时，指向的错误位置每次都不同，导致定位原因很难。

- [&#10007;] 一开始一直以为是由于堆栈溢出，尝试修改 Visual Studio 的预留空间大小，无效。
- [&#10007;] 怀疑是指针访问越界（野指针），于是将一些变量的作用域稍微做了修改，无效。
- [&#10003;] 没有给字符串添加结束符 `'\0'` 又使用了 `strlen()` 方法（野指针），修改有效。

这些问题都是由于没有良好的编码习惯，不会顺手给字符数组加结尾符号，导致调试错误比写代码的时间还要长。
