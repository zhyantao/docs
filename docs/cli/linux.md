# Linux

```{note}
- 内核与驱动开发：<https://gitee.com/zhyantao/pdf/raw/master/linux/linux-kernel-slides.pdf>
- 调试技术：<https://gitee.com/zhyantao/pdf/raw/master/linux/debugging-slides.pdf>
- 音频模块：<https://gitee.com/zhyantao/pdf/raw/master/linux/audio-slides.pdf>
- 抢占式实时 OS：<https://gitee.com/zhyantao/pdf/raw/master/linux/preempt-rt-slides.pdf>
- 嵌入式 Linux：<https://gitee.com/zhyantao/pdf/raw/master/linux/embedded-linux-slides.pdf>
- 图形与图像系统：<https://gitee.com/zhyantao/pdf/raw/master/linux/graphics-slides.pdf>
```

## 系统信息

| 命令                  | 说明                                                                |
| --------------------- | ------------------------------------------------------------------- |
| `cat /proc/version`   | 显示内核版本、编译器版本及构建时间等详细信息                        |
| `uname -a`            | 显示系统信息（包括内核名称、版本、主机名、处理器类型、硬件架构等）  |
| `uname -r`            | 仅显示当前内核版本号                                                |
| `lsb_release -a`      | 显示 LSB（Linux 标准库）兼容的发行版信息（需要安装 lsb-release 包） |
| `cat /etc/os-release` | 查看发行版版本及 ID 信息（适用于大多数现代系统）                    |
| `cat /etc/issue`      | 查看发行版版本信息（简短信息，可能不含详细信息）                    |
| `getconf LONG_BIT`    | 显示系统位数（32 或 64 位）                                         |
| `file /bin/ls`        | 通过分析/bin/ls 可执行文件判断系统位数                              |
| `uname -m`            | 显示系统硬件架构（如 x86_64、armv7l 等）                            |

## 目录结构

下面是 Linux 系统中一些重要目录的简要说明：

| 目录          | 说明                                             |
| ------------- | ------------------------------------------------ |
| `/bin`        | 存放系统基本的可执行命令（binary）               |
| `/boot`       | 启动加载所需的文件，如内核、初始化 RAM 磁盘等    |
| `/dev`        | 设备文件目录，包含所有设备的特殊文件             |
| `/etc`        | 系统和应用程序的配置文件                         |
| `/home`       | 普通用户主目录的默认位置                         |
| `/lib`        | 库文件目录，包含系统运行所需的共享库             |
| `/media`      | 自动挂载可移动介质的目录                         |
| `/mnt`        | 临时挂载额外文件系统的目录                       |
| `/opt`        | 第三方应用程序的安装目录                         |
| `/root`       | 超级用户（root）的主目录                         |
| `/sbin`       | 系统管理命令存放目录，供 root 用户使用           |
| `/usr`        | 用户程序、库文件、文档等资源的第二层次目录       |
| `/srv`        | 服务数据目录，用于存储本机或公开提供的服务的数据 |
| `/lost+found` | 系统意外崩溃后，fsck 工具可能恢复的文件存放处    |
| `/proc`       | 虚拟文件系统，提供关于内核和进程的信息           |
| `/sys`        | 提供有关系统硬件和驱动程序的详细信息             |
| `/run`        | 存放系统运行时需要的文件，如 pid 文件和 socket   |

## 设备文件

设备文件根据访问方式分为：

| 设备类型 | 标识符 | 特性                                       |
| -------- | ------ | ------------------------------------------ |
| 字符设备 | `c`    | 无缓冲，适合按顺序读写的设备，如键盘、串口 |
| 块设备   | `b`    | 有缓冲，支持随机访问，如硬盘、闪存         |

根据是否映射到物理实体可分为：

| 设备类型 | 特性                                                 |
| -------- | ---------------------------------------------------- |
| 物理设备 | 对应实际硬件，如硬盘、网卡                           |
| 虚拟设备 | 由软件模拟，如 loop 设备、随机数生成器 `/dev/random` |

每个设备文件在 `/dev` 目录下都有对应的节点，通过主设备号和次设备号唯一标识。主设备号关联设备驱动，而次设备号用于区分同一类型的多个设备。可以使用 `ls -l /dev` 查看设备文件详情，或通过 `cat /proc/devices` 查看已注册的设备驱动及其主设备号。

**注意**：`/dev` 目录不仅包含设备文件，还可能有 FIFO 管道、套接字（socket）、符号链接、硬链接和目录等非设备文件，它们不具备主设备号或次设备号。

以下内容摘自：<https://elixir.bootlin.com/linux/v3.4/source/Documentation/devices.txt>

```text
...

  4 char	TTY devices
          0 = /dev/tty0		Current virtual console

          1 = /dev/tty1		First virtual console
            ...
         63 = /dev/tty63	63rd virtual console
         64 = /dev/ttyS0	First UART serial port
            ...
        255 = /dev/ttyS191	192nd UART serial port

        UART serial ports refer to 8250/16450/16550 series devices.

        Older versions of the Linux kernel used this major
        number for BSD PTY devices.  As of Linux 2.1.115, this
        is no longer supported.	 Use major numbers 2 and 3.

...
```

## 快捷键

```{code-block} bash
Ctrl + s        # 冻结窗口，用 Ctrl + q，Ctrl + C 退出

Ctrl + l        # 清屏

Ctrl + c        # 终止程序运行

echo            # 输出到屏幕
    $PATH       # 环境环境变量
    $?          # 上次命令是否运行成功，成功为 0，其他失败

df              # 查看内存和交换分区的使用情况
    [-m|-g|-k]  # 显示的单位可以是 M、G、K

shutdown        # 关机
reboot          # 重启
halt            # 关机后关闭电源
```

## 命令行高亮

```{code-block} bash
PS1='\[\e]0;\w\a\]\n\[\e[32m\]\u@\h \[\e[33m\]\w\[\e[0m\]\n\$ '
```

格式说明与示例：

```{code-block} bash
\033[字体格式;背景颜色;字体颜色  加粗+闪烁+天蓝底+黑字  \033[结尾控制

\033[1;5;46;30m                加粗+闪烁+天蓝底+黑字  \033[0m
```

`````{tab-set}
````{tab-item} 字体格式
```{code-block} bash
0        重新设置属性到缺省设置
1        设置粗体
2        设置一半亮度(模拟彩色显示器的颜色)
4        设置下划线(模拟彩色显示器的颜色)
5        设置闪烁
7        设置反向图象
22       设置一般密度
24       关闭下划线
25       关闭闪烁
27       关闭反向图象
```
````

````{tab-item} 背景颜色;字体颜色
```{code-block} bash
# 颜色范围：40 ~ 47
\033[40;37m  黑底白字   \033[0m
\033[41;30m  红底黑字   \033[0m
\033[42;34m  绿底蓝字   \033[0m
\033[43;34m  黄底蓝字   \033[0m
\033[44;30m  蓝底黑字   \033[0m
\033[45;30m  紫底黑字   \033[0m
\033[46;30m  天蓝底黑字 \033[0m
\033[47;34m  白底蓝字   \033[0m
```
````

````{tab-item} 字体颜色
```{code-block} bash
# 颜色范围：30 ~ 37
\033[30m  黑色字  \033[0m
\033[31m  红色字  \033[0m
\033[32m  绿色字  \033[0m
\033[33m  黄色字  \033[0m
\033[34m  蓝色字  \033[0m
\033[35m  紫色字  \033[0m
\033[36m  天蓝字  \033[0m
\033[37m  白色字  \033[0m
```
````

````{tab-item} 结尾控制
```{code-block} bash
\033[0m               关闭所有属性，常用选项，一般会选择使用此项
\033[1m               设置高亮度
\033[4m               下划线
\033[5m               闪烁
\033[7m               反显
\033[8m               消隐
\033[30m ~ \033[37m   设置前景色
\033[40m ~ \033[47m   设置背景色
```
````
`````
