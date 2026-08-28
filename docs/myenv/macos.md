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

## VirtualBox 增强功能

设备 - 安装增强功能

```bash
sudo mount /dev/cdrom /mnt
sudo ./VBoxLinuxAdditions-arm64.run
```

## Virtual Box（VS Code Remote-SSH）

下面的步骤在 Ubuntu 虚拟机中安装并启动 SSH 服务器：

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

在 VirtualBox 中配置网络端口转发：选中 Ubuntu 虚拟机，点击 `设置` > `网络` > `Adapter 1`，确认 `Attached to` 为 `NAT`，点击 `高级` > `端口转发`，新增规则：

名称设为 `ssh`，协议 `TCP`，主机 IP 填 `127.0.0.1`，主机端口设 `2222`，子系统端口设 `22`。

在 Mac 的 VS Code 中安装 `Remote - SSH` 扩展，按 `Ctrl + Shift + P` 搜索 `Remote-SSH: Add New SSH Host`，输入 `ssh <你的Ubuntu用户名>@127.0.0.1 -p 2222` 并保存配置；再次按 `Ctrl + Shift + P` 搜索 `Remote-SSH: Connect to Host`，选择已添加的主机，即可远程连接 Ubuntu 虚拟机。

## 快捷键

需求：在 Mac 上使用 Windows 的快捷键。

- 安装 <https://karabiner-elements.pqrs.org/>
- 登录 <https://ke-complex-modifications.pqrs.org/>
- 导入插件 `Windows shortcuts on macOS`
- 导入插件 `Left Shift -> Change to/from English input`

## 鼠标滚轮操作

安装 Scroll Reverser：<https://pilotmoon.com/scrollreverser/>
