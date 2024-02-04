# define

## 使用可变参数宏

::::{tab-set}
:::{tab-item} \_\_VA\_ARGS\_\_

- **含义：**`__VA_ARGS__` 是一个在宏中用来表示可变参数的标识符。它允许在宏中使用可变数量的参数。
- **用法：**`__VA_ARGS__` 被用在宏定义中，用于表示可变参数的位置。
- **示例：**

```cpp
#include <cstdio>

#define PRINT_VALUES(...) printf(__VA_ARGS__)

int main()
{
    PRINT_VALUES("Sum: %d\n", 10 + 20);
    PRINT_VALUES("Product: %d\n", 5 * 6);
    return 0;
}
```
:::

:::{tab-item} \#\_\_VA\_ARGS\_\_

- **含义：**`#__VA_ARGS__` 是字符串化运算符，用于将可变参数转换为字符串。
- **用法：**`#` 运算符用于将宏参数转换为字符串。
- **示例：**

```cpp
#include <cstdio>

#define SHOW_VALUES(...) puts(#__VA_ARGS__)

int main()
{
    SHOW_VALUES(1, "x", int); // 展开成 puts("1, \"x\", int")
    return 0;
}
```
:::

:::{tab-item} \#\#\_\_VA\_ARGS\_\_

- **含义：**`##` 运算符用于在宏中连接两个标识符。`##__VA_ARGS__` 用于处理可变参数的连接问题。
- **用法：**`##` 用于在宏中连接可变参数和其他标识符。
- **示例：**

```cpp
#include <cstdio>

#define CONCATENATE(a, b) a##b

int main()
{
    int xy = CONCATENATE(10, 20); // 展开成 int xy = 1020;
    printf("%d", xy);
    return 0;
}
```
:::

:::{tab-item} \_\_VA\_OPT\_\_

- **含义：**`__VA_OPT__` 是一个在可变参数宏中用于处理可选参数的特殊宏。
- **用法：**`__VA_OPT__(...)` 表示可选参数，若 `__VA_ARGS__` 非空，则插入括号内的内容；否则，将其忽略。
- **示例：**

```cpp
#include <cstdio>

#define LOG_MSG(fmt, ...) printf(fmt __VA_OPT__(, ) __VA_ARGS__)

int main()
{
    LOG_MSG("Sum: %d, %d\n", 10 + 20, 40); // 展开成 printf("Sum: %d, %d\n", 10 + 20, 40);
    LOG_MSG("Hello, World!\n");            // 展开成 printf("Hello, World!\n");
    return 0;
}
```
:::
::::

```cpp
#include <iostream>

// 制造函数工厂并使用它
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

## 定义一个函数

如果我们想要定义一个函数，比如 `MAX(a, b)`，直接使用 `#define` 会出现问题。因为 `#define` 只是简单的文本替换，它不能理解 C 语言的语法。例如，下面的代码会导致编译错误：

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
```

这是因为预处理器会把这段代码替换为：

```c
((a) > (b) ? (a) : (b))
```

这显然不是一个有效的 C 语言函数定义。

为了解决这个问题，C 语言引入了 `do { ... } while(0)` 结构。这个结构的意思是执行 `{ ... }` 中的代码，然后检查 `while(0)` 的条件是否成立。由于 `while(0)` 的条件永远不成立，所以这个结构可以用来定义一个多行的宏。这样，我们就可以定义一个函数了：

```c
#define MAX(a, b)       \
    do                  \
    {                   \
        if ((a) > (b))  \
            return (a); \
        else            \
            return (b); \
    } while (0)
```

这样，预处理器就会把这段代码替换为：

```c
if ((a) > (b))
    return (a);
else
    return (b);
```

这就是一个有效的 C 语言函数定义了。
