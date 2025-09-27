# gcov

gcov 是 GCC 配套的测试覆盖率分析工具，用于统计代码被执行的情况，帮助开发者发现程序中未经测试的部分。

## 使用方法

### 编译阶段

在由 `.c` 源文件生成 `.o` 目标文件时，添加 `--coverage` 编译选项：

```makefile
$(OBJS): %.o: %.c
	$(CC) $(CFLAGS) --coverage -c $< -o $@
```

在链接阶段生成可执行文件时，同样需要添加 `--coverage` 选项：

```makefile
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) --coverage -o $@ $^
```

```{note}
`--coverage` 是 GCC 提供的宏选项，它等价于同时使用以下三个选项：

- `-fprofile-arcs`：编译时插桩，用于记录代码执行路径
- `-ftest-coverage`：生成程序结构信息文件
- `-lgcov`：链接覆盖率运行时支持库
```

## 生成覆盖率报告

### 1. 运行程序生成数据文件

执行编译后的程序：

```bash
./your_program
```

程序运行后会生成 `.gcda`（运行时数据）和 `.gcno`（程序结构信息）文件。

### 2. 生成原始覆盖率数据

对每个需要分析的源文件执行 gcov 命令：

```bash
gcov main.c
```

此命令会生成对应的 `.gcov` 文本格式报告文件。

### 3. 生成可视化报告

#### 方法一：使用 lcov + genhtml

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

#### 方法二：使用 gcovr（推荐）

```bash
# 安装 gcovr
pip install gcovr

# 生成详细 HTML 报告
gcovr -r . --html --html-details -o coverage_report.html

# 查看报告
firefox coverage_report.html
```

````{dropdown} gcovr 常用参数
```bash
# 生成简洁版 HTML 报告
gcovr -r . --html -o coverage.html

# 包含分支覆盖率信息
gcovr -r . --html --html-details --branches -o coverage.html

# 设置覆盖率通过阈值（低于90%则失败）
gcovr -r . --html --html-details --fail-under-line 90 -o coverage.html

# 排除测试目录文件
gcovr -r . --exclude 'test/*' --html -o coverage.html
```
````

## 结果解读

### HTML 报告内容

- **文件列表视图**：显示每个文件的总体覆盖率百分比
- **行级覆盖详情**：点击文件名可查看每行代码的执行情况
- **颜色标识**：
  - 绿色：已覆盖的代码
  - 红色：未覆盖的代码
  - 黄色：部分覆盖（分支覆盖率）

### 覆盖率指标

- **行覆盖率**（Line Coverage）：已执行代码行占总代码行的比例
- **函数覆盖率**（Function Coverage）：已调用函数占全部函数的比例
- **分支覆盖率**（Branch Coverage）：已执行分支占全部控制流分支的比例

## 桩函数使用示例

```{admonition} 如何对 static 函数或变量进行打桩？

对于 `static` 函数，由于作用域限制无法直接打桩，但可以通过间接方式模拟。考虑到 `static` 函数必然在同一文件的其他位置被调用，可以针对调用点进行测试。对于 `static` 变量，通常会在非 `static` 函数中被赋值，因此只需对这些函数进行打桩，即可控制 `static` 变量的值，使其符合测试预期。

```

````{admonition} 桩函数不生效的解决方案

当编译器将函数优化为内联函数时，会导致桩函数失效。解决方法是在需要打桩的函数声明前添加 `__attribute__((noinline))` 属性，例如：

```cpp
__attribute__((noinline)) bool stop_while_1_stub() {
    return true;
}
```
````

### 桩函数代码示例

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
    if (ptr->last) { ptr->last->type = UCI_TYPE_OPTION; }

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
