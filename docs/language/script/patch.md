# patch

补丁（Patch）是透过更新计算机程序或支持文件，用来修补软件问题的资料程序。
Linux 一般自带了 `diff` 和 `patch` 这两个命令，无需自己安装。

## diff

`diff` 命令主要用于制作补丁。`diff` 可以比较两个东西，并可同时记录下二者的区别。

```bash
# Compare files (lists changes to turn `old_file` into `new_file`):
diff old_file new_file

# Compare files, ignoring white spaces:
diff --ignore-all-space old_file new_file

# Compare files, showing the differences side by side:
diff --side-by-side old_file new_file

# Compare files, showing the differences in unified format 
# (as used by `git diff`):
diff --unified old_file new_file

# Compare directories recursively 
# (shows names for differing files/directories as well as changes made to files):
diff --recursive old_directory new_directory

# Compare directories, only showing the names of files that differ:
diff --recursive --brief old_directory new_directory

# Create a patch file for Git from the differences of two text files, 
# treating nonexistent files as empty:
diff --text --unified --new-file old_file new_file > diff.patch
```

## patch

`patch` 主要用于应用补丁。将 `diff` 记录的结果（即补丁）应用到相应文件（夹）上。

```bash
# Apply a patch using a diff file 
# (filenames must be included in the diff file)
patch < patch.diff

# Apply a patch to a specific file
patch path/to/file < patch.diff

# Patch a file writing the result to a different file:
patch path/to/input_file -o path/to/output_file < patch.diff

# 在当前目录下应用补丁文件（可以同时对多个文件打补丁，打补丁的依据是补丁中出现的文件目录名）
# p1 表示忽略第 1 级目录
patch -p1 < patch.diff
# 如果不想忽略第 1 级目录，需要用下面的命令
patch -p0 < patch.diff

# Apply the reverse of a patch:
patch -R < patch.diff
```
