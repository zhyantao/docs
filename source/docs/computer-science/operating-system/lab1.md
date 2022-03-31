(microkernel_os_lab1)=
# 实验一

在本次实验中，你将学习下面几个知识点：

- 熟悉 x86 汇编语言；
- 熟悉计算机的启动过程；
- 熟悉 QEMU/GDB 的调试方法。

开始实验之前，你应该对本次实验有一个宏观认识。实验一可分为三个部分：

- 第一部分聚焦于熟悉 x86 汇编语言，QEMU 仿真器，以及计算机上电启动过程。
- 第二部分着重于跟踪调试 `lab/boot` 目录下的 bootloader。
- 第三部分深入 kernel 初始化过程，侧重于跟踪调试 `lab/kern` 目录下的 kernel，也就是 JOS。

## 准备工作环境

MIT6.828 提到使用 Athena machine 将更加方便，但是不是这个学校的学生可能接触不到这个机器。
因此后续工作将在自己的虚拟机上完成，用到的环境如下：

- Ubuntu 16.04 [32-bit PC (i386) desktop image](https://releases.ubuntu.com/16.04/)
  (不要装  64 位虚拟机) 以及 VMWare
- GIT 2.25.1 / Python 2.7 / GCC 5.4.0 以及 **gcc-multilib** /
  [6.828 patched QEMU](https://github.com/mit-pdos/6.828-qemu)

需要注意的是，在 Ubuntu 这个系统中，默认应该是有 Python 2.7 的，可以通过 `python2 --version`
检查一下。如果没有，我们可能需要用 `sudo apt install python2`
来安装一下，如果有，我们直接给它建立软连接或硬连接就可以了。

```{code-block} text
sudo ln /usr/bin/python2 /usr/bin/python
```

我们并不是完全地从 0 开始写代码，而是在已有内核上添加一些新功能，故我们先将内核代码克隆到虚拟机上：

```{code-block} text
mkdir ~/6.828
cd ~/6.828
git clone https://pdos.csail.mit.edu/6.828/2018/jos.git lab
```

有一些简单的 Git 命令你需要掌握，比如查看做了哪些修改，如何提交代码等，这些知识可以参考
{ref}`另一篇文章 <git-syntax>`。

然后我们需要安装硬件仿真器 QEMU，但是 6.282 并不推荐我们使用 qemu.org 提供的 QEMU。故改用
6.828 打过补丁的 QEMU，但是，若直接使用 6.828 patched QEMU，在 `make` 时，会出现一些报错。
后面我通过查阅资料，修复了这些报错，所以你可以直接使用我改好的代码来进行编译：

```{code-block} text
cd ~/6.828
git clone https://github.com/zhyantao/6.828-qemu.git qemu
```

在编译 QEMU 源代码之前，我们需要安装一些依赖。
如果你使用清华的镜像源，可能找不到某些需要的依赖包，因此现在 **统一使用**
[阿里云的镜像源](https://developer.aliyun.com/mirror/)：

```{code-block} text
sudo apt install -y libsdl1.2-dev libtool-bin libglib2.0-dev libz-dev libpixman-1-dev
```

安装完依赖后，就可以在 QEMU 源代码的基础上进行编译和安装了。

```{code-block} text
cd ~/6.828/qemu
./configure --disable-kvm --disable-werror \
  [--prefix=PFX] [--target-list="i386-softmmu x86_64-softmmu"]
make
sudo make install
```

上面中括号部分是可选项，若不指定 `--prefix`，则默认安装到 `/usr/local` 下，`--target-list` 将会对
QEMU 进行瘦身，编译安装指定的架构，若你不熟悉自己的 CPU 架构，可以缺省这个参数 [^cite_ref-2]。

(asm_syntax)=
## 汇编语法

汇编语法并不是本门课的重点，但是在后续课程中，你要能看懂别人写的汇编，因此你需要自学汇编语言，
6.828 给我们推荐了一些资料。

*[PC 汇编语言](https://kdocs.cn/l/cq5FqOlocImF)* [^cite_ref-5]
用的是支持 Intel 语法的 Netwide Assembler (NASM)，而 6.828 用的是支持的是 AT&T
语法的 GNU Assembler。这意味着要学会这这两种语法的相互转换，因此 6.828 强烈建议我们阅读
{ref}`inline_assembly_syntax`。

除了 *PC 汇编语言* 这本书，还有两个参考手册供我们查阅，一个是
[简洁版的 i386 编程手册](https://pdos.csail.mit.edu/6.828/2018/readings/i386/toc.htm)，另一个是
[详细版的](http://www.intel.com/content/www/us/en/processors/architectures-software-developer-manuals.html)
的。对于 6.828 这门课而言，简洁版已经够用了。

如果你想了解更多关于指令集的知识，除了 Intel 提供的指令集手册，AMD 官网也提供了
[相似的手册](https://developer.amd.com/resources/developer-guides-manuals/)。

## 运行 kernel 代码

不知道你注意到 QEMU 这个软件没有，它在实验中充当的是一个虚拟电脑的角色。
这台虚拟电脑和我们在现实中用到的电脑在功能上没有什么两样，只不过这台虚拟电脑以代码的形式存在。

如果我们在真实物理机上启动操作系统，这并不是一个难事，但是如果想要调试这个操作系统，问题就来了。
如何在程序启动的过程中设置断点？
这好像是在电脑上电后我们无法控制的事情，那么如果这台电脑以软件的形式存在，那么设置断点就很好办了。

所以，QEMU 因此诞生，它的职责就是充当台式机或笔记本电脑，允许我们把写好的操作系统运行在其中。

那么 QEMU 是如何起作用的呢？
其实，我们写的代码，经过 QEMU 的一层封装之后，它还是实际在使用真实物理机。
因此，本质上我们写的软件和硬件发生关系的链条是：

```{code-block} text
我们写的操作系统 --- QEMU --- Ubuntu --- VMware --- Windows --- 真实物理机
```

可以看出来，这是一个多层嵌套的关系。
我们写的操作系统被各种软件层层包围，最后才能触及真实物理机上的硬件设备。

那么，如何使用 QEMU 这个硬件仿真器呢？
使用仿真器之前，确保你已经使用命令 `make` 编译过内核，并得到了内核映像 `kernel.img`。
正确的输出应该是下面这个样子：

```{code-block} text
user02@node1:~/6.828/lab$ make
+ as kern/entry.S
+ cc kern/entrypgdir.c
+ cc kern/init.c
+ cc kern/console.c
+ cc kern/monitor.c
+ cc kern/printf.c
+ cc kern/kdebug.c
+ cc lib/printfmt.c
+ cc lib/readline.c
+ cc lib/string.c
+ ld obj/kern/kernel
ld: warning: section `.bss' type changed to PROGBITS
+ as boot/boot.S
+ cc -Os boot/main.c
+ ld boot/boot
boot block is 412 bytes (max 510)
+ mk obj/kern/kernel.img
user02@node1:~/6.828/lab$ 
```

那么我们现在已经有了 "内核" 源代码，怎么将内核源码存放到磁盘（disk）中并加载运行呢？
这个工作已经被 QEMU 做了，它帮我们存储并解析了 bootloader (`obj/boot/boot`) 和 kernel
(`obj/kernel`)，但是，如何它是如何存储和解析的，这些细节现在暂时还不清楚，下一节将会解答。
但是现在能知道的是，使用 `make qemu` 或 `make qemu-nox` (在使用 SSH 时推荐用后一种)
这两个命令中的任何一个，都可以帮我们启动内核。
因此，`make qemu` 的效果就跟按下电脑开机键一样，从磁盘加载引导文件，然后启动操作系统内核。
启动成功后的效果如下所示：

```{code-block} text
user02@node1:~/6.828/lab$ make qemu-nox
sed "s/localhost:1234/localhost:26000/" < .gdbinit.tmpl > .gdbinit
***
*** Use Ctrl-a x to exit qemu
***
qemu-system-i386 -nographic -drive file=obj/kern/kernel.img,index=0,media=disk,\
    format=raw -serial mon:stdio -gdb tcp::26000 -D qemu.log 
6828 decimal is XXX octal!
entering test_backtrace 5
entering test_backtrace 4
entering test_backtrace 3
entering test_backtrace 2
entering test_backtrace 1
entering test_backtrace 0
leaving test_backtrace 0
leaving test_backtrace 1
leaving test_backtrace 2
leaving test_backtrace 3
leaving test_backtrace 4
leaving test_backtrace 5
Welcome to the JOS kernel monitor!
Type 'help' for a list of commands.
K>
```

内核启动成功后，我们看到的是一个 JOS kernel monitor，这个监视器会监听串口输入（键盘输入）。
这个内核监视器是直接运行在仿真器的原始硬件上的。如果你把 `obj/kern/kernel.img`
拷贝到磁盘的引导区中，插到真实物理机上，通电，开机，将会看到和 QEMU 仿真器输出一样的内容。

现在这个内核只有 `help` 和 `kerninfo` 两个命令，后面随着学习的深入，我们会为它扩展新功能。

现在，我们应该能大概理解 QEMU 的作用了：**为我们编写操作系统提供一个运行环境**。

## 内存和寻址

如果想要在一个金属裸机上直接运行内核源码，那么势必需要知道 **内核源码的入口地址** 在哪里。
如果我们不加约束，每个人都自定义一个入口地址，那么我写的操作系统可能在你的机器上就找不到入口地址。
因此，为了通用性，我们会按照约定，将内核源代码放在磁盘中一个固定的位置，也就是下面展示的低 1MB 空间中。

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

从上面的内存地址编码上就可以看出来，每个地址都是 32 位的，因此这是一个 32 位机。
我们还可以发现，这个机器可以寻址 4GB 的物理内存，也就是说，如果我们给这个机器挂载一个 8GB
的磁盘，那么它将无法充分使用这个外加磁盘。
RAM 之下就是我们常说的内存，所有需要上 CPU 运行的程序，都会先加载到 RAM 中。
图中的 Low Memory 通常被用于存储中断向量表、BIOS 控制信息、应用程序内部信息 [^cite_ref-3]。

从 `0x000A0000` 到 `0x000FFFFF` 的 384KB 是为硬件预留的区域，在本例中被用作了图像缓冲（VGA Display）。
当然最重要的用途还是用于存储 BIOS，它占用了 64KB 的大小。
在早期计算机中，BIOS 是存储在只读存储器中（ROM）的，但是现在的计算机把 BIOS 存储在了 flash 中了。
BIOS 的作用是提供系统初始化功能，比如激活显卡、检查已用内存。
初始化完成后，BIOS 从磁盘、软盘或 USB 等设备上加载操作系统，并把 CPU 的控制权转移给操作系统。

在早期的计算机中，寻址能力其实是很弱的，比如 16 位的 Intel 8088 处理器只能寻址 1MB
的物理内存，从 `0x00000000` 开始，到 `0x000FFFFF` 结束，而不是上图所示的 `0xFFFFFFFF`。
事实上，更早期的计算机只能配置 16KB、32KB、或 64KB 的 RAM。
这种转变是在英特尔发布 80286 和 80386 处理器后，突破了 1MB 的内存限制，开始支持 16MB 和 4GB
的物理地址空间。

但为了能够向后兼容，现在的计算机仍然保留了低 1MB 物理地址空间的原始布局，给 16-bit devices
预留空间，这是第一个 hole。并把 RAM 之下的部分分成三个区域，分别叫做 Low Memory，Conventional
Memory 和 Extended Memory。
现在的 x86 处理器支持扩展内存，所以 4GB RAM 并不是上限，在这种情况下，BIOS 又必须给 32
位设备映射预留空间，也就是上图所示的 32-bit memory mapped devices，这是第二个 hole。

因为设计的限制，JOS 仅使用前 256MB 的物理地址空间，所以在后面的实验中，我们将会假设所有的计算机仅有
32 位物理地址空间。

## 内核的启动流程

知道了内核源码的入口地址，那么接下来就需要尝试，如何启动内核程序了。
在这部分，我们将使用 QEMU 的调试工具来研究如何启动一个 [IA-32](https://zh.wikipedia.org/wiki/IA-32)
(Intel Architecture, 32-bit) 兼容的电脑。

打开两个 Terminal，并 `cd` 到 `lab` 目录下，在其中一个 Terminal 中键入 `make qemu-gdb`，或者
`make qemu-nox-gdb`，在另一个 Terminal 中键入 `make gdb`。

命令 `make qemu-gdb` 会启动 QEMU，并让它在卡在第一条内核代码之前，方便我们一步步地调试内核源码。

命令 `make gdb` 可以让我们在前面的卡住的地方继续向下执行，并把执行的命令在这里显示出来。
比如，如果我们按照上面的步骤操作，应该会得到下面类似的输出：

```{code-block} text
+ target remote localhost:26000

The target architecture is assumed to be i8086
[f000:fff0]    0xffff0: ljmp   $0xf000,$0xe05b
0x0000fff0 in ?? ()
+ symbol-file obj/kern/kernel
(gdb) 
```

之所以有上面的的输出，是因为我们在源代码 `.gdbinit` 定义了某些监听规则。
从效果上观察，`make qemu-gdb` 可以让是 QEMU 的卡在启动过程，`make gdb` 让 QEMU
继续执行，并把执行细节（执行的汇编语句）显示出来。

有了这种工具，我们就可以一步一步地调试，然后看在计算机的启动过程中，到底发生了什么。

```{code-block} text
[f000:fff0]    0xffff0: ljmp   $0xf000,$0xe05b
```

上面那行代码是 GDB 对内核启动后，第一条指令的的反汇编。从输出可以推断出一些信息：

- 计算机启动后的能够找到的 **内核的入口地址** 是 `[CS:IP]=[0xf000:0xfff0]`；
- 逻辑地址 `[0xf000:0xfff0]` 转化为物理地址是 `0x000ffff0`；
- `0x000ffff0` 处于 BIOS ROM 预留区域，并且该物理地址位于预留区域顶部之下的 16 字节；
- 第一条被执行的指令是 `ljmp`，它跳转到段地址 `[0xf000:0xe05b]`。

因为 BIOS 在计算机中是硬连线的，把内核的入口地址写在固定的位置，可以确保 BIOS
在电脑上电后能够始终最先得到 CPU 的控制权，当 BIOS
执行完一些必要的初始化工作后，再将 CPU 的控制权转移给操作系统。
**这种设计是非常重要的，因为在计算机上电后的瞬间，机器的 RAM 中除了 BIOS 没有其他的程序可以执行。**

在处理器复位时，仿真器将会进入实模式，并把 CS 和 IP 分别设置为 `0xf000` 和
`0xfff0`，确保每次都能找到内核的入口地址。

```{admonition} 练习 2
使用 GDB 的 `si` 命令继续追踪 BIOS，观察汇编指令，总结一下 BIOS 完成了什么功能。
如果你想理解更多计算机内存和 I/O 的工作细节，可以参考
[[webpage](http://web.archive.org/web/20040404164813/members.iweb.net.au/~pstorr/pcbook/book2/book2.htm)]。
但是现在你并不需要明白所有的细节，针对 BIOS 是如何启动的，有一个大致的思路就可以了。

如果你并不熟悉应该如何具体操作，那么关于 GDB 的命令，我建议先阅读一下
[gdb cheatsheet](https://kdocs.cn/l/cncEx5Kq8rkd)。
如果你能够使用 Tmux 来分屏显示，那么可能效率会更高，详细的命令参考 [tmux cheatsheet](https://quickref.me/tmux)。
```

完整的启动流程如下：

- 系统上电，处理器复位（重置 `CS:IP`），找到当 BIOS 入口地址，执行第一条语句；
- BIOS 负责建立中断描述表、初始化 PCI 总线、初始化各种设备（比如 VGA、SeaBIOS）；
- BIOS 搜索装有操作系统内核的设备（如磁盘、软盘、CD-ROM、USB 等）；
- BIOS 从设备中将 bootloader 加载到内存，并让它上 CPU 执行（转移 CPU 控制权）；
- 开机引导程序（bootloader）负责启动操作系统内核，开机成功。

## 调试 bootloader

开机引导程序（bootloader）是嵌入式系统在加电后执行的第一段代码，主要的工作流程如下 [^cite_ref-4]：

1. 完成 CPU 和相关硬件的初始化之；
2. 将操作系统映像或固化的嵌入式应用程序装载到内存中；
3. 跳转到操作系统所在的空间，启动操作系统运行。

磁盘按照 512 字节的大小划分扇区（sectors），它是磁盘 I/O 的最小粒度。
每次 **读/写** 操作都必须是一个或多个扇区，且符合边界对齐规则。
如果在第一个扇区装有 bootloader，那么这个扇区可以被称为启动扇区，对应的磁盘叫做启动盘。

当 BIOS 找到启动盘后，它首先将启动扇区载入内存 `0x7c00` - `0x7dff` 中，
然后用 `jmp` 指令将 `CS:IP` 设置为 `0000:7c00`，将 CPU 的控制权转移给 bootloader。
需要注意的是启动扇区载入内存后的物理地址并不是一成不变的，只要遵守约定，能够让 BIOS
跳转到那里就可以了。

现代计算机可以通过多种方式启动内核，比如 CD-ROM，这种启动方式更复杂、更强大。
CD-ROM 的扇区大小是 2048 字节，因扇区大小不同于磁盘，实现细节也略有不同，如果有兴趣可以参考
[[webpage](https://pdos.csail.mit.edu/6.828/2018/readings/boot-cdrom.pdf)]。

对于 6.828 这门课程而言，我们使用的是传统的磁盘启动方式，也就是说 bootloader 必须调整为 512 字节。

bootloader 包括一个汇编源文件 `boot/boot.S` 和一个 C 源文件 `boot/main.c`。
仔细阅读源文件，并确保你能看懂源文件中的代码，理解启动过程发生了什么事情。

如果你读完了这两个代码，会发现 bootloader 主要完成下面两个功能：

1）bootloader 将处理器从实模式转换为 32 位保护模式。因为只有在保护模式下，软件才能访问超过 1MB
的所有内存空间。现在，你只需要理解在保护模式下逻辑地址 `[CS:IP]`
翻译为物理地址的过程是与实模式下的翻译过程是不相同的，并且翻译完成后 IP 是 32 位 而不是 16 位。
关于保护模式的具体细节参考 [[webpage](https://pdos.csail.mit.edu/6.828/2018/readings/pcasm-book.pdf)]
的 1.2.7 节和 1.2.8 节。如果遇到不会的指令，可以复习 {ref}`asm_syntax` 中提到的超链接。

2）bootloader 通过 x86 提供的特殊的 I/O 指令直接访问 IDE 磁盘设备寄存器从磁盘中读取内核。
如果你想更好地理解这些特殊的 I/O 指令是什么意思，可以参考
[[webpage](https://pdos.csail.mit.edu/6.828/2018/reference.html)] 中提到的 IDE Hard drive controller 部分。
但是，你并不需要在本课程中学习过多关于如何针对特定设备进行编程（驱动开发）的知识，因为这不是这门课的重点。

在你理解了 bootloader 的源代码后，阅读一下汇编文件 `obj/boot/boot.asm`，它是编译完 bootloader
后，GNUMakefile 创建的反汇编文件。
这个反汇编文件让我们能够更简单地看懂在物理内存上，到底存放了怎样的 bootloader 源代码。
并且，也能够让我们在使用 GDB 调试 bootloader 时，更轻松地追踪代码。
同样地，`obj/kern/kernel.asm` 是 JOS kernel 的反汇编文件，也是为了帮助我们简化调试过程。

你可以用指令 `b` 在 GDB 中添加断点。比如 `b *0x7c00` 在地址 `0x7c00` 设置了一个断点。
执行到断点处，你可以使用 `c` 和 `si` 让它继续执行：指令 `c` 是继续执行直到碰到下一个断点，`si N`
是在继续执行 `N` 条指令。

命令 `x/i` 是一个反汇编指令，也可以用来查看内存中的值，从输出上看内存中可能存的是指令也可能是数据。
`x/Ni ADDR` 可以用来查看从地址 `ADDR` 算起，之后 `N` 个内存单元中的值。

```{admonition} 练习 3
根据 [[webpage](https://pdos.csail.mit.edu/6.828/2018/labguide.html)] 学习 GDB
调试技巧，并完成下面几个小任务。

- 在 `0x7c00` 设置断点（这是启动扇区被加载的位置），继续执行直到碰到下一个断点；
- 完整追踪调试 `boot/boot.S`，参考 `obj/boot/boot.asm` 来明确程序现在运行到哪里了；
- 利用命令 `x/i` 反汇编 bootloader，然后分别与源代码和反汇编代码 `obj/boot/boot.asm` 作对比；
- 单步调试 `boot/main.c` 并进入子函数 `bootmain()` 然后进入子函数 `readsect()`；
- 找到 `readsect()` 函数声明语句对应的汇编指令；
- 调试 `readsect()` 函数中的剩余语句，然后返回 `bootmain()` 函数；
- 找到 `for` 循环从磁盘读取剩余内核扇区的开始和结束位置；
- 找出循环结束后将会执行什么代码，并在循环执行结束的位置设置一个断点；
- 从断点继续向下执行，追踪 bootloader 的剩余部分。
```

做完练习 3 后，你应该尝试回答下述问题：

- 处理器从什么位置开始执行 32 位的代码？什么代码触发了从 16 位到 32 位的转换？
- bootloader 的最后一条指令是什么？内核被加载的第一条指令在哪里，是什么？
- bootloader 如何确定需要读多少个扇区，保证从磁盘中读取出一个完整内核？它从哪里找到这些信息？

## 如何定位 kernel

在继续向下学习之前，我们需要确保你对 C 语言的指针有一定的了解。

```{admonition} 练习 4
阅读 *[C 语言程序设计](https://kdocs.cn/l/coVOZtu777O9)* 5.1 到 5.5 小节，然后下载
[pointers.c](https://pdos.csail.mit.edu/6.828/2018/labs/lab1/pointers.c) 源代码，并运行。
确保你能理解源代码输出。尤其是要确保你能理解第 1 行和第 6 行的指针地址来自哪里，第 2 行和第 4
行的输出值是如何跳到那里的，为什么第 5 行的输出值看起来是错误的？

除了上面指出的参考书外，我本人更推荐阅读
*[C 指针详解](https://kdocs.cn/l/ciF7l7TJt4Wl)*、
*[C 语言陷阱和缺陷](https://kdocs.cn/l/cp8WedXw5Mrk)*、
*[高质量 C/C++ 编程](https://kdocs.cn/l/crepwkaIiC96)*
这三本书，这些辅助资料为我们提供了需要注意的更多细节。
```

我们现在更深一步地探索 C 语言部分的 bootloader，源代码是 `boot/main.c`。

为了搞明白 `boot/main.c` 你需要知道什么是 ELF 二进制。
当你编译和链接一个 C 程序，比如 JOS kernel，编译器将会把 C 源代码转换为对象文件（`.o`）。
这个对象文件包含了硬件所能理解的二进制格式表示的汇编指令。
然后 linker 将所有编译过的 `.o` 文件合成一个二进制镜像，比如 `obj/kern/kernel`。
`obj/kern/kernel` 是 ELF 格式的，它表示可执行与可链接格式。
关于 ELF 格式，可以参考维基百科的
[简单介绍](http://en.wikipedia.org/wiki/Executable_and_Linkable_Format)，也可以参考另一个
[更详细的介绍](https://pdos.csail.mit.edu/6.828/2018/readings/elf.pdf)。
但是你并不需要深入了解这个格式的细节，因为在课程中不会涉及它最复杂的部分：共享库的动态链接。

为了能够顺利完成 6.828 你可以将 ELF 可执行文件看做一个带有加载信息的 header，
这个 header 后面是 program sections，每个 program section 都是一些连续的代码块或希望被加载进内存的数据。
bootloader 不会修改这些代码或数据，它只是把它们加载进内存然后开始执行它们。

ELF 二进制文件以一个固定长度的 ELF header 开始，后面是可变长度的 program header。
在 ELF header 的 C 语言头文件 `inc/elf.h` 中 program header
把所有需要被加载的 program section 都列了出来。但是我们感兴趣的字段只有下面几个：

- `.text` 是程序的可执行指令；
- `.rodata` 是只读数据，比如由 C 编译器产生的 ASCII 字符串常量；
- `.data` 是数据部分，保存了程序的初始化数据，比如全局变量；

当 linker 根据程序代码计算出需要的内存空间后，它会给未初始化的全局变量预留空间，比如 `int x`。
在内存的 section 部分 `.bss` 后紧跟着 `.data`。

因为 C 语言要求未初始化的全局变量以 0 值代替，所以我们不需要在 ELF 二进制文件中保存 `.bss` 的内容。
这是因为 `.bss` 可以通过只保存 `.bss` section 的位置和大小，然后让 bootloader 或者源码本身给
`.bss` section 赋予 0 值即可。

我们如何得到内核中所有的 section 的名字、大小、link address 呢？只需要键入下面的命令即可：

```{code-block} text
objdump -h obj/kern/kernel
```

你将会看到更多 section 被列了出来，但是其他部分对我们理解原理而言不是那么重要。

```{code-block} text
user02@node1:~/6.828/lab$ objdump -h obj/kern/kernel

obj/kern/kernel:     file format elf32-i386

Sections:
Idx Name          Size      VMA       LMA       File off  Algn
  0 .text         00001acd  f0100000  00100000  00001000  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, CODE
  1 .rodata       000006bc  f0101ae0  00101ae0  00002ae0  2**5
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  2 .stab         00004291  f010219c  0010219c  0000319c  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  3 .stabstr      0000197f  f010642d  0010642d  0000742d  2**0
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  4 .data         00009300  f0108000  00108000  00009000  2**12
                  CONTENTS, ALLOC, LOAD, DATA
  5 .got          00000008  f0111300  00111300  00012300  2**2
                  CONTENTS, ALLOC, LOAD, DATA
  6 .got.plt      0000000c  f0111308  00111308  00012308  2**2
                  CONTENTS, ALLOC, LOAD, DATA
  7 .data.rel.local 00001000  f0112000  00112000  00013000  2**12
                  CONTENTS, ALLOC, LOAD, DATA
  8 .data.rel.ro.local 00000044  f0113000  00113000  00014000  2**2
                  CONTENTS, ALLOC, LOAD, DATA
  9 .bss          00000648  f0113060  00113060  00014060  2**5
                  CONTENTS, ALLOC, LOAD, DATA
 10 .comment      00000029  00000000  00000000  000146a8  2**0
                  CONTENTS, READONLY
```

注意看 `.text` section 中的 VMA（link address）和 LMA（load address）。
load address 表示哪个 section 需要被加载进内存，link address 表示哪个 section 需要被执行。

linker 支持以相对路径或绝对路径的方式来查找相应的 link address。
如果我们给出了错误的 link address，那么二进制则无法起作用。
在现代的机器中，通常使用相对地址来表示 link address，优点是容易扩展，缺点是复杂性能差。
我们在本课程中不用相对路径，而是使用更简单的绝对地址来表示 link address。

一般来说，link address 和 load address 地址是相同的，比如看一下 bootloader 的 `.text` 部分

```{code-block} text
user02@node1:~/6.828/lab$ objdump -h obj/boot/boot.out

obj/boot/boot.out:     file format elf32-i386

Sections:
Idx Name          Size      VMA       LMA       File off  Algn
  0 .text         0000019c  00007c00  00007c00  00000074  2**2
                  CONTENTS, ALLOC, LOAD, CODE
  1 .eh_frame     0000009c  00007d9c  00007d9c  00000210  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  2 .stab         00000870  00000000  00000000  000002ac  2**2
                  CONTENTS, READONLY, DEBUGGING
  3 .stabstr      00000940  00000000  00000000  00000b1c  2**0
                  CONTENTS, READONLY, DEBUGGING
  4 .comment      00000029  00000000  00000000  0000145c  2**0
                  CONTENTS, READONLY
```

bootloader 用 ELF program header 来确定如何加载 section。
因为在 program header 中明确了 ELF 对象的哪一部分需要加载进内存和每一个需要使用的目标地址。
你可以通过下面的命令观察一下 progarm header：

```{code-block} text
objdump -x obj/kern/kernel
```

稍微解释一下上面这条命令的输出：ELF 对象把需要加载进内存的部分标记为了 LOAD。
vaddr 表示虚拟地址，paddr 表示物理地址，memsz 表示加载区域的大小，filesz 表示文件大小。

在 `boot/main.c` 中 `ph->p_ca` 保存的是每一个 program header 的目标段（segment）的物理地址。
尽管 ELF 规范对该字段的实际含义模糊不清，它实际上是一个物理地址。

BIOS 从 `0x7c00` 将启动扇区载入到内存，这是 bootloader 的 load address，也是 link address。
也可以将 `0x7c00` 称为 bootloader 的入口地址。
我们可以通过给 `boot/Makefrag` 中的 linker 传递参数 `-Ttext 0x7c00` 来设置 link address，让
linker 可以在生成的代码中产生正确的内存地址。

```{admonition} 练习 5
重新追踪 bootloader 的初始的几条指令，然后确定程序时从哪里开始 break 的，或者说，如果你拿到了
bootloader 错误的 linker address 从哪里开始报错。然后尝试在 `boot/Makefrag` 中更改错误的 
link address，运行 `make clean`，重新编译实验代码 `make`，然后重新追踪 bootloader 观察发生了什么。
```

对比 kernel 和 bootloader 的 load address / link address。
在 bootloader 中这两个地址是相同的，但是 kernel 中这两个地址不同。
这种现象是因为 bootloader 会把 kernel 加载到低地址（1MB）让 kernel 从高地址开始执行。
我们将会在下一节深入探讨如何在这种思路下，实现内核代码。

除了 section 信息，在 ELF header 中还有一个字段对我们来讲是重要的，它是 `e_entry`。
这个字段保存了 entry point 的 link address：程序的 `.text` section
中的内存地址，这是程序开始执行的地方，你可以通过下面的命令查看：

```{code-block} text
objdump -f obj/kern/kernel
```

通过分析 `boot/main.c` 你现在应该能理解如何加载并执行 ELF 文件了。
根据 load address 把每个 section 从磁盘中读取到内存中，然后跳转到 kernel 的
entry point，按照从高地址往下的顺序依次执行指令。

```{admonition} 练习 6
参考 [[webpage](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html)]，使用命令
`x/Nx ADDR` 来检查内存，它会打印内存从 `ADDR` 开始的 `N` 个字。
需要注意的是，字的大小并不是一个统一标准，在 GNU 汇编中，一个字是 2 个字节，16 bit。

退出 qemu-gdb 然后重新启动，从 `0x00100000` 开始，跳过 8 个字的内存（16 个字节），定位到
bootloader 的入口地址，然后重复操作，定位到从 bootloader 进入到 kernel 的位置。
为什么他们是不同的？在第二个断点处有什么？（你不需要使用 QEMU 来回答这个问题，只需要思考一下就可以了）
```

## 分析 kernel 源码

我们在这一小节更详细地了解 minimal JOS kernel 的细节：

- 内核是如何完成从虚拟地址到物理地址的映射的？
- 如何将内核运行时的信息更规范地输出到屏幕上？

和 bootloader 一样，kernel 也是以一些汇编代码开始，完成必要初始化后 C 代码才可以正常地执行。

使用虚拟内存来解决位置依赖性。
前面讲到 bootloader 的 link address 和 load address 是一样的，但是 kernel 的 link 和
load address 这两个地址并不相同。这是因为链接 kernel 比链接 bootloader 更复杂，所以 link address
和 load address 处于 `kern/kernel.ld` 的最顶端。

OS kernel 经常在非常高的 virtual address 进行链接和运行，比如
`0xf0100000`，这为了把处理器的低虚拟地址空间留给用户程序使用。

但是，许多机器并没有物理地址 `0xf0100000`，所以我们不能指望把内核放在那个位置。
因此，我们使用处理器的地址转换机构把虚拟地址 `0xf0100000` 映射到物理地址 `0x00100000` 上。
`0xf0100000` 是 kernel 源代码希望运行的 link address，`0x00100000` 是 bootloader
把内核加载到物理地址空间的位置。通过这种方式，虽然 kernel
的虚拟地址已经高到可以给用户进程留下足够的地址空间，但是它仍然会被加载到计算机 RAM 的低地址空间上。
这种方式要求计算机最少要有几兆字节的物理内存，来保证物理地址 `0x00100000` 是有效的。

在下一个实验中，我们将会把整个计算机物理地址空间底部的 256MB (`0x00000000` - `0x0fffffff`)
的内容映射到虚拟地址 `0xf0000000` - `0xffffffff` 中。你应该可以理解为什么 JOS 可以只用头部的 256MB
的物理内存了。

现在，我们仅映射 4MB 的物理内存，这对于启动和运行系统来说，已经足够了。
我们通过 **人工编写** 静态初始化页目录和页表来实现相应的映射关系，详细代码参考 `kern/entrypgdir.c`。
现在，你不需要理解这种方式的工作细节，只需要观察结果就可以了。

在阅读下面的内容之前，我们需要了解关于内存地址的概念，以及他们之间的相互转化关系：

```{code-block} text
虚拟地址 --- 逻辑地址 --- 线性地址 --- 物理地址
```

- **虚拟地址** 指由程序产生的由段选择符和段内偏移地址组成的地址。
- **逻辑地址** 指由程序产生的段内偏移。有时候直接把逻辑地址当做虚拟地址。
- **线性地址** 指虚拟地址到物理地址变换的中间层，是 *处理器可寻址的内存空间中的地址*。
  程序代码会产生逻辑地址，也就是段中的偏移地址，加上相应的段基址就成了线性地址。
  如果开启了分页机制，那么线性地址需要再经过变换，转为为物理地址。
  如果无分页机制，那么线性地址就是物理地址。
- **物理地址** 指CPU外部地址总线上寻址物理内存的地址信号，是地址变换的最终结果。

只有在 `kern/entry.S` 设置了 `CR0_PG` 标志后，内存引用才会被视为 "物理地址"。
更严格地将，这里说的内存引用实际上是线性地址，因为在 `boot/boot.S`
中设置了从线性地址到物理地址的线性映射，所以才能将这个线性地址看作物理地址。
所以说，一旦 `CR0_PG` 被设置，内存引用就会经过虚拟内存硬件的翻译，从虚拟地址变为物理地址。
而充当翻译角色的代码是 `kern/entry_pgdir.c`。它把虚拟地址 `0xf0000000` - `0xf0400000`
翻译为物理地址 `0x00000000` - `0x00400000`，而虚拟地址 `0x00000000` - `0x00400000` 也会被翻译为
`0x00000000` - `0x00400000`。

任何不在这个范围的虚拟地址将会导致硬件异常，但是我们目前还没有设置中断处理机制，这将会导致 QEMU
转储机器的状态并退出，如果你没有使用 [6.828 patched QEMU](https://github.com/mit-pdos/6.828-qemu)
的话，这将会永无止境地重启。

```{admonition} 练习 7
使用 qemu-gdb 追踪 JOS kernel，并在 `mov1 %eax, %cr0` 停止，检查内存 `0x00100000` 和 `0xf0100000`
中的内容。然后，使用 `stepi` 单步调试，重复检查 `0x00100000` 和 `0xf0100000` 中的内容。
确保你能理解发生了什么。

在新映射建立之后，第一条由于映射关系的错误发生失败的指令是什么？
在 `kern/entry.S` 中注释掉 `mov1 %eax, %cr0`，追踪这个错误映射，检验你的观察是否正确。
```

下面我们将介绍如何格式化输出到 Terminal，在 OS kernel 中，我们将会自己实现所有的 I/O，包括
`printf()`。

阅读 `kern/printf.c`，`lib/printfmt.c`，`kern/console.c` 并确保你能理解他们之间的关系。
后面你就会明白为什么会把 `printfmt.c` 单独隔离出来放在 `lib` 目录下。

```{admonition} 练习 8
我们省略了使用格式控制符 `%o` 打印八进制数字的必要代码。找出并补全代码片段。
```

你需要能够回答下面的问题：

1. 观察 `printf.c` 和 `console.c` 之间的接口：`console.c` 输出了什么？为什么这个函数被 `printf.c` 使用了？
2. 根据 `console.c` 解释下面的代码：

    ```{code-block} c
    if (crt_pos >= CRT_SIZE) {
        int i;
        memmove(crt_buf, crt_buf + CRT_COLS, (CRT_SIZE - CRT_COLS) * sizeof(uint16_t));
        for (i = CRT_SIZE - CRT_COLS; i < CRT_SIZE; i++)
            crt_buf[i] = 0x0700 | ' ';
        crt_pos -= CRT_COLS;
    }
    ```

3. 下面的问题你可能需要参考 lecture 2 的笔记，这些笔记涵盖了 x86 平台上的 GCC 调用规则。

    追踪下面语句的执行过程：

    ```{code-block} c
    int x = 1, y = 3, z = 4;
    cprintf("x %d, y %x, z %d\n", x, y, z);
    ```

    - 在调用 `cprintf()` 时，`fmt` 指向了什么？`ap` 指向了什么？
    - 根据执行顺序，列出针对 `cons_putc`，`va_arg`，`vcprintf` 的每一个调用。
    - 对于 `cons_putc` 列出他的参数，对于 `var_arg`，分别列出在调用前后 `ap` 分别指向了什么。
    - 对于 `vcprintf` 列出它的两个参数的值。

4. 运行下面的代码：

    ```{code-block} c
    unsigned int i = 0x00646c72;
    cprintf("H%x Wo%s", 57616, &i);
    ```

    输出是什么？解释为什么会得到这样的输出（你可能需要参考 ASCII 码表）。

    有这样的输出是因为 x86 是小端模式。如果 x86 是大端模式，你应该如何设置 `i`？
    的值来得到同样的输出？你是否应该修改 57616？

5. 在下面的代码中，`y` 的值是多少（结果并不是一个确定的值）？为什么会出现这种现象？

    ```{code-block} c
    cprintf("x=%d y=%d", 3);
    ```

6. 假设 GCC 更改了调用规则，并因此它按照声明的顺序将参数进行压栈，故最后一个声明的参数是最后一个压栈的。
你将如何更改 `cprintf` 或他的接口，来让它能够接收可变数量的参数？

```{admonition} 挑战
加强版的 console 可以在 Terminal 中输出不同颜色的字体。
传统的做法是用 ANSI escape sequence 包裹文本，然后由 Terminal 来解释这段包裹代码。
如果你兴趣，可以参考 [[webpage](https://pdos.csail.mit.edu/6.828/2018/reference.html)]
来根据自己的兴趣做更改，这可能涉及到关于 VGA 显示硬件的编程。
首先你应该把 VGA 硬件调整到 graphics 模式，然后让控制台能够在 graphical frame buffer
中绘制彩色文本。
```

## 栈：追踪 kernel

在本次实验的最后一个练习中，我们将探索 C 语言是如何在 x86 架构上使用栈的。
在这个过程中，我们将会编写一个内核监视器函数，让它打印栈的
backtrace（栈轨迹）：包含指令指针 (IP) 以及对应的值（这些指令指针来自嵌套的 `call` 函数）。

```{admonition} 练习 9
kernel 执行到什么语句开始创建栈空间？并准确定栈空间保存在内存的什么位置。
kernel 是如何为他的栈来预留空间的？栈指针指向的是栈顶还是栈底？
```

x86 栈指针（esp 寄存器）指向栈中正在使用的最低的地址，所有处于该地址以下的区域都是空闲区域。

每次向栈中压入一个值，都会先使栈指针下移一个单位，然后把值写入栈指针指向的位置。

从栈中弹出一个值，包含了读取栈指针指向的值、栈指针增加一个单位两个过程。
许多 x86 指令，比如 `call`，都是借助栈指针寄存器采用直接地址寻址的方式来找到相应的指令或数据。
在 32 位模式下，栈只能存取 32 位的值，并且 esp 寄存器经常被四等分。

根据软件惯例，ebp 寄存器（基指针）主要与栈相关联。
在 C 函数的入口处，函数的 prologue 代码通过将前一个函数的基指针压栈来保存这个基指针。
然后，为了保持函数之间的相互调用关系，把当前 esp 的值拷贝到 ebp。
如果程序中所有的函数都遵守这个约定，那么在程序执行期间的任何时间点，都可以通过对栈回溯找到函数之间的调用关系。
发现调用关系的能力非常重要，比如，如果某个函数由于非法参数导致了 assert 或
panic，但是你又不知道这个非法参数是谁传递过来的，那么栈回溯就可以帮你应对这种场景了。

```{admonition} 练习 10
熟悉 x86 平台上的 C 语言调用规则，找到 `obj/kern/kernel.asm` 中函数 `test_backtrace`
的入口地址，在那里设置一个断点，然后检查在内核启动后，每次调用都会发生什么。
在每个 `test_backtrace` 级别上，有多少个 32 位的字被压栈，这些被压入的字都是什么？

注意，如果你想要成功地完成这个实验，你需要使用 6.828 patched
QEMU，否则，你需要自行地翻译所有断点的内存地址到线性地址。
```

练习 10 包含了关于如何实现栈回溯函数的一些信息，这些信息来源与函数 `mon_backtrace()`。
它的原型函数已经在 `kern/monitor.c` 中实现了。
如果你打算用纯 C 代码编写，你会发现 `inc/x86.h` 中的 `read_ebp()` 函数十分有用。
你可能也需要在 kernel montor 的命令参数列表中对这个新函数创建钩子，然后它就可以跟用户交互了。

我们编写完的回溯函数应该可以展示一系列的函数调用，比如类似下面这样的输出：

```{code-block} text
Stack backtrace:
  ebp f0109e58  eip f0100a62  args 00000001 f0109e80 f0109e98 f0100ed2 00000031
  ebp f0109ed8  eip f01000d6  args 00000000 00000000 f0100058 f0109f28 00000061
  ...
```

每一行都包括 `ebp`，`eip`，`args`。

`ebp` 表示函数正在使用的基指针，基指针保存于函数入口和函数的创建基指针的代码（prologue code）的后面。

`eip` 是函数 return 指令的指针，即函数返回时的那条控制指令的地址。
return 指令指针通常指向在 `call` 指令之后的指令（为什么呢）。

`args` 是函数的参数列表，在本例中它有 5 个可用参数。
这 5 个 16 进制数字是函数的前 5 个参数，在函数调用发生之前就会被压栈了。
当然，函数调用需要用到的参数也可以少于 5
个（为什么回溯代码不能检测真实需要多少个参数？这种缺陷应该如何修复？）。

从栈轨迹上，我们可以得出结论：

- 第一行输出展示了当前正在执行的函数，是 `mon_backtrace` 本身；
- 第二行输出展示了是谁在调用 `mon_backtrace` 函数；
- 第三行展示了调用第二行函数的函数，并依次循环。

学习完这个例子后，你应该学会了打印所有的栈帧。
通过学习 `kern/entry.S` 你可以发现这有一个简单地方式来告诉函数什么时候停止。

阅读 *C 语言程序设计* 时，有一些重要的知识点，需要你记忆，后面的实验可能会用到：

- 若 `int *p = (int *) 100`，则 `(int)p + 1` 和 `(int)(p+1)` 的值分别是 101 和 104。
  当给指针加一个整型数字时，也就是第二种情况所示，这个整型数字被默认乘以了指针指向的对象的大小。
- `p[i]` 和 `*(p+i)` 是等价的，都是 `p` 指向的内存空间中的第 `i` 个对象
- `&p[i]` 和 `(p+i)` 是等价的，都是 `p` 指向的内存空间中的第 `i` 个对象的地址

虽然大多数 C 代码都不需要指针和整型数字之间的相互转换，但是操作系统却经常需要这么干。
无论什么时候见到在内存地址上做加法，你都要问问自己这是一个 **整型加法** 还是 **指针加法**。
检查一下，如果是整型数字加到了指针上，是否乘以了相应的倍数。

```{admonition} 练习 11
实现上述提到的 backtrace 函数，让输出满足上文提到的格式。

注意，如果你在使用 `read_ebp()`，GCC 可能会生成优化过的代码：在 `mon_backtrace()` 函数的
prologue code **之前** 调用了 `read_ebp()`，这将会导致不完整的栈轨迹（关于函数调用的许多栈帧都丢失了）。
如果你尝试关闭优化，这将会导致栈帧的重新排序，你需要亲自尝试调试 `mon_backtrace()`
的汇编代码，并确保 `read_ebp()` 函数调用发生在 prologue code `之后`。
```

到目前为止，你的 backtrace 函数应该可以通过调用 `mon_backtrace()` 给出栈中的函数调用地址了。
然而，在实战中，你经常还想知道对应内存地址上的函数名字，这在定位 bug 时十分有用。
为了帮助你实现这个功能，我们提供了函数 `debuginfo_eip()`，它会在符号表中查找 `eip`
并返回对应内存地址上的调试信息。关于 `debuginfo_eip()` 函数的定义参考 `kern/kdebug.c` 中了。

````{admonition} 练习 12
我们在这个练习中，将实现对栈帧的格式化打印，充分展示函数之间的调用关系。
针对每一个 `eip` 修改它对应的函数名、源文件名、行号、栈回溯函数的显示信息。

`debuginfo_eip` 中的 `__STAB_*` 来自哪里？为了便于理解，我们希望你先完成下面几件事情：

- 在文件 `kern/kernel.ld` 中查找 `__STAB_*`
- 运行命令 `objdump -h obj/kern/kernel`
- 运行命令 `objdump -G obj/kern/kernel`
- 运行命令 `gcc -pipe -nostdinc -O2 -fno-builtin -I. -MD -Wall -Wno-format 
  -DJOS_KERNEL -gstabs -c -S kern/init.c`，然后查看 `init.s` 文件
- 查看 bootloader 是否把符号表作为 kernel 二进制文件的一部分，加载到内存中了。

提示：在实现 `debuginfo_eip` 函数时，可以使用 `stab_binsearch` 函数来根据一个内存地址查找行号。

向 kernel monitor 中添加 `backtrace` 命令，并在你的 `mon_backtrace` 函数中扩展 `debuginfo_eip`
函数，然后按照如下格式打印每个栈帧。

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

关于这种输出格式，我们稍作说明：

- `ebp`：函数的基地址；
- `eip`：函数的第一条指令所在的地址；
- `kern/monitor.c:143: monitor+106`：函数名：函数的第一条指令相对于 `eip`
  的偏移：函数最后一条指令相对于函数的第一条指令的偏移（单位：字节）。

提示：你可以用类似 `printf("%.*s", length, string)` 这样的语句让输出看起来更标准。

你可能会发现在打印输出中，丢失了一些栈轨迹。
比如，你可能看到了关于 `monitor()` 的调用，但是不是 `runcmd()`，这是因为编译优化，内联了一些函数调用。
其他的优化可能也会导致你看到不希望看到的行号。
如果你想让栈轨迹可能看起来才会更加合理，在 GMUMakefile 中使用 `-O2` 参数，但这会导致运行速度的降低。
````

---

[^cite_ref-2]: <https://pdos.csail.mit.edu/6.828/2018/tools.html>
[^cite_ref-3]: <http://web.archive.org/web/20040322145608/http://members.iweb.net.au/~pstorr/pcbook/book2/memory.htm>
[^cite_ref-4]: 李广军，阎波，林水生．微处理器系统结构与嵌入式系统系统设计：电子工业出版社，2011：338-339
[^cite_ref-5]: <http://pacman128.github.io/pcasm/>
