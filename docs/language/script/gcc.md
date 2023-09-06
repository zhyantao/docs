# GCC

如需了解更多细节，请参阅 <https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html>。

## 常用选项

| 编译选项       | 解释                                                         |
| -------------- | ------------------------------------------------------------ |
| `-ansi`        | 只支持 ANSI 标准的 C 语法。<br>这一选项将禁止 GNU C 的某些特色，例如 `asm` 或 `typeof` 关键词 |
| `-c`           | 只编译并生成目标文件                                         |
| `-DMACRO`      | 以字符串 `"1"` 定义 MACRO 宏                                 |
| `-DMACRO=DEFN` | 以字符串 `"DEFN"` 定义 MACRO 宏                               |
| `-E`           | 只运行 C 预编译器                                            |
| `-g`           | 生成调试信息。GNU 调试器可利用该信息                         |
| `-IDIRECTORY`  | 指定额外的头文件搜索路径 `DIRECTORY`                         |
| `-LDIRECTORY`  | 指定额外的函数库搜索路径 `DIRECTORY`                         |
| `-lLIBRARY`    | 连接时搜索指定的函数库 `LIBRARY`                             |
| `-m486`        | 针对 486 进行代码优化                                        |
| `-o`           | FILE 生成指定的输出文件。用在生成可执行文件时                |
| `-O0`          | 不进行优化处理                                               |
| `-O`           | 或 `-O1` 优化生成代码                                        |
| `-O2`          | 进一步优化                                                   |
| `-O3`          | 比 `-O2` 更进一步优化，包括 `inline` 函数                    |
| `-shared`      | 生成共享目标文件。通常用在建立共享库时                       |
| `-static`      | 禁止使用共享连接                                             |
| `-UMACRO`      | 取消对 MACRO 宏的定义                                        |
| `-w`           | 不生成任何警告信息                                           |
| `-Wall`        | 生成所有警告信息                                             |

## 优化选项

| 编译选项 | 解释                 |
| -------- | -------------------- |
| `-O1`    | 最小化空间           |
| `-Op[-]` | 改善浮点数一致性     |
| `-O2`    | 最大化速度           |
| `-Os`    | 优选代码空间         |
| `-Oa`    | 假设没有别名         |
| `-Ot`    | 优选代码速度         |
| `-Ob`    | 内联展开（默认 n=0） |
| `-Ow`    | 假设交叉函数别名     |
| `-Od`    | 禁用优化（默认值）   |
| `-Ox`    | 最大化选项           |
| `-Og`    | 启用全局优化         |
| `-Oy[-]` | 启用框架指针省略     |
| `-Oi`    | 启用内建函数         |

## 警告选项

| 编译选项                                | 解释                                                         |
| --------------------------------------- | ------------------------------------------------------------ |
| `--all-warnings`                        | 此开关缺少可用文档                                           |
| `--extra-warnings`                      | 此开关缺少可用文档                                           |
| `-W`                                    | 不建议使用此开关；请改用 `-Wextra`                           |
| `-Wabi`                                 | 当结果与 ABI 相容的编译器的编译结果不同时给出警告            |
| `-Waddress`                             | 使用可疑的内存地址时给出警告                                 |
| `-Waggregate-return`                    | 当返回结构、联合或数组时给出警告                             |
| `-Waliasing`                            | 为可能的虚参重叠给出警告                                     |
| `-Walign-commons`                       | 对 `COMMON` 块对齐的警告                                     |
| `-Wall`                                 | 启用大部分警告信息                                           |
| `-Wampersand`                           | 若延续字符常量中缺少 `&` 则给出警告                          |
| `-Warray-bounds`                        | 当数组访问越界时给出警告                                     |
| `-Warray-temporaries`                   | 创建临时数组时给出警告                                       |
| `-Wassign-intercept`                    | 当 Objective-C 赋值可能为垃圾回收所介入时给出警告            |
| `-Wattributes`                          | 当对属性的使用不合适时给出警告                               |
| `-Wbad-function-cast`                   | 当把函数转换为不兼容类型时给出警告                           |
| `-Wbuiltin-macro-redefined`             | 当内建预处理宏未定义或重定义时给出警告                       |
| `-Wc++-compat`                          | 当在 C 语言中使用了 C 与 C++交集以外的构造时给出警告         |
| `-Wlong-long`                           | 当使用 `-pedantic` 时不对 `long long` 给出警告               |
| `-Wcast-align`                          | 当转换指针类型导致对齐边界增长时给出警告                     |
| `-Wcast-qual`                           | 当类型转换丢失限定信息时给出警告                             |
| `-Wchar-subscripts`                     | 当下标类型为 `char` 时给出警告                               |
| `-Wcharacter-truncation`                | 对被截断的字符表达式给出警告                                 |
| `-Wclobbered`                           | 对能为 `longjmp` 或 `vfork` 所篡改的变量给出警告             |
| `-Wcomment`                             | 对可能嵌套的注释和长度超过一个物理行长的 C++ 注释给出警告    |
| `-Wcomments`                            | `-Wcomment` 的同义词                                         |
| `-Wconversion`                          | 当隐式类型转换可能改变值时给出警告                           |
| `-Wconversion-extra`                    | 对大多数隐式类型转换给出警告                                 |
| `-Wconversion-null`                     | 将 `NULL` 转换为非指针类型时给出警告                         |
| `-Wcoverage-mismatch`                   | 当配置文件中的 `-fprofile-use` 不匹配时给出警告              |
| `-Wcpp`                                 | 当出现 `#warning` 指示时给出警告                             |
| `-Wctor-dtor-privacy`                   | 当所有构造函数和析构函数都是私有时给出警告                   |
| `-Wdeclaration-after-statement`         | 当声明出现在语句后时给出警告                                 |
| `-Wdeprecated`                          | 使用不建议的编译器特性、类、方法或字段时给出警告             |
| `-Wdeprecated-declarations`             | 对 `attribute(deprecated)` 声明给出警告                      |
| `-Wdisabled-optimization`               | 当某趟优化被禁用时给出警告                                   |
| `-Wdiv-by-zero`                         | 对编译时发现的零除给出警告                                   |
| `-Wdouble-promotion`                    | 对从 `float` 到 `double` 的隐式转换给出警告                  |
| `-Weffc++`                              | 对不遵循《Effetive C++》的风格给出警告                       |
| `-Wempty-body`                          | 当 `if` 或 `else` 语句体为空时给出警告                       |
| `-Wendif-labels`                        | 当 `#elif` 和 `#endif` 后面跟有其他标识符时给出警告          |
| `-Wenum-compare`                        | 对不同枚举类型之间的比较给出警告                             |
| `-Werror-implicit-function-declaration` | 不建议使用此开关；请改用 `-Werror=implicit-function-declaration` |
| `-Wextra`                               | 打印额外(可能您并不想要)的警告信息                           |
| `-Wfloat-equal`                         | 当比较浮点数是否相等时给出警告                               |
| `-Wformat`                              | 对 `printf/scanf/strftime/strfmon` 中的格式字符串异常给出警告 |
| `-Wformat-contains-nul`                 | 当格式字符串包含 NUL 字节时给出警告                          |
| `-Wformat-extra-args`                   | 当传递给格式字符串的参数太多时给出警告                       |
| `-Wformat-nonliteral`                   | 当格式字符串不是字面值时给出警告                             |
| `-Wformat-security`                     | 当使用格式字符串的函数可能导致安全问题时给出警告             |
| `-Wformat-y2k`                          | 当 `strftime` 格式给出 2 位记年时给出警告                    |
| `-Wformat-zero-length`                  | 对长度为 0 的格式字符串给出警告                              |
| `-Wformat=`                             | 此开关缺少可用文档                                           |
| `-Wignored-qualifiers`                  | 当类型限定符被忽略时给出警告。                               |
| `-Wimplicit`                            | 对隐式函数声明给出警告                                       |
| `-Wimplicit-function-declaration`       | 对隐式函数声明给出警告                                       |
| `-Wimplicit-int`                        | 当声明未指定类型时给出警告                                   |
| `-Wimplicit-interface`                  | 对带有隐式接口的调用给出警告                                 |
| `-Wimplicit-procedure`                  | 对没有隐式声明的过程调用给出警告                             |
| `-Winit-self`                           | 对初始化为自身的变量给出警告。                               |
| `-Winline`                              | 当内联函数无法被内联时给出警告                               |
| `-Wint-to-pointer-cast`                 | 当将一个大小不同的整数转换为指针时给出警告                   |
| `-Wintrinsic-shadow`                    | 如果用户过程有与内建过程相同的名字则警告                     |
| `-Wintrinsics-std`                      | 当内建函数不是所选标准的一部分时给出警告                     |
| `-Winvalid-offsetof`                    | 对 `offsetof` 宏无效的使用给出警告                           |
| `-Winvalid-pch`                         | 在找到了 PCH 文件但未使用的情况给出警告                      |
| `-Wjump-misses-init`                    | 当跳转略过变量初始化时给出警告                               |
| `-Wlarger-than-`                        | 此开关缺少可用文档                                           |
| `-Wlarger-than=`                        | 当目标文件大于 N 字节时给出警告                              |
| `-Wline-truncation`                     | 对被截断的源文件行给出警告                                   |
| `-Wlogical-op`                          | 当逻辑操作结果似乎总为真或假时给出警告                       |
| `-Wlong-long`                           | 当使用 `-pedantic` 时不对 `long long` 给出警告               |
| `-Wmain`                                | 对可疑的 `main` 声明给出警告                                 |
| `-Wmissing-braces`                      | 若初始值设定项中可能缺少花括号则给出警告                     |
| `-Wmissing-declarations`                | 当全局函数没有前向声明时给出警告                             |
| `-Wmissing-field-initializers`          | 若结构初始值设定项中缺少字段则给出警告                       |
| `-Wmissing-format-attribute`            | 当函数可能是 `format` 属性的备选时给出警告                   |
| `-Wmissing-include-dirs`                | 当用户给定的包含目录不存在时给出警告                         |
| `-Wmissing-noreturn`                    | 当函数可能是 `attribute((noreturn))` 的备选时给出警告        |
| `-Wmissing-parameter-type`              | K&R风格函数参数声明中未指定类型限定符时给出警告              |
| `-Wmissing-prototypes`                  | 全局函数没有原型时给出警告                                   |
| `-Wmudflap`                             | 当构造未被 `-fmudflap` 处理时给出警告                        |
| `-Wmultichar`                           | 使用多字节字符集的字符常量时给出警告                         |
| `-Wnested-externs`                      | 当 `extern` 声明不在文件作用域时给出警告                    |
| `-Wnoexcept`                            | Warn when a noexcept expression evaluates to false even though the expression can't actually throw |
| `-Wnon-template-friend`                 | 在模板内声明未模板化的友元函数时给出警告                     |
| `-Wnon-virtual-dtor`                    | 当析构函数不是虚函数时给出警告                               |
| `-Wnonnull`                             | 当将 `NULL` 传递给需要非 `NULL` 的参数的函数时给出警告       |
| `-Wnormalized=`                         |                                                           |
| `-Wold-style-cast`                      | 程序使用 C 风格的类型转换时给出警告                          |
| `-Wold-style-declaration`               | 对声明中的过时用法给出警告                                   |
| `-Wold-style-definition`                | 使用旧式形参定义时给出警告                                   |
| `-Woverflow`                            | 算术表示式溢出时给出警告                                     |
| `-Woverlength-strings`                  | 当字符串长度超过标准规定的可移植的最大长度时给出警告         |
| `-Woverloaded-virtual`                  | 重载虚函数名时给出警告                                       |
| `-Woverride-init`                       | 覆盖无副作用的初始值设定时给出警告                           |
| `-Wpacked`                              | 当 `packed` 属性对结构布局不起作用时给出警告                 |
| `-Wpacked-bitfield-compat`              | 当紧实位段的偏移量因 GCC 4.4 而改变时给出警告                |
| `-Wpadded`                              | 当需要填补才能对齐结构成员时给出警告                         |
| `-Wparentheses`                         | 可能缺少括号的情况下给出警告                                 |
| `-Wpmf-conversions`                     | 当改变成员函数指针的类型时给出警告                           |
| `-Wpointer-arith`                       | 当在算术表达式中使用函数指针时给出警告                       |
| `-Wpointer-sign`                        | 赋值时如指针符号不一致则给出警告                             |
| `-Wpointer-to-int-cast`                 | 将一个指针转换为大小不同的整数时给出警告                     |
| `-Wpragmas`                             | 对错误使用的 `pragma` 加以警告                               |
| `-Wproperty-assign-default`             | Warn if a property for an Objective-C object has no assign semantics specified |
| `-Wprotocol`                            | 当继承来的方法未被实现时给出警告                             |
| `-Wreal-q-constant`                     | Warn about real-literal-constants with 'q' exponent-letter   |
| `-Wredundant-decls`                     | 对同一个对象多次声明时给出警告                               |
| `-Wreorder`                             | 编译器将代码重新排序时给出警告                               |
| `-Wreturn-type`                         | 当 C 函数的返回值默认为 `int`，或者 C++ 函数的返回类型不一致时给出警告 |
| `-Wselector`                            | 当选择子有多个方法时给出警告                                 |
| `-Wsequence-point`                      | 当可能违反定序点规则时给出警告                               |
| `-Wshadow`                              | 当一个局部变量掩盖了另一个局部变量时给出警告                 |
| `-Wsign-compare`                        | 在有符号和无符号数间进行比较时给出警告                       |
| `-Wsign-promo`                          | 当重载将无符号数提升为有符号数时给出警告                     |
| `-Wstack-protector`                     | 当因为某种原因堆栈保护失效时给出警告                         |
| `-Wstrict-aliasing`                     | 当代码可能破坏强重叠规则时给出警告                           |
| `-Wstrict-aliasing=`                    | 当代码可能破坏强重叠规则时给出警告                           |
| `-Wstrict-null-sentinel`                | 将未作转换的 NULL用作哨兵时给出警告                          |
| `-Wstrict-overflow`                     | 禁用假定有符号数溢出行为未被定义的优化                       |
| `-Wstrict-overflow=`                    | 禁用假定有符号数溢出行为未被定义的优化                       |
| `-Wstrict-prototypes`                   | 使用了非原型的函数声明时给出警告                             |
| `-Wstrict-selector-match`               | 当备选方法的类型签字不完全匹配时给出警告                     |
| `-Wsuggest-attribute=const`             | Warn about functions which might be candidates forattribute((const)) |
| `-Wsuggest-attribute=noreturn`          | 当函数可能是 `attribute((noreturn))` 的备选时给出警告        |
| `-Wsuggest-attribute=pure`              | Warn about functions which might be candidates forattribute((pure)) |
| `-Wsurprising`                          | 对“可疑”的构造给出警告                                       |
| `-Wswitch`                              | 当使用枚举类型作为开关变量，没有提供 `default` 分支，但又缺少某个 `case` 时给出警告 |
| `-Wswitch-default`                      | 当使用枚举类型作为开关变量，但没有提供 `default` 分支时给出警告 |
| `-Wswitch-enum`                         | 当使用枚举类型作为开关变量但又缺少某个`case` 时给出警告  |
| `-Wsync-nand`                           | 当 `__sync_fetch_and_nand` 和 `__sync_nand_and_fetch` 内建函数被使用时给出警告 |
| `-Wsynth`                               | 不建议使用。此开关不起作用。                                 |
| `-Wsystem-headers`                      | 不抑制系统头文件中的警告                                     |
| `-Wtabs`                                | 允许使用不符合规范的制表符                                   |
| `-Wtraditional`                         | 使用了传统 C 不支持的特性时给出警告                          |
| `-Wtraditional-conversion`              | 原型导致的类型转换与无原型时的类型转换不同时给出警告         |
| `-Wtrampolines`                         | Warn whenever a trampoline is generated                      |
| `-Wtrigraphs`                           | 当三字母序列可能影响程序意义时给出警告                       |
| `-Wtype-limits`                         | 当由于数据类型范围限制比较结果永远为真或假时给出警告         |
| `-Wundeclared-selector`                 | 当使用 `@selector()` 却不作事先声明时给出警告                |
| `-Wundef`                               | 当 `#if` 指令中用到未定义的宏时给出警告                      |
| `-Wunderflow`                           | 数字常量表达式下溢时警告                                     |
| `-Wuninitialized`                       | 自动变量未初始化时警告                                       |
| `-Wunknown-pragmas`                     | 对无法识别的 pragma 加以警告                                 |
| `-Wunsafe-loop-optimizations`           | 当循环因为不平凡的假定而不能被优化时给出警告                 |
| `-Wunsuffixed-float-constants`          | 对不带后缀的浮点常量给出警告                                 |
| `-Wunused`                              | 启用所有关于 `XX` 未使用 `"` 的警告                          |
| `-Wunused-but-set-parameter`            | Warn when a function parameter is only set, otherwise unused |
| `-Wunused-but-set-variable`             | Warn when a variable is only set, otherwise unused           |
| `-Wunused-dummy-argument`               | 对未使用的哑元给出警告。                                     |
| `-Wunused-function`                     | 有未使用的函数时警告                                         |
| `-Wunused-label`                        | 有未使用的标号时警告                                         |
| `-Wunused-macros`                       | 当定义在主文件中的宏未被使用时给出警告                       |
| `-Wunused-parameter`                    | 发现未使用的函数指针时给出警告                               |
| `-Wunused-result`                       | 当一个带有 `warn_unused_result` 属性的函数的调用者未使用前者的返回值时给出警告 |
| `-Wunused-value`                        | 当一个表达式的值未被使用时给出警告                           |
| `-Wunused-variable`                     | 有未使用的变量时警告                                         |
| `-Wvariadic-macros`                     | 指定 `-pedantic` 时不为可变参数宏给出警告                    |
| `-Wvla`                                 | 使用变长数组时警告                                           |
| `-Wvolatile-register-var`               | 当一个寄存器变量被声明为 `volatile` 时给出警告               |
| `-Wwrite-strings`                       | 在 C++ 中，非零值表示将字面字符串转换为 `char *` 时给出警告。在 C 中，给出相似的警告，但这种类型转换是符合 ISO C 标准的。 |
| `-frequire-return-statement`            | Functions which return values must end with return statements |

```{note}
每一个都有一个相应的否定形式，在 `W` 后面插入 `no-`，这将关闭警告。例如 `-Wno-unused-function`，参考 <https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html>
```
