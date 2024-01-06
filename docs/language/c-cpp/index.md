# C/C++ 编程基础

学习 C/C++ 是一个持久的战役，这个语言几乎每年都会有新的特性加进来，因此，我们不可能在博客中把所有的细节都表现出来。在学习的过程中，需要注重日积月累，把碰到的不会的东西逐渐地加以总结和凝练，用通俗易懂的方式重新表述一遍，是这个系列博客存在的意义。

另外，推荐一个可以在线运行 C/C++ 代码的环境：<https://coliru.stacked-crooked.com>

```{toctree}
:titlesonly:
:hidden:
:glob:

hello.md
multifile-compile.md
macro.md
argument.md
init.md
overflow.md
size.md
char.md
bool.md
intmax.md
float.md
precision.md
nan.md
conversion.md
if.md
ternary.md
while.md
for.md
goto.md
switch.md
array.md
variable-array.md
index-bound.md
md-array.md
const-array.md
initchar.md
stringop.md
stdstring.md
struct.md
structpadding.md
union.md
enum.md
typedef.md
pointer.md
pointer-struct.md
pointer-pointer.md
const-pointer.md
pointer-array.md
arithmetic.md
bound.md
newdelete.md
function.md
param-pointer.md
reference.md
param-reference.md
inline.md
default-argument.md
overload.md
template1.md
template2.md
specialization-function.md
function-pointer.md
function-reference.md
recursion.md
avx2-openmp.md
firstclass.md
access-attribute.md
outer-class-function.md
constructor.md
destructor.md
object-array.md
this.md
const.md
static.md
cmake.md
operator-overload.md
overload-+-+=.md
overload-+string.md
overload-int+MyTime.md
overload-int()-=-ostream.md
overload-++.md
memory-leak.md
hard-copy.md
shared_ptr.md
unique_ptr.md
well-organized-code.md
derive.md
protect.md
virtual.md
matclass.md
mattemplate.md
nontypeparam.md
specialization-class.md
stderr.md
assert.md
abort.md
return.md
throw.md
throw-try-catch.md
catch-by-caller.md
catch-by-derived-class.md
nothrow.md
friend.md
define-friend-outer-class.md
nested-enum.md
nestedclass.md
rtti.md
typeid.md
const_cast.md
reinterpret_cast.md
extern.md
file.md
file+.md
readline-by-getchar.md
process-one-line.md
print-format-control.md
scanf-format-control.md
break-input-output.md
scanf-hints.md
lambda.md
varargs.md
predefined-macros.md
condition_variable.md
future.md
weak_ptr.md
socket.md
callback.md
read-tty.md
```

## Google Code Style

- 尽量不使用宏
- 不使用异常
- 禁止使用 RTTI
- 使用 `printf` 之类的代替流
- 除位域不使用无符号数字
- 除特定环境，不使用操作符重载
- 使用 4 中 `cast` 运算符转换类型
- 禁止使用 `Class` 类型全局变量，若使用必须为单例模式
- `sizeof(var)` 代替 `sizeof(type)`
- `scoped_ptr` 可以胜任智能指针
- 特殊情况下可用 `shared_ptr`
- 任何时候都不使用 `auto_ptr`

```cpp
// style.h (文件名全小写，可包含下划线或短线)

// Copyright 2008 Google Inc.
// License(BSD/GPL/...)
// Author: Your Name
// This file mainly describes ...

// 防止重复包含，宏格式为：<project>_<path>_<file>_
#ifndef PROJECT_EVENTLOOP_H_
#define PROJECT_EVENTLOOP_H_

// 头文件中尽量使用前置声明
// STL 类例外，不使用前置声明，使用 #include
class Channel;

// 命名空间全小写，顶头无空格，cpp 文件里提倡使用不具名命名空间
namespace mynamespace {

// 类名大写开头单词，使用组合通常比使用继承更适宜
// 若用继承，只用公有继承
// 另：接口类命名以 Interface 结尾
class EventLoop : public CallbackInterface {
public:
    // 每一个限定符内，声明的顺序如下：
    // 1 typedefs 和 enums
    // 2 常量
    // 3 构造函数
    // 4 析构函数
    // 5 成员函数，含静态数据成员
    // 6 成员变量，含静态成员变量

    typedef vector< int > IntVector;

    // 枚举名同类名，大写开头单词
    enum UrlTableErrors {
        ERROR_OUT_OF_MEMORY = 0, /* 枚举成员：全大写下划线 */
        ERROR_MALFORMED_INPUT,
    };

    // explicit 修饰但参数构造函数，防止隐式类型转换误用
    explicit EventLoop(const int xx);

    // 若定义了成员变量无其他构造函数，要定义一个默认构造函数
    // EventLoop() {
    // }

    // 普通函数命名，大写开头单词
    // 输入参数在前为 const 引用，输出参数在后为指针
    // 不为参数设置缺省值
    void Add(const std::string &input, Channel *output);

    // 存取函数命名
    // 取：同变量名
    // 存：值函数名为 set_varname
    // 短小的存取函数可用内联
    int num_entries() const { /* 尽可能使用 const */
        return num_entries_;
    }
    void set_num_entries(int num_entries) {
        num_entries_ = num_entries;
    }

    // 仅在需要拷贝对象时，使用拷贝构造函数

private:
    DISALLOW_COPY_AND_ASSIGN(EventLoop); // 不需要拷贝时，在 private 里使用 DISALLOW_COPY_ASSIGN 宏

    // 变量用描述性名称，不要节约空间，让别人理解你的代码更重要
    const int kDaysInWeek = 7;      // const 变量用 k 开头，后跟大写开头单词
    int num_entries_;               // 变量命名：全小写，有意义的单词和下划线
    int num_complated_connections_; // 类成员变量下划线结尾

    Channel *channel_; // 头文件中只用了指针/引用，则前向声明而非引入头文件
};

} // namespace mynamespace

#endif // PORJECT_EVENTLOOP_H_  /* 保护宏结尾加注释 */
```

```cpp
// style.cpp (文件名全小写，可包含下划线或短线)

// Copyright 2008 Google Inc.
// License(BSD/GPL/...)
// Author: Your Name
// This file mainly describes ...

// 包含次序标准化，避免隐藏依赖：
// 1 本类的声明（第一个包含本类 h 文件，有效减少依赖）
// 2 C 系统文件
// 3 C++ 系统文件
// 4 其他库头文件
// 5 本项目内头文件（避免使用 UNIX 文件路径和 . 和 ..）
#include "base/basictypes.h"
#include "eventloop.h"
#include "foo/public/bar.h"
#include <sys/types.h>
#include <vector>

// 可以在整个 cpp 文件和 h 文件的方法内使用 using
// 禁止使用 using namespace xxx 污染命名空间
using std::string;

namespace mynamespace {

EventLoop::EventLoop() : num_entries_(10), num_complated_connections_(false) {
}

ReturnType ClassName::ReallyLongFunctionName(const Type &par_name1, Type *par_name2) {
    bool retval = DoSometing(averyveryveryverylongargument1, argument2, argument3);
    if (condition) {
        for (int i = 0; i < kSomeNumber; ++i) { /* 前置自增运算 */
            if (this_one_thing > this_other_thing && a_third_thing == a_forth_thing) {
                // 临时方案使用 TODO 注释，后面括号里加上你的大名，邮件地址
                // TODO (zh6tao@gmail.com): zh6tao
            }
        }
    } else {
        nt j = g();
    }

    switch (var) {
    case 0:
        break;

    default:
        assert(false); /* 若 default 永不执行可使用 assert */
    }

    return x;
}
} // namespace mynamespace /* 命名空间结束注释 */
```

## Clang Format

首先在 VS Code 中安装 Clang Format 扩展，然后在项目根目录下创建 `.clang-format`，文件内容如下：

```yaml
# This configuration file can be used to auto-format the code base.
# Not all guidelines specified in CODING_STYLE are followed, so the
# result MUST NOT be committed indiscriminately, but each automated
# change should be reviewed and only the appropriate ones committed.
#
# The easiest way to apply the formatting to your changes ONLY,
# is to use the git-clang-format script (usually installed with clang-format).
#
# -  Fix up formatting before committing
# 1. Edit and stage your files.
# 2. Run `git clang-format`.
# 3. Verify + correct + (un)stage changes.
# 4. Commit.
#
# -  Fix up formatting after committing
# 1. Commit your changes.
# 2. Run `git clang-format HEAD~` - Refer the commit *before* your changes here.
# 3. Verify + correct changes, `git difftool -d` can help here.
# 4. Stage + commit, potentially with `--amend` (means to fixup the last commit).
#
# To run clang-format on all sourcefiles, use the following line:
# $ git ls-files 'src/*.[ch]' 'src/*.cc' | xargs clang-format -i -style=file
#
# You can find more information on the different config parameters in this file here:
# https://clang.llvm.org/docs/ClangFormatStyleOptions.html
---
AccessModifierOffset: -4
AlignAfterOpenBracket: AlwaysBreak
AlignEscapedNewlines: Left
AlignOperands: false
AllowShortFunctionsOnASingleLine: None
AlwaysBreakBeforeMultilineStrings: true
AlwaysBreakTemplateDeclarations: Yes
BinPackArguments: false
BinPackParameters: false
BraceWrapping:
  AfterEnum: false
  SplitEmptyFunction: false
  SplitEmptyRecord: false
  SplitEmptyNamespace: false
BreakBeforeBraces: Custom
BreakBeforeTernaryOperators: false
BreakInheritanceList: BeforeComma
BreakStringLiterals: false
ColumnLimit: 109
CompactNamespaces: true
ConstructorInitializerAllOnOneLineOrOnePerLine: true
ConstructorInitializerIndentWidth: 8
ContinuationIndentWidth: 16
Cpp11BracedListStyle: false
ForEachMacros:
  - BITMAP_FOREACH
  - CMSG_FOREACH
  - _DNS_ANSWER_FOREACH
  - DNS_ANSWER_FOREACH
  - _DNS_ANSWER_FOREACH_FLAGS
  - DNS_ANSWER_FOREACH_FLAGS
  - _DNS_ANSWER_FOREACH_FULL
  - DNS_ANSWER_FOREACH_FULL
  - _DNS_ANSWER_FOREACH_IFINDEX
  - DNS_ANSWER_FOREACH_IFINDEX
  - _DNS_QUESTION_FOREACH
  - DNS_QUESTION_FOREACH
  - FDSET_FOREACH
  - FOREACH_BTRFS_IOCTL_SEARCH_HEADER
  - FOREACH_DEVICE
  - FOREACH_DEVICE_AND_SUBSYSTEM
  - FOREACH_DEVICE_DEVLINK
  - FOREACH_DEVICE_PROPERTY
  - FOREACH_DEVICE_SYSATTR
  - FOREACH_DEVICE_TAG
  - FOREACH_DIRENT
  - FOREACH_DIRENT_ALL
  - FOREACH_INOTIFY_EVENT
  - FOREACH_STRING
  - FOREACH_SUBSYSTEM
  - HASHMAP_FOREACH
  - HASHMAP_FOREACH_IDX
  - HASHMAP_FOREACH_KEY
  - JOURNAL_FOREACH_DATA_RETVAL
  - JSON_VARIANT_ARRAY_FOREACH
  - JSON_VARIANT_OBJECT_FOREACH
  - LIST_FOREACH
  - LIST_FOREACH_AFTER
  - LIST_FOREACH_BEFORE
  - LIST_FOREACH_OTHERS
  - LIST_FOREACH_SAFE
  - MESSAGE_FOREACH_PART
  - NULSTR_FOREACH
  - NULSTR_FOREACH_PAIR
  - OBJECT_PATH_FOREACH_PREFIX
  - ORDERED_HASHMAP_FOREACH
  - ORDERED_HASHMAP_FOREACH_KEY
  - ORDERED_SET_FOREACH
  - PATH_FOREACH_PREFIX
  - PATH_FOREACH_PREFIX_MORE
  - SD_HWDB_FOREACH_PROPERTY
  - SD_JOURNAL_FOREACH
  - SD_JOURNAL_FOREACH_BACKWARDS
  - SD_JOURNAL_FOREACH_DATA
  - SD_JOURNAL_FOREACH_FIELD
  - SD_JOURNAL_FOREACH_UNIQUE
  - SECCOMP_FOREACH_LOCAL_ARCH
  - SET_FOREACH
  - SET_FOREACH_MOVE
  - STRV_FOREACH
  - STRV_FOREACH_BACKWARDS
  - STRV_FOREACH_PAIR
IndentPPDirectives: AfterHash
IndentWidth: 4
IndentWrappedFunctionNames: true
MaxEmptyLinesToKeep: 2
PenaltyBreakAssignment: 65
PenaltyBreakBeforeFirstCallParameter: 16
PenaltyBreakComment: 320
PenaltyBreakFirstLessLess: 50
PenaltyBreakString: 0
PenaltyExcessCharacter: 10
PenaltyReturnTypeOnItsOwnLine: 100
PointerAlignment: Right
SpaceAfterCStyleCast: true
SpaceAroundPointerQualifiers: Both
SpaceBeforeParens: ControlStatementsExceptForEachMacros
SpacesInAngles: true
TabWidth: 4
UseCRLF: false
```
