# Repo

在管理多个 Git 仓库时，`repo` 命令简化了管理过程。它的存在不是为了代替 `git`，而是为了更好地管理仓库。

如需详细了解 `repo` 命令，请参阅 <https://source.android.com/docs/setup/create/repo?hl=zh-cn>。

##  init

```bash
repo init -u https://android.googlesource.com/platform/manifest

# the same but depth=1 for faster clone
repo init  --depth=1 -u https://android.googlesource.com/platform/manifest
```

## sync

```bash
# sync network in 4 threads and sync local in 16 threads
repo sync -n -j 4 && repo sync -l -j 16

# the same but sync only current branch -c
repo sync -c -n -j 4 && repo sync -c -l -j 16
```
