# MSYS2

MSYS2 经常被我用来在 Windows 上安装必要的 Linux 开发环境，尤其是当涉及到 Windows 和 Linux 差异时。

下载 MSYS2：<https://www.msys2.org/>。

## 更新 MSYS2

```bash
pacman -Syuu
```

## 安装基础开发环境

```bash
pacman -S base-devel
```

## 安装 MinGW

主要是为了解决 `<sys/socket.h>` 等类的系统头文件缺失。

```bash
# 安装 64 位环境
pacman -S mingw-w64-x86_64-toolchain
pacman -S mingw-w64-x86_64-autotools

# 安装 32 位环境（如有必要）
pacman -S mingw-w64-i686-toolchain
pacman -S mingw-w64-i686-autotools
```

## 安装 Clang++

```bash
pacman -S mingw-w64-x86_64-clang
```

## 安装 GCC

```bash
pacman -S mingw-w64-x86_64-gcc
```
