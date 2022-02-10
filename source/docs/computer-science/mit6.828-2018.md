(microkernel_os)=
# 微内核操作系统

## 学习路线

学习路线方案的制定参考了 MIT6.828 schedule [^cite_ref-1]，课程讲义为《[xv6 book](https://kdocs.cn/l/caQbBFQ1ener)》和《[xv6 source](https://kdocs.cn/l/cbGOwLHZ1EK4)》。

```{panels}
:container: timeline
:column: col-6 p-0
:card:

---
:column: +entry left

第 1 讲：操作系统简介
^^^

- 了解 Unix [[video](https://www.youtube.com/watch?v=tc4ROCJYbm0)]
- [实验 1](https://pdos.csail.mit.edu/6.828/2018/labs/lab1/)：C、汇编、工具、启动

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

## 环境安装

编译仿真器 QEMU 的时间较长。而且跟着步骤走，可能编译源代码的时候会出现点问题。

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

## 参考文献

[^cite_ref-1]: <https://pdos.csail.mit.edu/6.828/2018/schedule.html>