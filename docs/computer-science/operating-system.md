# 操作系统基础

学习路线方案的制定参考了
[MIT 6.S081 schedule](https://pdos.csail.mit.edu/6.S081/2020/schedule.html)，课程讲义为
[xv6 book 2021](https://kdocs.cn/l/cr5Ryc7FZbRm)。

```{panels}
:container: timeline
:column: col-6 p-0
:card:

---
:column: +entry left

第 1 讲：O/S 概述
^^^

- 预习 [第 1 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/lec-6.s081-2020/tree/master/l-overview)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-overview.txt) /
  [YouTube](https://youtu.be/L6YqHxYHa7A)
- [实验：使用 Xv6 和 Unix 工具](https://pdos.csail.mit.edu/6.S081/2020/labs/util.html)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 2 讲：系统调用
^^^

- 学习 [C](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-c-slides.pdf) 和
  [GDB](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-overview.txt) /
  [C 指针](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/pointers.c)
- [C 语言程序设计](https://kdocs.cn/l/coVOZtu777O9) 2.9、第 5 章和 6.4
- [实验：系统调用](https://pdos.csail.mit.edu/6.S081/2020/labs/syscall.html)

---
:column: +entry left

第 3 讲：O/S 组织方式
^^^

- 预习 [第 2 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/proc.h)
  [2](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/defs.h)
  [3](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/entry.S)
  [4](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/main.c)
  [5](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/user/initcode.S)
  [6](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/user/init.c)
  [7](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/proc.c)
  [8](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/exec.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-os.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-os-boards.pdf) /
  [YouTube](https://youtu.be/o44d---Dk4o)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 4 讲：页表
^^^

- 预习 [第 3 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/memlayout.h)
  [2](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/vm.c)
  [3](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/kalloc.c)
  [4](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/riscv.h)
  [5](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/exec.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-vm.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-vm-boards.pdf) /
  [YouTube](https://youtu.be/f1Hpjty3TT8)
- [实验：页表](https://pdos.csail.mit.edu/6.S081/2020/labs/pgtbl.html)

---
:column: +entry left

第 5 讲：RISC-V 的调用规则和栈帧
^^^

- 预习 [调用规则](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/riscv-calling.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-riscv.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-riscv-slides.pdf) /
  [YouTube](https://youtu.be/s-Z5t_yTyTM)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 6 讲：隔离性、系统调用的入口点和出口点
^^^

- 预习 [第 4 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/riscv.h)
  [2](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/trampoline.S)
  [3](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/trap.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-internal.txt) /
  [YouTube](https://youtu.be/T26UuauaxWA)
- [实验：陷入](https://pdos.csail.mit.edu/6.S081/2020/labs/traps.html)

---
:column: +entry left

第 7 讲：答疑
^^^

- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-QA1.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-QA1.pdf) /
  [YouTube](https://youtu.be/_WWjNIJAfVg)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 8 讲：页错误
^^^

- 预习 [第 4 章](https://kdocs.cn/l/cr5Ryc7FZbRm)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-pgfaults.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-pgfaults.pdf) /
  [YouTube](https://youtu.be/KSYO-gTZo0A) /
  [bilibili](https://www.bilibili.com/video/BV19k4y1C7kA?p=7)
- [实验：懒加载](https://pdos.csail.mit.edu/6.S081/2020/labs/lazy.html)

---
:column: +entry left

第 9 讲：中断
^^^

- 预习 [第 5 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/kernelvec.S)
  [2](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/plic.c)
  [3](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/console.c)
  [4](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/uart.c)
  [5](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/printf.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-interrupt.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-interrupt.pdf) /
  [YouTube](https://youtu.be/zRnGNndcVEA)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 10 讲：多处理器和锁
^^^

- 预习 [第 6 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/spinlock.h)
  [2](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/spinlock.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-lockv2.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-lock.pdf) /
  [YouTube](https://youtu.be/NGXu3vN7yAk)
- [实验：fork 写入时复制](https://pdos.csail.mit.edu/6.S081/2020/labs/cow.html)

---
:column: +entry left

第 11 讲：进程切换
^^^

- 预习 [第 7 章](https://kdocs.cn/l/cr5Ryc7FZbRm)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-threads.txt) /
  [YouTube](https://youtu.be/vsgrTHY5tkg)
- [实验：多进程](https://pdos.csail.mit.edu/6.S081/2020/labs/thread.html)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 12 讲：答疑
^^^

- [YouTube](https://youtu.be/S8ZTJKzhQao)

---
:column: +entry left

第 13 讲：睡眠和唤醒
^^^

- 预习 [第 7 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-coordination.c)
  [2](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/proc.c)
  [3](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/sleeplock.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-coordination.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-vm-boards.pdf) /
  [YouTube](https://youtu.be/gP67sJ4PTnc)
- [实验：并行和锁](https://pdos.csail.mit.edu/6.S081/2020/labs/lock.html)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 14 讲：文件系统
^^^

- 预习 [第 8 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/bio.c)
  [2](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/fs.c)
  [3](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/sysfile.c)
  [4](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/file.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-fs.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-fs.pdf) /
  [YouTube](https://youtu.be/ADzLv1nRtR8)
- [实验：页表](https://pdos.csail.mit.edu/6.S081/2020/labs/pgtbl.html)

---
:column: +entry left

第 15 讲：故障恢复
^^^

- 预习 [第 8 章](https://kdocs.cn/l/cr5Ryc7FZbRm) /
  [1](https://gitee.com/zhyantao/xv6-riscv/blob/riscv/kernel/log.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-crash.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-crash.pdf) /
  [YouTube](https://youtu.be/7Hk2dIorDkk)
- [实验：文件系统](https://pdos.csail.mit.edu/6.S081/2020/labs/fs.html)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 16 讲：文件系统性能和快速恢复
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/journal-design.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-journal.txt) /
  [YouTube](https://youtu.be/CmDcf6rjFb4)

---
:column: +entry left

第 17 讲：虚拟内存
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/appel-li.pdf) /
  [1](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/sqrt.c)
  [2](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/baker.c)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-uservm.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-uservm.pdf) /
  [YouTube](https://youtu.be/YNQghIvk0jc)
- [实验：mmap](https://pdos.csail.mit.edu/6.S081/2020/labs/mmap.html)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 18 讲：O/S 组织方式
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/microkernel.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-organization.txt) /
  [YouTube](https://youtu.be/dM9PLdaTpnA)

---
:column: +entry left

第 19 讲：虚拟机
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/belay-dune.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-vmm.txt) /
  [YouTube](https://youtu.be/R8obXHAIPY0) /
  [bilibili](https://www.bilibili.com/video/BV19k4y1C7kA?p=18)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 20 讲：内核和 HLL
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/biscuit.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-biscuit.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-biscuit-slides.pdf) /
  [YouTube](https://youtu.be/AAtXWGwxI9k) /
  [bilibili](https://www.bilibili.com/video/BV19k4y1C7kA?p=19)
- [实验：网络栈](https://pdos.csail.mit.edu/6.S081/2020/labs/net.html)

---
:column: +entry left

第 21 讲：网络
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/mogul96usenix.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-net.txt) /
  [YouTube](https://youtu.be/Fcjychg4Tvk) /
  [bilibili](https://www.bilibili.com/video/BV19k4y1C7kA?p=20)

---
:column: +right
---
:column: +left
---
:column: +entry right

第 22 讲：安全
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/meltdown.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-meltdown.txt) /
  [YouTube](https://youtu.be/WpKVr3p5rjE)

---
:column: +entry left

第 23 讲：写入时更新
^^^

- 预习 [论文](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/reading/rcu-decade-later.pdf)
- [课程大纲](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-rcu.txt) /
  [PPT](https://gitee.com/zhyantao/lec-6.s081-2020/raw/master/l-rcu.pdf) /
  [YouTube](https://youtu.be/KUwyCGMTeq8)

```

实验参考答案：<https://github.com/wangdh15/xv6>

```{toctree}
:titlesonly:
:glob:
:hidden:

operating-system/*
```
