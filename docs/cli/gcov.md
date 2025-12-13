# gcov

gcov 是 GCC 工具链中的代码覆盖率分析工具，能够精确展示单元测试对源代码的覆盖情况。

## 使用方法

在编译阶段，由 `.c` 源文件生成 `.o` 目标文件时，需添加 `--coverage` 编译选项：

```makefile
$(OBJS): %.o: %.c
	$(CC) $(CFLAGS) --coverage -c $< -o $@
```

在链接生成可执行文件时，同样需要添加 `--coverage` 选项：

```makefile
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) --coverage -o $@ $^
```

```{note}
`--coverage` 是 GCC 提供的宏选项，等价于同时使用以下三个选项：

- `-fprofile-arcs`：编译时插桩，记录代码执行路径
- `-ftest-coverage`：生成程序结构信息文件
- `-lgcov`：链接覆盖率运行时支持库
```

## 生成覆盖率报告

**运行程序生成数据文件**：执行编译后的程序：

```bash
./your_program
```

程序运行后会生成 `.gcda`（运行时数据）和 `.gcno`（程序结构信息）文件。

**生成原始覆盖率数据**：对每个需要分析的源文件执行 gcov 命令：

```bash
gcov main.c
```

此命令会生成对应的 `.gcov` 文本格式报告文件。

**生成可视化报告**：使用 lcov + genhtml 工具链：

```bash
# 1. 收集覆盖率数据
lcov -c -d . -o coverage.info

# 2. 可选：过滤系统头文件
lcov -r coverage.info '/usr/include/*' -o coverage_filtered.info

# 3. 生成 HTML 报告
genhtml coverage_filtered.info -o coverage_report

# 4. 查看报告
firefox coverage_report/index.html
```

````{dropdown} lcov 常用参数
```bash
# 仅收集指定目录的覆盖率数据
lcov -c -d src/ -o coverage.info

# 合并多个覆盖率数据文件
lcov -a coverage1.info -a coverage2.info -o total.info
```
````

**覆盖率报告解读**

双击 lcov 生成的 index.html 文件，即可在浏览器中查看覆盖率报告。报告主要包含以下三列数据：

| 列名        | 说明                                                                  |
| ----------- | --------------------------------------------------------------------- |
| Branch data | 分支覆盖率，显示代码中每个分支（如 `if/else`、`switch` 等）的执行情况 |
| Line Data   | 行覆盖率，显示每行代码是否被执行过                                    |
| Source code | 对应的源代码，通过颜色高亮显示覆盖情况                                |

## 桩函数使用示例

```cpp
#include <cstdlib>
#include <cstring>
#include <uci.h>

// 分配上下文失败桩函数
struct uci_context* uci_alloc_context_stub_fail() {
    return nullptr;
}

// 查找指针成功桩函数
int uci_lookup_ptr_stub_success(struct uci_context* ctx, struct uci_ptr* ptr, char* str,
                                bool extended) {
    ptr->last = (struct uci_element*)malloc(sizeof(struct uci_element));
    if (ptr->last) {
        ptr->last->type = UCI_TYPE_OPTION;
    }

    ptr->p = (struct uci_package*)malloc(sizeof(struct uci_package));
    ptr->value = NULL;
    ptr->flags = uci_ptr::UCI_LOOKUP_COMPLETE;

    ptr->o = (struct uci_option*)malloc(sizeof(struct uci_option));
    if (ptr->o) {
        ptr->o->type = UCI_TYPE_STRING;
        ptr->o->v.string = strdup("test_value");
    }

    return UCI_OK;
}

// 设置操作成功桩函数
int uci_set_stub_success(struct uci_context* ctx, struct uci_ptr* ptr) {
    return UCI_OK;
}

// 保存操作成功桩函数
int uci_save_stub_success(struct uci_context* ctx, struct uci_package* p) {
    return UCI_OK;
}

// 提交操作成功桩函数
int uci_commit_stub_success(struct uci_context* ctx, struct uci_package** p, bool overwrite) {
    return UCI_OK;
}

// 提交操作失败桩函数
int uci_commit_stub_fail(struct uci_context* ctx, struct uci_package** p, bool overwrite) {
    return UCI_FRR_UNKNOWN;
}

// 卸载操作成功桩函数
int uci_unload_stub_success(struct uci_context* ctx, struct uci_package* p) {
    return UCI_OK;
}

// 释放上下文成功桩函数
void uci_free_context_stub_success(struct uci_context* ctx) {
    // 桩函数实现为空
}
```

:::{admonition} 如何对 static 函数或变量进行打桩？

对于 `static` 函数，由于作用域限制无法直接打桩，但可以通过间接方式模拟。考虑到 `static` 函数必然在同一文件的其他位置被调用，可以针对调用点进行测试。对于 `static` 变量，通常会在非 `static` 函数中被赋值，因此只需对这些函数进行打桩，即可控制 `static` 变量的值，使其符合测试预期。
:::

:::{admonition} 桩函数不生效的解决方案

当编译器将函数优化为内联函数时，会导致桩函数失效。解决方法是在需要打桩的函数声明前添加 `__attribute__((noinline))` 属性，例如：

```cpp
__attribute__((noinline)) bool stop_while_1_stub() {
    return true;
}
```

:::

:::{admonition} qemu: uncaught target signal 11 (Segmentation fault) - core dumped

当被测试函数需要指针类型的参数时，必须确保传入有效的内存地址。正确做法是：

1. **声明变量**：先定义一个具体类型的变量
2. **获取地址**：使用取地址运算符 `&` 获取该变量的内存地址
3. **传入函数**：将地址传递给需要指针参数的函数

```cpp
// 正确示例
int actual_variable;         // 1. 声明实际变量
test_func(&actual_variable); // 2. 获取地址并传入函数

// 错误示例：传入未初始化的野指针
int* wild_pointer;       // 未初始化的指针
test_func(wild_pointer); // 可能导致段错误或未定义行为
```

**核心原则**：永远不要将未初始化的指针传递给函数，这会导致程序崩溃或不可预测的行为。
:::

:::{admonition} 屏蔽相关代码的统计

如需从覆盖率统计中排除特定代码，请在源代码中添加对应的屏蔽注释并重新编译。重新生成的库文件在运行时将忽略被标记的代码，使其不参与覆盖率统计。

支持以下屏蔽方式：

- **多行屏蔽**：在目标代码段起始处添加 `// LCOV_EXCL_START`，在结束处添加 `// LCOV_EXCL_STOP`
- **单行屏蔽**：在代码行末尾添加 `// LCOV_EXCL_LINE`
- **分支屏蔽**：仅排除分支统计，保留代码执行统计，在分支判断语句后添加 `// LCOV_EXCL_BR_LINE`

示例：

```cpp
// LCOV_EXCL_START
void unused_function() {
    // 此函数不会被统计
}
// LCOV_EXCL_STOP

void active_function() {
    log("running");  // LCOV_EXCL_LINE
    if (condition) { // LCOV_EXCL_BR_LINE
        // 此分支不纳入分支统计
    }
}
```

:::
