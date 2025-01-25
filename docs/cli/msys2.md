# MSYS2

MSYS2 可以用来在 Windows 上配置编译工具链，包括 `make`、`cmake`、`gcc` 等。

下载 MSYS2：<https://www.msys2.org>。然后，配置环境变量：

::::{tab-set}
:::{tab-item} 64 位
:sync: 64

```text
D:\msys64\usr\bin
D:\msys64\mingw64\bin
```

:::
:::{tab-item} 32 位
:sync: 32

```text
D:\msys64\usr\bin
D:\msys64\mingw32\bin
```

:::
::::

```{warning}
如果电脑上安装过的 MinGW，确保 make 和 gcc 的位数相同，否则编译出的程序可能无法正常工作。
```

## 切换镜像源

::::{tab-set}
:::{tab-item} 中科大源

```bash
sed -i "s#mirror.msys2.org/#mirrors.ustc.edu.cn/msys2/#g" /etc/pacman.d/mirrorlist*

# 查看更改是否生效
head -n 6 /etc/pacman.d/mirrorlist.msys
```

:::
:::{tab-item} 清华源

```bash
sed -i "s#mirror.msys2.org/#mirrors.tuna.tsinghua.edu.cn/msys2/#g" /etc/pacman.d/mirrorlist*

# 查看更改是否生效
head -n 6 /etc/pacman.d/mirrorlist.msys
```

:::
::::

## 更新 MSYS2

```bash
# 清理旧缓存
pacman -Scc

# 更新软件包列表并升级系统
pacman -Syu
```

## 安装基础开发套件

```bash
pacman -S base-devel
```

## 安装 MinGW

::::{tab-set}
:::{tab-item} 64 位
:sync: 64

```bash
pacman -S mingw-w64-x86_64-toolchain
pacman -S mingw-w64-x86_64-autotools
```

:::
:::{tab-item} 32 位
:sync: 32

```bash
pacman -S mingw-w64-i686-toolchain
pacman -S mingw-w64-i686-autotools
```

:::
::::

## 安装 GCC

::::{tab-set}
:::{tab-item} 64 位
:sync: 64

```bash
pacman -S mingw-w64-x86_64-gcc
```

:::
:::{tab-item} 32 位
:sync: 32

```bash
pacman -S mingw-w64-i686-gcc
```

:::
::::

## 安装 Clang

::::{tab-set}
:::{tab-item} 64 位
:sync: 64

```bash
pacman -S mingw-w64-x86_64-clang
```

:::
:::{tab-item} 32 位
:sync: 32

```bash
pacman -S mingw-w64-i686-clang
```

:::
::::
