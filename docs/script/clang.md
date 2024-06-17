# Clang

## 认识 LLVM 和 Clang

`LLVM`（Low Level Virtual Machine）是一个开源的编译器基础设施项目，它提供了一组模块化和可重用的编译器和工具链技术。`LLVM` 包括一个前端，用于解析源代码并生成中间表示（IR），以及一系列后端，用于将 IR 转换为目标机器代码。

`Clang` 是基于 `LLVM` 构建的 C、C++ 和 Objective-C 编译器。`Clang` 继承了 `LLVM` 的许多特性，如中间表示（IR）和代码优化，同时还提供了一些额外的功能，如代码补全、静态分析和重构工具。

简而言之，`LLVM` 是一个框架，而 `Clang` 是使用该框架构建的编译器。`Clang` 是 `LLVM` 的一个重要组成部分，因为它利用了 `LLVM` 的中间表示和优化技术来提高编译速度和生成更高效的代码。

## 安装 Clang

::::{tab-set}
:::{tab-item} LLVM (x86)
参考 <https://apt.llvm.org>，在安装 LLVM 的同时，也就把 Clang 装好了。
:::
:::{tab-item} LLVM (AArch64)
参考 <https://learn.arm.com/install-guides/llvm-embedded>
:::
::::
