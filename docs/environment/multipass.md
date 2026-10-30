# Multipass

用 [Multipass](https://canonical.com/multipass/install) 快速启动 Ubuntu 虚拟机，在里面按 `qemu.md` 的 Ubuntu 步骤编译工具链，避免污染宿主机环境。

## 1. 安装

::::{tab-set}
:::{tab-item} Ubuntu
```bash
sudo snap install multipass
```
:::
:::{tab-item} macOS
```bash
brew install --cask multipass
```
也可从[官方下载页](https://canonical.com/multipass/install)下载 `.pkg` 安装（macOS 14+）。
:::
:::{tab-item} Windows
从[官方下载页](https://canonical.com/multipass/install)下载 `.msi` 安装（Windows 10/11，需启用 Virtual Machine Platform）。
:::
::::

验证：`multipass version`

## 2. 创建并进入虚拟机

默认配置（1 核 / 1G / 5G）不够编译，需显式指定资源，磁盘创建后难以调整，建议一次给足：

```bash
multipass launch --name riscv-dev --cpus 4 --memory 8G --disk 40G
multipass shell riscv-dev
```

进入后按 `qemu.md` 的 **Ubuntu** 步骤操作。

## 3. 传输文件

```bash
# 宿主机 -> 虚拟机
multipass transfer local.txt riscv-dev:.

# 虚拟机 -> 宿主机
multipass transfer riscv-dev:remote.txt .

# 挂载目录
multipass mount /host/path riscv-dev:/home/ubuntu/shared
```

建议在虚拟机自己的磁盘里克隆和编译，挂载目录只用来交换少量文件。

## 4. 常用管理命令

```bash
# 查看虚拟机
multipass list

# 停止（start 启动）
multipass stop riscv-dev

# 编译前打快照（需先停止）
multipass stop riscv-dev && multipass snapshot riscv-dev

# 回滚（需先停止）
multipass restore riscv-dev.snapshot1

# 删除并永久清除
multipass delete riscv-dev && multipass purge
```
