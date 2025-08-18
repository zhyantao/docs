# gcov

gcov 是 GCC 配套的测试覆盖率分析工具，用于发现程序中未经测试的部分。

## 如何使用

由 `.c` 生成 `.o` 文件时，增加编译选项 `--coverage`

```
$(OBJS): %.o: %.c
	$(CC) $(CFLAGS) --coverage -c $< -o $@
```

由 `.o` 生成目标文件时，增加编译选项 `--coverage`

```
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -lgcov -o $@ $^
```

```{note}
`--coverage` 是 GCC 提供的 "宏选项"，它自动组合了三个必要的功能：

- 编译时插桩（`-fprofile-arcs`）
- 生成程序结构信息（`-ftest-coverage`）
- 链接运行时支持库（`-lgcov`）
```

## 生成覆盖率报告

**1、运行程序生成数据文件：**

```bash
./your_program
```

这会生成 `.gcda` 和 `.gcno` 文件

**2、生成原始覆盖率数据：**

```bash
gcov main.c  # 对每个源文件执行
```

生成 `.gcov` 文本报告

**3、生成 HTML 可视化报告：**

方法一：使用 lcov + genhtml

```bash
# 1. 收集覆盖率数据
lcov -c -d . -o coverage.info

# 2. 可选：移除系统头文件数据
lcov -r coverage.info '/usr/include/*' -o coverage_filtered.info

# 3. 生成 HTML 报告
genhtml coverage_filtered.info -o coverage_report

# 4. 查看报告
firefox coverage_report/index.html
```

```{dropdown} lcov 常用参数
# 只收集特定目录的数据
lcov -c -d src/ -o coverage.info

# 合并多个覆盖率数据
lcov -a coverage1.info -a coverage2.info -o total.info
```

方法二：使用 gcovr (推荐)

```bash
# 安装
pip install gcovr

# 生成 HTML 报告
gcovr -r . --html --html-details -o coverage_report.html

# 查看报告
firefox coverage_report.html
```

```{dropdown} gcovr 常用参数
# 生成简洁的 HTML 报告
gcovr -r . --html -o coverage.html

# 包含分支覆盖率
gcovr -r . --html --html-details --branches -o coverage.html

# 设置覆盖率阈值
gcovr -r . --html --html-details --fail-under-line 90 -o coverage.html

# 排除特定目录
gcovr -r . --exclude 'test/*' --html -o coverage.html
```

## 结果解读

**1、HTML 报告内容：**

- 文件列表视图显示每个文件的覆盖率百分比
- 点击文件可查看行级覆盖详情
- 绿色表示已覆盖，红色表示未覆盖
- 黄色表示部分覆盖（分支覆盖率）

**2、覆盖率指标：**

- 行覆盖率（Line Coverage）
- 函数覆盖率（Function Coverage）
- 分支覆盖率（Branch Coverage）
