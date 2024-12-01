# WSL2 配置方案

## 解决 WSL2 常见路径错误

在用 Windows 上的应用程序对 WSL2 上的项目进行修改时，会遇到一些路径问题，这是因为 WSL2 在 Windows 上的访问路径是 `\\wsl.localhost` 开头的，而标准的 Windows 访问路径则是以盘符开头，比如 `C:\`，这种不一致会导致错误发生。比如，我在使用 STM32CubeIDE 编译位于 WSL2 上的项目时，会遇到 No such file or directory 的错误。解决方案如下：

第 1 步：右击 `此电脑`，选择 `映射网络驱动器...`

第 2 步：任意指定一个盘符，比如 `Z:`，文件夹设置为 `\\wsl.localhost\Ubuntu-20.04`

```{figure} ../_static/images/wsl2-mapping-to-vdisk.png
:name: wsl2-mapping-to-vdisk
```


## WSL2 访问外网的配置方法

### 推荐方案

WSL2 可以使用 Windows 的代理来访问外网。在 PowerShell 中运行下面的命令，升级 WSL 到最新版本：

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

在测试网络的时候，如果直接 `ping` 外网是不通的，但是，我们确实已经可以访问 Google 了：

```bash
curl -o test_google.html google.com
```

### 备选方案

首先打开代理工具（比如 Clash）的局域网访问权限：

```{figure} ../_static/images/wsl2-access-google.png
:name: wsl2-access-google

打开代理工具的局域网访问权限
```

在 Ubuntu 中运行下面的命令（每个人的端口号可能都不一样，参考 {numref}`wsl2-access-google` 我是 `7890`）：

```bash
cat <<EOF | tee -a ~/.bashrc
export ALL_PROXY="http://$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):7890"
EOF
```
