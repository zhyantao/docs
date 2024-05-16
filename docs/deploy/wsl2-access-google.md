# WSL2 访问外网的配置方法

WSL2 可以通过使用 Windows 的代理来访问 Google。

首先打开代理工具（比如 Clash）的局域网访问权限：

```{figure} ../_static/images/wsl2-access-google.png
:name: wsl2-access-google

打开代理工具的局域网访问权限
```

在 Windows PowerShell 中运行下面的命令，升级 WSL 到最新版本：

```bash
wsl --update --pre-release
```

然后，在 Windows 上创建或编辑 `%UserProfile%/.wslconfig` 文件：

```
[wsl2]
nestedVirtualization=true
ipv6=true
[experimental]
autoMemoryReclaim=gradual # gradual | dropcache | disabled
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true
```

接下来，在 Ubuntu 中运行下面的命令（每个人的端口号可能都不一样，参考 {numref}`wsl2-access-google` 我是 `7890`）：

```bash
cat <<EOF | tee -a ~/.bashrc
export ALL_PROXY="http://$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):7890"
EOF
```

在测试网络的时候，如果直接 `ping` 外网是不通的，但是，我们确实已经可以访问 Google 了：

```bash
curl -o test_google.html google.com
```
