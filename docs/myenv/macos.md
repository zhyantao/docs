# macOS

## 修改默认打开方式

安装 duti：`brew install duti`

```bash
# 查看 macOS 应用的 Bundle Identifier
BUNDLE_ID=$(mdls -name kMDItemCFBundleIdentifier -raw /Applications/Trae\ CN.app)
echo "Bundle ID: $BUNDLE_ID"

# 设置默认打开方式
EXTENSIONS=(
  css scss sass less js jsx ts tsx vue json xml
  py java c cpp h go rs php rb swift kt dart
  sh zsh bash fish env yml yaml ini conf
  gitignore dockerignore Makefile log sql
)

for ext in "${EXTENSIONS[@]}"; do
  duti -s "$BUNDLE_ID" ".$ext" all
done
```


## VS Code Remote-SSH (Multipass)

在 macOS 上运行：

```bash
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub

brew install multipass
```

在 Multipass Ubuntu 上运行：

```bash
# 将 MacOS 上 cat ~/.ssh/id_ed25519.pub 的输出文本追加到 ~/.ssh/authorized_keys 中
vim ~/.ssh/authorized_keys

# 设置 root 用户的密码
sudo passwd
# 设置 ubuntu 用户的密码
sudo passwd ubuntu
```

在 VS Code 中选择 Remote-SSH 插件输入：

```bash
ssh ubuntu@< Ubuntu IP >
```

完成

## 快捷键

需求：在 Mac 上使用 Windows 的快捷键。

- 安装 <https://karabiner-elements.pqrs.org/>
- 登录 <https://ke-complex-modifications.pqrs.org/>
- 导入插件 `Windows shortcuts on macOS`
- 导入插件 `Left Shift -> Change to/from English input`

## 鼠标滚轮操作

安装 Scroll Reverser：<https://pilotmoon.com/scrollreverser/>

## 交叉编译环境

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
  expect

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

# 阶段 4：从源码编译支持 riscv64-unknown-elf 的 gdb
# --with-python 指向 pyenv 装好的那个 python，而不是系统 python3
wget https://mirrors.tuna.tsinghua.edu.cn/gnu/gdb/gdb-13.2.tar.xz
tar -xf gdb-13.2.tar.xz
cd gdb-13.2

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
