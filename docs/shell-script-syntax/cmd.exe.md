# Cmd

## 设置 Anaconda 自动启动

和 Linux 不同的是，Windows 命令行没有 ``.cmdrc`` 文件。如果想设置 conda 自动启动，需要将注册表：

- ``\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor`` 或者
- ``\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor``

两者中的某一个 ``AutoRun`` 数据字段（如果没有就**新建**可扩充字符串值）的值设置为：``conda activate``。

或者，你也可以参考 [Windows 终端中的动态配置文件](https://docs.microsoft.com/zh-cn/windows/terminal/dynamic-profiles)。

## 更改 PowerShell 风格

Microsoft 新开发的 [Windows Terminal](https://github.com/microsoft/terminal) 可以更好地支持本地开发工作。

1. 安装 Oh My Posh：`Install-Module oh-my-posh -Scope CurrentUser` [^cite_ref-1]（网络原因，耗时较长）
2. 导入模块：`Import-Module oh-my-posh`（这一步会下载 `oh-my-posh.exe` 并配置环境变量）
3. 现在可能有些字符无法正常显示，先下载安装字体
   [MesloLGM NF](https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Meslo.zip)，
   再修改 Windows Termial 的配置文件 `Settings.json`（可以从 Windows Terminal 软件界面的下拉三角中找见）
   **补充**如下信息：

```json
{
    "profiles":
    {
        "defaults":
        {
            "fontFace": "MesloLGM NF"
        }
    }
}
```

4. 启用 Oh My Posh：`Set-PoshPrompt -Theme Paradox`

```{note}
上面的改动可能会让你的 VS Code Terminal 出现乱码。解决方式是打开 VS Code 使用 ``Ctrl + Shift + P`` 搜索 ``settings.json``，添加新下载的字体 ``"terminal.integrated.fontFamily": "MesloLGM NF",``。
```

---

[^cite_ref-1]: <https://ohmyposh.dev/docs/installation/windows>
