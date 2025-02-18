# 如何判断 WAN 口是否已联网

要判断 `wan1` 和 `wan5` 是否已经联网，可以按照以下步骤操作：

## 1. 使用 `ping` 命令

通过 `ping` 命令测试网络连通性。

```bash
ping -I wan1 8.8.8.8
ping -I wan5 8.8.8.8
```

- `-I` 指定网络接口。
- `8.8.8.8` 是 Google 的公共 DNS 服务器。

如果收到回复，说明接口已联网。

## 2. 使用 `ip` 命令

查看接口的 IP 地址和状态。

```bash
ip addr show wan1
ip addr show wan5
```

- 如果接口有 IP 地址且状态为 `UP`，通常表示已联网。

## 3. 使用 `ifconfig` 命令

查看接口状态。

```bash
ifconfig wan1
ifconfig wan5
```

- 有 IP 地址且接口状态为 `UP` 时，通常表示已联网。

## 4. 检查路由表

查看路由表确认接口是否配置了默认路由。

```bash
ip route show
```

- 如果 `wan1` 或 `wan5` 有默认路由，通常表示已联网。

## 5. 使用 `curl` 或 `wget`

通过 `curl` 或 `wget` 测试网络访问。

```bash
curl --interface wan1 http://example.com
curl --interface wan5 http://example.com
```

- 如果能获取网页内容，说明接口已联网。

## 6. 查看系统日志

检查系统日志获取接口状态信息。

```bash
dmesg | grep wan1
dmesg | grep wan5
```

- 日志中可能包含接口的连接状态信息。
