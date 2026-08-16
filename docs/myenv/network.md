# 网络排障

## 网卡驱动调试技巧

```{note}
替换 `<interface_name>` 和 `your_module` 为实际的接口名称和模块名。
```

### 检查网卡连接状态

#### 基本命令

使用 `ip link` 命令检查特定网卡（如 eth0）的状态：

```bash
ip link show eth0
```

#### 结果解读

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

#### 进一步操作

- 查看所有网卡状态：`ip link show`
- 检查网络配置文件，确保配置正确。
- 重启网络服务：
  - Debian/Ubuntu: `sudo systemctl restart networking`
  - CentOS/RHEL: `sudo systemctl restart network`

### 检查驱动是否加载

#### 使用 `lsmod` 命令

```bash
lsmod | grep your_module
```

#### 检查 `dmesg` 日志

```bash
dmesg | grep your_module
```

#### 使用 `modinfo` 命令

```bash
modinfo your_module
```

#### 检查 `sysfs` 文件系统

```bash
ls /sys/module/your_module
```

#### 使用 `lspci` 或 `lsusb` 命令

- PCI 网卡：`lspci | grep -i network`
- USB 网卡：`lsusb | grep -i network`

#### 使用 `ethtool` 命令

查看网卡驱动详细信息：

```bash
ethtool -i <interface_name>
```

## 如何判断 WAN 口是否已联网

要判断 `wan1` 和 `wan5` 是否已经联网，可以按照以下步骤操作：

### 1. 使用 `ping` 命令

通过 `ping` 命令测试网络连通性。

```bash
ping -I wan1 8.8.8.8
ping -I wan5 8.8.8.8
```

- `-I` 指定网络接口。
- `8.8.8.8` 是 Google 的公共 DNS 服务器。

如果收到回复，说明接口已联网。

### 2. 使用 `ip` 命令

查看接口的 IP 地址和状态。

```bash
ip addr show wan1
ip addr show wan5
```

- 如果接口有 IP 地址且状态为 `UP`，通常表示已联网。

### 3. 使用 `ifconfig` 命令

查看接口状态。

```bash
ifconfig wan1
ifconfig wan5
```

- 有 IP 地址且接口状态为 `UP` 时，通常表示已联网。

### 4. 检查路由表

查看路由表确认接口是否配置了默认路由。

```bash
ip route show
```

- 如果 `wan1` 或 `wan5` 有默认路由，通常表示已联网。

### 5. 使用 `curl` 或 `wget`

通过 `curl` 或 `wget` 测试网络访问。

```bash
curl --interface wan1 http://example.com
curl --interface wan5 http://example.com
```

- 如果能获取网页内容，说明接口已联网。

### 6. 查看系统日志

检查系统日志获取接口状态信息。

```bash
dmesg | grep wan1
dmesg | grep wan5
```

- 日志中可能包含接口的连接状态信息。

## 外网访问实验室服务器

### 路由器管理页面

一般是 <http://192.168.3.1> 或者 <http://192.168.0.1>

```{figure} ../_static/images/routing_main.png
:name: router-management-system-main-page

路由器管理页面
```

### 添加端口映射规则

1、添加端口映射

```{figure} ../_static/images/routing_nat_1.png
:name: router-management-system-nat-page1

添加端口映射
```

2、配置映射规则

```{figure} ../_static/images/routing_nat_2.png
:name: router-management-system-nat-page2

配置映射规则
```

### 测试 SSH 连接

```{figure} ../_static/images/routing_connection.png
:name: router-management-system-connection

测试 SSH 连接
```
