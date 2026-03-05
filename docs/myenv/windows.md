# Windows

## Windows Path

```{note}
推荐将常用的环境装在 C 盘下，方便软件工具自动识别。
```

### Java

| 变量名      | 变量值                                  |
| ----------- | --------------------------------------- |
| `JAVA_HOME` | `C:\Program Files\Java\jdk-1.8`         |
| `JDK_HOME`  | `%JAVA_HOME%`                           |
| `JRE_HOME`  | `%JAVA_HOME%\jre`                       |
| `CLASSPATH` | `.;%JAVA_HOME%\lib;%JAVA_HOME%\jre\lib` |
| `PATH`      | `%JAVA_HOME%\bin`                       |

```{note}
配置好 Java 环境变量才能让 VS Code 识别到 Java 环境。
```

### Python

| 变量名       | 变量值                                            |
| ------------ | ------------------------------------------------- |
| `PYTHONHOME` | `C:\Program Files\Python312`                      |
| `PYTHONPATH` | `%PYTHONHOME%\Lib;%PYTHONHOME%\Lib\site-packages` |
| `PATH`       | `%PYTHONHOME%\Scripts;%PYTHONHOME%`               |

### Maven

| 变量名       | 变量值                              |
| ------------ | ----------------------------------- |
| `MAVEN_HOME` | `D:\ProgramData\apache-maven-3.9.9` |
| `M2_HOME`    | `%MAVEN_HOME%`                      |
| `PATH`       | `%MAVEN_HOME%\bin`                  |

## PowerShell

### 分栏快捷键

左右分栏：`Alt` + `Shift` + `=`

上下分栏：`Alt` + `Shift` + `-`

关闭分栏：`Ctrl` + `Shift` + `w`

### 设置 Anaconda 自动启动

和 Linux 不同的是，Windows 命令行没有 `.cmdrc` 文件。如果想设置 conda 自动启动，需要将注册表：

- `\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor` 或者
- `\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor`

两者中的某一个 `AutoRun` 数据字段（如果没有就 **新建** 可扩充字符串值）的值设置为：`conda activate`。或者，你也可以参考 [Windows 终端中的动态配置文件](https://docs.microsoft.com/zh-cn/windows/terminal/dynamic-profiles)。在 PowerShell 中显示 conda 环境：`conda init powershell`，然后重启 Terminal。

### 安装 Posh Git

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
## !! Contents within this block are managed by 'conda init' !!
(& "D:\ProgramData\Miniconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
#endregion
```


## WSL2 Ubuntu 管理

### 解决 WSL2 常见路径错误

在 Windows 上使用应用程序访问位于 WSL2 (Windows Subsystem for Linux 2) 中的项目时，可能会遇到路径兼容性的问题。这是因为 WSL2 内的文件路径与 Windows 系统中的路径格式不同：WSL2 使用 `\\wsl.localhost` 作为其路径的开头部分，而传统的 Windows 路径是以盘符（如 `C:\`）开始的。这种路径表示法上的差异，有时会导致程序无法正确识别或访问文件，进而产生错误。

例如，在尝试用 STM32CubeIDE 编译一个位于 WSL2 环境下的项目时，您可能会碰到 "No such file or directory" 的错误提示。为了解决这一问题，可以采取以下方案：

第 1 步：右击 `此电脑`，选择 `映射网络驱动器...`

第 2 步：任意指定一个盘符，比如 `Z:`，文件夹设置为 `\\wsl.localhost\Ubuntu-20.04`

```{figure} ../_static/images/wsl2-mapping-to-vdisk.png
:name: wsl2-mapping-to-vdisk
```

修改 `/etc/wsl.conf`，解决 Windows 和 WSL2 环境变量相互污染的问题：

```bash
sudo nano /etc/wsl.conf
```

添加如下内容：

```bash
[interop]
appendWindowsPath=false
```

重启 WSL2：

```bash
wsl --shutdown
wsl
```

### WSL2 访问外网的配置方法

#### 推荐方案

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
autoMemoryReclaim=gradual ## gradual | dropcache | disabled
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true
```

在测试网络的时候，如果直接 `ping` 外网是不通的，但是，我们确实已经可以访问 Google 了：

```bash
curl -o test_google.html google.com
```

#### 备选方案

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

### 压缩 WSL2 占用的 C 盘空间

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

## 备份 Windows 系统

在系统发生崩溃后，我们通常不希望总是从零开始，一个一个地重新安装应用程序。
如果能够将电脑当前的状态（包括操作系统，用户配置信息等）保存起来就好了，下一次直接从这个状态直接恢复。

借助 WinPE 工具，我们可以轻松地实现上述目标。

Windows PE 或 WinPE，全称 Windows 预先安装环境，是 Microsoft Windows 的轻量版本。
主要为个人电脑开发商、工作站、服务器打造定制的操作系统环境，或系统离线时进行故障排除。
它取代了格式较旧的 MS-DOS 启动磁片/启动光盘 [^cite_ref-1]。

注意，如果我们使用 Windows 自带的升级工具来重装系统，Windows 可能会自动将我们之前的系统保存到
`C:\Windows.old`。如果直接在文件夹上右击删除，往往没有足够的权限，比较推荐的做法是使用磁盘清理工具。

### 如何备份

1. 下载并安装 WinPE <https://www.wepe.com.cn>；
2. 选择 FAT32 制作 U 盘启动盘，注意，不建议选择 NTFS 或 exFat；
3. （备份）用 U 盘启动，进入可视化界面，使用 Ghost 封装系统；
4. （恢复）用 U 盘启动，进入可视化界面，使用 Ghost 恢复系统。

(windows_file_system)=

### 文件系统

Windows 操作系统支持 NTFS、FAT32、exFAT 三种不同文件系统。
文件系统是系统对文件的存放排列方式，不同格式的文件系统关系到数据如何在磁盘进行存储。

- NTFS 是目前 Windows 系统中一种**现代文件系统**，目前使用最广泛，内置的硬盘大多数都是 NTFS 格式；
- FAT32 是**老旧但通用**的文件系统，可以适配 Linux、Mac 或 Android（建议使用该格式制作启动盘）；
- exFAT 是 FAT32 文件格式的替代品，很多设备和操作系统都支持该文件系统，但是**目前用的不多** [^cite_ref-2]。

FAT（File Allocation Table，文件分配表）是一种由微软发明并拥有部分专利的**文件系统**。
供 MS-DOS 使用，也是所有非 NT（Windows New Technology，新技术视窗操作系统）核心的 Windows
系统使用的文件系统 [^cite_ref-3]。FAT32 表示文件分配表采用 32 位二进制数记录磁盘文件，单个文件最大寻址范围是
$2^{32} = 4 GB$。

## Windows 故障调试

### 无法通过 SSH 连接 VMware 虚拟机

**问题描述**

以前配置好了环境，可以通过 SSH 直接连接 VMware 虚拟机。重启电脑后，双击 MobaXterm 中保存的会话，无法连接到虚拟机，并且发现 Windows ping 不通虚拟机。

**解决方法**

`控制面板` > `网络和 Internet` > `网络连接` > 重启 VMnet8。

### Hyper-V 兼容性问题

**问题描述**

运行环境为 Windows 11，想要运行虚拟机，但是发现无法同时打开 VMware 和 Docker Desktop。

**解决方法**

启动 VMware Workstation 前，以管理员身份运行 PowerShell：

1. `bcdedit /set hypervisorlaunchtype off`
2. 重启电脑

启动 Docker Desktop（Windows）前，以管理员身份运行 PowerShell：

1. `bcdedit /set hypervisorlaunchtype auto`
2. 重启电脑

### 修复双屏扩展问题

**问题描述**

关闭扩展屏后，IDEA 无法在主屏幕上显示。

**解决方法**

`Alt` + `空格` > 选择 `最大化`。

**问题描述**

关闭扩展屏后，PPT 幻灯片放映，仍然在扩展屏显示。

**解决方法**

`幻灯片放映` > 选择主屏幕上的 `...` > `隐藏演示者视图`。

### 修复图标白色块问题

**问题描述**

电脑开机后，固定到任务栏中的图标显示为白色块。

**解决方法**

1. `Win + R` 打开 `%localappdata%`
2. 删除 `IconCache.db`（这是个隐藏文件）；
3. 打开 `任务管理器` > 重启 `Windows 资源管理器`。

### 声卡播放问题

**问题描述**

播放音频时，无声或声音断断续续。

**解决方法**

下载[联想驱动管理器](https://newsupport.lenovo.com.cn/driveDownloads_index.html)，检查主机编号：

```{figure} ../_static/images/windows-serialnumber.png
:name: LenovoSerialNumber

查找主机编号
```

访问[联想官网](https://newsupport.lenovo.com.cn/driveList.html?fromsource=driveList&selname=BH00QDHR)，下载对应驱动，安装即可。

### 关闭资源管理器中的工具栏

Win + R 打开 `regedit`，在地址栏输入：

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced
```

将 `AlwaysShowMenus` 的值改为 `0`。

---

[^cite_ref-1]: Windows 预先安装环境 <https://en.wikipedia.org/wiki/Windows_Preinstallation_Environment>

[^cite_ref-2]: File Allocation Table <https://en.wikipedia.org/wiki/File_Allocation_Table>

[^cite_ref-3]: NTFS，FAT32 和 exFAT 文件系统有什么区别？ <https://zhuanlan.zhihu.com/p/32364955>
