# 桌面软件环境

## Ubuntu 安装中文输入法

```bash
sudo apt update
sudo apt install ibus-libpinyin -y # 安装 iBUS
im-config -n ibus                  # 设置为默认输入法
sudo apt install fonts-noto-cjk -y # 安装中文字体
reboot
```

## VS Code 小技巧

### LeetCode 插件配置方法

```bash
VsCode Error: EACCES: permission denied
```

参考链接：<https://github.com/LeetCode-OpenSource/vscode-leetcode/issues/770>

注释掉 `%appdata%/Code/User/settings.json` 中的 `"leetcode.workspaceFolder"` 字段。

### UNC host '...' access is not allowed

- `Ctrl + ,`
- 搜索 `Allowed UNCHosts`
- `添加项`：写入目标主机的 IP

## Zotero

### 配合 WPS 实现文献云同步

由于 Zotero 提供的默认工作空间大小只有 300M，空间很小，通常不能满足科研需求。本文介绍使用 WPS 的同步功能来实现文献备份。

【编辑】-【首选项】-【高级】-【文件和文件夹】

```{figure} ../_static/images/zotero_1.png

```

### 格式化 PDF 文件名

【工具】-【添加组件】-【设置】-【Install Add-on From File】

安装插件 <https://github.com/jlegewie/zotfile>，重启 Zotero。

【工具】-【Zotfile Preferences】

```{figure} ../_static/images/zotero_2.png

```

右击参考文献 - 【Management Attachments】 - 【Rename and Move】

### 解决文献链接失效的问题

参考文章 <https://darencard.net/blog/2019-09-19-zotero-file-relink/>

安装插件 <https://github.com/wshanks/Zutilo>，打开下面这两个选项：

```{figure} ../_static/images/zotero_4.png

```

选中一篇文献 - 右击 - 【Zutilo】 - 【显示附件路径】

选中全部文献 - 右击 - 【Zutilo】 - 【修改附件路径】 - 旧字符串填写【`attachments:`】 - 勾选【替换所有部分路径字符串实例】 - 新字符串填写附件所在目录的实际路径，比如【`D:/`】

## PlatformIO

VS Code 搭配 PlatformIO 可以很方便地进行嵌入式代码开发。

但是安装过程中，可能会踩到一些坑，在这里记录一下。

首先，我是远程连接的 Linux 虚拟机，扩展插件如下所示：

```{figure} ../_static/images/platformio_install.png

```

从上图可以看到，PlatformIO 被安装到了远程机上，而不是本地机。因此接下来的配置针对的是 Linux 环境中的配置。

首先 PlatformIO 需要 Python3.6 以上版本的支持：

```bash
sudo yum update
sudo dnf install python3
```
