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
sprite $bFunction jar:archimate/process
sprite $aMacro jar:archimate/service
sprite $tGlobal jar:archimate/node

package kernel.ld {
    rectangle OUTPUT_ARCH <<$aMacro>> #Application
    rectangle ENTRY <<$bFunction>> #Business
    rectangle etext <<$tGlobal>> #Technology
}
package entry.S {
    rectangle _entry <<$bFunction>> #Business
    rectangle spin <<$bFunction>> #Business
}
package start.c {
    rectangle start <<$bFunction>> #Business
    rectangle timerinit <<$bFunction>> #Business
}
package main.c {
    rectangle main <<$bFunction>> #Business
}
package spinlock.c {
    rectangle initlock <<$bFunction>> #Business
    rectangle acquire <<$bFunction>> #Business
    rectangle release <<$bFunction>> #Business
    rectangle holding <<$bFunction>> #Business
    rectangle push_off <<$bFunction>> #Business
    rectangle pop_off <<$bFunction>> #Business
}
package printf.c {
    rectangle printfint <<$bFunction>> #Business
    rectangle printptr <<$bFunction>> #Business
    rectangle printf <<$bFunction>> #Business
    rectangle panic <<$bFunction>> #Business
    rectangle printfinit <<$bFunction>> #Business
    frame pr {
        rectangle lock as pr.lock <<$tGlobal>> #Technology
        rectangle locking <<$tGlobal>> #Technology
    }
}
package uart.c {
    rectangle uartinit <<$bFunction>> #Business
    rectangle uartputc <<$bFunction>> #Business
    rectangle uartputc_sync <<$bFunction>> #Business
    rectangle uartstart <<$bFunction>> #Business
    rectangle uartgetc <<$bFunction>> #Business
    rectangle uartintr <<$bFunction>> #Business
    rectangle uart_tx_lock <<$tGlobal>> #Technology
}
package console.c {
    rectangle consputc <<$bFunction>> #Business
    rectangle consolewrite <<$bFunction>> #Business
    rectangle consoleread <<$bFunction>> #Business
    rectangle consoleintr <<$bFunction>> #Business
    rectangle consoleinit <<$bFunction>> #Business
    frame cons {
        rectangle lock as cons.lock <<$tGlobal>> #Technology
        rectangle buf <<$tGlobal>> #Technology
        rectangle r <<$tGlobal>> #Technology
        rectangle w <<$tGlobal>> #Technology
        rectangle e <<$tGlobal>> #Technology
    }
}
package swtch.S {
    rectangle swtch <<$bFunction>> #Business
}
package kernelvec.S {
    rectangle kernelvec <<$bFunction>> #Business
    rectangle timervec <<$bFunction>> #Business
}
package trampoline.S {
    rectangle uservec <<$bFunction>> #Business
    rectangle userret <<$bFunction>> #Business
    rectangle trampoline <<$tGlobal>> #Technology
}
package kalloc.c {
    rectangle kinit <<$bFunction>> #Business
    rectangle freerange <<$bFunction>> #Business
    rectangle kfree <<$bFunction>> #Business
    rectangle kalloc <<$bFunction>> #Business
    frame kmem {
        rectangle lock as kmem.lock <<$tGlobal>> #Technology
        rectangle freelist <<$tGlobal>> #Technology
    }
}
package vm.c {
    rectangle kvminit <<$bFunction>> #Business
    rectangle kvminithart <<$bFunction>> #Business
    rectangle walk <<$bFunction>> #Business
    rectangle walkaddr <<$bFunction>> #Business
    rectangle kvmmap <<$bFunction>> #Business
    rectangle kvmpa <<$bFunction>> #Business
    rectangle mappages <<$bFunction>> #Business
    rectangle kvmcreate <<$bFunction>> #Business
    rectangle uvmunmap <<$bFunction>> #Business
    rectangle uvmcreate <<$bFunction>> #Business
    rectangle uvminit <<$bFunction>> #Business
    rectangle uvmalloc <<$bFunction>> #Business
    rectangle uvmdealloc <<$bFunction>> #Business
    rectangle freewalk <<$bFunction>> #Business
    rectangle uvmfree <<$bFunction>> #Business
    rectangle kvmfree <<$bFunction>> #Business
    rectangle uvmcopy <<$bFunction>> #Business
    rectangle uvmclear <<$bFunction>> #Business
    rectangle copyout <<$bFunction>> #Business
    rectangle copyin <<$bFunction>> #Business
    rectangle copyinstr <<$bFunction>> #Business
    rectangle vmprint2 <<$bFunction>> #Business
    rectangle vmprint <<$bFunction>> #Business
    rectangle kernel_pagetable <<$tGlobal>> #Technology
}
package proc.c {
    rectangle procinit <<$bFunction>> #Business
    rectangle cpuid <<$bFunction>> #Business
    rectangle mycpu <<$bFunction>> #Business
    rectangle myproc <<$bFunction>> #Business
    rectangle allocpid <<$bFunction>> #Business
    rectangle allocproc <<$bFunction>> #Business
    rectangle freeproc <<$bFunction>> #Business
    rectangle proc_pagetable <<$bFunction>> #Business
    rectangle proc_freepagetable <<$bFunction>> #Business
    rectangle userinit <<$bFunction>> #Business
    rectangle growproc <<$bFunction>> #Business
    rectangle fork <<$bFunction>> #Business
    rectangle reparent <<$bFunction>> #Business
    rectangle exit <<$bFunction>> #Business
    rectangle wait <<$bFunction>> #Business
    rectangle scheduler <<$bFunction>> #Business
    rectangle sched <<$bFunction>> #Business
    rectangle yield <<$bFunction>> #Business
    rectangle forkret <<$bFunction>> #Business
    rectangle sleep <<$bFunction>> #Business
    rectangle wakeup <<$bFunction>> #Business
    rectangle kill <<$bFunction>> #Business
    rectangle either_copyout <<$bFunction>> #Business
    rectangle either_copyin <<$bFunction>> #Business
    rectangle procdump <<$bFunction>> #Business
    rectangle cpus <<$tGlobal>> #Technology
    rectangle proc <<$tGlobal>> #Technology
    rectangle initpid <<$tGlobal>> #Technology
    rectangle nextpid <<$tGlobal>> #Technology
    rectangle pid_lock <<$tGlobal>> #Technology
}
package trap.c {
    rectangle trapinit <<$bFunction>> #Business
    rectangle trapinithart <<$bFunction>> #Business
    rectangle usertrap <<$bFunction>> #Business
    rectangle usertrapret <<$bFunction>> #Business
    rectangle kerneltrap <<$bFunction>> #Business
    rectangle clockintr <<$bFunction>> #Business
    rectangle deintr <<$bFunction>> #Business
    rectangle tickslock <<$tGlobal>> #Technology
}
package plic.c {
    rectangle plicinit <<$bFunction>> #Business
    rectangle plicinithart <<$bFunction>> #Business
    rectangle plic_claim <<$bFunction>> #Business
    rectangle plic_complete <<$bFunction>> #Business
}
package bio.c {
    rectangle binit <<$bFunction>> #Business
    rectangle bget <<$bFunction>> #Business
    rectangle bread <<$bFunction>> #Business
    rectangle bwrite <<$bFunction>> #Business
    rectangle brelse <<$bFunction>> #Business
    rectangle bpin <<$bFunction>> #Business
    rectangle bunpin <<$bFunction>> #Business
    frame bcache {
        rectangle lock as bcache.lock <<$tGlobal>> #Technology
        rectangle buf <<$tGlobal>> #Technology
        rectangle head <<$tGlobal>> #Technology
    }
}
package fs.c {
    rectangle readsb <<$bFunction>> #Business
    rectangle fsinit <<$bFunction>> #Business
    rectangle bzero <<$bFunction>> #Business
    rectangle balloc <<$bFunction>> #Business
    rectangle bfree <<$bFunction>> #Business
    rectangle iinit <<$bFunction>> #Business
    rectangle iget <<$bFunction>> #Business
    rectangle ialloc <<$bFunction>> #Business
    rectangle iupdate <<$bFunction>> #Business
    rectangle idup <<$bFunction>> #Business
    rectangle ilock <<$bFunction>> #Business
    rectangle iunlock <<$bFunction>> #Business
    rectangle iput <<$bFunction>> #Business
    rectangle iunlockput <<$bFunction>> #Business
    rectangle bmap <<$bFunction>> #Business
    rectangle itrunc <<$bFunction>> #Business
    rectangle stati <<$bFunction>> #Business
    rectangle readi <<$bFunction>> #Business
    rectangle writei <<$bFunction>> #Business
    rectangle namecmp <<$bFunction>> #Business
    rectangle dirlookup <<$bFunction>> #Business
    rectangle dirlink <<$bFunction>> #Business
    rectangle skipelem <<$bFunction>> #Business
    rectangle namex <<$bFunction>> #Business
    rectangle namei <<$bFunction>> #Business
    rectangle nameiparent <<$bFunction>> #Business
    frame icache {
        rectangle lock as icache.lock <<$tGlobal>> #Technology
        rectangle inode <<$tGlobal>> #Technology
    }
}
package file.c {
    rectangle fileinit <<$bFunction>> #Business
    rectangle filealloc <<$bFunction>> #Business
    rectangle filedup <<$bFunction>> #Business
    rectangle fileclose <<$bFunction>> #Business
    rectangle filestat <<$bFunction>> #Business
    rectangle fileread <<$bFunction>> #Business
    rectangle filewrite <<$bFunction>> #Business
    frame ftable {
        rectangle lock as ftable.lock <<$tGlobal>> #Technology
        rectangle f <<$tGlobal>> #Technology
    }
}
package virtio_disk.c {
    rectangle virtio_disk_init <<$bFunction>> #Business
    rectangle alloc_desc <<$bFunction>> #Business
    rectangle free_desc <<$bFunction>> #Business
    rectangle free_chain <<$bFunction>> #Business
    rectangle alloc3_desc <<$bFunction>> #Business
    rectangle virtio_disk_rw <<$bFunction>> #Business
    rectangle virtio_disk_intr <<$bFunction>> #Business
    frame disk {
        rectangle vdisk_lock <<$tGlobal>> #Technology
        rectangle pages <<$tGlobal>> #Technology
        rectangle desc <<$tGlobal>> #Technology
        rectangle avail <<$tGlobal>> #Technology
        rectangle used <<$tGlobal>> #Technology
        rectangle free <<$tGlobal>> #Technology
        rectangle used_idx <<$tGlobal>> #Technology
        rectangle info <<$tGlobal>> #Technology
    }
}
package riscv.h {
    rectangle w_satp <<$bFunction>> #Business
    rectangle sfence_vma <<$bFunction>> #Business
}
package memlayout.h {
    rectangle TRAPFRAME <<$aMacro>> #Application
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
