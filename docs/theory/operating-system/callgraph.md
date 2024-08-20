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
