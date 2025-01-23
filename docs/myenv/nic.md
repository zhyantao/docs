# 网卡驱动调试技巧

```{note}
替换 `<interface_name>` 和 `your_module` 为实际的接口名称和模块名。
```

## 检查网卡连接状态

### 基本命令

使用 `ip link` 命令检查特定网卡（如 eth0）的状态：

```bash
ip link show eth0
```

### 结果解读

- **正常连接状态**: 包含 `state UP`

```text
9: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br-lan state UP mode DEFAULT group default qlen 1000
    link/ether 40:00:c0:fe:01:05 brd ff:ff:ff:ff:ff:ff
```

- **未连接状态**: 包含 `state DOWN` 或者 `state UNKNOWN`

```text
9: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br-lan state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether 40:00:c0:fe:01:05 brd ff:ff:ff:ff:ff:ff
```

### 进一步操作

- 查看所有网卡状态：`ip link show`
- 检查网络配置文件，确保配置正确。
- 重启网络服务：
  - Debian/Ubuntu: `sudo systemctl restart networking`
  - CentOS/RHEL: `sudo systemctl restart network`

## 检查驱动是否加载

### 使用 `lsmod` 命令

```bash
lsmod | grep your_module
```

### 检查 `dmesg` 日志

```bash
dmesg | grep your_module
```

### 使用 `modinfo` 命令

```bash
modinfo your_module
```

### 检查 `sysfs` 文件系统

```bash
ls /sys/module/your_module
```

### 使用 `lspci` 或 `lsusb` 命令

- PCI 网卡：`lspci | grep -i network`
- USB 网卡：`lsusb | grep -i network`

### 使用 `ethtool` 命令

查看网卡驱动详细信息：

```bash
ethtool -i <interface_name>
```
