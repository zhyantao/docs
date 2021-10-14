# Windows Command Line

## 设置 Anaconda 自动启动

和 Linux 不同的是，Windows Command Line 没有 .bashrc 文件。如果想要设置这个文件，需要修改注册表项 `\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor` 中的 AutoRun（类型为 REG_EXPAND_SZ）的数据字段设置为 `if exist "D:\ProgramData\Anaconda3\condabin\conda_hook.bat" conda activate` 。数据字段很明显就是一段程序。

## 更改 Terminal 风格

Microsoft 新开发的 [Terminal](https://github.com/microsoft/terminal) 可以更好地支持本地开发工作，因此，现在换到这个 Terminal 上部署环境。

1. 首先，遵循 [oh-my-posh 的安装步骤](https://ohmyposh.dev/docs/pwsh)，完成基本安装。
2. 现在可能有些字符无法正常显示，我们需要在[Nerd Font](https://www.nerdfonts.com/)上随便下载一个字体。
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
