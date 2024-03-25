# Windows 故障调试

## 无法通过 SSH 连接 VMware 虚拟机

**问题描述**

以前配置好了环境，可以通过 SSH 直接连接 VMware 虚拟机。重启电脑后，双击 MobaXterm 中保存的会话，无法连接到虚拟机，并且发现 Windows ping 不通虚拟机。

**解决方法**

`控制面板` > `网络和 Internet` > `网络连接` > 重启 VMnet8。

## Hyper-V 兼容性问题

**问题描述**

运行环境为 Windows 11，想要运行虚拟机，但是发现无法同时打开 VMware 和 Docker Desktop。

**解决方法**

启动 VMware Workstation 前，以管理员身份运行 PowerShell：

1. `bcdedit /set hypervisorlaunchtype off`
2. 重启电脑

启动 Docker Desktop（Windows）前，以管理员身份运行 PowerShell：

1. `bcdedit /set hypervisorlaunchtype auto`
2. 重启电脑

## 修复双屏扩展问题

**问题描述**

关闭扩展屏后，IDEA 无法在主屏幕上显示。

**解决方法**

`Alt` + `空格` > 选择 `最大化`。

**问题描述**

关闭扩展屏后，PPT 幻灯片放映，仍然在扩展屏显示。

**解决方法**

`幻灯片放映` > 选择主屏幕上的 `...` > `隐藏演示者视图`。

## 修复图标白色块问题

**问题描述**

电脑开机后，固定到任务栏中的图标显示为白色块。

**解决方法**

1. 删除 `%localappdata%/localcache.db`（这是个隐藏文件）；
2. 打开 `任务管理器` > 重启 `Windows 资源管理器`。
