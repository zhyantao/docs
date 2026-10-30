# QEMU

## 1. 安装依赖包

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
sudo apt update
sudo apt install -y \
  git build-essential ninja-build pkg-config \
  libglib2.0-dev libpixman-1-dev libslirp-dev \
  make libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev \
  libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
  libncurses5-dev texinfo opensbi u-boot-qemu \
  expect libgmp-dev libmpfr-dev libmpc-dev bison flex \
  autoconf automake autotools-dev python3 python3-pip \
  gawk gperf libtool patchutils bc libexpat-dev cmake
```

:::
:::{tab-item} macOS
:sync: macos

```bash
# 提供 clang/make/git 等基础工具链
xcode-select --install   # 如果已装过会报已存在，忽略即可

# 先确认已安装 Homebrew：https://brew.sh
brew update
brew install \
  git ninja pkg-config \
  glib pixman libslirp \
  openssl readline sqlite \
  wget curl llvm \
  xz \
  libxml2 libxmlsec1 libffi \
  gmp mpfr libmpc isl bison flex \
  texinfo \
  autoconf automake libtool gawk gnu-sed gmake expat zlib cmake
```

:::
::::

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
echo 'export PATH="$HOME/riscv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

:::
:::{tab-item} macOS
:sync: macos

```bash
echo 'export PATH="$HOME/riscv/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

:::
::::

## 2. 用 pyenv 管理 Python 版本

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

:::
:::{tab-item} macOS
:sync: macos

```bash
brew install pyenv

# macOS 默认 shell 是 zsh，配置文件是 ~/.zshrc（如果你确实用 bash，改成 ~/.bash_profile）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

:::
::::

安装 Python 3.10

> 注意加 `--enable-shared`：后面编译 gdb 需要共享库（`libpython3.10.so` / `.dylib`）才能启用 gdb 的 Python 脚本支持，pyenv 默认编译是静态库，不加这个选项 gdb 编译时会检测不到可用的 Python。

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.14
```

:::
:::{tab-item} macOS
:sync: macos

```bash
# macOS 上还需显式把 openssl/readline/sqlite 的 brew 路径喂给编译器，否则容易缺依赖
export LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix sqlite)/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix readline)/include -I$(brew --prefix sqlite)/include"
export PKG_CONFIG_PATH="$(brew --prefix openssl)/lib/pkgconfig:$(brew --prefix readline)/lib/pkgconfig:$(brew --prefix sqlite)/lib/pkgconfig"

PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.14
```

:::
::::

```bash
pyenv global 3.10.14      # 设为全局默认；只想局部生效改用 pyenv local
python --version          # 验证：应输出 Python 3.10.14
```

## 3. 从源码编译 QEMU

```bash
# 下载源代码（浅克隆，只取指定版本；需要 master 时去掉 --branch 与 --depth）
git clone --depth 1 --branch v11.1.1 https://gitlab.com/qemu-project/qemu.git
cd qemu

# 安装依赖
pip install tomli sphinx_rtd_theme
```

macOS 需要让链接器找到 Homebrew 的库，Ubuntu 跳过这一步：

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
# 无需额外设置
```

:::
:::{tab-item} macOS
:sync: macos

```bash
export LIBRARY_PATH="$(brew --prefix)/lib${LIBRARY_PATH:+:$LIBRARY_PATH}"
```

:::
::::

```bash
mkdir build && cd build
../configure --prefix=$HOME/riscv --target-list=riscv64-softmmu,riscv32-softmmu
make -j"$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
make install
cd ../..
qemu-system-riscv64 --version
```

## 4. 从源码编译 RISC-V GCC

```bash
git clone https://github.com/riscv-collab/riscv-gnu-toolchain.git
cd riscv-gnu-toolchain
git checkout 2026.08.27   # 固定版本以便复现；可在仓库 tags 中选择更新的版本
# 只拉 newlib 版工具链必需的三个子模块（不拉 glibc/musl/qemu/spike/llvm/gdb 等）
git submodule update --init --depth 1 binutils gcc newlib
```

> GCC 体积仍然较大，首次拉取耗时较长，可以配置代理或使用镜像。GDB 在第 5 节单独编译，所以这里不拉 `gdb` 子模块，并在 `configure` 中加 `--disable-gdb`。

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
./configure --prefix=$HOME/riscv --enable-multilib --disable-gdb
make -j"$(nproc)"
```

:::
:::{tab-item} macOS
:sync: macos

```bash
# 使用 GNU sed / make，避免 BSD 版本导致构建失败
export PATH="$(brew --prefix gnu-sed)/libexec/gnubin:$(brew --prefix gmake)/libexec/gnubin:$PATH"

./configure --prefix=$HOME/riscv --enable-multilib --disable-gdb \
            --with-gmp=$(brew --prefix gmp) \
            --with-mpfr=$(brew --prefix mpfr) \
            --with-mpc=$(brew --prefix libmpc)
make -j"$(sysctl -n hw.ncpu)"
```

:::
::::

`make` 默认构建 newlib 版本（`riscv64-unknown-elf-*`），产物直接安装到 `--prefix` 指定目录，无需再执行 `make install`。

```bash
cd ..
riscv64-unknown-elf-gcc --version
```

## 5. 从源码编译 RISC-V GDB

工具链已经提供了 binutils，这里只编译 GDB 本体，避免重复安装 `as`/`ld` 等工具。两个平台都使用第 2 节的 pyenv Python，以保证带有共享库。

```bash
git clone --depth 1 --branch gdb-17.2-release https://sourceware.org/git/binutils-gdb.git
cd binutils-gdb

mkdir build && cd build
```

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
../configure --prefix=$HOME/riscv \
             --target=riscv64-unknown-elf \
             --disable-werror \
             --disable-binutils --disable-gas --disable-ld --disable-gprof \
             --with-python="$(pyenv root)/versions/3.10.14/bin/python3" \
             --enable-tui=yes
```

:::
:::{tab-item} macOS
:sync: macos

```bash
../configure --prefix=$HOME/riscv \
             --target=riscv64-unknown-elf \
             --disable-werror \
             --disable-binutils --disable-gas --disable-ld --disable-gprof \
             --with-python="$(pyenv root)/versions/3.10.14/bin/python3" \
             --enable-tui=yes \
             --with-gmp="$(brew --prefix gmp)" \
             --with-mpfr="$(brew --prefix mpfr)"
```

:::
::::

```bash
make -j"$(nproc 2>/dev/null || sysctl -n hw.ncpu)" all-gdb
make install-gdb
cd ../..
riscv64-unknown-elf-gdb --version
```

## 6. 配置 gdb 美化输出

使用 [gdb-dashboard](https://github.com/cyrus-and/gdb-dashboard)：

```bash
cp ~/.gdbinit ~/.gdbinit.bak 2>/dev/null
wget -O ~/.gdbinit https://raw.githubusercontent.com/cyrus-and/gdb-dashboard/master/.gdbinit
```

## 7. riscv64-unknown-elf-gdb 调试

1、下载源代码，编译，用 QEMU 启动 kernel.elf 并等待 GDB

```bash
git clone https://github.com/zhyantao/baremental.git
cd baremental
make debug
```

2、新开一个终端，用 GDB 连接调试

```bash
cd baremental
riscv64-unknown-elf-gdb kernel.elf
(gdb) target remote localhost:1234
(gdb) break _start
(gdb) continue
(gdb) next    # 输入一次 next 后持续按 Enter 就能重复 next 指令了
```
