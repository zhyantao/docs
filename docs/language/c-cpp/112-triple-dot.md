# ...

在 C/C++ 的高级语法中，我们会经常看到 `...` 这个符号，在不同的场景中，有不同的含义：

- 用在函数模板中，表示接受可变参数的形参（函数形参包）；
- 用在类模板中，表示接受可变参数的类类型（模板形参包）；
- 用在 Variadic 宏中，表示接受可变参数的替换列表；
- 用在 `catch` 子句中，表示可以捕获任何类型的异常；
- 用在 Lambda 表达式中，表示捕获可变数量的引用；
- 用在 `sizeof` 运算符中，表示依次调用 `sizeof`；

## 包展开

作为预备知识，我们需要了解包展开的规则，根据下面的这个例子去理解：

```cpp
template<class... Us>
void f(Us... pargs) {}
 
template<class... Ts>
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
template<typename... Ts>
void f(Ts...) {}
f('a', 1); // Ts... 会展开成 void f(char, int)
f(0.1);    // Ts... 会展开成 void f(double)
 
template<typename... Ts, int... N> void g(Ts (&...arr)[N]) {}
int n[1];
g<const char, int>("a", n); // Ts (&...arr)[N] 会展开成 
                            // const char (&)[2], int(&)[1]
```

## 变参类模板

```cpp
template<class A, class B, class... C>
void func(A arg1, B arg2, C...arg3)
{
    container<A, B, C...> t1; // 展开成 container<A, B, E1, E2, E3> 
    container<C..., A, B> t2; // 展开成 container<E1, E2, E3, A, B> 
    container<A, C..., B> t3; // 展开成 container<A, E1, E2, E3, B> 
}
```

## Variadic 宏

```cpp
#define F(...) f(0 __VA_OPT__(,) __VA_ARGS__)
#define G(X, ...) f(0, X __VA_OPT__(,) __VA_ARGS__)
#define SDEF(sname, ...) S sname __VA_OPT__(= { __VA_ARGS__ })
F(a, b, c) // 替换为 f(0, a, b, c)
F()        // 替换为 f(0)
G(a, b, c) // 替换为 f(0, a, b, c)
G(a, )     // 替换为 f(0, a)
G(a)       // 替换为 f(0, a)
SDEF(foo);       // 替换为 S foo;
SDEF(bar, 1, 2); // 替换为 S bar = { 1, 2 };
```

## catch 子句

```cpp
template<class... X>
void func(int arg) throw(X...)
{
    // ... 在不同情形下抛出不同的 X
    try{}
    catch(except1&){}
    catch(except2&){}
    catch(...){} // 接受所有异常
}
```

## Lambda 引用捕获

```cpp
template<class... Args>
void f(Args... args)
{
    auto lm = [&, args...] { return g(args...); };
    lm();
}
```

## sizeof 运算符

```cpp
template<class... Types>
struct count
{
    static const std::size_t value = sizeof...(Types);
};
```

---

更多资料参考：

- <https://zh.cppreference.com/w/cpp/language/parameter_pack>
- <https://zh.cppreference.com/w/cpp/preprocessor/replace>
