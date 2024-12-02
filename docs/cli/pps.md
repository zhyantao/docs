# PPS

```{note}
- `assert edge`: 上升沿
- `clear edge`: 下降沿
```

## ppsfind

**Description:** Find pps device by name

**Examples:**

```bash
ppsfind ""
```

## ppstest

**Description:** Simple tool to monitor PPS timestamps

**Examples:**

```bash
ppstest /dev/pps0
```

此命令将开始监控来自 `/dev/pps0` 的 PPS 脉冲，并输出每个脉冲的时间戳信息。

## ppswatch

**Description:** Advanced tool to monitor PPS timestamps

**Examples:**

```bash
ppswatch -a /dev/pps0
```

此命令将以高级模式监控来自 `/dev/pps0` 的 PPS 脉冲，显示更多详细信息。

## ppsldisc

**Description:** Setup PPS line discipline for RS232

**Examples:**

```bash
ppsldisc /dev/ttyS3
```

## ppsctl

**Description:** Control tool for PPS

**Examples:**

```bash
ppsctl -a /dev/pps0 -e
```

此命令将启用 `/dev/pps0` 设备上的上升沿捕获功能。
