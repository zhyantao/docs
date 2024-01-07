# Linux


## 查看系统信息

```text
# 查看内核版本
cat /proc/version
uname -a
uname -r

# 查看 Linux 版本信息
lsb_release -a
cat /etc/issue

# 查看系统是 32 位还是 64 位
getconf LONG_BIT
file /bin/ls

# 查看系统架构
aarch
aarch64
```


## 目录结构

```text
bin         # Linux 操作系统下可执行的系统级的二进制命令（binary 的缩写）
boot        # 系统开机时需要加载的一些文件和配置
dev         # 设备文件所在目录（device 的缩写）
etc         # 包含了当前操作系统用户所有配置的相关信息
home        # 当前操作系统所安装的用户的主目录
lib         # 操作系统使用的库文件以及相关的配置
media       # 系统自动挂载目录
mnt         # 手动挂载目录
opt         # 给第三方协力软体方放置的目录
root        # root 用户的宿主目录
sbin        # 超级用户需要用到的一些二进制命令存储在该目录（super binary 的缩写）
usr         # Unix 软件资源包管理目录，存放的是当前用户下的一些东西
srv         # 一些网络启动后，这些服务所需要取用的资料目录
lost+found  # 存放系统错误产生的文件碎片，方便用户查找和恢复
proc        # 内核提供的一个接口，主要用来存储系统统计信息
sys         # 与 proc 相似，记录与核心相关的资讯
run         # 存放系统运行时需要的一些文件
```

## 设备文件

按照存取方式的不同，可以分为两种：

| 设备类型 | 标识符 | 特性                         |
| -------- | ------ | ---------------------------- |
| 字符设备 | `c`    | 无缓冲且只能顺序存取         |
| 块设备   | `b`    | 有缓冲且可以随机（乱序）存取 |

按照是否对应物理实体，也可以分为两种：

| 设备类型 | 标识符 | 特性                        |
|------|-----|---------------------------|
| 物理设备 | 无   | 对实际存在的物理硬件的抽象             |
| 虚拟设备 | 无   | 不依赖于特定的物理硬件，仅是内核自身提供的某种功能 |

无论是哪种设备，在 `/dev` 目录下都有一个对应的文件（节点），并且每个设备文件都必须有主设备号或次设备号。主设备号相同的设备是同类设备，使用同一个驱动程序（**虽然目前的内核允许多个驱动共享一个主设备号，但绝大多数设备依然遵循一个驱动对应一个主设备号的原则**）。可以通过 `cat /proc/devices` 命令查看当前已经加载的设备驱动程序的主设备号。

注意：在 `/dev` 目录下除了各种设备节点之外还通常还会存在：FIFO 管道、Socket、软链接、硬链接、目录。这些东西并不是设备文件，因此也就没有主设备号或次设备号。

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

  5 char	Alternate TTY devices
          0 = /dev/tty		Current TTY device
          1 = /dev/console	System console
          2 = /dev/ptmx		PTY master multiplex
          3 = /dev/ttyprintk	User messages via printk TTY device
         64 = /dev/cua0		Callout device for ttyS0
            ...
        255 = /dev/cua191	Callout device for ttyS191

        (5,1) is /dev/console starting with Linux 2.1.71.  See
        the section on terminal devices for more information
        on /dev/console.

...

 ****	ADDITIONAL /dev DIRECTORY ENTRIES

This section details additional entries that should or may exist in
the /dev directory.  It is preferred that symbolic links use the same
form (absolute or relative) as is indicated here.  Links are
classified as "hard" or "symbolic" depending on the preferred type of
link; if possible, the indicated type of link should be used.


    Compulsory links

These links should exist on all systems:

/dev/fd		/proc/self/fd	symbolic	File descriptors
/dev/stdin	fd/0		symbolic	stdin file descriptor
/dev/stdout	fd/1		symbolic	stdout file descriptor
/dev/stderr	fd/2		symbolic	stderr file descriptor
/dev/nfsd	socksys		symbolic	Required by iBCS-2
/dev/X0R	null		symbolic	Required by iBCS-2

Note: /dev/X0R is <letter X>-<digit 0>-<letter R>.

    Recommended links

It is recommended that these links exist on all systems:

/dev/core	/proc/kcore	symbolic	Backward compatibility
/dev/ramdisk	ram0		symbolic	Backward compatibility
/dev/ftape	qft0		symbolic	Backward compatibility
/dev/bttv0	video0		symbolic	Backward compatibility
/dev/radio	radio0		symbolic	Backward compatibility
/dev/i2o*	/dev/i2o/*	symbolic	Backward compatibility
/dev/scd?	sr?		hard		Alternate SCSI CD-ROM name

    Locally defined links

The following links may be established locally to conform to the
configuration of the system.  This is merely a tabulation of existing
practice, and does not constitute a recommendation.  However, if they
exist, they should have the following uses.

/dev/mouse	mouse port	symbolic	Current mouse device
/dev/tape	tape device	symbolic	Current tape device
/dev/cdrom	CD-ROM device	symbolic	Current CD-ROM device
/dev/cdwriter	CD-writer	symbolic	Current CD-writer device
/dev/scanner	scanner		symbolic	Current scanner device
/dev/modem	modem port	symbolic	Current dialout device
/dev/root	root device	symbolic	Current root filesystem
/dev/swap	swap device	symbolic	Current swap device

/dev/modem should not be used for a modem which supports dialin as
well as dialout, as it tends to cause lock file problems.  If it
exists, /dev/modem should point to the appropriate primary TTY device
(the use of the alternate callout devices is deprecated).

For SCSI devices, /dev/tape and /dev/cdrom should point to the
``cooked'' devices (/dev/st* and /dev/sr*, respectively), whereas
/dev/cdwriter and /dev/scanner should point to the appropriate generic
SCSI devices (/dev/sg*).

/dev/mouse may point to a primary serial TTY device, a hardware mouse
device, or a socket for a mouse driver program (e.g. /dev/gpmdata).

    Sockets and pipes

Non-transient sockets and named pipes may exist in /dev.  Common entries are:

/dev/printer	socket		lpd local socket
/dev/log	socket		syslog local socket
/dev/gpmdata	socket		gpm mouse multiplexer

    Mount points

The following names are reserved for mounting special filesystems
under /dev.  These special filesystems provide kernel interfaces that
cannot be provided with standard device nodes.

/dev/pts	devpts		PTY slave filesystem
/dev/shm	tmpfs		POSIX shared memory maintenance access

 ****	TERMINAL DEVICES

Terminal, or TTY devices are a special class of character devices.  A
terminal device is any device that could act as a controlling terminal
for a session; this includes virtual consoles, serial ports, and
pseudoterminals (PTYs).

All terminal devices share a common set of capabilities known as line
disciplines; these include the common terminal line discipline as well
as SLIP and PPP modes.

All terminal devices are named similarly; this section explains the
naming and use of the various types of TTYs.  Note that the naming
conventions include several historical warts; some of these are
Linux-specific, some were inherited from other systems, and some
reflect Linux outgrowing a borrowed convention.

A hash mark (#) in a device name is used here to indicate a decimal
number without leading zeroes.

    Virtual consoles and the console device

Virtual consoles are full-screen terminal displays on the system video
monitor.  Virtual consoles are named /dev/tty#, with numbering
starting at /dev/tty1; /dev/tty0 is the current virtual console.
/dev/tty0 is the device that should be used to access the system video
card on those architectures for which the frame buffer devices
(/dev/fb*) are not applicable.	Do not use /dev/console
for this purpose.

The console device, /dev/console, is the device to which system
messages should be sent, and on which logins should be permitted in
single-user mode.  Starting with Linux 2.1.71, /dev/console is managed
by the kernel; for previous versions it should be a symbolic link to
either /dev/tty0, a specific virtual console such as /dev/tty1, or to
a serial port primary (tty*, not cu*) device, depending on the
configuration of the system.

    Serial ports

Serial ports are RS-232 serial ports and any device which simulates
one, either in hardware (such as internal modems) or in software (such
as the ISDN driver.)  Under Linux, each serial ports has two device
names, the primary or callin device and the alternate or callout one.
Each kind of device is indicated by a different letter.	 For any
letter X, the names of the devices are /dev/ttyX# and /dev/cux#,
respectively; for historical reasons, /dev/ttyS# and /dev/ttyC#
correspond to /dev/cua# and /dev/cub#.	In the future, it should be
expected that multiple letters will be used; all letters will be upper
case for the "tty" device (e.g. /dev/ttyDP#) and lower case for the
"cu" device (e.g. /dev/cudp#).

The names /dev/ttyQ# and /dev/cuq# are reserved for local use.

The alternate devices provide for kernel-based exclusion and somewhat
different defaults than the primary devices.  Their main purpose is to
allow the use of serial ports with programs with no inherent or broken
support for serial ports.  Their use is deprecated, and they may be
removed from a future version of Linux.

Arbitration of serial ports is provided by the use of lock files with
the names /var/lock/LCK..ttyX#.	 The contents of the lock file should
be the PID of the locking process as an ASCII number.

It is common practice to install links such as /dev/modem
which point to serial ports.  In order to ensure proper locking in the
presence of these links, it is recommended that software chase
symlinks and lock all possible names; additionally, it is recommended
that a lock file be installed with the corresponding alternate
device.	 In order to avoid deadlocks, it is recommended that the locks
are acquired in the following order, and released in the reverse:

    1. The symbolic link name, if any (/var/lock/LCK..modem)
    2. The "tty" name (/var/lock/LCK..ttyS2)
    3. The alternate device name (/var/lock/LCK..cua2)

In the case of nested symbolic links, the lock files should be
installed in the order the symlinks are resolved.

Under no circumstances should an application hold a lock while waiting
for another to be released.  In addition, applications which attempt
to create lock files for the corresponding alternate device names
should take into account the possibility of being used on a non-serial
port TTY, for which no alternate device would exist.

    Pseudoterminals (PTYs)

Pseudoterminals, or PTYs, are used to create login sessions or provide
other capabilities requiring a TTY line discipline (including SLIP or
PPP capability) to arbitrary data-generation processes.	 Each PTY has
a master side, named /dev/pty[p-za-e][0-9a-f], and a slave side, named
/dev/tty[p-za-e][0-9a-f].  The kernel arbitrates the use of PTYs by
allowing each master side to be opened only once.

Once the master side has been opened, the corresponding slave device
can be used in the same manner as any TTY device.  The master and
slave devices are connected by the kernel, generating the equivalent
of a bidirectional pipe with TTY capabilities.

Recent versions of the Linux kernels and GNU libc contain support for
the System V/Unix98 naming scheme for PTYs, which assigns a common
device, /dev/ptmx, to all the masters (opening it will automatically
give you a previously unassigned PTY) and a subdirectory, /dev/pts,
for the slaves; the slaves are named with decimal integers (/dev/pts/#
in our notation).  This removes the problem of exhausting the
namespace and enables the kernel to automatically create the device
nodes for the slaves on demand using the "devpts" filesystem.
```
