# Windows 故障调试

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

Alt + 空格，选择最大化。

**问题描述**

关闭扩展屏后，PPT 幻灯片放映，仍然在扩展屏显示。

**解决方法**

放映后在主屏幕选择“三个点”，选择“隐藏演示者视图”。

## 修复图标白色块问题

**问题描述**

电脑开机后，固定到任务栏中的图标显示为白色块。

**解决方法**

1. 右击桌面“开始菜单”，选择“任务管理器”。
2. 右击“进程”下的“Windows 资源管理器”，选择“重新启动”。
