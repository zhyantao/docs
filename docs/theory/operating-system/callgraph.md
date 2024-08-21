# 调用图

```{uml}
@startuml
start
if (cpuid()==0) then (yes)
    :kernel.ld: 加载 entry.S 到 0x80000000，指定程序入口 ENTRY;
    :entry.S: 从 _entry 开始执行，最后跳转到 start();
    :start.S: 通过 asm 指令切换到 C 程序入口 main();
    :consoleinit() 初始化锁和 UART，并将 `consoleread` 和 `consolewrite` 函数与系统调用相关联;
    if (defined LAB_PGTBL or LAB_LOCK?) then (yes)
        :statsinit() 初始化统计信息设备，包括初始化锁和设置读写函数;
    else (no)
    endif
    :printfinit() 初始化打印锁，确保在多核环境下控制台输出的线程安全;
    :kinit() 初始化内存分配器，并调用 `freerange` 函数来将内核结束后的物理地址范围标记为可用;
    :kvminit() 创建一个直接映射的内核页表，并将 UART、VirtIO 磁盘接口、CLINT 和 PLIC 等设备的物理地址映射到虚拟地址空间中;
    :kvminithart() 切换硬件页表寄存器以使用内核页表，并刷新 TLB;
    :procinit() 初始化进程表，为每个进程分配一个内核栈页面;
    :trapinit() 初始化一个用于同步的自旋锁 `tickslock`，并将 `ticks` 变量设置为 0;
    :trapinithart() 设置中断向量表（stvec），使其指向 `kernelvec` 函数;
    :plicinit() 设置了一些中断优先级，以确保 UART0 和 VIRTIO0 设备的中断能够被启用;
    :plicinithart() 为当前处理器核心设置了中断使能位，并设置了该核心在 S 模式下的优先级阈值;
    :binit() 初始化缓冲区缓存，创建一个双向链表，并初始化每个缓冲区的锁;
    :iinit() 初始化 inode 缓存;
    :fileinit() 初始化文件表，包括一个自旋锁来保护对文件表的访问;
    :virtio_disk_init() 初始化虚拟磁盘设备，包括检查设备的魔数、版本号、设备 ID 和供应商 ID，以及设置设备的特性;
    if (defined LAB_NET?) then (yes)
        :pic_init();
        :sockinit();
    else (no)
    endif
    :userinit() 设置第一个用户进程;
else (no)
    :kvminithart() 切换硬件页表寄存器以使用内核页表，并刷新 TLB;
    :trapinithart() 设置中断向量表（stvec），使其指向 `kernelvec` 函数;
    :plicinithart() 为当前处理器核心设置了中断使能位，并设置了该核心在 S 模式下的优先级阈值;
endif
:scheduler() 是一个循环，不断选择一个可运行的进程并切换到它;
stop
@enduml
```

```{uml}
@startuml
sprite $bProcess jar:archimate/business-process
sprite $aService jar:archimate/application-service
sprite $aComponent jar:archimate/application-component

package kernel.ld {
    rectangle OUTPUT_ARCH <<$aService>> #Application
    rectangle ENTRY <<$bProcess>> #Business
}
package entry.S {
    rectangle _entry <<$bProcess>> #Business
    rectangle spin <<$bProcess>> #Business
}
package start.c {
    rectangle start <<$bProcess>> #Business
    rectangle timerinit <<$bProcess>> #Business
}
package main.c {
    rectangle main <<$bProcess>> #Business
}
package spinlock.c {
    rectangle initlock <<$bProcess>> #Business
    rectangle acquire <<$bProcess>> #Business
    rectangle release <<$bProcess>> #Business
    rectangle holding <<$bProcess>> #Business
    rectangle push_off <<$bProcess>> #Business
    rectangle pop_off <<$bProcess>> #Business
}
package printf.c {
    rectangle printfint <<$bProcess>> #Business
    rectangle printptr <<$bProcess>> #Business
    rectangle printf <<$bProcess>> #Business
    rectangle panic <<$bProcess>> #Business
    rectangle printfinit <<$bProcess>> #Business
}
package uart.c {
    rectangle uartinit <<$bProcess>> #Business
    rectangle uartputc <<$bProcess>> #Business
    rectangle uartputc_sync <<$bProcess>> #Business
    rectangle uartstart <<$bProcess>> #Business
    rectangle uartgetc <<$bProcess>> #Business
    rectangle uartintr <<$bProcess>> #Business
}
package console.c {
    rectangle consputc <<$bProcess>> #Business
    rectangle consolewrite <<$bProcess>> #Business
    rectangle consoleread <<$bProcess>> #Business
    rectangle consoleintr <<$bProcess>> #Business
    rectangle consoleinit <<$bProcess>> #Business
}
package swtch.S {
    rectangle swtch <<$bProcess>> #Business
}
package kernelvec.S {
    rectangle kernelvec <<$bProcess>> #Business
    rectangle timervec <<$bProcess>> #Business
}
package trampoline.S {
    rectangle trampoline <<$bProcess>> #Business
    rectangle uservec <<$bProcess>> #Business
    rectangle userret <<$bProcess>> #Business
}
package kalloc.c {
    rectangle kinit <<$bProcess>> #Business
    rectangle freerange <<$bProcess>> #Business
    rectangle kfree <<$bProcess>> #Business
    rectangle kalloc <<$bProcess>> #Business
}
package vm.c {
    rectangle kvminit <<$bProcess>> #Business
    rectangle kvminithart <<$bProcess>> #Business
    rectangle walk <<$bProcess>> #Business
    rectangle walkaddr <<$bProcess>> #Business
    rectangle kvmmap <<$bProcess>> #Business
    rectangle kvmpa <<$bProcess>> #Business
    rectangle mappages <<$bProcess>> #Business
    rectangle kvmcreate <<$bProcess>> #Business
    rectangle uvmunmap <<$bProcess>> #Business
    rectangle uvmcreate <<$bProcess>> #Business
    rectangle uvminit <<$bProcess>> #Business
    rectangle uvmalloc <<$bProcess>> #Business
    rectangle uvmdealloc <<$bProcess>> #Business
    rectangle freewalk <<$bProcess>> #Business
    rectangle uvmfree <<$bProcess>> #Business
    rectangle kvmfree <<$bProcess>> #Business
    rectangle uvmcopy <<$bProcess>> #Business
    rectangle uvmclear <<$bProcess>> #Business
    rectangle copyout <<$bProcess>> #Business
    rectangle coupyin <<$bProcess>> #Business
    rectangle copyinstr <<$bProcess>> #Business
    rectangle vmprint2 <<$bProcess>> #Business
    rectangle vmprint <<$bProcess>> #Business
}
package proc.c {
    rectangle procinit <<$bProcess>> #Business
    rectangle cpuid <<$bProcess>> #Business
    rectangle mycpu <<$bProcess>> #Business
    rectangle myproc <<$bProcess>> #Business
    rectangle allocpid <<$bProcess>> #Business
    rectangle allocproc <<$bProcess>> #Business
    rectangle freeproc <<$bProcess>> #Business
    rectangle proc_pagetable <<$bProcess>> #Business
    rectangle proc_freepagetable <<$bProcess>> #Business
    rectangle userinit <<$bProcess>> #Business
    rectangle growproc <<$bProcess>> #Business
    rectangle fork <<$bProcess>> #Business
    rectangle reparent <<$bProcess>> #Business
    rectangle exit <<$bProcess>> #Business
    rectangle wait <<$bProcess>> #Business
    rectangle scheduler <<$bProcess>> #Business
    rectangle sched <<$bProcess>> #Business
    rectangle yield <<$bProcess>> #Business
    rectangle forkret <<$bProcess>> #Business
    rectangle sleep <<$bProcess>> #Business
    rectangle wakeup <<$bProcess>> #Business
    rectangle kill <<$bProcess>> #Business
    rectangle either_copyout <<$bProcess>> #Business
    rectangle either_copyin <<$bProcess>> #Business
    rectangle procdump <<$bProcess>> #Business
}
package trap.c {
    rectangle trapinit <<$bProcess>> #Business
    rectangle trapinithart <<$bProcess>> #Business
    rectangle usertrap <<$bProcess>> #Business
    rectangle usertrapret <<$bProcess>> #Business
    rectangle kerneltrap <<$bProcess>> #Business
    rectangle clockintr <<$bProcess>> #Business
    rectangle deintr <<$bProcess>> #Business
}
package plic.c {
    rectangle plicinit <<$bProcess>> #Business
    rectangle plicinithart <<$bProcess>> #Business
    rectangle plic_claim <<$bProcess>> #Business
    rectangle plic_complete <<$bProcess>> #Business
}
package bio.c {
    rectangle binit <<$bProcess>> #Business
    rectangle bget <<$bProcess>> #Business
    rectangle bread <<$bProcess>> #Business
    rectangle bwrite <<$bProcess>> #Business
    rectangle brelse <<$bProcess>> #Business
    rectangle bpin <<$bProcess>> #Business
    rectangle bunpin <<$bProcess>> #Business
}
package fs.c {
    rectangle readsb <<$bProcess>> #Business
    rectangle fsinit <<$bProcess>> #Business
    rectangle bzero <<$bProcess>> #Business
    rectangle balloc <<$bProcess>> #Business
    rectangle bfree <<$bProcess>> #Business
    rectangle iinit <<$bProcess>> #Business
    rectangle iget <<$bProcess>> #Business
    rectangle ialloc <<$bProcess>> #Business
    rectangle iupdate <<$bProcess>> #Business
    rectangle idup <<$bProcess>> #Business
    rectangle ilock <<$bProcess>> #Business
    rectangle iunlock <<$bProcess>> #Business
    rectangle iput <<$bProcess>> #Business
    rectangle iunlockput <<$bProcess>> #Business
    rectangle bmap <<$bProcess>> #Business
    rectangle itrunc <<$bProcess>> #Business
    rectangle stati <<$bProcess>> #Business
    rectangle readi <<$bProcess>> #Business
    rectangle writei <<$bProcess>> #Business
    rectangle namecmp <<$bProcess>> #Business
    rectangle dirlookup <<$bProcess>> #Business
    rectangle dirlink <<$bProcess>> #Business
    rectangle skipelem <<$bProcess>> #Business
    rectangle namex <<$bProcess>> #Business
    rectangle namei <<$bProcess>> #Business
    rectangle nameiparent <<$bProcess>> #Business
}
package file.c {
    rectangle fileinit <<$bProcess>> #Business
    rectangle filealloc <<$bProcess>> #Business
    rectangle filedup <<$bProcess>> #Business
    rectangle fileclose <<$bProcess>> #Business
    rectangle filestat <<$bProcess>> #Business
    rectangle fileread <<$bProcess>> #Business
    rectangle filewrite <<$bProcess>> #Business
}
package virtio_disk.c {
    rectangle virtio_disk_init <<$bProcess>> #Business
    rectangle alloc_desc <<$bProcess>> #Business
    rectangle free_desc <<$bProcess>> #Business
    rectangle free_chain <<$bProcess>> #Business
    rectangle alloc3_desc <<$bProcess>> #Business
    rectangle virtio_disk_rw <<$bProcess>> #Business
    rectangle virtio_disk_intr <<$bProcess>> #Business
}
package riscv.h {
    rectangle w_satp <<$bProcess>> #Business
    rectangle sfence_vma <<$bProcess>> #Business
}

OUTPUT_ARCH --> ENTRY
ENTRY --> _entry
_entry --> start
start --> main

/' main.c '/
main --> consoleinit
main --> printfinit
main --> kinit
main --> kvminit
main --> procinit
main --> trapinit
main --> trapinithart
main --> plicinit
main --> plicinithart
main --> binit
main --> iinit
main --> fileinit
main --> virtio_disk_init
main --> userinit
main --> scheduler

/' console.c '/
' consoleinit --> initlock
consoleinit --> uartinit

/' printf.c '/
' printfinit --> initlock

/' kalloc.c '/
' kinit --> initlock
kinit --> freerange

/' vm.c '/
kvminit --> kalloc
kvminit --> kvmmap
kvminithart --> w_satp
kvminithart --> sfence_vma

@enduml
```
