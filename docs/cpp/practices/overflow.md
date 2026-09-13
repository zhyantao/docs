# 隐式函数声明导致返回值截断

在较旧的 C 语言标准（C89/C90）中，如果函数在调用之前没有被声明，编译器会假定这个函数返回一个 `int` 类型的值。这种情况通常发生在函数定义或声明在调用之后，或者根本没有进行显式的函数声明的时候。而在 C99 及之后的标准中，隐式函数声明已经被移除，编译器会直接报错。

```cpp
// libbignum.so
long test_bignum() {
    return 366969859824;
}
```

```cpp
#include <stdio.h>

// 应该在这里加上声明：long test_bignum();
// 否则编译器按 int 类型处理返回值，导致数据高位丢失

int main(int argc, char* argv[]) {
    long num = test_bignum();
    printf("num = %ld (%lx)\n", num, num); // 隐式声明将导致数据高位丢失
    return 0;
}
```
