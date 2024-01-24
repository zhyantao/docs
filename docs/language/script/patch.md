# patch

## 制作补丁

`diff` 命令主要用于制作补丁。`diff` 可以比较两个文件，并可同时记录下二者的区别。

```bash
# （推荐）对已被 git track 的文件（夹）制作补丁
git diff > diff.patch

# （推荐）对未被 git track 的文件（夹）制作补丁
git diff <old_file> <new_file> > diff.patch

# 对比 <old_file> 和 <new_file>，将差异输出到屏幕
diff <old_file> <new_file>

# 对比 <old_file> 和 <new_file>，忽略所有空格
diff --ignore-all-space <old_file> <new_file>

# 对比 <old_file> 和 <new_file>，按左右两侧展示对比结果
diff --side-by-side <old_file> <new_file>

# 对比 <old_file> 和 <new_file>，以 unified 风格展示对比结果
diff --unified <old_file> <new_file>

# 递归对比 <old_dir> 和 <new_dir> 下的所有文件
diff --recursive <old_dir> <new_dir>

# 递归对比 <old_dir> 和 <new_dir> 下的所有文件，仅展示变动文件的文件名
diff --recursive --brief <old_dir> <new_dir>

# 将 <old_file> 和 <new_file> 的差异写入文件（不存在的文件当做空文件处理）
diff --text --unified --new-file <old_file> <new_file> > diff.patch
```

## 应用补丁

`patch` 主要用于应用补丁。将 `diff` 记录的结果（即补丁）应用到相应文件（夹）上。

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
前文提到 **忽略第 n 级目录**，解释一下这句话，以下述为例：

```text
--- a/src/module/filename.c
+++ b/src/module/filename.c
```

在这里，`a` 表示第 1 级目录，`src` 是第 2 级目录，以此类推。

假设你运行了 `patch -p2 ...` （忽略前 2 级目录），那么程序就会从当前目录去找 `./module/filename.c`，并在这个文件上应用补丁。
````
