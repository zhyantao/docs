# 预定义宏

下列宏名已预定义于每个翻译单元中：

| 预定义宏                        | 解释说明     |
| ------------------------------- | ------------------------------------------------------------ |
| `__cplusplus`                                                  | 代表所用的 C++ 标准版本，展开成值<br>199711L(C++11 前)<br>201103L(C++11)<br>201402L(C++14)<br>201703L(C++17)<br>202002L(C++20)<br>202302L(C++23) (宏常量) |
| `__STDC_HOSTED__`(C++11)                                       | 如果实现有宿主（在操作系统下运行）则展开成整数常量 `1`，如果实现自立（不在操作系统下运行）则展开成 `0` (宏常量) |
| `__FILE__`                                                     | 展开成当前文件名，作为字符串字面量，可用 [`#line`](https://zh.cppreference.com/w/cpp/preprocessor/line) 指令更改 (宏常量) |
| `__LINE__`                                                     | 展开成源文件行号，整数常量，可用 [`#line`](https://zh.cppreference.com/w/cpp/preprocessor/line) 指令更改 (宏常量) |
| `__DATE__`                                                     | 展开成翻译日期，形式为 `"Mmm dd yyyy"` 的字符串。如果月中日期数小于 `10` 则 `"dd"` 的首字符为空格。月份名如同以 [std::asctime](http://zh.cppreference.com/w/cpp/chrono/c/asctime)() 生成 (宏常量) |
| `__TIME__`                                                     | 展开成翻译时间，形式为 `"hh:mm:ss"` 的字符串字面量 (宏常量)  |
| `__STDCPP_DEFAULT_NEW_ALIGNMENT__`(C++17)                      | 展开成 [std::size_t](https://zh.cppreference.com/w/cpp/types/size_t) 字面量，其值为对不具对齐的 [operator new](https://zh.cppreference.com/w/cpp/memory/new/operator_new) 的调用所保证的对齐（更大的对齐将传递给具对齐重载，如 [operator new](http://zh.cppreference.com/w/cpp/memory/new/operator_new)([std::size_t](http://zh.cppreference.com/w/cpp/types/size_t), [std::align_val_t](http://zh.cppreference.com/w/cpp/memory/new/align_val_t))） (宏常量) |
| `__STDCPP_­BFLOAT16_­T__`<br> `__STDCPP_­FLOAT16_­T__`<br>`__STDCPP_FLOAT32_T__`<br>`__STDCPP_FLOAT64_T__`<br>`__STDCPP_FLOAT128_T__`(C++23) | 当且仅当实现支持对应的[扩展浮点类型](https://zh.cppreference.com/w/cpp/types/floating-point)时展开成 `1` (宏常量) |

实现可能会预定义下列其他的宏名：

| 预定义宏                        | 解释说明     |
| ------------------------------- | ------------------------------------------------------------ |
| `__STDC__`                        | 如果存在则为实现定义值，典型地用于指示 C 遵从性 (宏常量)     |
| `__STDC_VERSION__`(C++11)         | 如果存在则为实现定义值 (宏常量)                              |
| `__STDC_ISO_10646__`(C++11)       | 如果 `wchar_t` 使用 Unicode，那么展开成 `yyyymmL` 形式的整数常量，日期指示所支持的 Unicode 的最近版本(C++23 前)如果存在则为实现定义值(C++23 起) (宏常量) |
| `__STDC_MB_MIGHT_NEQ_WC__`(C++11) | 如果对于基本字符集成员 `'x' == L'x'` 可能为假，则展开成 `1`，如在基于 EBCDIC 并且为 `wchar_t` 使用 Unicode 的系统上。 (宏常量) |
| `__STDCPP_THREADS__`(C++11)       | 如果程序能拥有多于一个执行线程则展开成 `1` (宏常量)          |
| `__STDCPP_STRICT_POINTER_SAFETY__`(C++11)(C++23 中移除) | 如果实现支持严格 [std::pointer_safety](https://zh.cppreference.com/w/cpp/memory/gc/pointer_safety) 则展开成 `1` (宏常量) |

这些宏的值（除了 `__FILE__` 和 `__LINE__`）在整个翻译单元保持为常量。试图重定义或取消定义这些宏会导致未定义行为。

```{note}
注意：在每个函数体的作用域内部都有一个名为 __func__ 的特殊的函数局域预定义变量，它被定义为一个持有具有实现定义格式的函数名的静态字符数组。它不是预处理器宏，但它与 `__FILE__` 和 `__LINE__` 一起使用，例如 [assert](https://zh.cppreference.com/w/cpp/error/assert)。(C++11 起) 
```
