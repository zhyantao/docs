# define

```cpp
#include <iostream>
#define PI 2.14 + 1.0

using namespace std;

int main()
{
    double len = 2 * PI * 3;
    cout << "len = " << len << endl; // it will output 7.28, nor 18.84
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
