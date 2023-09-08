# Makefile

本文仅提供编写手动编写 Makefile 的简单示例，理解了本文就能够应付大部分的 Makefile 了，更加复杂的 Makefile 都是在这种简单规则上叠加的。但是只阅读本文是远远不够的，为了能够对 Makefile 有更加清晰的认识，我这里推荐另外一个文档：<https://seisman.github.io/how-to-write-makefile>。

```{note}
在实际工程中，虽然也有只用 Makefile 的项目，但是更为方便的方式是使用 CMakeList 来生成 Makefile。cmake 管理工程的最大优势在于跨平台，自己不用书写太复杂的脚本了，自己写一写配置文件，后面的工作就都是自动化的了。
```

## 版本一

最简单的方式就是把文件一个一个手打出来进行编译。

```bash
hello: main.cpp printhello.cpp  factorial.cpp
    g++ -o hello main.cpp printhello.cpp  factorial.cpp
```

## 版本二

采用 Makefile 只会更新有变动的文件，在工程比较大的情况下可以节省很多时间。

```bash
CXX = g++
TARGET = hello
OBJ = main.o printhello.o factorial.o

$(TARGET): $(OBJ)
    $(CXX) -o $(TARGET) $(OBJ)

main.o: main.cpp
    $(CXX) -c main.cpp

printhello.o: printhello.cpp
    $(CXX) -c printhello.cpp

factorial.o: factorial.cpp
    $(CXX) -c factorial.cpp
```

## 版本三

```bash
CXX = g++
TARGET = hello
OBJ = main.o printhello.o factorial.o

CXXFLAGS = -c -Wall

$(TARGET): $(OBJ)
    $(CXX) -o $@ $^

%.o: %.cpp
    $(CXX) $(CXXFLAGS) $< -o $@

.PHONY: clean
clean:
    rm -f *.o $(TARGET)
```

## 版本四

这是目前 Makefile 的主流编写方式。

```bash
# := 表示临时赋值
CXX := g++
TARGET := hello
SRC := $(wildcard *.cpp)
OBJ := $(patsubst %.cpp, %.o, $(SRC))

CXXFLAGS := -c -Wall

# 基本格式：目标文件:依赖文件
# $@ 代表目标文件，匹配目标二进制文件 hello
# $^ 代表依赖文件，匹配目标二进制文件 hello 依赖的所有 .o 文件，即 $(OBJ)
$(TARGET): $(OBJ)
    $(CXX) -o $@ $^

# 这句话用来将所有的 .cpp 文件编译成对应的 .o 文件（文件名不变，扩展名改变）
# $@ 代表目标文件，匹配目标 .o 文件
# $< 代表依赖文件，匹配目标 .o 文件依赖的第一个 .c 文件，即与 .o 文件文件名相同的 .cpp 文件
# % 是通配符，它和字符串中任意个数的字符相匹配
%.o: %.cpp
    $(CXX) $(CXXFLAGS) $< -o $@

# .PHONY 作用在于防止 clean 这个命令和系统中可能存在的 clean 命令冲突
.PHONY: clean
clean:
    rm -f *.o $(TARGET)
```

## 字符串替换和分析函数

| 函数                                 | 作用                                                         |
| ------------------------------------ | ------------------------------------------------------------ |
| `$(subst from,to,text)`             | 在文本 `text` 中使用 `to` 替换每一处 `from`。                     |
| `$(patsubst pattern,replacement,text)` | 寻找 `text` 中符合格式 `pattern` 的字，用 `replacement` 替换它们。`pattern` 和 `replacement` 中可以使用通配符。 |
| `$(strip string)`                      | 去掉前导和结尾空格，并将中间的多个空格压缩为单个空格。       |
| `$(findstring find,in)`                | 在字符串 `in` 中搜寻 `find` ，如果找到，则返回值是 `find`，否则返回值为空。 |
| `$(filter pattern...,text)`            | 返回在 `text` 中由空格隔开且匹配格式 `pattern...` 的字，去除不符合格式 `pattern...` 的字 |
| `$(filter-out pattern...,text)`        | 返回在 `text` 中由空格隔开且不匹配格式 `pattern...` 的字，去除符合格式 `pattern...` 的字。它是函数 `filter` 的反函数 |
| `$(sort list)`                         | 将 `list` 中的字按字母顺序排序，并去掉重复的字。输出由单个空格隔开的字的列表 |

## 文件名函数

| 函数                         | 作用                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `$(dir names...)`              | 抽取 `names...` 中每一个文件名的路径部分，文件名的路径部分包括从文件名的首字符到最后一个斜杠(含斜杠)之前的一切字符。 |
| `$(notdir names...)`           | 抽取 `names...` 中每一个文件名中除路径部分外一切字符（真正的文件名）。 |
| `$(suffix names...)`           | 抽取 `names...` 中每一个文件名的后缀                           |
| `$(basename names...)`         | 抽取 `names...` 中每一个文件名中除后缀外一切字符               |
| `$(addsuffix suffix,names...)` | 参数 `names...` 是一系列的文件名，文件名之间用空格隔开；`suffix` 是一个后缀名。将 `suffix` (后缀)的值附加在每一个独立文件名的后面，完成后将文件名串联起来，它们之间用单个空格隔开。 |
| `$(addprefix prefix,names...)` | 参数 `names` 是一系列的文件名，文件名之间用空格隔开；`prefix` 是一个前缀名。将 `preffix` (前缀)的值附加在每一个独立文件名的前面，完成后将文件名串联起来，它们之间用单个空格隔开。 |
| `$(wildcard pattern)`          | 参数 `pattern` 是一个文件名格式，包含有通配符(通配符和 shell 中的用法一样)。函数 wildcard 的结果是一列和格式匹配的且真实存在的文件的名称，文件名之间用一个空格隔开。 |

## 其他函数

| 函数                                  | 作用                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| `$(foreach var,list,text)`              | 前两个参数， `var` 和 `list` 将首先扩展，注意最后一个参数 `text` 此时不扩展；接着，`list` 扩展所得的每个字，都赋给 `var` 变量；然后 `text` 引用该变量进行扩展，因此 `text` 每次扩展都不相同。函数的结果是由空格隔开的 `text`  在 `list` 中多次扩展后，得到的新 `list` ，就是说： `text` 多次扩展的字串联起来，字与字之间由空格隔开，如此就产生了函数 `foreach` 的返回值。 |
| `$(if condition,then-part[,else-part])` | 首先把第一个参数 `condition` 的前导空格、结尾空格去掉，然后扩展。如果扩展为非空字符串，则条件 `condition` 为 `真` ；如果扩展为空字符串，则条件 `condition` 为 `假` 。<br/>如果条件 `condition` 为 `真` ,那么计算第二个参数 `then-part` 的值，并将该值作为整个函数 if 的值。<br/>如果条件 `condition` 为 `假` ,并且第三个参数存在，则计算第三个参数 `else-part` 的值，并将该值作为整个函数 `if` 的值；如果第三个参数不存在，函数 `if` 将什么也不计算，返回空值。 |
| `$(origin variable)`                    | 变量 `variable` 是一个查询变量的名称，不是对该变量的引用。所以，不能采用 `$` 和圆括号的格式书写该变量，当然，如果需要使用非常量的文件名，可以在文件名中使用变量引用。 |
| `$(shell command arguments)`            | 函数 shell 是 make 与外部环境的通讯工具。函数 shell 的执行结果和在控制台上执行 `command arguments` 的结果相似。不过如果 `command arguments` 的结果含有换行符（和回车符），则在函数 shell 的返回结果中将把它们处理为单个空格，若返回结果最后是换行符（和回车符）则被去掉。 |
