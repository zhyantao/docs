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
# 分别将 MacOS 和 Ubuntu 上 cat ~/.ssh/id_ed25519.pub 输出的
# 文本追加到对方的 ~/.ssh/authorized_keys 中
vim ~/.ssh/authorized_keys

# 在 macOS 上打开远程登录：系统设置 -> 通用 -> 共享 -> 远程登录 -> 打开

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

## Multipass

如果使用 Multipass UI 界面启动 Shell，默认走的是 `~/.bash_profile`，如果用户修改了 `~/.bashrc`，想每次启动 Shell 都生效，需要运行下面的指令：

```bash
echo '. ~/.bashrc' >> ~/.bash_profile
```
