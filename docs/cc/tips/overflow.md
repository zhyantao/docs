# 整数溢出

在较旧的 C 语言标准中，如果函数在调用之前没有被声明，编译器会假定这个函数返回一个 `int` 类型的值。这种情况通常发生在函数定义或声明在调用之后，或者根本没有进行显式的函数声明的时候。

```cpp
// libbignum.so
long test_bignum() {
    return 366969859824;
}
```

```cpp
// int test_bignum(); // warning: implicit declaration of function

int main(int argc, char* argv[]) {
    long num = test_bignum();
    printf("num = %ld (%lx)\n", num, num); // 隐式声明将导致数据高位丢失
    return 0;
}
```
