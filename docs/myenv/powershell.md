# PowerShell

## 分栏快捷键

左右分栏：`Alt` + `Shift` + `=`

上下分栏：`Alt` + `Shift` + `-`

关闭分栏：`Ctrl` + `Shift` + `w`

## 设置 Anaconda 自动启动

和 Linux 不同的是，Windows 命令行没有 `.cmdrc` 文件。如果想设置 conda 自动启动，需要将注册表：

- `\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor` 或者
- `\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor`

两者中的某一个 `AutoRun` 数据字段（如果没有就 **新建** 可扩充字符串值）的值设置为：`conda activate`。或者，你也可以参考 [Windows 终端中的动态配置文件](https://docs.microsoft.com/zh-cn/windows/terminal/dynamic-profiles)。在 PowerShell 中显示 conda 环境：`conda init powershell`，然后重启 Terminal。

## 安装 Posh Git

在 PowerShell 中更加轻松地使用 Git 命令，拥有命令自动补全、当前分支展示、改动提示等功能。

1. 以管理员身份运行 PowerShell
2. 修改执行策略：`Set-ExecutionPolicy RemoteSigned`
3. 安装模块：`Install-Module posh-git -Scope CurrentUser -Force`
4. 导入模块：`Import-Module posh-git`
5. 使用模块：`Add-PoshGitToProfile -AllHosts`

删除 Posh Git 模块：`Uninstall-Module posh-git`，同时需要删除 `notepad $PROFILE` 中的 `Import-Module posh-git`。

如果要想同时显示 `git branch` 和 `conda environment` 那么必须将 `Import-Module posh-git` 放在 `conda init` 之前，如下所示（注意，同时需要在 `%USERPROFILE%\.condarc` 中添加一行 `changeps1: true`）。

```bash
Import-Module posh-git

#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
(& "D:\ProgramData\Miniconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
#endregion
```
