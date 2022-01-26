# Windows

## 设置 Anaconda 自动启动

和 Linux 不同的是，Windows 命令行没有 ``.cmdrc`` 文件。如果想设置 conda 自动启动，需要将注册表：

- ``\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor`` 或者
- ``\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor``

两者中的某一个 ``AutoRun`` 数据字段（如果没有就**新建**可扩充字符串值）的值设置为：``conda activate``

## 更改 Terminal 风格

Microsoft 新开发的 [Terminal](https://github.com/microsoft/terminal) 可以更好地支持本地开发工作，因此，现在换到这个 Terminal 上部署环境。

1. 首先，遵循 [oh-my-posh 的安装步骤](https://ohmyposh.dev/docs/pwsh)，完成基本安装。
2. 现在可能有些字符无法正常显示，我们需要安装一些字体，推荐 [MesloLGM NF](https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Meslo.zip)。
3. 然后，修改配置 Windows Termial 的配置文件 [Settings.json](https://docs.microsoft.com/en-us/windows/terminal/customize-settings/profile-general)（这个 Settings.json 可以从 Windows Terminal 软件界面的下拉三角中找见），**补充**如下信息

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

```{note}
上面的改动可能会让你的 vscode Terminal 出现乱码。解决方式是打开 vscode 使用 ``Ctrl + Shift + P`` 搜索 ``settings.json`` ，添加新下载的字体 ``"terminal.integrated.fontFamily": "MesloLGM NF",`` 。
```
