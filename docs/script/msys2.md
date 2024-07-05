# MSYS2

MSYS2 可以用来在 Windows 上配置编译工具链，包括 `make`、`cmake`、`gcc` 等。

下载 MSYS2：<https://www.msys2.org>。然后，配置环境变量：

```text
D:\msys64\usr\bin
D:\msys64\mingw64\bin
```

## 切换镜像源

::::{tab-set}
:::{tab-item} 中科大源
```bash
# modify config files
sed -i "s#mirror.msys2.org/#mirrors.ustc.edu.cn/msys2/#g" /etc/pacman.d/mirrorlist*

# verify the modification
head -n 6 /etc/pacman.d/mirrorlist.msys

# clear cache
pacman -Scc

# update mirrors
pacman -Sy
```
:::
:::{tab-item} 清华源
```bash
# modify config files
sed -i "s#mirror.msys2.org/#mirrors.tuna.tsinghua.edu.cn/msys2/#g" /etc/pacman.d/mirrorlist*

# verify the modification
head -n 6 /etc/pacman.d/mirrorlist.msys

# clear cache
pacman -Scc

# update mirrors
pacman -Syu
```
:::
::::

## 更新 MSYS2

```bash
pacman -Syuu
```

## 安装基础开发环境

```bash
pacman -S base-devel
```

## 安装 MinGW

```bash
# 安装 32 位环境（推荐）
pacman -S mingw-w64-i686-toolchain
pacman -S mingw-w64-i686-autotools

# 安装 64 位环境（如有必要）
pacman -S mingw-w64-x86_64-toolchain
pacman -S mingw-w64-x86_64-autotools

```

## 安装 Clang++

```bash
pacman -S mingw-w64-x86_64-clang
```

## 安装 GCC

```bash
pacman -S mingw-w64-x86_64-gcc
```

## 配置环境变量

- 配置 `D:\msys64\usr\bin`：使用 `make` 工具（32 位）；
- 配置 `D:\msys64\mingw32\bin`：使用 `gcc` 工具（32 位）。

```{warning}
如果在电脑上装了多个 MinGW，而 `make` 工具和 `gcc` 工具位数不匹配，会导致编译生成的 `exe` 文件 **运行后没有输出**。
```
