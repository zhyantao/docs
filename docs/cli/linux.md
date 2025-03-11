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

| 命令                                            | 说明                       |
| ----------------------------------------------- | -------------------------- |
| `cat /proc/version`<br>`uname -a`<br>`uname -r` | 查看内核版本信息           |
| `lsb_release -a`<br>`cat /etc/issue`            | 查看 Linux 发行版版本信息  |
| `getconf LONG_BIT`<br>`file /bin/ls`            | 判断系统是 32 位还是 64 位 |
| `uname -m`                                      | 正确命令来查看系统架构     |

## 目录结构

下面是Linux系统中一些重要目录的简要说明：

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
| 虚拟设备 | 由软件模拟，如 loop 设备、随机数生成器 `/dev/random` |

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

## 常用命令

### find

语法：`find [路径] [选项] [操作]`

#### 选项

| 选项              | 说明                    | 选项                               | 说明                                         |
| ----------------- | ----------------------- | ---------------------------------- | -------------------------------------------- |
| `-name`           | 文件名                  | `-iname`                           | 文件名（忽略大小写）                         |
| `-perm 777`       | 文件权限                | `-type f \| d \| l \| c \| b \| p` | 文件类型                                     |
| `-user`           | 文件属主                | `-nouser`                          | 无有效属主                                   |
| `-group`          | 文件属组                | `-nogroup`                         | 无有效属组                                   |
| `-size -n \| +n`  | 文件大小                | `-prune`                           | 排除某些查找目录<br/>通常与 `-path` 一同使用 |
| `-mindepth n`     | 从 n 级子目录开始查找   | `-maxdepth n`                      | 最多搜索到 n 级子目录                        |
| `-mtime -n \| +n` | 文件修改时间（天）      | `-mmin -n \| +n`                   | 文件修改时间（分钟）                         |
| `-newer file1`    | 文件修改时间比 file1 早 |                                    |                                              |

示例：

```bash
# 文件名
find /etc/ -name '*.conf'

# 文件类型
# f 文件；d 目录；c 字符设备文件；
# b 块设备文件；l 链接文件；p 管道文件
find /etc/ -type f

# 文件大小
# -n 小于等于；+n 大于等于
find . -size +100M
find . -size -10k

# 文件修改时间
# -n < n天以内修改过的文件；
# n = n 天修改过得文件；
# +n > n天以外修改过的文件；
find . -mtime -3
find . -mtime 3
find . -mtime +3

# 排除目录
# -path ./test1 -prune 排除 test1 目录
# -path ./test2 -prune 排除 test2 目录
# -o type f 固定结尾写法
find . -path ./test1 -prune -o -path ./test2 -prune -o type f
```

#### 操作

- `-print` 打印输出
- `-exec 'command' {} \;` 其中 `{}` 是前面查找匹配到的结果
- `-ok` 与 `exec` 功能一样，但每次操作都给用户提示，由用户决定是否执行对应的操作。

示例：

```bash
# 查找 30 天以前的日志文件并删除
find /var/log -name '*.log' -mtime +30 -exec rm -f {} \;

# 查找所有 .conf 文件，并移动到指定目录
find /etc/apache -name '*.conf' -exec cp {} /home/user1/backup \;
```

### netstat

主要用于查看和网络相关的信息。

```bash
# 查看端口被哪个进程占用
netstat -tulpn | grep :<port_number>

# 查看进程正在使用哪个端口
netstat -tulpn | grep <process_name>
```

### printf

模仿 C 程序库（library）里的 `printf()` 程序，主要用于格式化输出。

默认 `printf` 不会像 `echo` 自动添加换行符，我们可以手动添加 `\n`。

其基本语法格式为：

```bash
printf  format-string  [arguments...]
```

说明：

- `format-string` 为格式控制字符串
- `arguments` 为参数列表。

示例：

```bash
printf "%-10s %-8s %-4s\n" 姓名 性别 体重kg
printf "%-10s %-8s %-4.2f\n" 郭靖 男 66.1234
printf "%-10s %-8s %-4.2f\n" 杨过 男 48.6543
printf "%-10s %-8s %-4.2f\n" 郭芙 女 47.9876
```

其中：

- `%s` `%c` `%d` `%f` 都是格式替代符；
- `%-10s` 指一个宽度为 10 个字符（`-` 表示左对齐，没有则表示右对齐），任何字符都会被显示在 10 个字符宽的字符内，如果不足则自动以空格填充，超过也会将内容全部显示出来。
- `%-4.2f` 指格式化为小数，其中 `.2` 指保留 2 位小数。

更多使用示例：

```bash
# 没有引号也可以输出
printf %s abcdef

# 格式只指定了一个参数，但多出的参数仍然会按照该格式输出，format-string 被重用
printf %s abc def
printf "%s\n" abc def

# 如果没有 arguments，那么 %s 用NULL代替，%d 用 0 代替
printf "%s and %d \n"
```

### test

用于检查某个条件是否成立，它可以进行数值、字符和文件三个方面的测试（详见第 3 节运算符部分）。

基本使用示例：

```bash
cd /bin
if test -e ./bash
then
    echo '文件已存在!'
else
    echo '文件不存在!'
fi
```

### xargs

用于将第一个命令的结果当做参数传递给第二个命令。

示例：

```bash
find -name "*.c" | xargs ls -l
```

### sed

`sed` 命令主要用于替换文本中的字符串。

示例：

```bash
# 将 filename.txt 中的 abc def 替换为 def abc
sed -i 's@abc def@def abc@' filename.txt
```

在前面的例子中，`@` 可以是其他符号，它的主要作用在于区分需要替换的字符串和原始字符串。

### tee

`tee` 命令主要用于将一段文字写入文件。

```bash
cat <<EOF | tee ~/.config/pip/pip.conf
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
EOF
```

如果向文件中添加的内容包含特殊字符，比如 `$()`，我们发现 `$()` 消失不见了，解决方式如下：

```bash
cat <<\EOF | tee test.txt
CURR_DIR := $(shell pwd)
EOF
```

### source

`source <file_name>` 表示读取并执行 `file_name` 中的命令。

习惯上，用 `.` 代替 `source`，也就是说 `source <file_name>` 等价于 `. <file_name>`。

### scp

`scp` 命令主要用于在本地机器和远端机器之间复制文件。

```bash
# 将远端文件（或文件夹）复制到本地
scp <root>@<remote_ip>:/path/to/<target_filename> <local_filename>
scp -r <root>@<remote_ip>:/path/to/<remote_dirname> <local_dirname>

# 将本地文件（或文件夹）复制到远端
scp <local_filename> <root>@<remote_ip>:/path/to/<target_filename>
scp -r <local_dirname> <root>@<remote_ip>:/path/to/<remote_dirname>
```

### tar

`tar` 命令主要用于打包文件和目录，并不直接进行压缩。

如果你希望在打包的同时也减小文件的大小，你需要在使用 `tar` 命令时结合一个压缩工具，如 `gzip`、`bzip2`、`xz` 等。例如：

- 使用 `gzip` 压缩：`tar czf archive_name.tar.gz file_or_directory_to_compress`
- 使用 `bzip2` 压缩：`tar cjf archive_name.tar.bz2 file_or_directory_to_compress`
- 使用 `xz` 压缩：`tar cJf archive_name.tar.xz file_or_directory_to_compress`

解压时，仍然需要跟上 `z`、`j` 或者 `J` 选项，才能正常解压。

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
