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
```

## C/C++ 命名规范

- 类名：驼峰式
- 函数名：下划线式
- 变量：下划线式

## Clang Format

首先在 VS Code 中安装 Clang Format 扩展，然后在项目根目录下创建 `.clang-format`，文件内容如下：

```text
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
IndentWidth: 8
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
TabWidth: 8
UseCRLF: false
```
