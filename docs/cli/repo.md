# repo

在管理多个 Git 仓库时，`repo` 命令简化了管理过程。它的存在不是为了代替 `git`，而是为了更好地管理仓库。

如需详细了解 `repo` 命令，请参阅 <https://source.android.com/docs/setup/create/repo?hl=zh-cn>。

## init

```bash
# 初始化仓库，-u 指定要使用的清单文件（manifest）所在位置
repo init -u https://android.googlesource.com/platform/manifest

# --depth=1 只检出最近的一次提交
repo init --depth=1 -u https://android.googlesource.com/platform/manifest
```

## manifest

```bash
# 查看被 repo 管理的各个仓库的远程仓库名称、本地存储路径、当前分支等信息
repo manifest
```

## sync

```bash
# -n 不会下载任何文件，只会显示将要执行的操作
# -l 下载和同步操作
# -j 指定会同时运行的线程数量
repo sync -n -j 4 && repo sync -l -j 16

# -c 只在当前分支上执行同步操作
repo sync -c -n -j 4 && repo sync -c -l -j 16
```
