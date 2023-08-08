# PlatformIO 安装指南

VS Code 搭配 PlatformIO 可以很方便地进行嵌入式代码开发。

但是安装过程中，可能会踩到一些坑，在这里记录一下。

首先，我是远程连接的 Linux 虚拟机，扩展插件如下所示：

```{figure} ../_static/images/pio-install-guide-1.png
```

从上图可以看到，PlatformIO 被安装到了远程机上，而不是本地机。因此接下来的配置针对的是 Linux 环境中的配置。

首先 PlatformIO 需要 Python3.6 以上版本的支持：

```bash
sudo yum update
sudo dnf install python3
```