# 杂项工具

## MPV

### 安装

```bash
pacman -S mingw-w64-ucrt-x86_64-mpv
```

### 配置

在 `mpv.exe` 所在目录新建一个 `scripts` 目录，将 [autoload.lua](https://github.com/mpv-player/mpv/blob/master/TOOLS/lua/autoload.lua) 放在这里。

更多脚本，请参考 <https://github.com/mpv-player/mpv/wiki/User-Scripts>。

## rbenv

使用 rbenv 管理不同的 Ruby 版本。

### 安装 rbenv

```bash
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
exec $SHELL

git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
exec $SHELL
```

### 安装 Ruby

```bash
rbenv install 3.3.6
rbenv global 3.3.6
```

## repo

在管理多个 Git 仓库时，`repo` 命令简化了管理过程。它的存在不是为了代替 `git`，而是为了更好地管理仓库。

如需详细了解 `repo` 命令，请参阅 <https://source.android.com/docs/setup/create/repo?hl=zh-cn>。

### init

```bash
# 初始化仓库，-u 指定要使用的清单文件（manifest）所在位置
repo init -u https://android.googlesource.com/platform/manifest

# --depth=1 只检出最近的一次提交
repo init --depth=1 -u https://android.googlesource.com/platform/manifest
```

### 查看清单与仓库信息

```bash
# 查看当前使用的清单文件（manifest）内容
repo manifest

# 查看被 repo 管理的各个仓库的远程仓库名称、本地存储路径、当前分支等信息
repo info
repo list
```

### sync

```bash
# -n 不会下载任何文件，只会显示将要执行的操作
# -l 下载和同步操作
# -j 指定会同时运行的线程数量
repo sync -n -j 4 && repo sync -l -j 16

# -c 只在当前分支上执行同步操作
repo sync -c -n -j 4 && repo sync -c -l -j 16
```
