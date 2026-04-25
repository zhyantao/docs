# patch

## 制作补丁

`git format-patch` 是 Git 推荐使用的补丁制作工具。与 `diff` 相比，它生成的补丁包含作者信息、提交时间、提交日志等元数据，更适合在协作开发中使用。

```bash
# （推荐）生成最近 n 次提交的补丁
git add <files>
git commit -m "Bump iperf3 from 3.20 to 3.21"
git format-patch -1                              # 最近 1 次提交
git format-patch -2                              # 最近 2 次提交

# （推荐）生成指定 commit 的补丁（仅包含该 single commit）
git format-patch -1 <commit_id>

# （推荐）生成两个 commit 之间的所有补丁
git format-patch <since_commit>..<until_commit>  # since～until 之间的提交
git format-patch <since_commit>..                # since 之后的所有提交

# （推荐）生成当前分支相对于 master 的独特提交
git format-patch master                          # 当前分支比 master 多的提交

# （可选）将所有补丁合并成一个文件（⚠️ 可能丢失邮件线索信息）
git format-patch master --stdout > all-changes.patch

# （补充）纯 diff 风格补丁（不推荐，仅作对比）
git diff > patch.diff                            # 对已 track 的文件制作补丁
git diff <old_file> <new_file> > patch.diff      # 对未 track 的文件制作补丁
```

```{tip}
`git format-patch` 生成的补丁文件默认命名格式为 `0001-commit-subject.patch`，文件名按提交顺序自动编号，便于批量应用。
```

## 应用补丁

### 应用 git format-patch 生成的补丁（推荐）

使用 `git am`（apply mailbox）应用 `format-patch` 生成的补丁，可以完整保留作者、提交时间、提交日志等信息。

```bash
# 应用单个补丁
git am 0001-fix-bug.patch

# 应用目录下所有补丁（按文件名顺序）
git am *.patch

# 应用时遇到冲突，解决后继续
git add . && git am --resolved

# 跳过当前有冲突的补丁
git am --skip

# 放弃本次应用操作
git am --abort
```

### 应用传统 diff 补丁（不推荐）

```bash
# （单文件打补丁）patch.diff 必须包含文件名，根据文件名应用补丁
patch < patch.diff

# （多文件打补丁）patch.diff 必须包含文件名，根据文件名应用补丁
cd <project_dir>
patch -p1 < patch.diff  # p1 表示忽略第 1 级目录，即 <project_dir>

# （多文件打补丁）patch.diff 必须包含文件名，根据文件名应用补丁
cd <project_dir>/..
patch -p0 < patch.diff

# 对指定文件应用补丁
patch path/to/file < patch.diff

# 对 input_file 应用补丁，但是将应用补丁后的结果写入 output_file
patch path/to/input_file -o path/to/output_file < patch.diff

# 反向应用补丁，即将打过补丁的文件还原
patch -R < patch.diff
```

````{note}
**关于 `-p<n>` 参数的含义**（忽略 n 级目录）

以 `format-patch` 生成的补丁头部为例：

```diff
--- a/src/module/test.c
+++ b/src/module/test.c
```

目录层级解析：
- `a` → 第 1 级目录
- `src` → 第 2 级目录
- `module` → 第 3 级目录

不同参数的行为：
- `patch -p0`：使用完整路径 `a/src/module/test.c`
- `patch -p1`：去掉 `a/`，在当前目录找 `src/module/test.c`
- `patch -p2`：去掉 `a/src/`，在当前目录找 `module/test.c`

```{tip}
使用 `git am` 应用补丁时无需关心 `-p` 参数，系统会自动处理路径信息。
```
````

## 对比：format-patch vs diff

| 特性               | `git format-patch`           | `git diff`             |
| :----------------- | :--------------------------- | :--------------------- |
| 作者信息           | ✅ 包含                      | ❌ 不包含              |
| 提交时间           | ✅ 包含                      | ❌ 不包含              |
| 提交日志           | ✅ 包含                      | ❌ 不包含              |
| 提交 SHA           | ✅ 包含                      | ❌ 不包含              |
| 应用后生成独立提交 | ✅ `git am` 自动生成         | ❌ 需手动 `git commit` |
| 多补丁排序         | ✅ 自动编号                  | ❌ 需手动管理          |
| 适用场景           | 开源协作、邮件审阅、代码合入 | 临时对比、本地快速同步 |

```{tip}
**通用原则**：
- **推荐**：只要是传送给别人的补丁，优先使用 `git format-patch` + `git am` 流程
- **可选**：仅自己临时记录改动，或补丁只用于单个文件同步时，可以考虑 `git diff` + `patch`
```
