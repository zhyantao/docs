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
  libncurses5-dev texinfo \
  gcc-riscv64-unknown-elf opensbi u-boot-qemu \
  expect libgmp-dev libmpfr-dev libmpc-dev bison flex
```
:::
:::{tab-item} macOS
:sync: macos
```bash
# 提供 clang/make/git 等基础工具链
xcode-select --install   # 如果已装过会报已存在，忽略即可

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
brew install -y pyenv

# macOS 默认 shell 是 zsh，配置文件是 ~/.zshrc（如果你确实用 bash，改成 ~/.bash_profile）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```
:::
::::

## 3. 安装 Python 3.10

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

## 4. 从源码编译 QEMU

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu
```bash
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
git checkout v11.1.1    # 或用 master 拿最新版
git submodule update --init --recursive

pip install tomli sphinx_rtd_theme
mkdir build && cd build
../configure --target-list=riscv64-softmmu,riscv32-softmmu
make -j"$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
sudo make install
cd ../..
qemu-system-riscv64 --version
```
:::
:::{tab-item} macOS
:sync: macos
```bash
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
git checkout v11.1.1    # 或用 master 拿最新版
git submodule update --init --recursive

pip install tomli sphinx_rtd_theme
export LIBRARY_PATH="$(brew --prefix)/lib${LIBRARY_PATH:+:$LIBRARY_PATH}"
mkdir build && cd build
../configure --target-list=riscv64-softmmu,riscv32-softmmu
make -j"$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
sudo make install
cd ../..
qemu-system-riscv64 --version
```
:::
::::

## 5. 从源码编译 GDB

```bash
git clone https://sourceware.org/git/binutils-gdb.git
cd binutils-gdb
git checkout gdb-17.2-release   # 或用 master 拿最新版

mkdir build && cd build
```

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu
```bash
../configure --target=riscv64-unknown-elf \
             --enable-multilib \
             --disable-werror \
             --with-python=/usr/bin/python3 \
             --enable-tui=yes
```
:::
:::{tab-item} macOS
:sync: macos
```bash
../configure --target=riscv64-unknown-elf \
             --enable-multilib \
             --disable-werror \
             --with-python="$(pyenv root)/versions/3.10.14/bin/python3" \
             --enable-tui=yes \
             --with-gmp=/opt/homebrew/opt/gmp \
             --with-mpfr=/opt/homebrew/opt/mpfr
```
:::
::::

```bash
make -j"$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
sudo make install
cd ../..
```

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu
Ubuntu 无需操作。
:::
:::{tab-item} macOS
:sync: macos
macOS 专属：给自编译的 GDB 做代码签名，否则会因 SIP 限制无法调试进程。

```bash
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

# 1. 生成带 codeSigning 扩展的自签名证书（私钥 + 证书）
openssl req -x509 -newkey rsa:2048 -keyout gdb-cert.key -out gdb-cert.pem \
  -days 3650 -nodes -subj "/CN=gdb-cert" \
  -addext "keyUsage=critical,digitalSignature" \
  -addext "extendedKeyUsage=critical,codeSigning"

# 2. 打包成 p12（导入钥匙串需要这个格式），设置一个临时密码
openssl pkcs12 -export -out gdb-cert.p12 \
  -inkey gdb-cert.key -in gdb-cert.pem -passout pass:temp123

# 3. 导入到登录钥匙串，并授权 codesign 使用该私钥（免弹窗）
security import gdb-cert.p12 -k ~/Library/Keychains/login.keychain-db \
  -P temp123 -T /usr/bin/codesign -A

# 4. 把证书加入信任设置，指定用于代码签名场景
security add-trusted-cert -d -r trustRoot \
  -k ~/Library/Keychains/login.keychain-db gdb-cert.pem

# 5. 清理明文密钥/密码文件（可选，安全起见）
rm -f gdb-cert.key gdb-cert.p12

# 验证证书是否可用
security find-certificate -c gdb-cert

# 能找到就说明证书已经在钥匙串里了，接着签名
codesign --entitlements gdb-entitlement.xml -fs gdb-cert "$(command -v riscv64-unknown-elf-gdb)"
```
:::
::::

```bash
riscv64-unknown-elf-gdb --version
```

## 6. 配置 gdb 美化输出

```bash
cp ~/.gdbinit ~/.gdbinit.bak 2>/dev/null
wget -P ~ https://git.io/.gdbinit
```
