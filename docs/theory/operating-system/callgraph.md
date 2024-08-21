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
sprite $function jar:archimate/business-process
sprite $macro jar:archimate/application-service
sprite $global jar:archimate/technology-node

package kernel.ld {
    rectangle OUTPUT_ARCH <<$macro>>
    rectangle ENTRY <<$function>>
    rectangle etext <<$global>>
}
package entry.S {
    rectangle _entry <<$function>>
    rectangle spin <<$function>>
}
package start.c {
    rectangle start <<$function>>
    rectangle timerinit <<$function>>
}
package main.c {
    rectangle main <<$function>>
}
package spinlock.c {
    rectangle initlock <<$function>>
    rectangle acquire <<$function>>
    rectangle release <<$function>>
    rectangle holding <<$function>>
    rectangle push_off <<$function>>
    rectangle pop_off <<$function>>
}
package printf.c {
    rectangle printfint <<$function>>
    rectangle printptr <<$function>>
    rectangle printf <<$function>>
    rectangle panic <<$function>>
    rectangle printfinit <<$function>>
}
package uart.c {
    rectangle uartinit <<$function>>
    rectangle uartputc <<$function>>
    rectangle uartputc_sync <<$function>>
    rectangle uartstart <<$function>>
    rectangle uartgetc <<$function>>
    rectangle uartintr <<$function>>
}
package console.c {
    rectangle consputc <<$function>>
    rectangle consolewrite <<$function>>
    rectangle consoleread <<$function>>
    rectangle consoleintr <<$function>>
    rectangle consoleinit <<$function>>
}
package swtch.S {
    rectangle swtch <<$function>>
}
package kernelvec.S {
    rectangle kernelvec <<$function>>
    rectangle timervec <<$function>>
}
package trampoline.S {
    rectangle uservec <<$function>>
    rectangle userret <<$function>>
    rectangle trampoline <<$global>>
}
package kalloc.c {
    rectangle kinit <<$function>>
    rectangle freerange <<$function>>
    rectangle kfree <<$function>>
    rectangle kalloc <<$function>>
}
package vm.c {
    rectangle kvminit <<$function>>
    rectangle kvminithart <<$function>>
    rectangle walk <<$function>>
    rectangle walkaddr <<$function>>
    rectangle kvmmap <<$function>>
    rectangle kvmpa <<$function>>
    rectangle mappages <<$function>>
    rectangle kvmcreate <<$function>>
    rectangle uvmunmap <<$function>>
    rectangle uvmcreate <<$function>>
    rectangle uvminit <<$function>>
    rectangle uvmalloc <<$function>>
    rectangle uvmdealloc <<$function>>
    rectangle freewalk <<$function>>
    rectangle uvmfree <<$function>>
    rectangle kvmfree <<$function>>
    rectangle uvmcopy <<$function>>
    rectangle uvmclear <<$function>>
    rectangle copyout <<$function>>
    rectangle coupyin <<$function>>
    rectangle copyinstr <<$function>>
    rectangle vmprint2 <<$function>>
    rectangle vmprint <<$function>>
    rectangle kernel_pagetable <<$global>>
}
package proc.c {
    rectangle procinit <<$function>>
    rectangle cpuid <<$function>>
    rectangle mycpu <<$function>>
    rectangle myproc <<$function>>
    rectangle allocpid <<$function>>
    rectangle allocproc <<$function>>
    rectangle freeproc <<$function>>
    rectangle proc_pagetable <<$function>>
    rectangle proc_freepagetable <<$function>>
    rectangle userinit <<$function>>
    rectangle growproc <<$function>>
    rectangle fork <<$function>>
    rectangle reparent <<$function>>
    rectangle exit <<$function>>
    rectangle wait <<$function>>
    rectangle scheduler <<$function>>
    rectangle sched <<$function>>
    rectangle yield <<$function>>
    rectangle forkret <<$function>>
    rectangle sleep <<$function>>
    rectangle wakeup <<$function>>
    rectangle kill <<$function>>
    rectangle either_copyout <<$function>>
    rectangle either_copyin <<$function>>
    rectangle procdump <<$function>>
    rectangle cpus <<$global>>
    rectangle proc <<$global>>
    rectangle initpid <<$global>>
    rectangle nextpid <<$global>>
    rectangle pid_lock <<$global>>
}
package trap.c {
    rectangle trapinit <<$function>>
    rectangle trapinithart <<$function>>
    rectangle usertrap <<$function>>
    rectangle usertrapret <<$function>>
    rectangle kerneltrap <<$function>>
    rectangle clockintr <<$function>>
    rectangle deintr <<$function>>
}
package plic.c {
    rectangle plicinit <<$function>>
    rectangle plicinithart <<$function>>
    rectangle plic_claim <<$function>>
    rectangle plic_complete <<$function>>
}
package bio.c {
    rectangle binit <<$function>>
    rectangle bget <<$function>>
    rectangle bread <<$function>>
    rectangle bwrite <<$function>>
    rectangle brelse <<$function>>
    rectangle bpin <<$function>>
    rectangle bunpin <<$function>>
    frame bcache {
        rectangle spinlock <<$macro>>
        rectangle buf <<$macro>>
        rectangle head <<$macro>>
    }
}
package fs.c {
    rectangle readsb <<$function>>
    rectangle fsinit <<$function>>
    rectangle bzero <<$function>>
    rectangle balloc <<$function>>
    rectangle bfree <<$function>>
    rectangle iinit <<$function>>
    rectangle iget <<$function>>
    rectangle ialloc <<$function>>
    rectangle iupdate <<$function>>
    rectangle idup <<$function>>
    rectangle ilock <<$function>>
    rectangle iunlock <<$function>>
    rectangle iput <<$function>>
    rectangle iunlockput <<$function>>
    rectangle bmap <<$function>>
    rectangle itrunc <<$function>>
    rectangle stati <<$function>>
    rectangle readi <<$function>>
    rectangle writei <<$function>>
    rectangle namecmp <<$function>>
    rectangle dirlookup <<$function>>
    rectangle dirlink <<$function>>
    rectangle skipelem <<$function>>
    rectangle namex <<$function>>
    rectangle namei <<$function>>
    rectangle nameiparent <<$function>>
}
package file.c {
    rectangle fileinit <<$function>>
    rectangle filealloc <<$function>>
    rectangle filedup <<$function>>
    rectangle fileclose <<$function>>
    rectangle filestat <<$function>>
    rectangle fileread <<$function>>
    rectangle filewrite <<$function>>
}
package virtio_disk.c {
    rectangle virtio_disk_init <<$function>>
    rectangle alloc_desc <<$function>>
    rectangle free_desc <<$function>>
    rectangle free_chain <<$function>>
    rectangle alloc3_desc <<$function>>
    rectangle virtio_disk_rw <<$function>>
    rectangle virtio_disk_intr <<$function>>
}
package riscv.h {
    rectangle w_satp <<$function>>
    rectangle sfence_vma <<$function>>
}
package memlayout.h {
    rectangle TRAPFRAME <<$macro>>
}

OUTPUT_ARCH -> ENTRY
ENTRY -> _entry
_entry -> start
start -> main

/' main.c '/
main -> consoleinit
main -> printfinit
main -> kinit
main -> kvminit
main -> procinit
main -> trapinit
main -> trapinithart
main -> plicinit
main -> plicinithart
main -> binit
main -> iinit
main -> fileinit
main -> virtio_disk_init
main -> userinit
main -> scheduler

/' console.c '/
' consoleinit -> initlock
consoleinit -> uartinit

/' printf.c '/
' printfinit -> initlock

/' kalloc.c '/
' kinit -> initlock
kinit -> freerange

/' vm.c '/
kvminit -> kalloc
kvminit -> kvmmap
kvminithart -> w_satp
kvminithart -> sfence_vma
walk -> kalloc

/' proc.c '/
procinit -> kalloc
procinit -> kvmmap
procinit -> kvminithart

/' trampoline.S '/
TRAPFRAME -- trampoline
trampoline - uservec
uservec -> usertrap

/' trap.c '/
usertrapret -> userret

@enduml
```
