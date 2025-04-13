# WSL2 Ubuntu 管理

## 解决 WSL2 常见路径错误

在 Windows 上使用应用程序访问位于 WSL2 (Windows Subsystem for Linux 2) 中的项目时，可能会遇到路径兼容性的问题。这是因为 WSL2 内的文件路径与 Windows 系统中的路径格式不同：WSL2 使用 `\\wsl.localhost` 作为其路径的开头部分，而传统的 Windows 路径是以盘符（如 `C:\`）开始的。这种路径表示法上的差异，有时会导致程序无法正确识别或访问文件，进而产生错误。

例如，在尝试用 STM32CubeIDE 编译一个位于 WSL2 环境下的项目时，您可能会碰到 "No such file or directory" 的错误提示。为了解决这一问题，可以采取以下方案：

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

## 压缩 WSL2 占用的 C 盘空间

WSL2 只会自动扩容，无法自动缩容。因此，如果 WSL2 占用的磁盘空间过大，可以尝试以下方法来压缩：

1、关闭 WSL

```bash
wsl --shutdown
```

2、启动 diskpart

```bash
diskpart
```

3、选择 `ext4.vhdx` 文件，并压缩

```bash
select vdisk file="C:\Users\yanta\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04LTS_79rhkp1fndgsc\LocalState\ext4.vhdx"
list disk
compact vdisk
list disk
```

````{note}
确保 WSL2 是关闭状态的，因为在 Windows 11 上，WSL2 有可能会自动重启。

```bash
> wsl --list --verbose
  NAME            STATE           VERSION
* Ubuntu-20.04    Stopped         2
```
````
