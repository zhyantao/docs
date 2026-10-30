# Multipass

在 macOS 上，可以用 [Multipass](https://documentation.ubuntu.com/multipass/latest/) 快速启动一个 Ubuntu 虚拟机，然后在虚拟机里按 `qemu.md` 的 Ubuntu 步骤编译工具链，避免直接在宿主机上配置环境。

## 1. 安装 Multipass

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

Multipass 以 snap 包发布，Ubuntu 默认已带 snapd。

```bash
sudo snap install multipass
multipass version
```

确认当前用户在可访问 Multipass socket 的组内（一般是 `sudo`）：

```bash
ls -l /var/snap/multipass/common/multipass_socket
groups | grep sudo
```

:::
:::{tab-item} macOS
:sync: macos

要求 macOS 14 Sonoma 及以上，M 系列或 Intel 均可。从[官方下载页](https://canonical.com/multipass/install)下载 `.pkg` 安装包，按提示安装（需要管理员权限）。

```bash
multipass version
```

默认使用 QEMU 作为虚拟化后端，如需改用 Apple Virtualization 框架：

```bash
multipass set local.driver=applevz
```

:::
:::{tab-item} Windows
:sync: windows

支持 Windows 10 或 11 的 Home、Pro、Enterprise 版本，系统版本至少 1809（October 2018 Update），并需要启用 Virtual Machine Platform 功能。

从[官方下载页](https://canonical.com/multipass/install)下载 `.msi` 安装包并运行，安装过程需要管理员权限。也可以用包管理器安装，但官方不提供支持。

安装后以普通用户身份打开 Command Prompt 或 PowerShell：

```powershell
multipass version
```

:::
::::

> 无论宿主机是哪种系统，虚拟机里都是 Ubuntu，所以后面各节的命令（除宿主机路径外）在三个平台上通用，虚拟机内的编译步骤都按 `qemu.md` 的 Ubuntu 标签页执行。

## 2. 创建虚拟机

`multipass launch` 不带镜像参数时使用最新的 Ubuntu LTS。用 `--name` 指定名称，`--cpus`、`--memory`、`--disk` 指定资源（默认只有 1 核、1G 内存、5G 磁盘，不够编译工具链）。

```bash
multipass launch --name riscv-dev --cpus 4 --memory 8G --disk 40G
```

> 资源数值是建议值：GCC 和 QEMU 编译占用较多内存与磁盘，可以按宿主机配置调整。磁盘大小在创建时指定，之后调整比较麻烦，建议一次给足。

查看可用镜像和已创建的虚拟机：

```bash
multipass images
multipass list
multipass info riscv-dev
```

## 3. 进入虚拟机

交互式登录：

```bash
multipass shell riscv-dev
```

或者在宿主机上直接执行单条命令，`--` 之后是虚拟机内的命令：

```bash
multipass exec riscv-dev -- uname -a
```

进入后，按 `qemu.md` 中 **Ubuntu** 标签页的步骤依次操作即可。

## 4. 宿主机与虚拟机之间传输文件

### 4.1 `transfer`：一次性拷贝

```bash
# 宿主机 -> 虚拟机（家目录）
multipass transfer local_file.txt riscv-dev:.

# 虚拟机 -> 宿主机（当前目录）
multipass transfer riscv-dev:remote_file.txt .

# 拷贝整个目录；目标路径不存在时加 --parents 创建父目录
multipass transfer --recursive riscv-dev:dir .
multipass transfer --parents local_file.txt riscv-dev:non/existent/path/remote_file.txt
```

递归传输不会跟随符号链接。

### 4.2 `mount`：挂载宿主机目录

```bash
multipass mount /host/path riscv-dev:/home/ubuntu/shared
multipass unmount riscv-dev
```

创建时也可以直接挂载：

```bash
multipass launch --name riscv-dev --mount /host/path:/home/ubuntu/shared
```

Windows 上宿主机路径写成 Windows 路径，例如 `C:\Users\me\work`，命令本身不变。

默认是 `classic` 挂载，也可用 `--type=native` 选择基于虚拟化后端的原生挂载。

> 建议把源码克隆和编译放在虚拟机自己的磁盘里（如 `~/`），只用挂载目录交换少量文件，避免在挂载目录里编译。这是经验建议，不是官方要求。

## 5. 虚拟机生命周期

```bash
multipass stop riscv-dev       # 停止，不占用资源
multipass start riscv-dev      # 启动
multipass suspend riscv-dev    # 挂起，保留内存状态
multipass restart riscv-dev    # 重启
```

## 6. 快照

编译前先打一个快照，出问题可以回滚。快照和恢复都要求虚拟机处于停止状态。

```bash
multipass stop riscv-dev
multipass snapshot riscv-dev
multipass snapshots riscv-dev
multipass restore riscv-dev.snapshot1
```

> `restore` 的快照名格式为 `<实例名>.<快照名>`；未指定名称时，默认名称以 `multipass snapshots` 的输出为准。

## 7. 删除虚拟机

`delete` 先把实例标记为已删除，`recover` 可以找回，`purge` 才会永久清除。

```bash
multipass delete riscv-dev
multipass recover riscv-dev    # 反悔时恢复
multipass purge                # 永久清除所有已删除的实例，不可恢复
```
