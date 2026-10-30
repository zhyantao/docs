# QEMU

## 1. 安装依赖包

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
sudo apt update
sudo apt install -y \
  build-essential git curl wget cmake ninja-build pkg-config expect \
  autoconf automake autotools-dev libtool bison flex gawk gperf texinfo patchutils bc \
  libglib2.0-dev libpixman-1-dev libslirp-dev \
  libgmp-dev libmpfr-dev libmpc-dev libexpat-dev \
  device-tree-compiler libboost-regex-dev libboost-system-dev \
  opensbi u-boot-qemu \
  python3 python3-pip llvm xz-utils tk-dev \
  libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
  libncurses-dev libncursesw5-dev libffi-dev liblzma-dev libxml2-dev libxmlsec1-dev
```

:::
:::{tab-item} Rocky 9
:sync: rocky

```bash
# ninja-build、texinfo、gperf 等位于 CRB / EPEL，需先启用
sudo dnf install -y dnf-plugins-core epel-release
sudo dnf config-manager --set-enabled crb

sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y \
  git wget cmake ninja-build pkgconf-pkg-config expect \
  autoconf automake libtool bison flex gawk gperf texinfo patchutils bc \
  glib2-devel pixman-devel libslirp-devel \
  gmp-devel mpfr-devel libmpc-devel expat-devel \
  dtc boost-devel \
  python3 python3-pip llvm xz tk-devel \
  openssl-devel zlib-devel bzip2-devel readline-devel sqlite-devel \
  ncurses-devel libffi-devel xz-devel libxml2-devel xmlsec1-devel
```

> Rocky 9 预装 `curl-minimal`，与完整版 `curl` 冲突，已能满足后文 `curl https://pyenv.run | bash`，因此不安装 `curl`。软件源中没有 `opensbi`、`u-boot-qemu`，从源码编译 QEMU 用不到，已省略。

:::
:::{tab-item} macOS
:sync: macos

```bash
# 提供 clang/make/git 等基础工具链
xcode-select --install

# 先确认已安装 Homebrew：https://brew.sh
brew update
brew install \
  git curl wget cmake ninja pkg-config gnu-sed gmake \
  autoconf automake libtool bison flex gawk texinfo \
  glib pixman libslirp \
  gmp mpfr libmpc isl expat \
  dtc boost \
  openssl readline sqlite xz zlib libffi libxml2 libxmlsec1
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
:::{tab-item} Rocky 9
:sync: rocky

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
:::{tab-item} Rocky 9
:sync: rocky

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
:::{tab-item} Rocky 9
:sync: rocky

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

macOS 需要让链接器找到 Homebrew 的库，Ubuntu 和 Rocky 9 跳过这一步：

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
# 无需额外设置
```

:::
:::{tab-item} Rocky 9
:sync: rocky

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

## 4. 从源码编译 RISC-V GCC 与 GDB

GDB 作为 `riscv-gnu-toolchain` 的子模块一起编译，与 GCC、binutils 共用同一个安装前缀。

```bash
git clone https://github.com/riscv-collab/riscv-gnu-toolchain.git
cd riscv-gnu-toolchain
git checkout 2026.08.27
# 只拉 newlib 版工具链必需的四个子模块（不拉 glibc/musl/qemu/spike/llvm 等）
git submodule update --init --depth 1 binutils gcc newlib gdb
```

> 子模块体积较大，首次拉取耗时较长，可以配置代理或使用镜像。GDB 会自动探测 PATH 中的 Python，因此编译前请确认第 2 节的 `pyenv global 3.10.14` 已生效。

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
./configure --prefix=$HOME/riscv --enable-multilib
make -j"$(nproc)"
```

:::
:::{tab-item} Rocky 9
:sync: rocky

```bash
./configure --prefix=$HOME/riscv --enable-multilib
make -j"$(nproc)"
```

:::
:::{tab-item} macOS
:sync: macos

```bash
# 使用 GNU sed / make，避免 BSD 版本导致构建失败
export PATH="$(brew --prefix gnu-sed)/libexec/gnubin:$(brew --prefix gmake)/libexec/gnubin:$PATH"

./configure --prefix=$HOME/riscv --enable-multilib \
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
riscv64-unknown-elf-gdb --version

# 验证 gdb 带有 Python 支持
riscv64-unknown-elf-gdb -batch -ex "python print(1)"
```

## 5. 从源码编译 Spike

Spike 是 RISC-V 官方 ISA 模拟器，独立于工具链单独编译。

```bash
git clone --depth 1 https://github.com/riscv-software-src/riscv-isa-sim.git
cd riscv-isa-sim
mkdir build && cd build
../configure --prefix=$HOME/riscv
make -j"$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
make install
cd ../..
spike --help
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
