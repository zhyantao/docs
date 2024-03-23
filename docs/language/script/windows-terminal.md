# Windows Terminal

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

## 安装 Oh My Posh（不建议安装）

在 PowerShell 中使用 Oh My Posh，将会有一个更为美观的主题。

1. 安装模块：`Set-ExecutionPolicy Bypass -Scope Process -Force; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://ohmyposh.dev/install.ps1'))` [^cite_ref-1]
2. 激活模块：`(Get-Command oh-my-posh).Source`
3. 新建或编辑配置文件：`notepad $PROFILE`，并添加一条命令：`oh-my-posh init pwsh | Invoke-Expression`
4. 安装字体 [Meslo.zip](https://github.com/ryanoasis/nerd-fonts/releases/) [^cite-ref-2]
5. 修改 Windows Termial 的配置文件 `Settings.json`（默认是 `CTRL + Shift + ,`）：

```json
{
    "profiles":
    {
        "defaults":
        {
            "font":
            {
                "face": "MesloLGM Nerd Font"
            }
        }
    }
}
```

```{note}
如果你在 VS Code 中安装了 PowerShell 插件，那么上面的改动可能会让你的 PowerShell 终端出现乱码。解决方式是 `Ctrl + Shift + P` 搜索 `settings.json`，添加新下载的字体 `"terminal.integrated.fontFamily": "MesloLGM Nerd Font"`。
```

## 配置 PSReadLine

PSReadLine 是 PowerShell 中自带的自动补全插件。我现在不太清楚是否 Windows 默认给安装了这个插件，如果没有安装，那么使用命令 `Install-Module PSReadLine -Force` 即可。

然后把下面的内容写入配置文件 `notepad $PROFILE` 中：

```bash
# Set-PSReadLineOption -PredictionSource History
# Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
# Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
# Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
# Set-PSReadLineOption -Colors @{ InlinePrediction = "#666666" }
# Set-PSReadLineOption -BellStyle none
# Set-PSReadLineOption -HistorySearchCursorMovesToEnd
```

经过一段时间的体验后，我把不希望使用的一些选项给关闭了，实在是影响我们键入命令。

[^cite_ref-1]: <https://ohmyposh.dev/docs/installation/windows>
[^cite-ref-2]: <https://ohmyposh.dev/docs/installation/fonts>
