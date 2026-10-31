# VS Code

## 常用快捷键

macOS 把 `Ctrl` 换成 `Cmd`，`Alt` 换成 `Option`。下面按 Windows/Linux 写。

### 多光标与块选、列选

| 功能 | 快捷键 |
| --- | --- |
| 列选（块选），鼠标拖动 | `Shift + Alt + 鼠标左键拖动` |
| 列选，键盘 | `Ctrl + Shift + Alt + 方向键` |
| 在点击处添加光标 | `Alt + 鼠标左键` |
| 在上/下一行添加光标 | `Ctrl + Alt + ↑ / ↓` |
| 选中当前词，重复按则选下一个相同词 | `Ctrl + D` |
| 选中所有相同词 | `Ctrl + Shift + L` |
| 选中的多行末尾各加光标 | `Shift + Alt + I` |
| 扩大/缩小选区 | `Shift + Alt + → / ←` |
| 退出多光标 | `Esc` |

### 编辑

| 功能 | 快捷键 |
| --- | --- |
| 上/下移动当前行 | `Alt + ↑ / ↓` |
| 上/下复制当前行 | `Shift + Alt + ↑ / ↓` |
| 删除当前行 | `Ctrl + Shift + K` |
| 注释当前行 | `Ctrl + /` |
| 块注释 | `Shift + Alt + A` |
| 格式化文档 | `Shift + Alt + F` |
| 重命名符号 | `F2` |
| 跳到定义 | `F12` |

### 导航

| 功能 | 快捷键 |
| --- | --- |
| 命令面板 | `Ctrl + Shift + P` |
| 快速打开文件 | `Ctrl + P` |
| 跳转到行 | `Ctrl + G` |
| 全局搜索 | `Ctrl + Shift + F` |
| 侧边栏显示/隐藏 | `Ctrl + B` |
| 终端显示/隐藏 | ``Ctrl + ` `` |

## LeetCode 插件

```bash
VsCode Error: EACCES: permission denied
```

参考链接：<https://github.com/LeetCode-OpenSource/vscode-leetcode/issues/770>

注释掉 `%appdata%/Code/User/settings.json` 中的 `"leetcode.workspaceFolder"` 字段。

## PlatformIO 插件

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
