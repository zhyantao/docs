# define...do...while

## `define...do...while`

如果我们想要 `define` 一个函数，比如 `MAX(a, b)`，直接使用 `#define` 会出现问题。因为 `#define` 只是简单的文本替换，它不能理解 C 语言的语法。例如，下面的代码会导致编译错误：

```cpp
#define MAX(a, b) ((a) > (b) ? (a) : (b))
```

这是因为预处理器会把这段代码替换为：

```cpp
((a) > (b) ? (a) : (b))
```

这显然不是一个有效的 C 语言函数定义。

为了解决这个问题，C 语言引入了 `do { ... } while(0)` 结构。这个结构的意思是执行 `{ ... }` 中的代码，然后检查 `while(0)` 的条件是否成立。由于 `while(0)` 的条件永远不成立，所以这个结构可以用来定义一个多行的宏。这样，我们就可以定义一个函数了：

```cpp
#define MAX(a, b)       \
    do {                \
        if ((a) > (b))  \
            return (a); \
        else            \
            return (b); \
    } while (0)
```

这样，预处理器就会把这段代码替换为：

```cpp
if ((a) > (b))
    return (a);
else
    return (b);
```

这就是一个有效的 C 语言函数定义了。
