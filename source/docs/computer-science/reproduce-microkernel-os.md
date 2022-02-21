(microkernel_os)=
# 微内核操作系统

## 学习路线

学习路线方案的制定参考了 MIT6.828 schedule [^cite_ref-1]，课程讲义为《[xv6 book](https://kdocs.cn/l/caQbBFQ1ener)
| [中文版](https://th0ar.gitbooks.io/xv6-chinese/content/index.html)》和《[xv6 source](https://kdocs.cn/l/cbGOwLHZ1EK4)》。

```{panels}
:container: timeline
:column: col-6 p-0
:card:

---
:column: +entry left

第 1 讲：操作系统简介
^^^

- 了解 UNIX 系统 [[video](https://www.youtube.com/watch?v=tc4ROCJYbm0)]
- 实验 1：准备工作环境 [[webpage](https://pdos.csail.mit.edu/6.828/2018/labs/lab1/)]

---
:column: +right
---
:column: +left
---
:column: +entry right

第 2 讲：计算机硬件架构和 x86 编程
^^^

- 阅读《xv6 book》Appendix A 和 B
- 阅读《xv6 source》相关代码
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-x86.html) 和 [幻灯片](https://kdocs.cn/l/cnhKtkx53jth)
- 作业：跑通 xv6 代码 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-boot.html)]

---
:column: +entry left

第 3 讲：学习如何调试由 C 编写的代码
^^^

- 阅读《[C 语言程序设计](https://kdocs.cn/l/coVOZtu777O9)》2.9、5.1 - 5.5 和 6.4
- 阅读 [幻灯片](https://kdocs.cn/l/co2YLTVPzUy6) 和 [示例代码](https://pdos.csail.mit.edu/6.828/2018/lec/pointers.c)
- 作业：脚本 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-shell.html)]
- 实验 2：内存管理 [[webpage](https://pdos.csail.mit.edu/6.828/2018/labs/lab2/)]

---
:column: +right
---
:column: +left
---
:column: +entry right

第 4 讲：脚本和操作系统组织
^^^

- 阅读《xv6 book》chapter 0
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-shell.txt)

---
:column: +entry left

第 5 讲：隔离机制（用户态和内核态）
^^^

- 阅读《xv6 book》chapter 1
- 阅读《xv6 source》相关代码
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-internal.txt)
- 作业：系统调用 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-syscall.html)]

---
:column: +right
---
:column: +left
---
:column: +entry right

第 6 讲：虚拟内存（上）
^^^

- 阅读《xv6 book》chapter 2
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-vm.md) 和 [幻灯片](https://kdocs.cn/l/caJl0eqf1x83)
- 阅读 [页表翻译机制](https://kdocs.cn/l/cea84466nzDf)
- 作业：写内存的懒分配 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-zero-fill.html)]

---
:column: +entry left

第 7 讲：虚拟内存（中）
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-usevm.md)、[手稿](https://pdos.csail.mit.edu/6.828/2018/lec/l-josmem.html)
  和 [幻灯片](https://kdocs.cn/l/cepqhIjZtd3k)
- 作业：xv6 CPU 时钟 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-alarm.html)]
- 实验 3：用户态环境 [[webpage](https://pdos.csail.mit.edu/6.828/2018/labs/lab3/)]

---
:column: +right
---
:column: +left
---
:column: +entry right

第 8 讲：系统调用，中断和异常
^^^

- 阅读《xv6 book》chapter 3
- 阅读《xv6 source》相关代码
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-interrupt.txt) 和 [手稿](https://kdocs.cn/l/cszWbTndffuP)
- 作业：多线程编程 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/lock.html)]

---
:column: +entry left

第 9 讲：多处理器和锁
^^^

- 阅读《xv6 book》chapter 4
- 阅读《xv6 source》spinlock.c 和 skim mp.c
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-lockv2.txt) 和 [幻灯片](https://kdocs.cn/l/cpgvtTpfx0Wq)
- 作业：xv6 锁机制的实现 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-lock.html)]
- 实验 4：抢先式多任务处理 [[webpage](https://pdos.csail.mit.edu/6.828/2018/labs/lab4/)]

---
:column: +right
---
:column: +left
---
:column: +entry right

第 10 讲：上下文切换
^^^

- 阅读《xv6 book》chapter 5
- 阅读《xv6 source》proc.c 和 swtch.S
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-threads.txt)
- 作业：超线程 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-uthread.html)]

---
:column: +entry left

第 11 讲：睡眠和唤醒
^^^

- 阅读《xv6 book》chapter 5
- 阅读《xv6 source》proc.c 相关代码
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-coordination.txt)
- 作业：同步屏障 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/barrier.html)]

---
:column: +right
---
:column: +left
---
:column: +entry right

第 12 讲：文件系统
^^^

- 阅读《xv6 book》chapter 6
- 阅读《xv6 source》bio.c、fs.c、sysfile.c 和 file.c
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-fs.txt)
- 作业：大文件 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-big-files.html)]

---
:column: +entry left

第 13 讲：崩溃后恢复
^^^

- 阅读《xv6 book》chapter 6
- 阅读《xv6 source》log.c
- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-crash.txt)
- 作业：崩溃 [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/xv6-new-log.html)]
- 实验 5：文件系统，spawn 和 sh [[webpage](https://pdos.csail.mit.edu/6.828/2018/labs/lab5/)]
- 实验 6：网络 [[webpage](https://pdos.csail.mit.edu/6.828/2018/labs/lab6/)]
- 实验 7：最终项目 [[webpage](https://pdos.csail.mit.edu/6.828/2018/labs/lab7/)]

---
:column: +right
---
:column: +left
---
:column: +entry right

第 14 讲：文件系统性能和快速崩溃恢复
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-journal.txt) 和
  [论文](https://pdos.csail.mit.edu/6.828/2018/homework/journal-ext2fs.html)
- 作业：mmap() [[webpage](https://pdos.csail.mit.edu/6.828/2018/homework/mmap.html)]

---
:column: +entry left

第 15 讲：虚拟内存（下）
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-vm-again.txt)、[幻灯片](https://kdocs.cn/l/cawTd6G1AMsJ)
  和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/appel-li.pdf)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 16 讲：操作系统组织
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-organization.txt) 和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/engler95exokernel.pdf)

---
:column: +entry left

第 17 讲：内核和高级语言
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-biscuit.txt) 和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/biscuit.pdf)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 18 讲：可扩展锁
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-scalable-lock.md)
  和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/linux-lock.pdf)
- 阅读 [幻灯片](https://kdocs.cn/l/cjgbA4CHxigP)
  和 [示例代码](https://pdos.csail.mit.edu/6.828/2018/lec/scalable-lock-code.c)

---
:column: +entry left

第 19 讲：可扩展内核
^^^

- 阅读 [幻灯片](https://kdocs.cn/l/cmkxaZO57wbg)
  和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/rcu-decade-later.pdf)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 20 讲：虚拟机（上）
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-vmware.txt)、[幻灯片](https://kdocs.cn/l/cgDpeTi8hufy)
  和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/adams06vmware.pdf)

---
:column: +entry left

第 21 讲：虚拟机（下）
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-vmm.md)、[幻灯片](https://kdocs.cn/l/co7NAA7sjY0Z)
  和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/belay-dune.pdf)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 22 讲：高性能网络
^^^

- 阅读 [笔记](https://pdos.csail.mit.edu/6.828/2018/lec/l-net.txt)
  和 [论文](https://pdos.csail.mit.edu/6.828/2018/readings/osdi14-paper-belay.pdf)

```

## 实验 1：准备工作环境

实验分为三部分。第一部分聚焦于熟悉 x86 汇编语言，QEMU 仿真器，以及 PC 上电启动过程。
第二部分测试启动器，在 lab/boot 目录下。第三部分深入初始化模板，叫做 JOS，在 kernel 目录下。

### 安装软件

在后续的实验中，你将频繁使用的工具是 git 版本控制系统，无需深入了解，简单知道如何使用即可。
笔记中给了两个链接供参考，但是也不需要详细阅读。

课程需要用的 git 仓库是 https://pdos.csail.mit.edu/6.828/2018/jos.git/，
笔记中频繁提到 Athena 机器，可能这是 mit 自己的超算平台提供的操作系统。
如果你拿不到这个 Athena，在自己的 Ubuntu 虚拟机上照常可以使用。
依次执行官网给出的几条命令行。

每做完一次作业，使用 git diff 可以查看你做了哪些修改，使用 git diff origin/lab1 
可以展示你相对于初始仓库做了哪些更改。因为 origin/lab1 是我们从服务器上下载的最初代码的样子的一个分支。

我们在 Athena 上安装了合适的 compliers 和 simulators，如果你用自己的虚拟机，可能需要自己编译。
如果要使用这些编译器和仿真器，你每次登录 Athena 都要运行 add -f 6.828。

如果你没有 Athena ，亦需要自己安装 qemu 和 gcc 遵循 
https://pdos.csail.mit.edu/6.828/2018/tools.html 的步骤。
如果你正在使用 Linux 和 BSD ，安装 gcc 可以使用包管理工具，如 apt yum。
qemu 要安装 6.828 已经适配过的，并自己编译，不要从 qemu 官网下载。

总结一下，这部分提到的是关于环境安装：

- 安装 git 并克隆代码到本地 https://pdos.csail.mit.edu/6.828/2018/jos.git/
- 安装编译器：gcc
- 安装仿真器：qemu，需要遵循 https://pdos.csail.mit.edu/6.828/2018/tools.html 的提示

编译仿真器 QEMU 的时间较长。而且跟着步骤走，可能编译源代码的时候会出现点问题。这里稍作整理。

```{code-block} text
undefined reference to `major'
undefined reference to `minor'
```

在相应文件中添加头文件 `#include <sys/sysmacros.h>` 就可以了。
[参考链接](https://pdos.csail.mit.edu/6.828/2018/tools.html)

```{code-block} text
error: static declaration of ‘gettid’ follows non-static declaration
```

参考
[Patch](https://patchwork.kernel.org/project/qemu-devel/patch/20190320161842.13908-3-berrange@redhat.com/)
修改一下源文件。

```{code-block} text
qemu/linux-user/syscall.c:5912: undefined reference to `stime'
```

将 `linux-user/syscall.c` 中 `get_errno(stime(&host_time));` 改为 `get_errno(clock_settime(CLOCK_REALTIME, &host_time));`

提交作业 Hand-In Procedure 的过程：这部分不用看

### 启动 PC

本节将教会你：

- x86 汇编语言，
- PC 的启动过程，
- 熟悉 QEMU 和 QEMU/GDB 调试过程

本节不需要写代码。

PC Assembly Language 这本书共 188 页，它将教会你汇编知识，但是内容很多。
而且，这本书中用到的 assembler 跟我们课程用到的 assembler 不一样。
这本书用的 assembler 是 NASM（Intel 语法）
我们用的 assembler 是 GNU（AT&T 语法）
虽然语义相同，但是汇编源文件相差巨大。
这两种语法的相互转化可以参考 http://www.delorie.com/djgpp/doc/brennan/brennan_att_inline_djgpp.html

练习1：根据参考文献 https://pdos.csail.mit.edu/6.828/2018/reference.html 自学汇编语言，
不用现在阅读，当你需要读或者写 x86 汇编语言的时候知道在哪里查就可以了。
但是我们建议你阅读 http://www.delorie.com/djgpp/doc/brennan/brennan_att_inline_djgpp.html

如果你要学习 x86 汇编语言，有两个主要的参考手册

- 简洁版的 https://pdos.csail.mit.edu/6.828/2018/readings/i386/toc.htm
- 详细版的 http://www.intel.com/content/www/us/en/processors/architectures-software-developer-manuals.html

简洁版的已经覆盖了我们课程需要的所有知识，详细版的供有兴趣的同学阅读。
除了 Intel 提供的指令集外，
AMD 也为我们提供了参考手册 https://developer.amd.com/resources/developer-guides-manuals/
你可以保存这些参考手册，如果后面用到处理器特性或指令集时，方便查阅。

### x86 仿真

我们不是在一个真实的物理机上开发一个操作系统，而是用一个软件模拟了一个真实物理机。
你在仿真器上编写的代码也会在真实物理机上生效，使用仿真器简化了调试过程，
比如，你能在 x86 仿真器中设置断点，而这在真实物理机上是很难办到的。

我们用到的仿真器是 QEMU。但是 QEMU 内置的监视器仅提供了有限的调试功能。
我们用 GDB 进行调试，把 QEMU 可以看做调试的目标。

开始使用这个仿真器之前，我们在 lab 文件夹下键入 make 来构建 boot loader 和 kernel，我们后面需要依赖的东西。
编译完成后，我们会得到内核映像 kernel.img ，为了能够运行内核，我们需要一个硬盘来存放这些程序代码，
现在启动 QEMU 这个虚拟硬盘，它将为我们保存 boot loader（obj/boot/boot）和 kernel（obj/kernel）。
启动 qemu 很简单，如果你使用 ssh 连接的 虚拟机，推荐使用 make qemu-nox
，如果你是在虚拟机上直接运行的 可以使用 make qemu

make qemu 的效果就跟按下电脑开机键一样，从磁盘加载引导文件，然后启动操作系统内核。

启动后的黑窗口界面只提供了两个命令：help 和 kerninfo
并且，它可以接收串口

如果只谈论效果，看到的东西很简单，但是理解原理，还是需要的。
这个内核监视器（shell）是直接运行在仿真器的原始硬件上的。
这意味着如果你把 obj/kern/kernel.img 这个文件拷贝到磁盘的引导区中去，
然后把那个磁盘插到真实物理机上，通电，开机，将会看到和 QEMU 仿真器展示给你的相同的内容。

### PC 的物理地址空间

我们现在更深入地了解一下 PC 机是如何一步步启动的？

PC 的物理地址空间大概是下面这种布局：

```{code-block} text
+------------------+  <- 0xFFFFFFFF (4GB)
|      32-bit      |
|  memory mapped   |
|     devices      |
|                  |
/\/\/\/\/\/\/\/\/\/\

/\/\/\/\/\/\/\/\/\/\
|                  |
|      Unused      |
|                  |
+------------------+  <- depends on amount of RAM
|                  |
|                  |
| Extended Memory  |
|                  |
|                  |
+------------------+  <- 0x00100000 (1MB)
|     BIOS ROM     |
+------------------+  <- 0x000F0000 (960KB)
|  16-bit devices, |
|  expansion ROMs  |
+------------------+  <- 0x000C0000 (768KB)
|   VGA Display    |
+------------------+  <- 0x000A0000 (640KB)
|                  |
|    Low Memory    |
|                  |
+------------------+  <- 0x00000000
```

从下往上，地址编号逐渐变大。

诞生的第一个 PC 是基于 16 位的 Intel 8088 处理器，只能寻址 1MB 的物理内存。
早期 PC 的物理地址空间从 0x00000000 开始，到 0x000FFFFF 结束，而不是上图所示的 0xFFFFFFFF。

上图中的 640K 叫做低内存，是早期计算机唯一一个可以随机存取的区域。
事实上，更早期的 PC 只能配置 16KB、32KB、或 64KB 的 RAM。

从 0x000A0000 到 0x000FFFFF 的 384KB 是为硬件预留的区域，用于视频显示缓冲区，非易失存储等。
当然最重要的用途还是基本输入输出系统（BIOS），它占用了 64KB 的大小，从 0x000F0000 到 0x000FFFFF。
在早期 PC 中，BIOS 是存储在只读存储器中（ROM）的，但是现在的 PC 把 BIOS 存储在了 flash 中了。
BIOS 的作用是提供系统初始化功能，比如激活显卡，检查已用内存。初始化完成后，BIOS 从磁盘或 USB 
等设备上的合适位置加载操作系统，并把控制权转移给操作系统。

在英特尔的 80286 和 80386 处理器发布后，打破了 1MB 屏障，开始支持 16MB 和 4GB 的物理地址空间。
PC 架构仍然保留了低 1MB 物理地址空间的原始布局，为了能够向后兼容。
现代 PC 从 0x000A0000 到 0x00100000 的物理内存上有一个 hole，把 RAM 分成了 low、conventional 
memory、extended memory 三部分。
另外，处于 RAM 之上的部分，现在通常被 BIOS 预留了，用于 32 位 PCI 设备。

最近 x86 处理器可以支持扩展内存，所以 4GB 的物理 RAM 并不是上限，所以，RAM 可以扩展到 0xFFFFFFFF 以上。
在这种情况下，BIOS 必须在系统 RAM 的高 32 位可寻址区域留下第二个 hole，预留空间给 32 位设备映射。

因为设计的限制，JOS 仅使用前 256MB 的物理地址空间，所以，截止到目前，我们将会假设所有的 PC 仅有 32 
位物理地址空间。但是处理复杂物理地址空间和其他方面的硬件组织仍然是一个十分有挑战性的 OS 开发工作。

### ROM BIOS

在这部分，你将使用 QEMU 的调试工具来研究如何启动一个 IA-32 兼容的电脑。

打开两个命令行终端，并 cd 到 lab 目录下，在其中一个终端中键入 make qemu-gdb，或者 make qemu-nox-gdb。在另一个终端中键入 make gdb。
make qemu-gdb 启动了 QEMU，但是 QEMU 在处理器执行第一条指令前就终止了，
它在等待 GDB 的调试连接。

在输出中，我们看到了类似下面的输出：

```{code-block} text
athena% make gdb
GNU gdb (GDB) 6.8-debian
Copyright (C) 2008 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-linux-gnu".
+ target remote localhost:26000
The target architecture is assumed to be i8086
[f000:fff0] 0xffff0:  ljmp  $0xf000,$0xe05b
0x0000fff0 in ?? ()
+ symbol-file obj/kern/kernel
(gdb) 
```

之所以有上面的的输出，是因为在源代码中提供了 .gdbinit 文件。
它启动 GDB 来调试之前在启动期间的 16 位代码并且让这个调试器监听 QEMU。

下面这行代码

[f000:fff0] 0xffff0:  ljmp  $0xf000,$0xe05b

是 GDB 对第一条指令的的反汇编。从输出可以推断出一些东西：

- IBM PC 从物理地址空间 0x000ffff0 开始执行，它在 64KB 区域的顶部，这部分区域是 ROM BIOS 的预留区域。
- PC 启动后的能够找到的程序入口地址是 CS=0xf000 IP=0xfff0
- 第一条被执行的指令是 jmp 指令，它跳转到段地址 CS=0xf000 IP=0xe05b

为什么 QEMU 会这样启动？这是因为 Intel 是这样设计 8088 处理器的，然后 IBM 在自己的机器中用了英特尔的处理器。
因为 BIOS 在 PC 中是硬连线的，它会占用地址空间 0x000f0000 - 0x000fffff，这种设计确保了 BIOS 在电脑上电后能够始终最先得到机器的控制权，这种设计是非常重要的，因为在最开始上电后，机器的 RAM 中没有其他的程序可以执行。
QEMU 仿真器提出了它自己的 BIOS，它把 BIOS 放在了处理器的虚拟物理地址空间的这个位置。
在处理器复位时，仿真处理器将会进入实模式，并把 CS 和 IP 分别设置为 0xf000 和 0xfff0，所以最开始执行的段地址是 CS:IP=0x000ffff0。
那么 0xf000:0xfff0 是如何转换为物理地址的呢？

为了回答这个问题，我们需要了解一点实模式寻址的原理。在实模式（实模式（real mode），也称为实地址模式（real address mode），是所有x86兼容CPU下的一种操作模式）下，地址转换机构按照一个公式来进行转换：
pyhsical address = 16 * segment + offset
因此，就实现了从 CS:IP 到真实物理地址的转换。

0xffff0 这个位置处于 BIOS 结束位置之下的 16 字节。
因此 BIOS 上来首先要做的是 jmp 向后跳转到 BIOS 开始的位置；
在这 16 字节的空间中能完成多少事情？

练习 2：使用 GDB 的 si 命令跟踪 ROM BIOS，然后尝试猜一下它在做什么。
如果你有足够的兴趣，可以进一步阅读 http://web.archive.org/web/20040404164813/members.iweb.net.au/~pstorr/pcbook/book2/book2.htm
，但是不需要探究明白所有的细节，针对 BIOS 是如何启动的，有一个大致的思路就可以了。
如果你只是用 si 来单步调试，那么可能永远不会结束，这是一个循环。
汇编语言是一个难点，读汇编语句，每一个语句都很好阅读，但是串起来，捋顺逻辑并不是一个容易事。

当 BIOS 启动后，它会建立一个中断描述表，并且初始化各种设备，比如 VGA 显示器，这就是为什么在 QEMU 上会有 Starting SeaBIOS 这条输出的原因了。

在初始化完成 PCI 总线和所有 BIOS 认为重要的设备后，BIOS 就开始搜索一个可以启动的设备，比如硬盘、CD-ROM 等。最终，它找到一个启动盘，然后 BIOS 从硬盘中读取 boot loader，并将控制权转移给 boot loader。

### Boot Loader

软盘和硬盘都分成 512 字节大小的区域，叫做扇区（sectors）。
扇区是磁盘的最小的转换粒度：每次读或写操作都必须是一个或多个扇区大小和边界对齐的。如果一个磁盘是可启动的，那么第一个扇区被称作是启动扇区，因为这是 boot loader 所在的区域。当 BIOS 找到 启动盘后，它载入 512 字节的启动扇区到内存空间（物理地址是 0x7c00 - 0x7dff）中，然后用 jmp 指令来设置 CS:IP 为 0000:7c00，将控制转移给 boot loader。就像被BIOS载入的物理地址一样，这些地址是相当随意的-但它们是为PC所固定和标准化的。

从 CD-ROM 启动 PC 是后面发展起来的，这种启动方式更复杂，且更强大。
CD-ROM 使用 2048 字节的扇区，而不是 512 字节，因此现代 BIOS 不得不重新设计 启动过程，将 BIOS 设计为能够加载更大的启动镜像到内存，然后将控制权转移给 boot loader，更详细的内容阅读 https://pdos.csail.mit.edu/6.828/2018/readings/boot-cdrom.pdf

对于 6.828 这门课程而言，我们仍然使用传统的硬启动机制，这意味着我们的 boot loader 必须调整为 512 字节。
boot loader 包括一个汇编源文件 boot/boot.S 和一个 C 源文件 boot/main.c。
仔细阅读源文件，并确保你能看懂源文件中的代码，理解启动过程发生了什么事情。
boot loader 必须完成下面两个功能：
1. boot loader 将处理器从实模式转换为 32 位保护模式，因为只有在保护模式
下，软件才能访问超过 1MB 的所有内存空间。保护模式的具体内容可以参考 https://pdos.csail.mit.edu/6.828/2018/readings/pcasm-book.pdf 的 1.2.7 节和 1.2.8 节，遇到一些指令 ，可以参考 Intel 架构的参考手册，在前面好像也是列举过。
在这里，你只需要理解在保护模式下，段地址（segment:offset）翻译为物理地址的过程是与实模式下的翻译过程是不相同的，并且翻译完成后 offset 是32 位 而不是 16 位。
2. boot loader 从硬盘中读取内核是通过 x86 的特殊的 I/O 指令直接访问 IDE 磁盘设备寄存器。如果你想更好地理解这些特殊的 I/O 指令是什么意思，可以参考 https://pdos.csail.mit.edu/6.828/2018/reference.html 中的 IDE Hard drive controller 部分。你不需要在本课程中学习过多关于如何针对特定设备进行编程（驱动开发），编写驱动器程序是操作系统开发非常重要的一环，但是从概念和架构视角看，它也是最无趣的。

在你理解了 boot loader 的源代码后，看一下汇编文件 obj/boot/boot.asm。
这个文件是编译完 boot loader 后，我们的 GNUmakefile 创建的反汇编文件。
这个反汇编文件让我们能够更简单地看懂在物理内存上，到底存放了怎样的 boot loader 源代码，并且，能够让我们使用 GDB 调试 boot loader 时，更容易地跟踪代码。
同样地，obj/kern/kernel.asm 是 JOS kernel 的反汇编，也是能够帮助我们简化调试过程。

你可以使用 b 指令在 GDB中添加断点。比如 b \*0x7c00 在 地址 0x7c00 设置了一个断点。在断点上，你可以使用 c 和 si 指令让它继续执行：指令 c 是继续执行直到碰到下一个断点， si N 是在继续执行 N 条指令。

为了检查内存中的指令（不是下一条需要执行的指令，下一条指令 GDB 会自动打印），你可以使用命令 x/i。这个命令的语法是 x/Ni ADDR，N 表示需要反汇编的连续的几条指令，ADDR 表示需要开始反汇编的内存地址。

练习 3：看一眼实验工具指导 https://pdos.csail.mit.edu/6.828/2018/labguide.html 尤其是 GDB 命令这部分。即使你熟悉 GDB，这部分包含了可能对 OS 工作机制有帮助的进阶的 GDB 命令

在 0x7c00 设置断点，这是 boot 扇区被加载的位置。继续执行直到碰到断点。
完整跟踪调试 boot/boot.S，利用源代码和反汇编文件 obj/boot/boot.asm 来保持跟踪你在何位置。
然后利用命令 x/i 来反汇编 boot loader 中的指令序列，然后对比原始的 boot loader 源代码和反汇编后的代码 obj/boot/boot.asm。

在 boot/main.c 中调试进入 bootmain()，然后进入 readsect()。
识别出在 readsect() 函数中的声明语句对应的确切的汇编指令。
跟踪 readsect() 函数中的剩余语句，然后返回 bootmain() 函数，
识别 for 循环从磁盘读取剩余内核扇区的开始和结束位置。
找出在循环执行完之后代码将会执行什么代码，并在这里设置一个断点，
继续从断点向下执行。
然后跟踪 boot loader 的剩余部分。

做完练习 3 后，你应该尝试回答下述问题：
- 处理器从什么位置开始执行 32 位的代码？具体是什么触发了从 16 位到 32 位的转换？
- boot loader 的最后一条指令是什么？内核被加载的第一条指令是什么？
- 内核中的第一条指令在哪里？
- boot loader 如何确定需要读多少个扇区来保证能够从磁盘中读取出一个完整的内核？它从哪里找到这些信息？

### 加载内核

我们现在更深一步地探索 C 语言部分的 boot loader，在 boot/main.c。
开始做这件事事前，最好先熟悉一下 C 语言编程基础。

练习 4：阅读《C 语言编程》的指针部分。
阅读 5.1 到 5.5。然后下载 pointers.c 这个文件的源代码，并运行它，
确保你能理解所有打印输出的值来自哪里。
尤其是要确保你能理解第 1 行和第 6 行的指针地址来自哪里，第 2 行和第 4 行的输出值是如何跳到那里的，为什么第 5 行的打印输出值看起来是损坏的？

如果你不是十分精通 C 语言，就不要跳过这个练习。如果你不是真正的理解 C 语言指针，在后面的实验中将会遭受难以言表的痛苦。

为了搞明白 boot/main.c 你需要知道什么是 ELF 二进制。
当你编译和链接一个 C 程序，比如 JOS kernel，编译器将会把 C 源代码转换为 对象文件（.o），这个对象文件包含了以二进制格式表示的汇编指令，而这个二进制格式是硬件所能理解的。
linker 然后将所有编译过的 object 文件组合成一个二进制镜像，比如 obj/kern/kernel，这个案例中，这个二进制镜像是 ELF 格式的，它表示 可执行与可链接格式。

关于 ELF 格式的完整介绍可以参考 https://pdos.csail.mit.edu/6.828/2018/readings/elf.pdf 但是在这门课中你并不需要深入了解这个格式的细节。
这个格式最复杂的部分是用来支持共享库的动态链接的，但是我们在这门课中并没有用到。维基百科 http://en.wikipedia.org/wiki/Executable_and_Linkable_Format 也有简短介绍。

为了能够顺利完成 6.828 你可以将 ELF 可执行文件看做一个带有加载信息的文件头，
文件头后面跟着若干的程序片段，每个程序片段都是一些连续的代码块或希望被加载进内存的数据。boot loader 不会修改代码或数据，它只是把它们加载进内存然后开始执行它们。

ELF 二进制以一个固定长度的 ELF header 开始，后面是可变长度的 program header，它列出了所有需要被加载的程序片段。
在 ELF header 的 C 语言定义在 inc/elf.h 中。
我们感兴趣的区域有下面几个：

- .text 程序的可执行指令
- .rodata 只读数据，比如由 C 编译器产生的 ASCII 字符串常量
- .data 数据部分，保存了程序的初始化数据，比如全局变量

当 linker 根据程序代码计算出内存布局后，它会位为未初始化的全局变量预留空间，
比如 int x。观察内存，在 section 部分，.bss 紧跟着 .data。
C 语言要求未初始化的全局变量以 0 值代替。因此我们不需要在 ELF 二进制文件中保存 .bss 的内容，因此 .bss 只是保存了 .bss section 的位置和大小。
故 boot loader 或者源代码本身必须需要自行给 .bss section 赋予 0 值。

如何了解在内核中所有的 section 的名字、大小、链接地址？
只需要键入下面的命令即可：

objdump -h obj/kern/kernel
（如果你是自己编译的工具链，可能需要使用 i386-jos-elf-objdump）

你将会看到更多 section 被列了出来，但是其他部分对我们理解原理而言不是那么重要。
其余输出的大部分都是在提示我们调试信息，这些调试信息一般包含在程序的可执行文件中，并不会被 program loader 加载进内存。

注意 .text section 的 VMA（或 link address）或 LMA（load address）。
load address 表示哪个 section 需要被加载进内存。
link address 表示哪个 section 需要被执行。
linker 把二进制文件中的 link address 用多种方式进行了编码，比如何时需要全局变量的地址，如果它从未链接的地址执行，则二进制通常不会起作用。
在现代的机器中，通常使用的是相对地址来链接，因为它更容易扩展，但是却有性能损耗并更加复杂，我们在本课程中不用这种方式，而是使用绝对地址来链接。

一般来说，链接和加载地址是相同的，比如看一下 boot loader 的 .text 部分

objdump -h obj/boot/boot.out

boot loader 用 ELF program header 来确定如何加载 section，program header 明确了 ELF 对象的那一部分需要加载进内存和每一个需要使用的目标地址。
你可以观察一下 progarm header 通过键入

objdump -x obj/kern/kernel

ELF 对象中需要别加载进内存中的部分被标记为了 LOAD。
其余信息是 虚拟地址 vaddr，或物理地址 paddr，加载区域的大小 memsz 和 filesz

回到 boot/main.c，ph->p_ca 字段是每一个 program header 保存的段目标物理地址。在这种情况下，它实际上是一个物理地址，尽管 ELF 规范对该字段的实际含义模糊不清。

BIOS 载入启动扇区到内存，从 0x7c00 开始，所以这是 启动扇区的加载地址。
这也是启动扇区开始执行的位置，也是 link address。
我们可以通过给 boot/Makefrag 中的 linker 传递参数 -Ttext 0x7c00 来设置 link address，所以 linker 可以在生成的代码中产生正确的内存地址。

练习 5：重新跟踪 boot loader 的初始的几条指令，然后确定程序时从哪里开始 break 的，或者说，如果你拿到了 boot loader 错误的 linker address 从哪里开始报错。然后尝试在 boot/Makefrag 中更改错误的 link address，运行 make clean，重新编译实验代码 make，然后重新跟踪 boot loader 观察发生了什么。

回顾内核的 load 和 link address。
不像 boot loader，这两个地址并不相同：kernel 告诉 boot loader 从低地址（1MB）把 kernel 加载进内存，但是它又起到从一个高地址开始执行。
我们将会在下一节深入探讨如何在这种思路下，实现内核代码。

除了 section 信息，在 ELF header 中还有一个 field 对我们来讲是重要的，
它叫做 e_entry。这个字段保存了 entry point 的 link address：程序的 text section 中的内存地址，这是程序开始执行的地方，你可以通过下面的命令查看：

objdump -f obj/kern/kernel

你现在应该能够在 boot/main.c 理解最小的 ELF loader 了。
它从磁盘中读取内核的每个 section，跟进 load address 把他们加载到内存中。
然后跳转到 kernel 的 entry point。

练习 6：我们可以通过 GDB 的命令 x 来测试内存。
https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html
给我们提供了关于 GDB 的详细的信息，但是现在，只需要知道 x/Nx ADDR
能打印内存的从 ADDR 开始的 N 个字就可以了。
需要注意的是，字的大小并不是一个统一标准，在 GNU 汇编中，一个 word 是 2 个字节。

退出 QEMU/GDB 然后重新启动，从 0x00100000 开始，测试 8 个字的内存，这是 BIOS 进入 boot loader 的位置，然后重复操作，定位到 从 boot loader 进入到 kernel 的位置。为什么他们是不同的？在第二个断点处有什么？
（你不需要使用 QEMU 来回答这个问题，只需要思考一下就可以了）

### 内核

我们现在将会更多地了解一些关于 minimal JOS kernel 的具体细节。
（在这部分你将会写一点代码）。
就像 boot loader 一样， kernel 以一些汇编代码开始，设置一些东西，然后 C 语言代码可以正常地执行。

使用虚拟内存来解决位置依赖性

当你观察上面讲到的 boot loader 的 linK 和 load address 时，它们两个可以完美地匹配，但是 kernel 的 link 和 load address 这两个地址并不相同。
链接内核比链接 boot loader 更加复杂，所以 link 和 load address 处于 kern/kernel.ld 的最顶端。

操作系统内核经常在非常高的 virtual address 进行连接和运行，比如 0xf0100000，这为了把处理器的低虚拟地址空间留给用户程序使用。
这种分配方式的理由将在下一个实验中变得更加清晰。

许多机器并没有物理地址 0xf0100000，所以我们不能指望把内核放在那个位置。
因此，我们使用处理器的内存管理硬件把 0xf0100000 映射到物理地址 0x00100000 上。
0xf0100000 是 kernel 源代码希望运行的 link address。
0x00100000 是 boot loader 把内核加载到物理地址空间的位置。
通过这种方式，虽然 kernel 的虚拟地址已经高到可以给用户进程留下足够的地址空间，但是它仍然会被加载到 PC RAM 的低地址空间上。
这种方式要求计算机最少要有几兆字节的物理内存，来保证物理地址 0x00100000 是有效的。

实际上，在下一个实验中，我们将会把整个 PC 物理地址空间底部的 256MB （0x00000000 - 0x0fffffff）的内容映射到虚拟地址 0xf0000000 - 0xffffffff。
你应该可以理解为什么 JOS 可以只用头部的 256MB 的物理内存了。

现在，我们将仅仅映射 4MB 的物理内存，这对于启动和运行系统来说，已经足够了。
我们使用手写、静态初始化页目录和页表来完成这项工作，详细代码参考 kern/entrypgdir.c。
现在，你不需要理解这种方式的工作细节，只需要从它完成的工作来观察结果就可以了。
直到 kern/entry.S 设置了 CRO_PG 标志，内存引用被视为物理地址。
更严格地将，他们是线性地址，但是 boot/boot.S 设置了从线性地址到物理地址的线性映射，我们将不会去修改这些。
一旦 CRO_PG 被设置了，内存引用就变成了虚拟地址，虚拟地址需要经过虚拟内存硬件翻译为物理地址。entry_pgdir 会把虚拟地址 0xf0000000 - 0xf0400000 翻译为物理地址 0x00000000 - 0x00400000，虚拟地址 0x00000000 - 0x00400000 也会被翻译为 0x00000000 - 0x00400000。
任何不在这个范围的虚拟地址将会导致硬件异常，但是我们目前还没有设置中断处理机制，这将会导致 QEMU 转储机器状态并退出，如果你没有使用 6.828-patched 版本的 QEMU 的话，这将会永无止境地重启。

练习 7：使用 QEMU 和 GDB 来跟踪 JOS kernel，并在 mov1 %eax, %cr0 停止。
测试 0x00100000 和 0xf0100000 的内存。
现在，使用 stepi 来进行单步调试。
重复测试 0x00100000 和 0xf0100000 的内存。
确保你能理解发生了什么。

在新映射建立之后，第一条由于映射关系的错误发生失败的指令是什么？
在 kern/entry.S 中注释掉 mov1 %eax, %cr0，跟踪它，并观察你是否正确。

格式化输出到终端

许多人认为 print() 是与生俱来的，而且甚至认为它们就是 C 语言原语的。
但是在 OS kernel 中，我们将会自己实现所有的 I/O。

阅读 kern/printf.c, lib/printfmt.c, kern/console.c 并确保你能理解他们之间的关系。
后面你就会明白为什么会把 printfmt.c 单独隔离出来放在 lib 目录下。

练习 8：我们省略了一小部分代码 —— 使用模式匹配 "%o" 打印八进制数字的必要代码。找出并填充好这个代码片段。

你需要能够回答下面的问题：

1. 解释 printf.c 和 console.c 之间的接口。尤其是 console.c 输出了什么？为什么这个函数被 printf.c 使用了？
2. 根据 console.c 解释下面的代码：

```{code-block} c
1      if (crt_pos >= CRT_SIZE) {
2              int i;
3              memmove(crt_buf, crt_buf + CRT_COLS, (CRT_SIZE - CRT_COLS) * sizeof(uint16_t));
4              for (i = CRT_SIZE - CRT_COLS; i < CRT_SIZE; i++)
5                      crt_buf[i] = 0x0700 | ' ';
6              crt_pos -= CRT_COLS;
7      }
```

3. 下面的问题你可能需要参考 lecture 2 的笔记。这些笔记涵盖了 x86 平台上的 GCC 调用规则。

跟踪下面语句的执行过程：

int x = 1, y = 3, z = 4;
cprintf("x %d, y %x, z %d\n", x, y, z);

- 在调用 cprintf() 时， fmt 指向了什么？ap 指向了什么？
- 根据执行顺序，列出针对 cons_putc va_arg vcprintf 的每一个调用。对于 cons_putc 列出他的参数，对于 var_arg ，分别列出在调用前后 ap 分别指向了什么。对于 vcprintf 列出它的两个参数的值。

4. 运行下面的代码：

unsigned int i = 0x00646c72;
cprintf("H%x Wo%s", 57616, &i);

输出是什么？解释为什么会得到这样的输出。你可能需要参考 ASCII 码表。

有这样的输出是因为 x86 是小端模式。如果 x86 是大端模式，你应该如何设置 i
的值来得到同样的输出？你是否应该修改 57616？

5. 在下面的代码中， y 的值是多少（结果并不是一个确定的值）？为什么会出现这种现象？

cprintf("x=%d y=%d", 3);

6. 假设 GCC 更改了调用规则，并因此它按照声明的顺序将参数进行压栈，故最后一个声明的参数是最后一个压栈的。你将如何更改 cprintf 或他的接口，来让它能够接收可变数量的参数？

挑战：加强版的 console 可以在终端中输出不同颜色的字体。
传统的做法是用 ANSI escape sequence 包裹文本，然后由终端来解释这段包裹代码。
如果你兴趣，可以参考 https://pdos.csail.mit.edu/6.828/2018/reference.html 来根据自己的兴趣做更改，这可能涉及到关于 VGA 显示硬件的编程。首先你应该把 VGA 硬件调整到 graphics 模式，然后让控制台能够在 graphical frame buffer 中绘制彩色文本。

### 栈

这是本次实验的最后一个练习，我们将探索 C 语言是如何在 x86 架构上使用栈的。在这个过程中，我们将会写一个有用的新的内核监视器函数，这个函数将能够输出栈中的 backtrace：一个保存了指令指针（IP）的值的列表，这些指令指针来自嵌套的 call 函数。

练习 9：明确 kernel 执行到什么语句开始创建栈空间，并准确定栈空间保存在内存的什么位置。
kernel 是如何为他的栈来预留空间的？栈指针指向的是栈顶还是栈底？

x86 栈指针（esp 寄存器）指向栈中正在使用的最低的地址。所有处于该地址以下的区域都是空闲区域。每次向栈中压入一个值，都会先使栈指针下移一个单位，然后把值写入栈指针指向的位置。从栈中弹出一个值，包含了读取栈指针指向的值和栈指针增加一个单位两个过程。
在32位模式下，栈只能存取 32 位的值，并且 esp 寄存器经常被四等分。
许多 x86 指令，比如 call，都是硬连线地区使用栈指针寄存器。

根据软件惯例，ebp 寄存器（基指针）主要与栈相关联。
在一个 C 函数的入口处，函数的 prologue 代码通过将前一个函数的基指针压栈来保存这个基指针，然后为了应对函数的 声明周期，把当前 esp 的值拷贝到 ebp。
如果程序中所有的函数都遵守这个约定，那么在程序执行期间，任何给定的时间点，都有可能通过对栈进行回溯找到函数之间的调用关系。
发现这种调用关系的能力非常重要，比如，如果某个函数由于非法参数导致了 assert 错误，或者 panic，但是你又不知道这个非法参数是谁传递过来的，那么栈回溯就可以帮你应对这种场景了。

练习 10：熟悉 x86 平台上的 C 语言调用规则，找到 obj/kern/kernel.asm 中函数 test_backtrace 的入口地址，在那里设置一个断点，然后测试在内核启动后，每次调用都会发生什么。在每个 test_backtrace 级别上，有多少个 32 位的字被压栈，这些被压入的字都是什么？

如果你想要成功地完成这个实验，你需要使用 patcked version of QEMU。
否则，你需要自行地翻译所有断点的内存地址到线性地址。

上面的练习给了你一些关于如何实现栈回溯函数的一些信息，这些信息来源与函数 mon_backtrace()。一个原型函数已经在 kern/monitor.c 中实现了。
你可以用纯 C 代码编写，但是你会发现 inc/x86.h 中的 read_ebp() 函数十分有用。
你可能也需要在 kernel montor 的命令参数列表中对这个新函数创建钩子，然后他就可以跟用户交互了。

回溯函数应该可以展示一系列的函数调用，比如类似下面这样的输出：

```{code-block} text
Stack backtrace:
  ebp f0109e58  eip f0100a62  args 00000001 f0109e80 f0109e98 f0100ed2 00000031
  ebp f0109ed8  eip f01000d6  args 00000000 00000000 f0100058 f0109f28 00000061
  ...
```

每一行都包括 ebp eip args。
ebp 表示函数正在使用的基指针，比如，基指针的位置紧跟在函数入口和函数的 创建基指针的代码（prologue code）的后面。
eip 是函数的返回指令指针，它是当函数返回时的那条控制命令的指令地址。
返回指令指针通常指向在 call 指令之后的指令（为什么呢）。
最后列在 args 之后的 5 个 16 进制数字是函数的前 5 个参数，在函数调用发生之前就会被压栈了。如果函数调用需要的参数少于 5 个，当然，这 5 个参数并不会都其效果（为什么回溯代码不能检测真实需要多少个参数？这种缺陷应该如何修复？）。

第一行输出展示了当前正在执行的函数，是 mon_backtrace 本身，
第二行输出展示了调用 mon_backtrace 的函数，
第三行展示了调用第二行函数的函数，并依次循环。

你应该打印所有的 outstanding 栈帧。
通过学习 kern/entry.S 你可以发现这有一个简单地方式来告诉函数什么时候停止。

阅读《C 语言程序设计》时，有一些重要的知识点，需要你记忆，后面的实验可能会用到：

- 如果 `int *p = (int *) 100`，并且 `(int)p + 1` 和 `(int)(p+1)` 是不同的数字：第一个是 101，但第二个是 104。当给指针加一个整形数字是，也就是第二种情况所示，这个整形数字被默认乘以了指针指向的对象的大小。
- `p[i]` 和 `*(p+i)` 是等价的，都是 p 指向的内存空间中的第 i 个对象
- `&p[i]` 和 `(p+i)` 是等价的，都是 p 指向的内存空间中的第 i 个对象的地址

虽然大多数 C 代码都不需要指针和整形数字之间的相互转换，但是操作系统却经常需要这么干。
无论什么时候见到在内存地址上做加法，你都要问问自己这是一个整形加法还是指针加法，并确保如果是整形数字加到了指针上，那么是否乘以了相应的倍数。

练习 11：实现上述提到的回溯函数。使用示例中提到的相同的格式，否则打分脚本（grading script）将会很混乱。
当你考虑你是否让它在正常工作是，使用 make grade 来查看输出，确认这种格式是符合我们打分脚本期待的，如果不是，请修改它。
在你提交 lab1 的代码后，你就可以随心所欲地修改回溯函数的输出格式了。

如果你在使用 read_ebp()，注意 GCC 可能会生成优化过的代码：在 mon_backtrace() 函数的 prologue 之前调用了 read_ebp()，这将会导致不完整的栈轨迹，关于最近函数调用的许多栈帧都丢失了。
当我们尝试来关闭优化的时候，这将会导致重新排序，你需要亲自尝试调试 mon_backtrace() 的汇编代码，并确保 read_ebp() 函数调用发生在 prologue 之后。

到目前为止，你的回溯函数应该可以通过调用 mon_backtrace() 给出栈中的函数调用地址了。
然而，在实战中，你经常想知道对应内存地址上的函数名字。
比如，你想知道那个函数包含的 bug 可能会导致 kernel 崩溃。

为了帮助你实现这个函数，我们提供了一个函数 debuginfo_eip()，它会在符号表中查找 eip 并返回对应内存地址上的调试信息。
这个函数被定义在了 kern/kdebug.c 中了。

练习 12：针对每一个 eip，修改它对应的函数名、源文件名、行号栈回溯函数的显示信息。

在 debuginfo_eip 中， `__STAB_*` 来自哪里？这个问题有一个很长的回答。
为了帮助你找到答案，我们希望你能完成下面几件事情：

- 在文件 kern/kernel.ld 中查找 `__STAB_*`
- 运行命令 objdump -h obj/kern/kernel
- 运行命令 objdump -G obj/kern/kernel
- 运行命令 gcc -pipe -nostdinc -O2 -fno-builtin -I. -MD -Wall -Wno-format -DJOS_KERNEL -gstabs -c -S kern/init.c，然后查看 init.s 文件
- 查看 bootloader 是否把符号表作为 kernel 二进制文件的一部分，加载到内存中了。

实现 debuginfo_eip 函数，可以使用 stab_binsearch 函数来根据一个内存地址查找行号。

向 kernel monitor 中添加 backtrace 命令，并在你的 mon_backtrace 函数中扩展 debuginfo_eip 函数，然后按照如下格式打印每个栈帧。

```{code-block} text
K> backtrace
Stack backtrace:
  ebp f010ff78  eip f01008ae  args 00000001 f010ff8c 00000000 f0110580 00000000
         kern/monitor.c:143: monitor+106
  ebp f010ffd8  eip f0100193  args 00000000 00001aac 00000660 00000000 00000000
         kern/init.c:49: i386_init+59
  ebp f010fff8  eip f010003d  args 00000000 00000000 0000ffff 10cf9a00 0000ffff
         kern/entry.S:70: <unknown>+0
K> 
```

ebp 是函数的基地址，eip 是函数的第一条指令所在的地址。
下面一行中首先是函数名，然后是函数的第一条指令相对于 eip 的偏置，
然后是函数的最后一条指令相对于函数的第一条指令的偏移的字节数。

你可以用类似 `printf("%.*s", length, string)` 这样的语句让输出看起来更标准。

你可能会发现在打印输出中，丢失了一些栈轨迹。比如，你可能看到了关于 monitor() 的调用，但是不是 runcmd()。这是因为编译器内联了一些函数调用。
其他的优化可能也会导致你看到不希望看到的行号。。如果你想避免这种现象，在 GMUMakefile 中使用 -O2 参数，然后栈轨迹可能看起来才会更加合理，但是你的内核可能会因为缺少了优化运行的更慢。

---

[^cite_ref-1]: <https://pdos.csail.mit.edu/6.828/2018/schedule.html>
