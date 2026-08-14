# macOS

## 批量修改文件默认打开方式（duti）

在 macOS 上，`duti` 是一款通过命令行批量、精准设置文件默认打开方式的工具，配合 Homebrew 即可快速安装，非常适合开发环境统一配置。

### 安装 duti

```bash
# 安装 duti（依赖 Homebrew）
brew install duti
```

### 常用基础命令

```bash
# 查看某类文件当前的默认打开程序（以 .md 为例）
duti -x .md

# 设置文件默认打开方式
# 格式：duti -s 软件BundleID 后缀名 all
duti -s com.microsoft.VSCode .md all
```

下面是**前端、后端、运维、脚本、配置、文档**等最常用源码/配置文件后缀，统一设置为 VS Code 打开：

```bash
# 文本与标记语言
duti -s com.microsoft.VSCode .md all
duti -s com.microsoft.VSCode .txt all
duti -s com.microsoft.VSCode .rtf all

# Web 前端
duti -s com.microsoft.VSCode .css all
duti -s com.microsoft.VSCode .scss all
duti -s com.microsoft.VSCode .sass all
duti -s com.microsoft.VSCode .less all
duti -s com.microsoft.VSCode .js all
duti -s com.microsoft.VSCode .jsx all
duti -s com.microsoft.VSCode .ts all
duti -s com.microsoft.VSCode .tsx all
duti -s com.microsoft.VSCode .vue all
duti -s com.microsoft.VSCode .json all
duti -s com.microsoft.VSCode .xml all

# 后端语言
duti -s com.microsoft.VSCode .py all
duti -s com.microsoft.VSCode .java all
duti -s com.microsoft.VSCode .c all
duti -s com.microsoft.VSCode .cpp all
duti -s com.microsoft.VSCode .h all
duti -s com.microsoft.VSCode .go all
duti -s com.microsoft.VSCode .rs all
duti -s com.microsoft.VSCode .php all
duti -s com.microsoft.VSCode .rb all
duti -s com.microsoft.VSCode .swift all
duti -s com.microsoft.VSCode .kt all
duti -s com.microsoft.VSCode .dart all

# Shell 与运维
duti -s com.microsoft.VSCode .sh all
duti -s com.microsoft.VSCode .zsh all
duti -s com.microsoft.VSCode .bash all
duti -s com.microsoft.VSCode .fish all
duti -s com.microsoft.VSCode .env all
duti -s com.microsoft.VSCode .yml all
duti -s com.microsoft.VSCode .yaml all
duti -s com.microsoft.VSCode .ini all
duti -s com.microsoft.VSCode .conf all
duti -s com.microsoft.VSCode .gitignore all
duti -s com.microsoft.VSCode .dockerignore all
duti -s com.microsoft.VSCode .Makefile all

# 数据与配置
duti -s com.microsoft.VSCode .csv all
duti -s com.microsoft.VSCode .log all
duti -s com.microsoft.VSCode .sql all
```

## VirtualBox 增强功能

设备 - 安装增强功能

```bash
sudo mount /dev/cdrom /mnt
sudo ./VBoxLinuxAdditions-arm64.run
```

## VS Code

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

在 VirtualBox 中配置网络端口转发：选中 Ubuntu 虚拟机，点击 `设置` > `网络` > `Adapter 1`，确认 `Attached to` 为 `NAT`，点击 `高级` > `端口转发`，新增规则：

名称设为 `ssh`，协议 `TCP`，主机 IP 填 `127.0.0.1`，主机端口设 `2222`，Guest 端口设 `22`。

在 Mac 的 VS Code 中安装 `Remote - SSH` 扩展，按 `Ctrl + Shift + P` 搜索 `Remote-SSH: Add New SSH Host`，输入 `ssh <你的Ubuntu用户名>@127.0.0.1 -p 2222` 并保存配置；再次按 `Ctrl + Shift + P` 搜索 `Remote-SSH: Connect to Host`，选择已添加的主机，即可远程连接 Ubuntu 虚拟机。

## 快捷键

需求：在 Mac 上使用 Windows 的快捷键。

- 安装 <https://karabiner-elements.pqrs.org/>
- 登录 <https://ke-complex-modifications.pqrs.org/>
- 导入插件 `Windows shortcuts on macOS`
- 导出插件 `Left Shift -> Change to/from English input`

## 鼠标滚轮操作

安装 Scroll Reverser：<https://pilotmoon.com/scrollreverser/>
