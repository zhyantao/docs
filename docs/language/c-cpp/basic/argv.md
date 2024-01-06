# argv

## 命令行传参

```cpp
#include <getopt.h>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    /**
     * struct option
     * {
     *      const char * name;
     *      int          has_arg;
     *      int        * flag;
     *      int          val;
     * }
     */
    static struct option long_options[] = {
        {"reqarg", required_argument, NULL, 'r'},
        {"optarg", optional_argument, NULL, 'o'},
        {"noarg", no_argument, NULL, 'n'},
        {NULL, 0, NULL, 0},
    };

    while (1)
    {
        int option_index = 0, opt;

        /**
         * getopt_long 会遍历 argv 数组，在每次迭代中，它会返回下一个选项字符（如果有），
         * 然后，这个字符与长选项列表进行比较，如果匹配，则对应的操作会被执行，如果没有匹配，那么函数将返回 -1。
         * 只有一个字符，不带冒号，只表示选项，如 -c
         * 一个字符，后接一个冒号，表示选项后面带一个参数，如 -a 100
         * 一个字符，后接两个冒号——表示选项后面带一个可选参数，即参数可有可无，如果带参数，则选项与参数直接不能有空格，如 -b200
         */
        opt = getopt_long(argc, argv, "a::b:c:d", long_options, &option_index);

        if (opt == -1)
            break;

        printf("opt = %c\t\t", opt);
        printf("optarg = %s\t\t", optarg);
        printf("optind = %d\t\t", optind);
        printf("argv[%d] = %s\t\t", optind, argv[optind]);
        printf("option_index = %d\n", option_index);
    }

    return 0;
}
// g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out --reqarg 100 --optarg=200 --noarg
// g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out –reqarg=100 --optarg=200 --noarg
// g++ -std=c++20 -O2 -Wall -pedantic -pthread main.cpp && ./a.out --reqarg 100 --optarg --noarg
```

## 可变数量的形参

在 C/C++ 的高级语法中，我们会经常看到 `...` 这个符号，它通常表示了可变数量的参数。下面是一个简单的示例程序：

```c
#include <stdarg.h> // for va_list
#include <stdio.h>

double sum(int num, ...)
{
    va_list valist; // 创建参数列表
    double ret = 0.0;
    int i = 0;

    va_start(valist, num); // 初始化参数列表

    for (int i = 0; i < num; i++)
    {
        ret += va_arg(valist, double); // 访问参数列表中的项
    }

    va_end(valist); // 清理参数列表占用的内存

    return ret;
}

int main()
{
    printf("Sum of 2, 3 is %f\n", sum(2, 2, 3));
    printf("Sum of 2, 3, 4, 5 is %f\n", sum(4, 2, 3, 4, 5));
}
```

本节主要介绍不同的场景下，`...` 的含义分别是什么，如下：

- 用在函数模板中，表示接受可变参数的形参（函数形参包）；
- 用在类模板中，表示接受可变参数的类类型（模板形参包）；
- 用在 Variadic 宏中，表示接受可变参数的替换列表；
- `catch(...)` 表示可以捕获任何类型的异常，但是这样做**不安全**；
- 用在 Lambda 表达式中，表示捕获可变数量的引用；
- 用在 `sizeof` 运算符中，表示依次调用 `sizeof`；

## 包展开

作为预备知识，我们需要了解包展开的规则，根据下面的这个例子去理解：

```cpp
template <class... Us>
void f(Us... pargs) {}

template <class... Ts>
void g(Ts... args)
{
    f(&args...); // “&args...” 是包展开
                 // “&args” 是它的模式
}

g(1, 0.2, "a"); // Ts... args 会展开成 int E1, double E2, const char* E3
                // &args... 会展开成 &E1, &E2, &E3
                // Us... 会展开成 int* E1, double* E2, const char** E3
```

## 变参函数模板

```cpp
template <typename... Ts>
void f(Ts...) {}
f('a', 1); // Ts... 会展开成 void f(char, int)

f(0.1);    // Ts... 会展开成 void f(double)

template <typename... Ts, int... N>
void g(Ts (&...arr)[N]) {}
int n[1];

g<const char, int>("a", n); // Ts (&...arr)[N] 会展开成
                            // const char (&)[2], int(&)[1]
```

## 变参类模板

```cpp
template <class A, class B, class... C>
void func(A arg1, B arg2, C... arg3)
{
    container<A, B, C...> t1; // 展开成 container<A, B, E1, E2, E3>
    container<C..., A, B> t2; // 展开成 container<E1, E2, E3, A, B>
    container<A, C..., B> t3; // 展开成 container<A, E1, E2, E3, B>
}
```

## Variadic 宏

```cpp
#define F(...) f(0 __VA_OPT__(, ) __VA_ARGS__)
#define G(X, ...) f(0, X __VA_OPT__(, ) __VA_ARGS__)
#define SDEF(sname, ...) S sname __VA_OPT__(= {__VA_ARGS__})
F(a, b, c)       // 替换为 f(0, a, b, c)
F()              // 替换为 f(0)
G(a, b, c)       // 替换为 f(0, a, b, c)
G(a, )           // 替换为 f(0, a)
G(a)             // 替换为 f(0, a)
SDEF(foo);       // 替换为 S foo;
SDEF(bar, 1, 2); // 替换为 S bar = { 1, 2 };

//__VA_ARGS__ 前的井号会给参数加上一个双引号
#define showlist(...) puts(#__VA_ARGS__)
showlist();            // 展开成 puts("")
showlist(1, "x", int); // 展开成 puts("1, \"x\", int")
```

```cpp
#include <iostream>

// 制造函数工厂并使用它
// __VA_ARGS__ 前的两个井号，表示在有形参时直接进行替换，没有形参时什么都不做
#define FUNCTION(name, a) \
    int fun_##name() { return a; }

FUNCTION(, 100)
FUNCTION(abcd, 12)
FUNCTION(fff, 2)
FUNCTION(qqq, 23)

#undef FUNCTION
#define FUNCTION 34
#define OUTPUT(a) std::cout << "output: " #a << '\n'

// 在后面的宏定义中使用之前的宏
#define WORD "Hello "
#define OUTER(...) WORD #__VA_ARGS__

int main()
{
    std::cout << "" << fun_() << '\n';
    std::cout << "abcd: " << fun_abcd() << '\n';
    std::cout << "fff: " << fun_fff() << '\n';
    std::cout << "qqq: " << fun_qqq() << '\n';
    std::cout << FUNCTION << '\n';
    OUTPUT(million); // 注意这里没有引号

    std::cout << OUTER(World) << '\n';
    std::cout << OUTER(WORD World) << '\n';
}

/**
 * 上面代码的输出如下：
 *
 * 100
 * abcd: 12
 * fff: 2
 * qqq: 23
 * 34
 * output: million
 * Hello World
 * Hello WORD World
 */
```

## catch 子句

```cpp
template <class... X>
void func(int arg) throw(X...)
{
    // ... 在不同情形下抛出不同的 X
    try
    {
    }
    catch (except1 &)
    {
    }
    catch (except2 &)
    {
    }
    catch (...)
    {
    } // 接受所有异常
}
```

## Lambda 引用捕获

```cpp
template <class... Args>
void f(Args... args)
{
    auto lm = [&, args...]
    {
        return g(args...);
    };

    lm();
}
```

## sizeof 运算符

```cpp
template <class... Types>
struct count
{
    static const std::size_t value = sizeof...(Types);
};
```

---

更多资料参考：

- <https://zh.cppreference.com/w/cpp/language/parameter_pack>
- <https://zh.cppreference.com/w/cpp/preprocessor/replace>


## 引用作为参数

```cpp
#include <iostream>
#include <float.h>

struct Matrix
{
    int rows;
    int cols;
    float *pData;
};

float matrix_max(const struct Matrix &mat)
{
    float max = FLT_MIN;
    // find max value of mat
    for (int r = 0; r < mat.rows; r++)
        for (int c = 0; c < mat.cols; c++)
        {
            float val = mat.pData[r * mat.cols + c];
            max = (max > val ? max : val);
        }
    return max;
}

int main()
{
    using namespace std;

    Matrix matA = {3, 4};
    matA.pData = new float[matA.rows * matA.cols]{1.f, 2.f, 3.f};

    Matrix matB = {4, 8};
    matB.pData = new float[matB.rows * matB.cols]{10.f, 20.f, 30.f};

    Matrix matC = {4, 2};
    matC.pData = new float[matC.rows * matC.cols]{100.f, 200.f, 300.f};

    // some operations on the matrices

    float maxa = matrix_max(matA);
    float maxb = matrix_max(matB);
    float maxc = matrix_max(matC);

    cout << "max(matA) = " << maxa << endl;
    cout << "max(matB) = " << maxb << endl;
    cout << "max(matC) = " << maxc << endl;

    delete[] matA.pData;
    delete[] matB.pData;
    delete[] matC.pData;

    return 0;
}
```

## 无类型参数

```cpp
#include <iostream>

using namespace std;

// Class Template
template <typename T, size_t rows, size_t cols>
class Mat
{
    T data[rows][cols];

public:
    Mat() {}
    //// the default copy constructor will copy each element of a static array member
    //// so we do not 'delete' the copy constructor
    //// the same with the assignment operator
    // Mat(const Mat&) = delete;
    // Mat& operator=(const Mat&) = delete;
    T getElement(size_t r, size_t c);
    bool setElement(size_t r, size_t c, T value);
};

template <typename T, size_t rows, size_t cols>
T Mat<T, rows, cols>::getElement(size_t r, size_t c)
{
    if (r >= rows || c >= cols)
    {
        cerr << "getElement(): indices are out of range" << endl;
        return 0;
    }
    return data[r][c];
}

template <typename T, size_t rows, size_t cols>
bool Mat<T, rows, cols>::setElement(size_t r, size_t c, T value)
{
    if (r >= rows || c >= cols)
    {
        cerr << "setElement(): Indices are out of range" << endl;
        return false;
    }

    data[r][c] = value;
    return true;
}

template class Mat<int, 2, 2>; // Explicitly instantiate template Mat<int, 2, 2>
typedef Mat<int, 2, 2> Mat22i;

// template Mat<float, 3, 1> will be instantiate implicitly

int main()
{
    Mat22i mat;

    mat.setElement(2, 3, 256);
    cout << mat.getElement(2, 3) << endl;

    mat.setElement(1, 1, 256);
    cout << mat.getElement(1, 1) << endl;

    Mat<float, 3, 1> vec;
    vec.setElement(2, 0, 3.14159f);
    cout << vec.getElement(2, 0) << endl;

    Mat<float, 3, 1> vec2(vec);
    cout << vec2.getElement(2, 0) << endl;

    // vec2 = mat; //error

    return 0;
}
```

## 默认形参

```cpp
#include <iostream>
#include <cmath>

using namespace std;

float norm(float x, float y, float z);
float norm(float x, float y, float z = 0);
float norm(float x, float y = 0, float z);

int main()
{
    cout << norm(3.0f) << endl;
    cout << norm(3.0f, 4.0f) << endl;
    cout << norm(3.0f, 4.0f, 5.0f) << endl;
    return 0;
}

float norm(float x, float y, float z)
{
    return sqrt(x * x + y * y + z * z);
}
```

## 指针作为参数

```cpp
#include <iostream>

using namespace std;

int foo1(int x)
{
    x += 10;
    return x;
}

int foo2(int *p)
{
    (*p) += 10;
    return *p;
}

int main()
{
    int num1 = 20;
    int num2 = foo1(num1);
    cout << "num1=" << num1 << endl;
    cout << "num2=" << num2 << endl;

    int *p = &num1;
    int num3 = foo2(p);
    cout << "num1=" << num1 << endl;
    cout << "*p=" << *p << endl;
    cout << "num3=" << num3 << endl;

    return 0;
}
```
