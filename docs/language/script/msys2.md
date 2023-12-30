# MSYS2

MSYS2 经常被我用来在 Windows 上安装必要的 Linux 开发环境，尤其是当涉及到 Windows 和 Linux 差异时。

MSYS2 设计目标是在 MS Windows 上运行 MinGW 工具链的，它有两套 MinGW 工具链，一个是 mingw32，一个是 mingw64。它们的功能是一样的，都是用于编译 MS Windows 上的代码（能调用 MS Windows 应用程序接口，不能调用 Unix/Linux 系统调用）的，可以生成 “纯净” 的 win32 和 win64 可执行文件。这些可执行文件运行时只依赖 MS Windows 系统的动态库或静态库。另外，MSYS2 自身还带了一个原生 GCC 工具链，它可用于编译 UNIX/Linux 代码，但支持的函数仅限于 POSIX 部分，其他系统调用都不支持，如 Linux 的 epoll、eventfd 等等，所以功能有限。原生 GCC 工具链可编译生成 MS Windows 平台上的可执行文件，但它们的运行必须依赖 msys2xxx.dll。

**开发专业应用软件，不要使用 MSYS2 的原生 GCC 工具链，它只是为了编译 MinGW 工具链而存在的，是制造工具的工具** [^cite-ref-1]。

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

[^cite-ref-1]: http://easior.is-programmer.com/posts/210854.html
