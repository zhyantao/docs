# QEMU 仿真环境

## Debian/Ubuntu

```bash
# 阶段 0：安装依赖包
sudo apt update
sudo apt install -y \
  git build-essential ninja-build pkg-config \
  libglib2.0-dev libpixman-1-dev libslirp-dev \
  make libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev \
  libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
  libncurses5-dev texinfo \
  gcc-riscv64-unknown-elf opensbi u-boot-qemu \
  expect libgmp-dev libmpfr-dev libmpc-dev bison flex

# 阶段 1：安装 pyenv，用于管理 Python 版本
curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# 阶段 2：安装 Python 3.10，注意加 --enable-shared
# 后面编译 gdb 需要 libpython3.10.so 这个共享库才能启用 gdb 的 python 脚本支持，
# pyenv 默认编译是静态库，不加这个选项 gdb 编译时会检测不到可用的 python
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.14
pyenv global 3.10.14      # 设为全局默认；只想局部生效改用 pyenv local
python --version          # 验证：应输出 Python 3.10.14

# 阶段 3：从源码编译 QEMU（riscv64 + riscv32 target）
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
git checkout v11.1.1
git submodule update --init --recursive

pip install tomli
mkdir build && cd build
../configure --target-list=riscv64-softmmu,riscv32-softmmu
make -j$(nproc)
sudo make install
cd ../..
qemu-system-riscv64 --version

# 阶段 4：从源码编译 GDB（riscv64 + riscv32 target）
git clone https://sourceware.org/git/binutils-gdb.git
cd binutils-gdb
git checkout gdb-17.2-release   # 或用 master 拿最新版

mkdir build && cd build
../configure --target=riscv64-unknown-elf \
             --enable-multilib \
             --disable-werror \
             --with-python=/usr/bin/python3 \
             --enable-tui=yes
make -j$(nproc)
sudo make install
cd ../..
riscv64-unknown-elf-gdb --version

# 阶段 5：配置 gdb 美化输出（gdb-dashboard）
cp ~/.gdbinit ~/.gdbinit.bak 2>/dev/null
wget -P ~ https://git.io/.gdbinit
```

## macOS

```bash
# 阶段 -1：安装 Xcode 命令行工具（提供 clang/make/git 等基础工具链）
xcode-select --install   # 如果已装过会报已存在，忽略即可

# 阶段 0：安装依赖包（Homebrew）
# 先确认已安装 Homebrew：https://brew.sh
brew update
brew install -y \
  git ninja pkg-config \
  glib pixman libslirp \
  openssl readline sqlite \
  wget curl llvm \
  xz \
  libxml2 libxmlsec1 libffi \
  gmp mpfr libmpc bison flex \
  gdb \
  coreutils   # 提供 gnproc，替代 Linux 的 nproc

# RISC-V 交叉编译工具链 + 固件（对应原来的 gcc-riscv64-unknown-elf / opensbi / u-boot-qemu）
brew tap riscv-software-src/riscv
brew trust riscv-software-src/riscv
brew install -y riscv-tools    # 内含交叉 gcc/binutils；opensbi、u-boot 需另行编译或从官方 release 下载二进制

# 阶段 1：安装 pyenv，用于管理 Python 版本
brew install -y pyenv

# macOS 默认 shell 是 zsh，配置文件是 ~/.zshrc（如果你确实用 bash，改成 ~/.bash_profile）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# 阶段 2：安装 Python 3.10，注意加 --enable-shared
# GDB 编译需要 libpython3.10.dylib 这个共享库才能启用 Python 脚本支持，
# pyenv 默认编译是静态库，不加这个选项 GDB 编译时会检测不到可用的 Python。
# macOS 上还需显式把 openssl/readline/sqlite 的 brew 路径喂给编译器，否则容易缺依赖。
export LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix sqlite)/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix readline)/include -I$(brew --prefix sqlite)/include"
export PKG_CONFIG_PATH="$(brew --prefix openssl)/lib/pkgconfig:$(brew --prefix readline)/lib/pkgconfig:$(brew --prefix sqlite)/lib/pkgconfig"

PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.14
pyenv global 3.10.14      # 设为全局默认；只想局部生效改用 pyenv local
python --version          # 验证：应输出 Python 3.10.14

# 阶段 3：从源码编译 QEMU（riscv64 + riscv32 target）
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
git checkout v11.1.1
git submodule update --init --recursive

pip install tomli
mkdir build && cd build
../configure --target-list=riscv64-softmmu,riscv32-softmmu
make -j"$(sysctl -n hw.ncpu)"
sudo make install
cd ../..
qemu-system-riscv64 --version

# 阶段 4：从源码编译 GDB（riscv64 + riscv32 target）
git clone https://sourceware.org/git/binutils-gdb.git
cd binutils-gdb
git checkout gdb-17.2-release   # 或用 master 拿最新版

mkdir build && cd build
../configure --target=riscv64-unknown-elf \
             --enable-multilib \
             --disable-werror \
             --with-python="$(pyenv root)/versions/3.10.14/bin/python3" \
             --enable-tui=yes \
             --with-gmp=/opt/homebrew/opt/gmp \
             --with-mpfr=/opt/homebrew/opt/mpfr
make -j"$(sysctl -n hw.ncpu)"
sudo make install
cd ../..

# --- macOS 特有步骤：给自编译的 GDB 做代码签名，否则会因 SIP 限制无法调试进程 ---
cat > gdb-entitlement.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.debugger</key>
    <true/>
</dict>
</plist>
EOF

# 生成一个自签名证书（仅需一次，可在钥匙串访问.app 里手动做，也可用命令行）
# 手动方式：打开"钥匙串访问" -> 证书助理 -> 创建证书 -> 名称 gdb-cert -> 证书类型: 代码签名 ->
#          在"钥匙串访问"里右键该证书 -> 显示简介 -> 信任 -> 代码签名: 始终信任
security find-certificate -c gdb-cert  # 确认证书已存在后再执行下面这行

codesign --entitlements gdb-entitlement.xml -fs gdb-cert "$(command -v riscv64-unknown-elf-gdb)"

riscv64-unknown-elf-gdb --version

# 阶段 5：配置 gdb 美化输出（gdb-dashboard）
cp ~/.gdbinit ~/.gdbinit.bak 2>/dev/null
wget -P ~ https://git.io/.gdbinit
```
