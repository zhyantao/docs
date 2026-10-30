# OrbStack

用 [OrbStack](https://orbstack.dev) 在 macOS 上快速启动 Ubuntu 虚拟机（Linux machine），在里面按 {doc}`qemu` 的 Ubuntu 或 Rocky 9 步骤编译工具链，避免污染宿主机环境。OrbStack 同时提供 Docker 容器支持，启动快、资源占用低。

## 1. 安装

仅支持 macOS（macOS 13+，Apple Silicon 或 Intel）。

```bash
brew install --cask orbstack
```

也可从[官方下载页](https://orbstack.dev/download)下载 `.dmg` 安装。首次启动 OrbStack.app 完成初始化后，命令行工具 `orb`、`orbctl` 和 `docker` 即可使用。

验证：`orb version`

## 2. 创建并进入虚拟机

OrbStack 的虚拟机共享一个内核，CPU 和内存按需动态分配，磁盘按使用量增长，无需为单个虚拟机指定资源。资源上限在全局设置中调整：OrbStack 菜单 -> Settings -> System，或使用命令：

```bash
orbctl config set cpu 8
orbctl config set memory_mib 16384
```

按发行版创建并进入虚拟机：

::::{tab-set}
:::{tab-item} Ubuntu
:sync: ubuntu

```bash
orb create ubuntu riscv-dev
orb shell -m riscv-dev
```

指定版本和架构：

```bash
orb create ubuntu:jammy riscv-dev
orb create -a amd64 ubuntu riscv-dev-x86
```

:::
:::{tab-item} Rocky 9
:sync: rocky

```bash
orb create -a amd64 rocky:9 rocky9
orb shell -m rocky9
```

使用原生架构时去掉 `-a amd64`：

```bash
orb create rocky:9 rocky9
```

:::
::::

进入后按 `qemu.md` 中对应的标签页（**Ubuntu** 或 **Rocky 9**）操作。默认用户名与 macOS 用户名一致，并拥有免密 `sudo`。

## 3. 传输文件

OrbStack 自动与宿主机双向共享文件系统，不需要手动挂载：

```bash
# 宿主机 -> 虚拟机
orb push -m riscv-dev local.txt

# 虚拟机 -> 宿主机
orb pull -m riscv-dev remote.txt .
```

- 虚拟机内可直接访问宿主机目录，路径与宿主机一致（如 `/Users/<name>/...`）。
- 宿主机可在 Finder 中访问虚拟机文件，路径为 `~/OrbStack/riscv-dev`。

跨文件系统访问较慢，建议在虚拟机自己的磁盘（如 `~/`）里克隆和编译，共享目录只用来交换少量文件。

## 4. 常用管理命令

```bash
# 查看虚拟机
orb list

# 停止（start 启动）
orb stop riscv-dev

# 在虚拟机中执行单条命令
orb -m riscv-dev uname -a

# 克隆（用作"快照"，编译前备份）
orb clone riscv-dev riscv-dev-backup

# 导出 / 导入
orb export riscv-dev riscv-dev.tar.zst
orb import riscv-dev.tar.zst

# 删除
orb delete riscv-dev
```
