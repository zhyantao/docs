# 故障现场恢复指南

在实际应用中，`gpsd` 通常从 `/dev/ttyS3` 读取 NMEA 数据。然而，客户在使用仿真设备时遇到了一个问题，即 `gpsd` 在解析数据时出现了错误。为了解决这个问题，我们可以通过使用伪终端来恢复故障现场。相关代码可以在以下链接中找到：

<https://gitee.com/zhyantao/misc/raw/master/tests/test_dev_pts.cc>

请注意，由于权限问题，上述链接可能无法访问。如果您遇到此类问题，请联系作者。

运行上述代码后，将生成以下日志输出：

```
Master FD: 5, Slave FD: 6, Slave Name: /dev/pts/2
```

为了启动 `gpsd` 并指定从特定的串口读取数据，您需要执行以下命令：

```bash
/usr/sbin/gpsd -n /dev/pts/2 /dev/pps0 -s 115200 -N
```
