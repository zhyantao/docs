# 操作系统

## 什么是操作系统

操作系统是管理电脑硬件与软件资源的程序。

## 什么是微内核

微内核是提供操作系统核心功能的内核的精简版本。

## 什么是硬实时和软实时

实时操作系统（RTOS），又称即时操作系统。它会按照排序运行、管理系统资源，并为开发应用程序提供一致的基础。实时操作系统与一般的操作系统相比，最大的特色就是 “实时性”，如果有一个任务需要执行，实时操作系统会马上（在较短时间内）执行该任务，不会有较长的延时。这种特性保证了各个任务的及时执行。

硬实时系统有一个刚性的、不可改变的时间限制，它不允许任何超出时限的错误。超时错误会带来损害甚至导致系统失败、或者导致系统不能实现它的预期目标。

软实时系统的时限是一个柔性灵活的，它可以容忍偶然的超时错误。失败造成的后果并不严重，例如在网络中仅仅是轻微地降低了系统的吞吐量。

## 并行和并发有什么区别

并发：把任务在不同的时间点交给处理器进行处理。 在同一时间点，任务并不会同时运行。

并行：把每一个任务分配给每一个处理器独立完成。 在同一时间点，任务一定是同时运行。

## 什么是用户态和内核态

为了避免操作系统和关键数据被用户程序破坏，将处理器的执行状态分为内核态和用户态。内核态是操作系统管理程序执行时所处的状态，能够执行包含特权指令在内的一切指令，能够访问系统内所有的存储空间。

用户态是用户程序执行时处理器所处的状态，不能执行特权指令，只能访问用户地址空间。

用户程序运行在用户态，操作系统内核运行在内核态。

## 用户态和内核态是如何切换的

处理器从用户态切换到内核态的方法有三种：系统调用、异常和外部中断。

1. **系统调用**，是操作系统的最小功能单位，是操作系统提供的用户接口，系统调用本身是一种软中断。

2. **异常**，也叫做内中断，是由错误引起的，如文件损坏、缺页故障等。

3. **外部中断**，是通过两根信号线来通知处理器外设的状态变化，是硬中断。

## 什么是硬中断和软中断

中断是指在 CPU 正常运行程序时，由于内部或外部事件引起 CPU 暂时停止正在运行的程序，转而去执行请求 CPU 服务的内部事件或外部事件的**服务子程序**，待该服务子程序处理完毕后又返回到被中止的程序继续运行。

硬中断是由外部事件引起的中断，比如键盘或鼠标输入，定时器等，具有随机性和突发性。软中断通常由程序调用引起，是通讯进程之间用来模拟硬中断的一种信号通讯方式。

## DMA 和中断的联系

在 CPU 参与的内存访问过程中，如果外部设备需要访问内存，则首先需要向 CPU 发出中断信号，大量的中断负载会让 CPU 有较大的负担，因此为了解放 CPU，提出了 DMA 技术。

DMA 是直接内存访问的缩写，承担了 CPU 的一部分功能，但其运行过程仍需要中断的支持。但是 DMA 会导致缓存一致性问题。

## 什么是中断隐指令

中断隐指令是在机器指令系统中没有的指令。

它是 CPU 在中断周期内由硬件自动完成的一条指令，其功能包括保护程序断点，寻找中断服务程序的入口地址，关中断等功能。

## 简述系统调用的过程

- Trap（中断）
- 传参
- 服务程序
- 返回结果

## call 和 return 具体做了哪些工作

call：参数压栈、返回地址压栈、保护现场。

return：返回地址、恢复现场。

## 什么是进程

进程是一个执行中的程序的实例。

一个进程通常由 PCB、程序段、数据段、堆栈组成。

## 进程和线程的区别

进程：资源分配和调度的基本单位，进程切换耗费资源比线程切换大。进程有独立的进程地址空间。

线程：线程是进程中的一个实体，是 CPU 调度的基本单位，是比进程更小的能独立运行的基本单位。线程自己不拥有系统资源，只拥有运行中必不可少的资源（如程序计数器、寄存器、栈）。

在同一个进程内，可以有多个线程，多个线程共享同一个进程的资源，每个线程具有自己的线程栈。线程没有独立的线程地址空间，多个线程共享同一个进程地址空间。

 进程间不会相互影响。一个进程内某个线程挂掉将导致整个进程挂掉。

## 为什么需要线程

进程可以使多个程序能并发执行，提高了资源的利用率和系统的吞吐量，但是其具有一些缺点：

1. 进程在同一时刻只能做一个任务，很多时候不能充分利用CPU资源。

2. 进程在执行的过程中如果发生阻塞，整个进程就会挂起，即使进程中其它任务不依赖于等待的资源，进程仍会被阻塞。

引入线程就是为了解决以上进程的不足，线程具有以下的优点：

1. 从资源上来讲，开辟一个线程所需要的资源要远小于一个进程。

2. 从切换效率上来讲，运行于一个进程中的多个线程，它们之间使用相同的地址空间，而且线程间彼此切换所需时间也远远小于进程间切换所需要的时间（这种时间的差异主要由于缓存的大量未命中导致）。

3. 从通信机制上来讲，线程间方便的通信机制。对不同进程来说，它们具有独立的地址空间，要进行数据的传递只能通过进程间通信的方式进行。线程则不然，属于同一个进程的不同线程之间共享同一地址空间，所以一个线程的数据可以被其它线程感知，线程间可以直接读写进程数据段（如全局变量）来进行通信（需要一些同步措施）。

## 进程和线程空间是什么

线程运行所需要的内存空间，比如线程程序的存储空间，数据空间，运行空间等。

逻辑地址和物理地址之间的切换，是由 CPU 的内存管理单元 MMU 完成。Linux 内核维护每个进程的逻辑地址到物理地址的对照表。当用户空间进程切换时，内核会更新对照表，用户空间也跟随变。

每个进程的用户空间都是相互独立的，把同一个程序同时运行 10 次，会看到 10 个进程使用的线性地址一模一样但物理内存不一样。

## 进程和程序的区别

进程：程序的一次执行过程，一个动态的过程。存在生命周期，包括创建、运行、挂起、结束。

程序：代码 + 数据的一个集合，一个静态的表示。

## 进程或线程同步的方法

- 互斥锁
- 读写锁
- 条件变量
- 信号量
- 自旋锁
- 屏障

## 进程同步和线程同步的区别

进程之间地址空间不同，不能感知对方的存在，同步时需要将锁放在多进程共享的空间。

而线程之间共享同一地址空间，同步时把锁放在所属的同一进程空间即可。

## 进程和线程的基本操作

进程 API 以 UNIX 系统为例，线程相关的 API 属于 POSIX 线程（pthreads）标准接口。

| 进程原语 | 线程原语            | 描述                       |
| -------- | ------------------- | -------------------------- |
| fork     | pthread_create      | 创建新的控制流             |
| exit     | pthread_exit        | 从现有的控制流中退出       |
| waitpid  | pthread_join        | 从控制流中得到退出状态     |
| atexit   | pthread_cancel_push | 注册控制流退出时调用的函数 |
| getpid   | pthread_self        | 获取控制流的 ID            |
| abort    | pthread_cancel      | 请求控制流的非正常退出     |

## 多线程模型

1. 多对一模型。将多个用户级线程映射到一个内核级线程上。该模型下，线程在用户空间进行管理，效率较高。缺点就是一个线程阻塞，整个进程内的所有线程都会阻塞。*几乎没有系统继续使用这个模型*。

2. 一对一模型。将内核线程与用户线程一一对应。优点是一个线程阻塞时，不会影响到其它线程的执行。该模型具有更好的并发性。缺点是内核线程数量一般有上限，会限制用户线程的数量。更多的内核线程数目也给线程切换带来额外的负担。*Linux 和 Windows 操作系统家族都是使用一对一模型*。

3. 多对多模型。将多个用户级线程映射到多个内核级线程上。结合了多对一模型和一对一模型的特点。

## 守护进程、僵尸进程和孤儿进程

一个父进程退出，而它的一个或多个子进程还在运行，那么那些子进程将成为孤儿进程。孤儿进程将被 init 进程(进程号为 1)所收养，并由 init 进程对它们完成状态收集工作。由于孤儿进程会被 init 进程给收养，所以孤儿进程不会对系统造成危害。

一个进程使用 fork 创建子进程，如果子进程退出，而父进程并没有调用 wait 或 waitpid 获取子进程的状态信息，那么子进程的进程描述符仍然保存在系统中。这种进程称之为僵死进程。

守护进程是运行在后台的一种特殊进程。它独立于控制终端并且周期性地执行某种任务或等待处理某些发生的事件。它不需要用户输入就能运行而且提供某种服务，不是对整个系统就是对某个用户程序提供服务。Linux 系统的大多数服务器就是通过守护进程实现的。常见的守护进程包括系统日志进程 syslogd、 web 服务器 httpd、邮件服务器 sendmail 和数据库服务器 mysqld 等。守护进程一般在系统启动时开始运行，除非强行终止，否则直到系统关机都保持运行。守护进程经常以超级用户（root）权限运行，因为它们要使用特殊的端口（1-1024）或访问某些特殊的资源。*一个守护进程的父进程是 init 进程*，因为它真正的父进程在 fork 出子进程后就先于子进程 exit 退出了，所以它是一个由 init 继承的孤儿进程。守护进程是非交互式程序，没有控制终端，所以任何输出，无论是向标准输出设备 stdout 还是标准出错设备 stderr 的输出都需要特殊处理。守护进程的名称通常以 d 结尾，比如 sshd、xinetd、crond 等。

## 如何避免僵尸进程

如果进程不调用 wait / waitpid 的话， 那么保留的那段信息就不会释放，其进程号就会一直被占用，但是系统所能使用的进程号是有限的，如果大量的产生僵死进程，将因为没有可用的进程号而导致系统不能产生新的进程。此即为僵尸进程的危害，应当避免。

任何一个子进程(init 除外)在 exit() 之后，并非马上就消失掉，而是留下一个称为僵尸进程(Zombie)的数据结构，等待父进程处理。这是每个子进程在结束时都要经过的阶段。如果子进程在 exit() 之后，父进程没有来得及处理，这时用 ps 命令就能看到子进程的状态是 “Z”。如果父进程能及时处理，可能用 ps 命令就来不及看到子进程的僵尸状态，但这并不等于子进程不经过僵尸状态。 如果父进程在子进程结束之前退出，则子进程将由 init 接管。init 将会以父进程的身份对僵尸状态的子进程进行处理。

一个进程如果只复制 fork 子进程而不负责对子进程进行 wait() 或是 waitpid() 调用来释放其所占有资源的话，那么就会产生很多的僵死进程，*如果要消灭系统中大量的僵死进程，只需要将其父进程杀死*，此时所有的僵死进程就会编程孤儿进程，从而被 init 所收养，这样 init 就会释放所有的僵死进程所占有的资源，从而结束僵死进程。

## 常见的页面置换算法有哪些

当访问一个内存中不存在的页，并且内存已满，则需要从内存中调出一个页或将数据送至磁盘对换区，替换一个页，这种现象叫做缺页置换。

先进先出（FIFO）算法：

- 思路：置换最先调入内存的页面，即置换在内存中驻留时间最久的页面。
- 实现：按照进入内存的先后次序排列成队列，从队尾进入，从队首删除。
- 特点：实现简单；性能较差，调出的页面可能是经常访问的。

最近最少使用（LRU）算法:

- 思路：置换最近一段时间以来最长时间未访问过的页面。根据程序局部性原理，刚被访问的页面，可能马上又要被访问；而较长时间内没有被访问的页面，可能最近不会被访问。
- 实现：缺页时，计算内存中每个逻辑页面的上一次访问时间，选择上一次使用到当前时间最长的页面。
- 特点：可能达到最优的效果，维护这样的访问链表开销比较大当前最常采用的就是 LRU 算法。

最不常用（LFU）算法

- 思路：缺页时，置换访问次数最少的页面。
- 实现：每个页面设置一个访问计数，访问页面时，访问计数加 1，缺页时，置换计数最小的页面。
- 特点：算法开销大，开始时频繁使用，但以后不使用的页面很难置换。

## 进程树和线程树

进程树是一个形象化的比喻，比如一个进程启动了一个程序，而启动的这个进程就是原来那个进程的子进程，依此形成的一种树形的结构。我们可以在进程管理器选择结束进程树，就可以结束其子进程和派生的子进程。

## 进程和作业的区别

作业是用户需要计算机完成的某项任务，是要求计算机所做工作的集合。作业是用户向计算机提交任务的**任务实体**。在用户向计算机提交作业后，系统将它放入外存中的作业等待队列中等待执行。

进程则是完成用户任务的**执行实体**，是向系统申请分配资源的基本单位。任一进程，只要它被创建，总有相应的部分存在于内存中。

一个作业可由多个进程组成，且必须至少由一个进程组成，反过来则不成立。作业的概念主要用在批处理系统中，像 UNIX 这样的分时系统中就没有作业的概念。而进程的概念则用在几乎所有的多道程序系统中进程是操作系统进行资源分配的单位。

## 什么是写入时复制

如果多个进程要**读取**它们自己的那部分资源的副本，那么复制是不必要的。每个进程只要保存一个指向这个资源的指针就可以了。只要没有进程要去**修改**自己的 “副本”，就存在着这样的幻觉：每个进程好像独占那个资源。从而就避免了复制带来的负担。

如果一个进程要**修改**自己的那份资源 “副本”，那么就会复制那份资源，并把复制的那份提供给进程。不过其中的复制对进程来说是透明的。这个进程就可以修改复制后的资源了，同时其他的进程仍然共享那份没有修改过的资源。所以这就是名称的由来：在写入时进行复制。

写时复制的主要好处在于：**如果进程从来就不需要修改资源，则不需要进行复制**。惰性算法的好处就在于它们尽量推迟代价高昂的操作，直到必要的时刻才会去执行。

在使用虚拟内存的情况下，写时复制（Copy-On-Write）是以页为基础进行的。所以，只要进程不修改它全部的地址空间，那么就不必复制整个地址空间。在 fork() 调用结束后，父进程和子进程都相信它们有一个自己的地址空间，但实际上它们共享父进程的原始页，接下来这些页又可以被其他的父进程或子进程共享。

## 进程调度算法

先来先服务，短作业优先，优先级，时间片轮转，高响应比，多级反馈队列

## 进程调度的时机

1. 当前运行的进程运行结束。

2. 当前运行的进程由于某种原因阻塞。

3. 执行完系统调用等系统程序后返回用户进程。

4. 在使用抢占调度的系统中，具有更高优先级的进程就绪时。

5. 分时系统中，分给当前进程的时间片用完。

## 不能进行进程调度的情况

1. 在中断处理程序执行时。 
2. 在操作系统的内核程序临界区内。
3. 其它需要完全屏蔽中断的原子操作过程中。

## 简述进程间的通信方法

每个进程各自有不同的用户地址空间，任何一个进程的全局变量在另一个进程中都看不到，所以 *进程之间要交换数据必须通过内核*。在内核中开辟一块缓冲区，进程 A 把数据从用户空间拷到内核缓冲区，进程 B 再从内核缓冲区把数据读走，内核提供的这种机制称为进程间通信。

不同进程间的通信本质：进程之间可以看到一份公共资源；而提供这份资源的形式或者提供者不同，造成了通信方式不同。

进程间通信主要包括管道、系统 IPC（包括消息队列、信号量、信号、共享内存等）、以及套接字 Socket。

## 进程如何通过管道进行通信

管道是一种最基本的 IPC 机制，作用于有血缘关系的进程之间，完成数据传递。调用 pipe 系统函数即可创建一个管道。

有如下特质：

1. 其本质是一个伪文件（实为内核缓冲区）。

2. 由两个文件描述符引用，一个表示读端，一个表示写端。

3. 规定数据从管道的写端流入管道，从读端流出。

管道的原理：管道实为内核使用环形队列机制，借助内核缓冲区实现。

管道的局限性：

1. 数据自己读不能自己写。

2. 数据一旦被读走，便不在管道中存在，不可反复读取。

3. 由于管道采用半双工通信方式。因此，数据只能在一个方向上流动。

4. 只能在有公共祖先的进程间使用管道。

## 进程如何通过共享内存通信

共享内存使得多个进程可以访问同一块内存空间，不同进程可以及时看到对方进程对共享内存中数据的更新。

这种方式需要依靠某种同步操作，如互斥锁和信号量等。特点如下：

1. 共享内存是最快的一种 IPC，因为进程是直接对内存进行操作来实现通信，避免了数据在用户空间和内核空间来回拷贝。

2. 因为多个进程可以同时操作，所以需要进行同步处理。

3. 信号量和共享内存通常结合在一起使用，信号量用来同步对共享内存的访问。

## 如何解决优先级反转

由于多进程共享资源，具有最高优先权的进程被低优先级进程阻塞，反而使具有中优先级的进程先于高优先级的进程执行，导致系统的崩溃。这就是所谓的优先级反转。

其实，优先级反转是在高优先级（假设为 A）的任务要访问一个被低优先级任务（假设为 C）占有的资源时，被阻塞，而此时又有优先

级高于 C，而低于 A 的任务（假设为 B）时，于是，占有资源的任务就被挂起（占有的资源仍为它占有），因为占有资源的任务优先级很低，所以，它可能一直被另外的任务挂起，而它占有的资源也就一直不能释放。这样，引起任务 A 一直没办法执行，而比它优先低的任务 B 却可以执行。

目前解决优先级反转有许多种方法。其中普遍使用的有 2 种方法：

1. 优先级继承：指将低优先级任务的优先级提升到等待它所占有的资源的最高优先级任务的优先级。当高优先级任务由于等待资源而被阻塞时，此时资源的拥有者的优先级将会自动被提升。

2. 优先级天花板：是指将申请某资源的任务的优先级提升到可能访问该资源的所有任务中最高优先级任务的优先级（这个优先级称为该资源的优先级天花板）。

## 死锁的定义

死锁是指两个或两个以上的进程在执行过程中，因争夺资源而造成的一种互相等待的现象。若无外力作用，它们都将无法推进下去。

## 产生死锁的必要条件

- 互斥条件：当前进程所占有的临界资源，其他进程不可访问。
- 请求和保持条件：当前进程占有资源，但又请求其他资源。
- 不可被剥夺条件：当前进程结束前，所占有的资源不可被剥夺。
- 环路等待条件：进程发生死锁后，必然存在一个进程之间相互等待的环形链。

## 破坏死锁的必要条件

- 破坏请求和保持条件：资源一次性分配，只要有一个资源得不到分配，就不给这个进程分配其他的资源。
- 破坏不可被剥夺条件：如果已分配了部分资源，但其他资源未得到满足，释放已占有的资源。
- 破坏环路等待条件：资源有序分配，系统给每类资源赋予一个序号，每个进程按编号递增的请求资源，释放则相反。

## 预防死锁与银行家算法

该算法需要检查申请者对资源的最大需求量，如果系统现存的各类资源可以满足申请者的请求，就满足申请者的请求。

这样申请者就可很快完成其计算，然后释放它占用的资源，从而保证了系统中的所有进程都能完成，所以可**避免死锁**的发生。

## 什么是信号量

信号量是一种实现进程同步和互斥的工具。

整型信号量：所谓整型信号量就是一个用于表示资源个数的整型量。

记录型信号量：就是用一个结构体实现，里面包含了表示资源个数的整型量和一个等待队列。

## 什么是 PV 操作

PV 操作是指申请和释放信号量的操作，P 操作相当于申请资源，V 操作相当于释放资源。PV 操作是一种实现进程互斥与同步的有效方法。PV 操作以原语形式实现，信号量的值仅能由这两条原语加以改变。

## 什么是原子操作

所谓原子操作是指不会被线程调度机制打断的操作。

这种操作一旦开始，就一直运行倒结束，中间不会有任何上下文切换（切换到另一个线程）。

## 原子操作的是如何实现的

处理器使用基于 *对缓存加锁* 或 *总线加锁* 的方式来实现多处理器之间的原子操作。

首先处理器会自动保证基本的内存操作的原子性。处理器保证从系统内存中读取或者写入一个字节是原子的，意思是当一个处理器读取一个字节时，其他处理器不能访问这个字节的内存地址。

Pentium 6 和最新的处理器能自动保证单处理器对同一个缓存行里进行 16/32/64 位的操作是原子的，但是复杂的内存操作处理器是不能自动保证其原子性的，比如跨总线宽度、跨多个缓存行和跨页表的访问。

但是，处理器提供总线锁定和缓存锁定两个机制来保证复杂内存操作的原子性。

- 使用总线锁保证原子性：如果多个处理器同时对共享变量进行读改写操作（`i++` 就是经典的读改写操作），那么共享变量就会被多个处理器同时进行操作，这样读改写操作就不是原子的，操作完之后共享变量的值会和期望的不一致。举个例子，如果 `i=1`，我们进行两次 `i++` 操作，我们期望的结果是 3，但是有可能结果是 2，如图下图所示：

  ```
  CPU1    CPU2
  i=1     i=1
  i+1     i+1
  i=2     i=2
  ```

  原因可能是多个处理器同时从各自的缓存中读取变量 `i`，分别进行加 1 操作，然后分别写入系统内存中。

  那么，想要保证读改写共享变量的操作是原子的，就必须保证 CPU1 读改写共享变量的时候，CPU2 不能操作缓存了该共享变量内存地址的缓存。处理器使用总线锁就是来解决这个问题的。所谓总线锁就是使用处理器提供的一个 `LOCK＃` 信号，当一个处理器在总线上输出此信号时，其他处理器的请求将被阻塞住，那么该处理器可以独占共享内存。

- 使用缓存锁保证原子性：在同一时刻，我们只需保证对某个内存地址的操作是原子性即可，但总线锁定把 CPU 和内存之间的通信锁住了，这使得锁定期间，其他处理器不能操作其他内存地址的数据，所以总线锁定的开销比较大，目前处理器在某些场合下使用缓存锁定代替总线锁定来进行优化。

  频繁使用的内存会缓存在处理器的 L1、L2 和 L3 高速缓存里，那么原子操作就可以直接在处理器内部缓存中进行，并不需要声明总线锁，在 Pentium 6 和目前的处理器中可以使用 “缓存锁定” 的方式来实现复杂的原子性。

  所谓 “缓存锁定” 是指内存区域如果被缓存在处理器的缓存行中，并且在 `Lock` 操作期间被锁定，那么当它执行锁操作回写到内存时，处理器不在总线上声明 `LOCK＃` 信号，而是修改内部的内存地址，并允许它的缓存一致性机制来保证操作的原子性，因为缓存一致性机制会阻止同时修改由两个以上处理器缓存的内存区域数据，当其他处理器回写已被锁定的缓存行的数据时，会使缓存行无效，在如上图所示的例子中，当 CPU1 修改缓存行中的 `i` 时使用了缓存锁定，那么 CPU2 就不能使用同时缓存 `i` 的缓存行。

  但是有两种情况下处理器不会使用缓存锁定。 1）当操作的数据不能被缓存在处理器内部，或操作的数据跨多个缓存行时，则处理器会调用总线锁定。2）有些处理器不支持缓存锁定。对于 Intel 486 和 Pentium 处理器，就算锁定的内存区域在处理器的缓存行中也会调用总线锁定。

## 存储器管理应具有的功能

- 内存的分配和回收
- 地址变换：从逻辑地址转换为物理地址
- 扩充内存容量：从逻辑上扩充内存容量
- 存储保护：进入内存的各道作业在自己的存储空间运行，互不干扰


## 什么是 TLB

Cache 是一种高速缓存存储器，TLB 缓存虚拟地址和其映射的物理地址。

## 程序的链接方式有哪些

1、静态链接：
2、装入时动态链接：边装入边链接
3、运行时动态链接：方便对目标模块的共享

## 程序的装入方式有哪些

1、绝对装入：
2、可重定位装入：也叫静态重定位，地址变换通常是装入时一次性完成的。
3、动态运行装入：程序运行时可在内存中移动位置，只有到程序需要真正执行时才把相对地址转换为绝对地址。

## 什么是页表、页表的作用

页表是为了便于在内存中找到进程的每个页面所对应的物理块，系统为每个进程建立一张页面映射表。

作用：形成映射。

## 分页与分段的区别

段是信息的逻辑单位，它是根据用户的需要划分的，因此段对用户是可见的 ；页是信息的物理单位，是为了管理主存的方便而划分的，对用户是透明的；  

段的大小不固定，有它所完成的功能决定；页大大小固定，由系统决定；  

段向用户提供二维地址空间；页向用户提供的是一维地址空间； 

段是信息的逻辑单位，便于存储保护和信息的共享，页的保护和共享受到限制。

## 什么是内部碎片、外部碎片

内部碎片：分配给作业的存储空间中未被利用的部分。

外部碎片：系统中无法利用的小存储块，比如通过动态内存分配技术从空闲内存区上分配内存后剩下的那部分内存块。

## 交换技术、覆盖技术

覆盖技术：把一个大的程序划分为一系列的覆盖，每个覆盖就是一个相对独立的程序单元，把程序执行时并不要求同时装入内存的覆盖组成一组，称为覆盖段。将一个覆盖段分配到同一个存储区域，这个存储区域就称为覆盖区。

主要区别：

- 交换主要是在进程和作业之间进行。

- 覆盖主要在同一个进程或作业中进行。

- 打破了一个程序一旦进入主存便一直运行到结束的限制。

- 打破了必须将一个进程的全部信息装入主存后才能运行的限制。


## 虚拟存储有什么作用

实现多道程序的并行运行，大的程序在小的内存环境中运行（页面调度）。

## 虚拟地址、物理地址

**虚拟地址** 指由程序产生的由 *段选择符* 和 *段内偏移地址* 组成的地址。

**逻辑地址** 指由程序产生的 *段内偏移*。有时候直接把逻辑地址当做虚拟地址。

**线性地址** 指虚拟地址到物理地址变换的中间层，是 *处理器可寻址的内存空间中的地址*。

**物理地址** 指 CPU 外部地址总线上寻址物理内存的地址信号，是地址变换的最终结果。

程序代码会产生逻辑地址，也就是段内偏移地址，加上相应的段基址就成了线性地址。

如果开启了分页机制，那么线性地址需要再经过变换，变成物理地址。 如果无分页机制，那么线性地址就是物理地址。

因此，整个变换过程为：`虚拟地址 ~ 逻辑地址 > 线性地址 ~ 物理地址`。

## 什么是虚拟内存

为了更加有效地管理内存并且少出错，现代系统提供了一种*对主存的抽象概念*，叫做 虚拟内存（VM）。

虚拟内存是硬件异常、硬件地址翻译、主存、磁盘文件和内核软件的完美交互，它为每个进程提供了一个大的、一致的和私有的地址空间。通过一个很清晰的机制，虚拟内存提供了三个重要的能力：

1. 它将主存看成是一个存储在磁盘上的地址空间的高速缓存，在主存中只保存活动区域，并根据需要在磁盘和主存之间来回传送数据，通过这种方式，它高效地使用了主存。

2. 它为每个进程提供了一致的地址空间，从而简化了内存管理。

3. 它保护了每个进程的地址空间不被其他进程破坏。

## 为什么要引入虚拟内存

**虚拟内存作为缓存的工具**

虚拟内存被组织为一个由 *存放在磁盘上* 的 N 个连续的字节大小的单元组成的数组。虚拟内存利用 DRAM 缓存来自通常更大的虚拟地址空间的页面。

**虚拟内存作为内存管理的工具**

操作系统为 *每个进程提供了一个独立的页表*，也就是 *独立的虚拟地址空间*。多个虚拟页面可以映射到同一个物理页面上。

- 简化链接：独立的地址空间允许每个进程的内存映像使用相同的基本格式，而不管代码和数据实际存放在物理内存的何处。例如：一个给定的 Linux 系统上的每个进程都是用类似的内存格式，对于 64 位地址空间，代码段总是从虚拟地址 `0x400000` 开始。
- 简化加载：虚拟内存还使得容易向内存中加载可执行文件和共享对象文件。要把目标文件中 `.text` 和 `.data` 节加载到一个新创建的进程中，Linux 加载器为代码段和数据段分配虚拟页（VP），把他们标记为无效（未被缓存），将页表条目指向目标文件的起始位置。加载器从不在磁盘到内存实际复制任何数据，在每个页初次被引用时，虚拟内存系统会按照需要自动的调入数据页。
- 简化共享：独立地址空间为 OS 提供了一个管理用户进程和操作系统自身之间共享的一致机制。一般，每个进程有各自私有的代码，数据，堆栈，是不和其他进程共享的，在这种情况下 OS 创建页表，会把不同进程的虚拟页映射到不同的物理页面。某些情况下，需要进程来共享代码和数据。例如每个进程调用相同的操作系统内核代码，或者 C 标准库函数，OS 会把不同进程中适当的虚拟页面映射到相同的物理页面。
- 简化内存分配：虚拟内存向用户提供一个简单的分配额外内存的机制。当一个运行在用户进程中的程序要求额外的堆空间时（如 malloc），OS 分配一个适当 k 大小个连续的虚拟内存页面，并且将他们映射到物理内存中任意位置的 k 个任意物理页面，因此操作系统没有必要分配 k 个连续的物理内存页面，页面可以随机的分散在物理内存中。

**虚拟内存作为内存保护的工具**

不应该允许一个用户进程修改它的只读段，也不允许它修改任何内核代码和数据结构，不允许读写其他进程的私有内存，不允许修改任何与其他进程共享的虚拟页面。每次 CPU 生成一个地址时， MMU 会读一个 PTE，通过在 PTE 上添加一些额外的许可位来控制对一个虚拟页面内容的访问十分简单。

## 内存连续分配管理方式有哪几种

1. 单一连续：适合单道程序。

2. 固定分区分配：适合多道程序，简单。

3. 动态分区分配：根据内存实际需要，动态地为进程分配空间。

## 连续分区分配、非连续分区分配

连续分区分配：只能一次性装载。

非连续内存分配方式：允许将程序分散装载到很多个不相邻的小分区中（基本分页存储管理方式、请求分页存储管理方式）。

## 动态分区分配算法有哪些

最佳适应、首次适应、最坏适应、临近适应。

## 拼接技术、紧凑技术

移动存储中所有已分配区到内存的一端，将其余空闲分区合并为一个大的空闲分区。

## 常用存储保护方法有哪些

- 界限寄存器：1）上下界寄存器方法，2）基址、限长寄存器方法。

- 存储保护键：给每个存储块分配一个单独的存储键，它相当于一把锁。

## 什么是信号

一个信号就是一条小消息，它通知进程系统中发生了一个某种类型的事件。

Linux 系统上支持的 30 种不同类型的信号。每种信号类型都对应于某种系统事件。低层的硬件异常是由内核异常处理程序处理的，正常情况下，对用户进程而言是不可见的。

信号提供了一种机制，通知用户进程发生了这些异常。

1. 发送信号：内核通过更新目的进程上下文中的某个状态，发送（递送）一个信号给目的进程。发送信号可以有如下两种原因：
   - 内核检测到一个系统事件，比如除零错误或者子进程终止。
   - —个进程调用了 kill 函数， 显式地要求内核发送一个信号给目的进程。一个进程可以发送信号给它自己。

2. 接收信号：当目的进程被内核强迫以某种方式对信号的发送做出反应时，它就接收了信号。进程可以忽略这个信号，终止或者通过执行一个称为 *信号处理程序* 的用户层函数捕获这个信号。

## Cache 与寄存器的区别

寄存器是中央处理器内的组成部份。寄存器是有限存贮容量的高速存贮部件，它们可用来暂存指令、数据和地址。

Cache 是高速缓冲存储器，一种特殊的存储器子系统，其中复制了频繁使用的数据以利于快速访问。高速缓冲存储器存储了频繁访问的 RAM 位置的内容及这些数据项的存储地址。

## 实现内存管理需要完成哪些功能

管理需求：重定位，保护，共享，逻辑组织，物理组织。

分区方法：固定分区，动态分区（最佳适配，首次适配，临近适配）。

分页（具体略） 分段（具体略）。

## 文件重命名和删除后再新建有什么区别

物理地址：前者不变，后者变化。

PCB：前者只改了文件名，后者重新建立 PCB。

## Windows 两种文件系统的区别

FAT 是传统的文件系统，而 NTFS 是 Windows 2000 的设计者所开发的， 用于满足工作站和服务器中的高级要求。

相对于 FAT，NTFS 有以下显著特征：

- 可恢复性：之所以要建立新的 Windows 2000 文件系统，就是为了具备从系统崩溃和磁盘故障中恢复的能力。

- 安全性：NTFS 使用 Windows 2000 对象模型来实施安全机制。

- 大磁盘和大文件：NTFS 比包括 FAT 在内的其它大多数文件系统都能够更有效地支持非常大的磁盘和非常大的文件。

- 多数据流：文件的实际内容被当作字节流处理，在 NTFS 中可以为一个文件定义多个数据流。

- 通用索引功能：NTFS 中每个文件都有一组属性与之关联。这样，文件管理系统中文件描述的集合组织成一个关系数据库，因而文件可以建立关于任何属性的索引。


## CISC 和 RISC 的区别

RSIC 固定的指令长度，CISC 指令集的长度一般可变。

RSIC 的一条指令（汇编后的机器代码）长度是固定的，而 CISC 的一条指令（汇编后的机器代码）长度是不固定的。

RSIC 结构的处理器的数据指令只访问寄存器，而 CISC 结构的处理器的数据处理指令操作数的来源范围没这么苛刻。

## 什么是通道

通道是一个独立于 CPU 的专门控制 I/O 的处理机，控制设备与内存直接进行数据交换。

它有自己的通道命令，可由 CPU 执行相应指令来启动通道，并在操作结束时向 CPU 发出中断信号。

通道指令的格式一般由：操作码，记数段，内存地址段，结束标志组成。

## 同步、异步、阻塞、非阻塞

- 同步：当一个同步调用发出后，调用者要一直等待返回结果。通知后，才能进行后续的执行。 
- 异步：当一个异步过程调用发出后，调用者不能立刻得到返回结果。实际处理这个调用的部件在完成后，通过状态、通知和回调来通知调用者。
- 阻塞：是指调用结果返回前，当前线程会被挂起，即阻塞。
- 非阻塞：是指即使调用结果没返回，也不会阻塞当前线程。

## 什么是缓冲区溢出

缓冲区为暂时置放输出或输入资料的内存。

缓冲区溢出是指当计算机向缓冲区填充数据时超出了缓冲区本身的容量，溢出的数据覆盖在合法数据上。

造成缓冲区溢出的主要原因是程序中没有仔细检查用户输入是否合理。

计算机中，缓冲区溢出会造成的危害主要有以下两点：

- 程序崩溃导致拒绝服务
- 跳转并且执行一段恶意代码

## 什么是抖动或颠簸现象

刚刚换出的页面马上又要换入内存，刚刚换入的页面马上又要换出外存，这种频繁的页面调度行为称为抖动，或颠簸。

产生抖动的主要原因是进程频繁访问的页面数目高于可用的物理块数（分配给进程的物理块不够）。

为进程分配的物理块太少，会使进程发生抖动现象。为进程分配的物理块太多，又会降低系统整体的并发度，降低某些资源的利用率。

为了研究为应该为每个进程分配多少个物理块，Denning 提出了进程工作集的概念。

## 一段代码的完整生命周期

- 编写源代码
- 预编译：主要处理源代码文件中的以 `#` 开头的预编译指令。
- 编译：把预编译之后生成的 `xxx.i` 或 `xxx.ii`，进行一系列词法分析、语法分析、语义分析及优化后，生成相应的汇编代码文件。 
- 汇编：将汇编代码转变成机器可以执行的指令（机器码文件）。 汇编器的汇编过程相对于编译器来说更简单，没有复杂的语法，也没有语义，更不需要做指令优化，只是根据汇编指令和机器指令的对照表一一翻译过来，汇编过程有汇编器 `as` 完成。经汇编之后，产生目标文件（与可执行文件格式几乎一样）`xxx.o`（Linux 下）、`xxx.obj`（Windows 下）。  
- 链接：将不同的源文件产生的目标文件进行链接，从而形成一个可以执行的程序。链接分为静态链接和动态链接。
- 加载到内存
- 执行

## 预编译过程的具体细节

- 删除所有的 `#define`，展开所有的宏定义。  
- 处理所有的条件预编译指令，如 `#if`、`#endif`、`#ifdef`、`#elif` 和 `#else` 。  
- 处理 `#include` 预编译指令，将文件内容替换到它的位置，若文件中包含其他文件，则这个过程是递归进行的。  
- 删除所有的注释，`//` 和 `/**/`。 
- 保留所有的 `#pragma` 编译器指令，编译器需要用到他们，如：`#pragma once` 是为了防止有文件被重复引用。  
- 添加行号和文件标识，便于编译时编译器产生调试用的行号信息，和编译时产生编译错误或警告是 能够显示行号。  

## 编译过程的具体细节

- 词法分析：利用类似于有限状态机的算法，将源代码程序输入到扫描机中，将其中的字符序列分割成一系列的记号。  
- 语法分析：语法分析器对由扫描器产生的记号，进行语法分析，产生语法树。由语法分析器输出的语法树是一种以表达式为节点的树。  
- 语义分析：语法分析器只是完成了对表达式语法层面的分析，语义分析器则对表达式是否有意义进行判断，其分析的语义是静态语义（在编译期能分析的语义）。相对应的动态语义是在运行期才能确定的语义。  
- 优化：源代码级别的一个优化过程。  
- 目标代码生成：由代码生成器将中间代码转换成目标机器代码，生成一系列的代码序列（汇编语言表示）。  
- 目标代码优化：对上述的目标机器代码进行优化：寻找合适的寻址方式、使用位移来替代乘法运算、删除多余的指令等。  

## 动态链接和静态链接的区别

- 静态链接：函数和数据被编译进一个二进制文件。在使用静态库的情况下，在编译链接可执行文件时，链接器从库中复制这些函数和数据并把它们和应用程序的其它模块组合起来创建最终的可执行文件。 
  - 空间浪费：因为每个可执行程序中对所有需要的目标文件都要有一份副本，所以如果多个程序对同一个目标文件都有依赖，会出现同一个目标文件都在内存存在多个副本。
  - 更新困难：每当库函数的代码修改了，这个时候就需要重新进行编译链接形成可执行程序。  
  - 运行速度快：在可执行程序中已经具备了所有执行程序所需要的任何东西，在执行的时候运行速度快。  
- 动态链接： 把程序按照模块拆分成各个相对独立部分，在程序运行时才将它们链接在一起形成一个完整的程序，而不是像静态链接一样把所有程序模块都链接成一个单独的可执行文件。  
  - 共享库：就是即使需要每个程序都依赖同一个库，但是该库不会像静态链接那样在内存中存在多份副本，而是这多个程序在执行时共享同一份副本。 
  - 更新方便：更新时只需要替换原来的目标文件，而无需将所有的程序再重新链接一遍。当程序下一次运行时，新版本的目标文件会被自动加载到内存并且链接起来，程序就完成了升级的目标。  
  - 性能损耗：因为把链接推迟到了程序运行时，所以每次执行程序都需要进行链接，所以性能会有一定损失。

## 进程终止的方式

- 正常退出
- 错误退出
- 严重错误退出
- 被其他进程杀死

## 介绍一下几种典型的锁

**读写锁**

- 多个读者可以同时进行读
- 写者必须互斥（只允许一个写者写，也不能读者写者同时进行）
- 写者优先于读者（一旦有写者，则后续读者必须等待，唤醒时优先考虑写者）

**互斥锁**

一次只能一个线程拥有互斥锁，其他线程只有等待。互斥锁是在抢锁失败的情况下主动放弃 CPU 进入睡眠状态直到锁的状态改变时再唤醒，而操作系统负责线程调度。

为了实现锁的状态发生改变时唤醒阻塞的线程或者进程，需要把锁交给操作系统管理，所以互斥锁在加锁操作时涉及上下文的切换。

互斥锁实际的效率还是可以让人接受的，加锁的时间大概 100ns 左右，而实际上互斥锁的一种可能的实现是先自旋一段时间，当自旋的时间超过阀值之后再将线程投入睡眠中，因此在并发运算中使用互斥锁（每次占用锁的时间很短）的效果可能不亚于使用自旋锁。

**条件变量**

互斥锁一个明显的缺点是它只有两种状态：锁定和非锁定。而条件变量通过允许线程 *阻塞和等待* 另一个线程发送信号，弥补了互斥锁的不足，它常和互斥锁一起使用，以免出现竞态条件。

当条件不满足时，线程往往解开相应的互斥锁并阻塞线程，然后等待条件发生变化。一旦其他的某个线程改变了条件变量，它将通知相应的条件变量唤醒一个或多个正被此条件变量阻塞的线程。

总的来说互斥锁是线程间互斥的机制，条件变量则是同步机制。  

**自旋锁**

如果进线程无法取得锁，进线程不会立刻放弃 CPU 时间片，而是一直循环尝试获取锁，直到获取为止。

如果别的线程长时期占有锁，那么自旋就是在浪费 CPU 做无用功，但是自旋锁一般应用于加锁时间很短的场景，这个时候效率比较高。

## 常见内存分配内存错误

**内存分配未成功，却使用了它**

编程新手常犯这种错误，因为他们没有意识到内存分配会不成功。常用解决办法是，在使用内存之前检查指针是否为 `NULL`。

- 如果指针 `p` 是函数的参数，那么在函数的入口处用 `assert(p!=NULL)` 进行检查。
- 如果是用 `malloc` 或 `new` 来申请内存，应该用 `if(p= =NULL)` 或 `if(p!=NULL)` 进行防错处理。  

**内存分配虽然成功，但是尚未初始化就引用它**

犯这种错误主要有两个起因：一是没有初始化的观念；二是误以为内存的缺省初值全为零，导致引用初值错误（例如数组）。

内存的缺省初值究竟是什么并没有统一的标准，尽管有些时候为零值，我们宁可信其无不可信其有。所以无论用何种方式创建数组，都别忘了赋初值，即便是赋零值也不可省略，不要嫌麻烦。 

内存分配成功并且已经初始化，但操作越过了内存的边界。  

例如，在使用数组时经常发生下标 “多1” 或者 “少1” 的操作。特别是在 `for` 循环语句中，循环次数很容易搞错，导致数组操作越界。  

**忘记了释放内存，造成内存泄露**

含有这种错误的函数每被调用一次就丢失一块内存。刚开始时系统的内存充足，你看不到错误。终有一次程序突然挂掉，系统出现提示：内存耗尽。动态内存的申请与释放必须配对，程序中 `malloc` 与 `free` 的使用次数一定要相同，否则肯定有错误（`new`/`delete` 同理）。  

**释放了内存却继续使用它**

常见于以下有三种情况：程序中的对象调用关系过于复杂，实在难以搞清楚某个对象究竟是否已经释放了内存，此时应该重新设计数据结构，从根本上解决对象管理的混乱局面。

函数的 `return` 语句写错了，注意不要返回指向 “栈内存” 的 “指针” 或者 “引用”，因为该内存在函数体结束时被自动销毁。 

使用 `free`或 `delete` 释放了内存后，没有将指针设置为 `NULL`，导致产生 “野指针”。

## 内存交换时被换出的进程保存在哪里

保存在磁盘中，也就是外存中。

具有对换功能的操作系统，通常把磁盘空间分为文件区和对换区两部分。

- 文件区主要用于存放文件，主要追求存储空间的利用率，因此对文件区空间的管理采用 *离散分配方式*。
- 对换区空间只占磁盘空间的小部分，被换出的进程数据就存放在对换区。由于对换的速度直接影响到系统的整体速度，因此对换区空间的管理主要追求换入换出速度，因此通常对换区采用 *连续分配方式*。总之，对换区的I/O速度比文件区的更快。