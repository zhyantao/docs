# 操作系统原理

## 操作系统概述

操作系统是一段程序，运行于硬件之上，它是一种系统软件。
它负责协调硬件、软件等计算机资源的工作，为上层用户、应用程序提供简单易用的服务。
因此，操作系统是一个资源管理者，它管理着 CPU 、存储器、文件、设备。

操作系统具有四大特征（牢记）：

- 并发，交替上 CPU 运行
- 共享，共享方式分为两种：互斥共享（如摄像头）和同时共享（如磁盘）
- 虚拟，对 CPU 的虚拟就是线程（时分复用），对磁盘的虚拟就是文件（空分复用）
- 异步，指进程以不可预知的速度向前推进，不知道什么时候开始、暂停、结束

没有并发和共享，就谈不上虚拟和异步，因此并发和共享是操作系统的两个最基本的特征。

### 操作系统的运行机制

手工编写高级语言代码（如 C 语言）经由编译器编译后可以生成硬件理解的语言。
将硬件理解的语言（代码）放在磁盘的合适位置，磁盘开始从那个位置开始执行。

虽然同为操作系统的源代码，在同一份操作系统源代码中并不是所有语句都具备相同的权限。
能够直接和硬件打交道的代码是内核程序，它们对应的指令是特权指令；
而使用内核程序给我们开放的接口进行编写的程序是应用程序，对应的指令是非特权指令。

操作系统的层次结构如下图所示：

```{figure} ../_static/images/os-architecture.*
操作系统的层次结构
```

正在运行特权指令的处理器处于内核态（也叫核心态或管态），正在运行非特权指令的处理器则处于用户态（也叫目态）。
从内核态到用户态的转变，需要修改一条 PSW 特权指令，而从用户态转变到内核态则由中断引起，硬件自动完成。
中断的作用是让操作系统内核强行夺回 CPU 的控制权，使 CPU 从用户态变为内核态。
因此，没有中断机制，就不可能实现操作系统，不可能实现程序并发。

中断分为两种：内中断和外中断。
内中断也叫异常，触发内中断的条件可以是陷阱（trap）、故障（fault）或终止（abort）。
外中断简称中断，触发条件是时钟中断或 I/O 中断请求。
CPU 在执行指令时会自动检查是否有异常发生，由程序自动触发内中断。
在每个指令周期的末尾，CPU 都会检查是否由外部信号需要处理，以此判断是否需要执行外中断。
内中断和外中断都会通过中断向量表来找到相应的中断处理程序。

当我们需要进行设备管理、文件管理、进程管理、进程通信、内存管理时，就需要用到系统调用了。
系统调用时操作系统对应用程序或程序员提供的接口。
系统调用的通过传参、陷入或访管指令触发，由操作系统内核程序处理系统调用请求，返回给应用程序。

宏内核性能高，但是内核代码庞大，结构混乱，难以维护。微内核功能少，但是需要频繁地变态，性能差。
**在我们后续的实验中，使用的是宏内核设计。**

### 操作系统的架构设计

参考 Deepin 的架构设计：<https://www.deepin.org/zh/developer-community/architectural-design/>

```{figure} ../_static/images/deepin-arch.drawio.jpeg
Deepin 操作系统的架构设计
```

## 进程管理

### 进程的概念

进程是进程实体的运行过程，是系统资源进行分配和调度的一个独立单位。

一个进程实体/映像包括以下几个部分：

- PCB（进程控制块）
- 程序段
- 数据段

进程控制块又可以细分为：

- 进程描述信息：进程标识符 PID、用户标识符 UID
- 进程控制和管理信息：CPU、磁盘、网络流量使用情况、进程当前状态（就绪、阻塞、运行...）
- 资源分配清单：正在使用哪些文件、正在使用哪些内存区域、正在使用哪些 I/O 设备
- CPU 相关信息：如 PSW、PC 等各种寄存器的值（用于实现进程切换）

当我们 `fork` 出来一个新的进程后，它们的程序段是相同的，但是它们的 PCB 和数据段并不相同。

进程的组织方式可以分为链接和索引两种。
链接方式是指按照进程状态将 PCB 分为多个队列，操作系统持有指向各个队列的指针。
索引方式是指根据进程状态的不同，建立几张索引表，操作系统持有指向各个索引表的指针。

进程之间的切换如下图所示：

```{figure} ../_static/images/os-process-schedule.*
操作系统的进程调度的 5 状态模型
```

在进程控制的过程中，必须完成的三件事：

- 更新 PCB 中的相关信息：修改进程状态标志、保存运行环境、恢复运行环境
- 将 PCB 插入合适的队列
- 分配/回收资源

在代码实现中，这五种状态间的切换如下图所示：

```{figure} ../_static/images/os-process-switch.png
操作系统的进程调度的 5 种状态间切换 [^cite_ref-3]
```

### 进程间的通信

进程之间的通信方式有三种：

1、共享存储

设置共享空间，然后互斥地访问共享空间。

2、管道通信

设置一个特殊的共享文件（管道），其实就是一个缓冲区。
但是一个管道只能实现半双工通信，要想实现双向同时通信要建立两个管道。
各个进程互斥地访问管道。

3、消息传递

传递结构化的消息（消息头和消息体），提供提供 "发送/接收原语"。
在具体的实现上，一种是直接通信，将消息直接挂在接收方的消息队列里，另一种是信箱方式，先把消息发送到信箱中。

### 线程的概念

进程是资源分配的基本单位，线程是 CPU 调度的基本单位。

同一进程内的各个线程共享拥有的资源，同一进程内的线程切换不会导致进程切换。

引入进程的目的是增加并发度，减少并发带来的系统开销。

### 资源调度

所谓调度，需要回答的核心问题是：在何时将何种任务分配给何种资源以何种方式执行。
调度广泛存在于操作系统、编程语言运行时、容器编排和业务系统中，其核心目的是
"对有限的资源进行分配以实现最大化资源的利用率、降低系统的尾延迟或最小化任务的完工时间" [^cite_ref-1]。

在计算机科学中，调度就是一种将任务（Work）分配给资源的方法。
任务可能是虚拟的计算任务，例如线程、进程或者数据流，这些任务会被调度到硬件资源上执行，例如：处理器 CPU 等设备
[^cite_ref-2]。

在 Linux 操作系统中，带执行的任务就是操作系统的基本单位是线程，而可分配的资源就是 CPU 的时间。
类似地，Kubernetes 调度的基本单位是 Pod，可分配的资源是 Node [^cite_ref-2]。

关于操作系统的调度问题及其相关的优化，作者 draveness 在 _调度系统设计精要_ [^cite_ref-2]
一文中做了详细介绍。

#### CPU 调度

按照某种算法选择一个进程，将 CPU 分配给它。

```{note}
存储器的种类很多，按其用途可分为主存储器（又叫 "内存储器"，简称 "内存"）和辅助存储器（又称
"外存储器"，简称 "外存"）。外存简单来说就是日常所说的 "存储"，主要分为固态硬盘跟机械硬盘。
内存是可以进行高速读写的储存器，包括常见的内存条、显卡内存（又叫 "显存"）。
```

为减轻系统负担，提高系统的资源利用率，将暂时不执行的进程调到外存，变为 "挂起态"。

```{figure} ../_static/images/os-process-schedule-7.*
操作系统的进程调度的 7 状态模型
```

CPU 的调度分为三个层次：

```{list-table}
:header-rows: 1
:widths: 15, 20, 60, 10

* - 调度层次
  - 调度方向
  - 调度规则
  - 频率
* - 高级调度 (作业调度)
  - 外存 $\rightarrow$ 内存
  - 按照某种规则，从后备队列中选择合适的作业将其调入内存，并为其创建进程
  - 低
* - 中级调度 (内存调度)
  - 外存 $\rightarrow$ 内存
  - 按照某种规则，从挂起队列中选择合适的进程将其数据调回内存
  - 中
* - 低级调度 (进程调度)
  - 内存 $\rightarrow$ CPU
  - 按照某种规则，从就绪队列中选择一个进程为其分配处理机
  - 高
```

#### 评价指标

1、CPU 利用率

$$
CPU 利用率 = \frac{忙碌的时间}{总时间}
$$

2、系统吞吐量

$$
系统吞吐量 = \frac{总共完成了多少道作业}{总共花了多少时间}
$$

3、周转时间

$$
周转时间 &= 作业完成时间 - 作业提交时间 \\ \\
平均周转时间 &= \frac{各作业周转时间之和}{作业数} \\ \\
带权周转时间 &= \frac{作业周转时间}{作业实际运行的时间} \\ \\
平均带权周转时间 &= \frac{各作业带权周转时间之和}{作业数}
$$

4、等待时间

$$
等待时间 = 进程或作业等待被服务的时间之和
$$

5、响应时间

$$
响应时间 = 从用户提交请求到首次产生响应所用的时间
$$

#### 调度算法

```{list-table}
:header-rows: 1
:widths: 35, 50, 15

* - 调度算法
  - 特点
  - 产生饥饿
* - 先来先服务（FCFS）
  - 不公平，对长作业有利，对短作业不利
  - $\times$
* - 短作业优先（SJF/SPF/SRTN）
  - 不公平，对短作业有利，对长作业不利
  - $\checkmark$
* - 高响应比优先（HRRN）
  - 综合 FCFS 和 SJF 的优点
  - $\times$
* - 时间片轮转（RR）
  - 公平，适用于分时系统
  - $\times$
* - 优先级调度（PSA）
  - 不公平，适用于实时系统
  - $\checkmark$
* - 多级反馈队列（MFQS）
  - 综合 RR 和 PSA 的优点
  - $\checkmark$
```

### 同步和互斥

访问临界区需要遵循的四个原则：

```{note}
"忙等" 是指当前进程无法获得全部资源，但又会在占用 CPU 的同时，等待所需资源的一种状态。
需要特别注意的是，"忙等" 并不是 "忙则等待" 的简称。
```

- 空闲让进：临界区空闲时，可以允许一个请求进入临界区的进程立即进入临界区
- 忙则等待：当已有进程进入临界区时，其他试图进入临界区的进程必须等待
- 有限等待：对请求访问的进程，应保证能在有限时间内进入临界区（保证不会饥饿）
- 让权等待：当进程不能进入临界区时，应立即释放处理机，防止进程忙等待

#### 单标志法的软件实现

:::{card}

```{code-block} c
int turn = 0;
// P0 进程
while (turn != 0); // 进入区
critical section;  // 临界区
turn = 1;          // 退出区
remainder section; // 剩余区
```

:::

:::{card}

```{code-block} c
int turn = 0;
// P1 进程
while (turn != 1); // 进入区
critical section;  // 临界区
turn = 0;          // 退出区
remainder section; // 剩余区
```

:::

在进⼊区只做 "检查"，不
"上锁"，在退出区把临界区的使用权转交给另一个进程（相当于在退出区既给另一个进程
"解锁"，又给自己 "上锁"。

不遵循 "空闲让进" 原则。

#### 双标志先检查的软件实现

:::{card}

```{code-block} c
bool flag[2];
flag[0] = false;
flag[1] = false;
// P0 进程
while (flag[1]);   // 进入区（检查）
flag[0] = true;    // 进入区（上锁）
critical section;  // 临界区
flag[0] = false;   // 退出区
remainder section; // 剩余区
```

:::

:::{card}

```{code-block} c
bool flag[2];
flag[0] = false;
flag[1] = false;
// P1 进程
while (flag[0]);   // 进入区（检查）
flag[1] = true;    // 进入区（上锁）
critical section;  // 临界区
flag[1] = false;   // 退出区
remainder section; // 剩余区
```

:::

由于检查和上锁两个操作并不是原子操作，所以不遵循 "忙则等待" 原则。

#### 双标志后检查的软件实现

:::{card}

```{code-block} c
bool flag[2];
flag[0] = false;
flag[1] = false;
// P0 进程
flag[0] = true;    // 进入区（上锁）
while (flag[1]);   // 进入区（检查）
critical section;  // 临界区
flag[0] = false;   // 退出区
remainder section; // 剩余区
```

:::

:::{card}

```{code-block} c
bool flag[2];
flag[0] = false;
flag[1] = false;
// P1 进程
flag[1] = true;    // 进入区（上锁）
while (flag[0]);   // 进入区（检查）
critical section;  // 临界区
flag[1] = false;   // 退出区
remainder section; // 剩余区
```

:::

解决了 "忙则等待" 问题，但是违背了 "空闲让进" 和 "有限等待" 原则，有可能产生 "饥饿"。

#### Perterson 算法的软件实现

:::{card}

```{code-block} c
bool flag[2];
int turn = 0;
// P0 进程
flag[0] = true;               // 进入区（上锁）
turn = 1;                     // 谦让
while (flag[1] && turn == 1); // 进入区（检查）
critical section;             // 临界区
flag[0] = false;              // 退出区
remainder section;            // 剩余区
```

:::

:::{card}

```{code-block} c
bool flag[2];
int turn = 0;
// P1 进程
flag[1] = true;               // 进入区（上锁）
turn = 0;                     // 谦让
while (flag[0] && turn == 0); // 进入区（检查）
critical section;             // 临界区
flag[1] = false;              // 退出区
remainder section;            // 剩余区
```

:::

在进入区 "主动争取 —— 主动谦让 —— 检查对方是否想进、己方是否谦让"。

不遵循 "让权等待" 原则，暂时无法进入临界区的进程会占用 CPU 并循环执行，导致 "忙等"。

#### 中断屏蔽法的硬件描述

具体实现：关中断 —— 访问临界区 —— 开中断。

简单、高效，但是不适用于多处理机，只适用于操作系统内核进程，不适用于用户进程。

#### `TS`指令/`TSL`指令的硬件描述

:::{card}

```{code-block} c
// 硬件实现的逻辑表达
bool TestAndSet(bool *lock) {
  bool old;
  old = *lock;
  *lock = true;
  return old;
}

// 使用 TSL 指令
while (TestAndSet(&lock)) { // 上锁并检查
  critial section;          // 临界区
  lock = false;             // 退出区
  remainder section;        // 剩余区
}
```

:::

将上锁和检查变为了原子操作，适用于多处理机环境。

不满足 "让权等待"，暂时无法进入临界区的进程会占用 CPU 并循环执行，导致 "忙等"。

#### `XCHG`指令的硬件描述

:::{card}

```{code-block} c
// 硬件实现的逻辑表达
Swap (bool *a, bool *b) {
  bool temp;
  temp = *a;
  *a = *b;
  *b = temp;
}

// 使用 Swap 指令
bool old = true;
while (old == true) {
  Swap(&lock, &old);
}
critial section;
lock = false;
remainder section;
```

:::

将上锁和检查变为了原子操作，适用于多处理机环境。

不满足 "让权等待"，暂时无法进入临界区的进程会占用 CPU 并循环执行，导致 "忙等"。

#### 信号量机制的软件实现

信号量其实就是一个变量（可以是一个整数，也可以是更复杂的记录型变量）。
可以用一个信号量来表示系统中某种资源的数量，比如：系统中只有一台打印机，就可以设置初值为 1 的信号量。

```{note}
`wait`、`signal` 原语常简称为 PV 操作（来自荷兰语 Proberen 和 Verhogen）。
因此，我们有时简写为 `P(S)`、`V(S)`。

`wait(S)` 理解为等待 `S` 有资源可用；`signal(S)` 理解为释放 `S` 的资源。
注意，翻译的顺序，动词始终在前面，否则可能会引发理解偏差。

```

用户进程可以通过使用操作系统提供的 `wait(S)` 和 `signal(S)`
原语来对信号量进行操作，从而很方便地实现进程互斥和同步。
原语是由关中断/开中断指令实现的。

##### 整型信号量

:::{card}

```{code-block} c
int S = 1;

void wait(int S) {  // wait 原语，相当于进入区
  while (S <= 0);   // 循环等待
  S = S - 1;
}

void signal(int S) { // signal 原语，相当于退出区
  S = S + 1;
}
```

:::

:::{card}

```{code-block} c
// P0 进程
wait(S);
//使用打印机资源;
signal(S);
```

:::

:::{card}

```{code-block} c
// P1 进程
wait(S);
//使用打印机资源;
signal(S);
```

:::

不满足 "让权等待" 原则。

##### 记录型信号量

整型信号量的缺陷是存在 "忙等" 问题，因此人们又提出了 "记录型信号量"，即用记录型数据结构表示的信号量。

:::{card}

```{code-block} c
typedef struct {
  int value;         // 剩余资源数
  struct process *L; // 等待队列
} semaphore;

void wait(semaphore S) {
  S.value--;
  if (S.value < 0) { // 如果无可用资源
    block(S.L);
  }
}

void signal(semaphore S) {
  S.value++;
  if (S.value <=0) { // 如果有等待进程
    wakeup(S.L);
  }
}
```

:::

:::{card}

```{code-block} c
// P0 进程
wait(S);
//使用打印机资源;
signal(S);
```

:::

:::{card}

```{code-block} c
// P1 进程
wait(S);
//使用打印机资源;
signal(S);
```

:::

因为资源不可用时，会自动加入到阻塞队列，符合 "让权等待" 原则，不会出现 "忙等" 现象。

:::{card}
例：有如下所示的同步关系，请完成代码实现。

```{figure} ../_static/images/os-process-semaphore.*
进程之间的同步关系
```

:::

:::{card}

```{code-block} c
P1() {
  S1;
  V(a);
  V(b);
}
```

:::

:::{card}

```{code-block} c
P2() {
  P(a);
  S2;
  V(c);
}
```

:::

:::{card}

```{code-block} c
P3() {
  P(b);
  S3;
}
```

:::

:::{card}

```{code-block} c
P4() {
  P(c);
  S4;
}
```

:::

#### 经典同步问题

##### 生产者-消费者问题

```{figure} ../_static/images/os-process-producer-consumer.*
生产者-消费者问题
```

```{note}
缓冲区是临界资源，各进程必须互斥地访问。

实现互斥的 P 操作必须在实现同步的 P 操作之后，否则有可能发生死锁。

思考：能不能用一个同步信号量实现生产者消费者模型？
```

:::{card}

```{code-block} c
semaphore mutex = 1;        // 互斥信号量，实现对缓冲区的互斥访问
semaphore not_empty = n;    // 同步信号量，表示空闲缓冲区的数量
semaphore not_full = 0;     // 同步信号量，表示非空缓冲区的数量
```

:::

:::{card}

```{code-block} c
producer() {
  while (1) {
    // 生产一个产品
    P(not_empty); // 等待缓冲区不空
    P(mutex);
    // 把产品放入缓冲区
    V(mutex);
    V(not_full);  // 占用缓冲区
  }
}
```

:::

:::{card}

```{code-block} c
consumer() {
  while (1) {
    P(not_full);  // 等待缓冲区不满
    P(mutex);
    // 从缓冲区取出一个产品
    V(mutex);
    V(not_empty); // 释放缓冲区
    // 使用产品
  }
}
```

:::

##### 多生产者-多消费者问题

单生产者-单消费者问题指的是生产者生产额消费者消费的是同一种产品，
而多生产者-多消费者问题指的是生产者可以生产多种产品，消费者也可以消费多种产品。

```{figure} ../_static/images/os-process-multi-producer-consumer.*
多生产者-多消费者问题
```

```{note}
不知道你注意到没有，有向图中有几条有向线段，我们就声明几个同步信号量。

如果缓冲区的大小是 1，那么有可能不需要设置互斥信号量就可以实现互斥地访问缓冲区。
当然，这不是绝对的，要具体问题具体分析。
```

:::{card}

```{code-block} c
semaphore mutex = 1;      // 互斥信号量，实现对缓冲区（盘子）的互斥访问
semaphore apple = 0;      // 同步信号量，盘子中有几个苹果
semaphore orange = 0;     // 同步信号量，盘子中有几个橘子
semaphore plate = 1;      // 同步信号量，盘子中还可以放几个水果
```

:::

:::{card}

```{code-block} c
producer1() {
  while (1) {
    // 准备一个苹果
    P(plate);
    P(mutex);
    // 把苹果放入盘子
    V(mutex);
    V(apple);
  }
}
```

:::

:::{card}

```{code-block} c
producer2() {
  while (1) {
    // 准备一个橘子
    P(plate);
    P(mutex);
    // 把苹果放入盘子
    V(mutex);
    V(orange);
  }
}
```

:::

:::{card}

```{code-block} c
consumer1() {
  while (1) {
    P(apple);
    P(mutex);
    // 从盘子中取出苹果
    V(mutex);
    V(plate);
    // 吃掉苹果
  }
}
```

:::

:::{card}

```{code-block} c
consumer2() {
  while (1) {
    P(orange);
    P(mutex);
    // 从盘子中取出橘子
    V(mutex);
    V(plate);
    // 吃掉橘子
  }
}
```

:::

##### 吸烟者问题

```{figure} ../_static/images/os-process-smoker.*
吸烟者问题
```

本质上，这个问题也是属于 "生产者-消费者" 问题，更详细地说是 "单生产者-多消费者" 问题。

:::{card}

```{code-block} c
//semaphore mutex = 1;    // 缓冲区只有一个，忽略不写了
semaphore offer1 = 0;     // 同步信号量
semaphore offer2 = 0;     // 同步信号量
semaphore offer3 = 0;     // 同步信号量
semaphore finish = 0;     // 同步信号量
int i = 0;                // 用于实现 "三个吸烟者轮流吸烟"
```

:::

:::{card}

```{code-block} c
provider() {
  while (1) {
    if (i == 0) {
      // 将组合一放在桌上
      V(offer1);
    }
    else if (i == 1) {
      // 将组合二放在桌上
      V(offer2);
    }
    else if (i == 2) {
      // 将组合三放在桌上
      V(offer3);
    }
    i = (i + 1) % 3;
    P(finish);
  }
}
```

:::

:::{card}

```{code-block} c
smoker1() {
  while (1) {
    P(offer1);
    // 从桌子上拿走组合一，卷烟，抽烟
    V(finish);
  }
}
```

:::

:::{card}

```{code-block} c
smoker2() {
  while (1) {
    P(offer2);
    // 从桌子上拿走组合二，卷烟，抽烟
    V(finish);
  }
}
```

:::

---

:column: col-lg-6 col-md-6 col-sm-6 p-3

```{code-block} c
smoker3() {
  while (1) {
    P(offer3);
    // 从桌子上拿走组合三，卷烟，抽烟
    V(finish);
  }
}
```

:::

##### 读者-写者问题

允许多个读者同时读，读者和写者、写者和写者不能同时操作。

:::{card}

```{code-block} c
semaphore rw = 1;         // 用于实现对共享文件的互斥访问
int count = 0;            // 记录当前几个读进程在访问文件
semaphore mutex = 1;      // 保证对 count 变量的互斥访问
```

:::

:::{card}

```{code-block} c
writer() {
  while (1) {
    P(rw);        // 申请读写锁
    // 写文件
    V(rw);        // 释放读写锁
  }
}
```

:::

:::{card}

```{code-block} c
reader() {
  while (1) {
    P(mutex);
    if (count == 0)
      P(rw);// 第一个读进程申请读写锁
    count++;
    V(mutex);
    // 读文件
    P(mutex);
    count--;
    if (count == 0)
      V(rw);        // 释放读写锁
    V(mutex);
  }
}
```

:::

只要有都进程还在读，写进程就要一直阻塞等待，可能 "饿死"。因此，在这种算法中，读进程是优先的。

在下面的算法中，实现了写优先。有的书上也把这个算法称为 "读写公平法"。

:::{card}

```{code-block} c
semaphore rw = 1;         // 用于实现对共享文件的互斥访问
int count = 0;            // 记录当前几个读进程在访问文件
semaphore mutex = 1;      // 保证对 count 变量的互斥访问
semaphore w = 1;          // 用于实现 "写优先"
```

:::

:::{card}

```{code-block} c
writer() {
  while (1) {
    P(w);
    P(rw);        // 申请读写锁
    // 写文件
    V(rw);        // 释放读写锁
    V(w);
  }
}
```

:::

:::{card}

```{code-block} c
reader() {
  while (1) {
    P(w);
    P(mutex);
    if (count == 0)
      P(rw);// 第一个读进程申请读写锁
    count++;
    V(mutex);
    V(w);
    // 读文件
    P(mutex);
    count--;
    if (count == 0)
      V(rw);        // 释放读写锁
    V(mutex);
  }
}
```

:::

##### 哲学家进餐问题

```{figure} ../_static/images/An_illustration_of_the_dining_philosophers_problem.png
:height: 300px

哲学家就餐问题
```

5 位哲学家 5 根筷子，如何在避免死锁的情况下，顺利的进餐。

```{note}
在并发的情况下，如果 5 位哲学家都拿起了左边的筷子，又都在等待右手的筷子，就发生了死锁。

这些进程之间只存在互斥关系，但与之前的互斥关系不同，每个进程都要同时持有两个临界资源，因此就有可能发生 "死锁"。

因此，如果碰到了一个进程需要同时持有多个临界资源的情况，就应该参考哲学家问题的思想。
```

为了避免死锁，提供了三种思路供参考（三选一）：

- 要求奇数号的哲学家先拿左边的筷子，偶数号的哲学家先拿右手边的筷子。
- 仅当一个哲学家左右两边的筷子都能拿时，才允许他抓起筷子。
- 最多允许 4 位哲学家拿筷子，这样肯定有一个人时满足可以拿起两边的筷子的。

:::{card}

```{code-block} c
semaphore chopstick[5] = {1, 1, 1, 1, 1};
semaphore mutex = 1;    // 互斥地取筷子
Pi() {
  while (1) {
    P(mutex);           // 同时拿起左右两边的筷子
    P(chopstick[i]);
    P(chopstick[ (i + 1) % 5 ]);
    V(mutex);
    // 进餐
    V(chopstick[i]);
    V(chopstick[ (i + 1) % 5 ]);
    // 思考
  }
}
```

:::

#### 管程

使用信号量实现进程的同步和互斥问题，编程困难而且容易出错。
管程则提供了更简单的操作方式。

管程是一种特殊的软件模块，有这些部分组成：

- 局部于管程的共享数据结构说明；
- 对该数据结构进行操作的一组过程（函数）；
- 对局部于管程的共享数据设置初始值的语句；
- 管程有一个名字。

管程的基本特征：

- 局部于管程的数据只能被局部于管程的过程所访问；
- 一个进程只有通过调用管程内的过程才能进入管程访问共享数据；
- 每次只允许一个进程在管程内执行某个内部过程。

### 死锁

在并发环境下，各进程因竞争资源而造成的一种互相等待对方手里的资源，导致各进程都阻塞，都无法向前推进的现象，就是
"死锁"。发生死锁后若无外力干涉，这些进程都将无法向前推进。

```{note}
死锁、饥饿、死循环的区别和联系

共同点：都是进程无法顺利向前推进的现象。

不同点：死锁一定是 "循环等待对方手里的资源" 导致的，发生死锁，至少有两个进程。
发生死锁的进程一定处于阻塞态。
发生 "饥饿" 可能只有一个进程，该进程既可能处于阻塞态，也可能处于就绪态。
发生死循环的进程可能只有一个，该进程可以处于运行态。

死锁和饥饿是操作系统需要解决的问题，而死循环是程序员需要解决的问题。
```

死锁产生的必要条件：

- 互斥条件：共享资源不会导致死锁。
- 不剥夺条件：进程当前占有的资源不可被剥夺，只能主动释放。
- 请求和保持条件：进程已经保持了一个资源，但又提出了新的资源请求。
- 循环等待条件：存在一个环，该环中的每个进程都在请求其他进程保持的资源。

#### 死锁的处理策略

##### 预防死锁（不允许死锁发生）

破坏产生死锁的四个必要条件中的一个或者几个，可能会导致系统资源利用率和系统吞吐量降低。

```{list-table}
:header-rows: 1
:widths: 15, 45, 40

* -
  - 措施
  - 缺点
* - 破坏互斥条件
  - 将临界资源改造为可共享使用的资源（如 SPOOLing 技术）
  - 可行性不高，很多时候无法破坏互斥条件
* - 破坏不可剥夺条件
  - 方案1：申请的资源得不到满足时，立即释放拥有的所有资源；
    方案2：申请的资源被其他进程占用时，由操作系统协助剥夺（考虑优先级）
  - 实现复杂，剥夺资源可能导致部分工作失效，反复申请和释放导致系统开销大，可能导致饥饿
* - 破坏请求和保持条件
  - 运行前分配好所有需要的资源，之后一直保持
  - 资源利用率低，可能导致饥饿
* - 破坏循环等待条件
  - 给资源编号，必须按编号从小到大的顺序申请资源
  - 不方便增加新设备，会导致资源浪费，用户编程麻烦
```

##### 避免死锁（不允许死锁发生）

```{note}
如果能够找到一个安全序列，就是安全状态，如果一个都找不到，即为不安全状态。
系统处于安全状态，一定不会发生死锁，而处于不安全状态，不一定会发生死锁。
```

在资源的动态分配过程中，用银行家算法去防止系统进入不安全状态，从而避免发生死锁。

在进程提出资源申请时，先预判此次分配是否会导致系统进入不安全状态。
如果会进入不安全状态，就暂时不答应这次请求，让该进程先阻塞等待。

##### 检测和解除（允许死锁发生）

检测死锁的算法是资源分配图。
在资源分配图中，找出既不阻塞又不孤立的结点，消除于它相邻的所有的请求边和分配边，使之成为孤立结点。
如果最后所有的结点都成为了孤立结点，那么这个图就是可完全简化的，得到的序列就是一个安全序列。
如果最终不能消除所有的边，那么此时就发生了死锁，最终被边连着的结点就是处于死锁状态的结点。

一旦检测出死锁的发生，就应该立即解除死锁。对死锁的结点我们通常做如下处理：

- 资源剥夺法：撤销或挂起一些进程，回收资源，再将这些资源分配给已处于阻塞状态的进程。
- 撤销进程法（终止进程法）：强行撤销部分、甚至全部死锁进程，并剥夺这些进程的资源。
- 进程回退法：这要求系统要记录进程的历史信息，设置还原点。

## 内存管理

## 文件管理

文件是对磁盘的抽象，是一组有意义的信息的集合。

在研究文件管理的问题时，应当考虑以下问题：

- 文件有哪些属性（文件名、标识符、类型、位置、大小、保护信息）
- 文件内部的组织方式（逻辑结构）
- 文件之间的组织方式（目录结构）
- 文件如何存储在外存上（物理结构）
- 如何管理磁盘的空闲块（存储空间管理）
- 开放哪些接口（`create`、`delete`、`open`、`close`、`read`、`write`）

### 文件的逻辑结构

无结构的文件：由二进制流或字符流组成，无明显的逻辑结构。

有结构文件：由记录组成，分成定长记录、可变长记录。

对有结构文件，他们的逻辑结构可以细分为：

```{list-table}
:header-rows: 1
:widths: 20, 80

* - 文件的逻辑结构
  - 注解
* - 顺序文件
  - 可变长记录无法实现随机存取，定长记录可以实现
* - 索引文件
  - 索引表本身是定长记录的顺序文件，可以实现快速检索
* - 索引顺序文件
  - 将记录分组，每组对应一个索引表项
```

### 文件的目录结构

文件目录的实现：一个文件对应一个 FCB，一个 FCB 就是一个目录项，多个 FCB 组成文件目录。

```{list-table}
:header-rows: 1
:widths: 20, 80

* - 文件的目录结构
  - 注解
* - 单级目录结构
  - 一个系统只有一张目录表，不允许文件重名
* - 两级目录结构
  - 不同的用户的文件可以重名，但不能对文件进行分类
* - 多级（树形）目录结构
  - 不同目录下的文件可以重名，可以对文件进行分类，不方便文件共享
* - 无环图目录结构
  - 在树形目录结构的基础上，增加一些指向同一结点的有向边，使整个目录成为一个有向无环图。
    为共享结点设置一个共享计数器，计数器为 0 时才能真正删除该结点
```

### 文件的物理结构

文件的物理结构也是文件的分配方式：

```{list-table}
:header-rows: 1
:widths: 20, 80

* - 文件分配方式
  - 注解
* - 顺序分配
  - 为文件分配的必须是连续的磁盘块
* - 隐式链接分配
  - 每个磁盘块都有指向下一个磁盘块的指针
* - 显示连接分配
  - 把指向磁盘块的指针放在文件分配表（FAT）中，文件分配表常驻内存
* - 索引分配
  - 为文件数据块建立索引表，若文件太大，可采用链接方案、多层索引、混合索引
```

### 空闲块管理

空闲表法：建立如下所示的数据结构，可以使用首次适应算法、最佳适应、最坏适应算法。

```{list-table}
:header-rows: 1

* - 第一个空闲盘块号
  - 空闲盘块数
* - 0
  - 2
* - 5
  - 1
* - 13
  - 2
* - 18
  - 3
```

空闲链表法：如果以盘块为单位组成一条空闲链，可以称为空闲盘块链；如果以盘区为单位组成一条链，可以成为空闲盘区链。
在分配空间时，从链头摘下若干空闲的盘块，并修改空闲链的链头指针即可（链头指针由操作系统维护）。
回收的盘块再次加到链表末尾即可。

位示图法：一般用若干连续的字（一个字等于 16 位）来表示磁盘中的盘块。每个二进制位对应一个盘块。

成组链接法：这是 UNIX 系统中采用的方法。在文件卷的目录区中专门用一个磁盘块作为 "超级块"，当系统启动时将超级块读入内存。
要保证内存和外存中的超级块数据一致。

### 磁盘调度算法

磁盘调度算法是指，我们怎么样修改访问磁道的顺序，才能最大限度地减少时间成本。

```{list-table}
:header-rows: 1
:widths: 30, 70

* - 寻道策略
  - 注解
* - 先来先服务（FCFS）
  - 最先发出访问请求的进程，优先响应，因此第一个进程想访问哪个磁道，磁头就先移动到哪个磁道
* - 最短寻道时间（SSTF）
  - 在若干进行的访问请求中，最先访问与当前磁头最近的磁道，可能产生 "饥饿" 现象
* - 扫描算法（SCAN）
  - 磁头先向磁道边缘移动，移动到最边缘，再向内侧移动，因此相应请求的顺序和请求书顺序不一致，但是解决了 SSTF 的饥饿问题
* - LOOK 调度算法
  - SCAN 需要移动到最边缘才会折返，这种可能会导致无效访问，LOOK 算法边移动边观察，因此不需要移动到最边缘才折返
* - 循环扫描算法（C-SCAN）
  - 磁头先向磁道边缘移动，移动到外边缘后立刻返回到最内侧，但不做响应，从内侧向外侧移动时才会响应
* - C-LOOK 调度算法
  - 与 LOOK 算法类似，也不需要移动到最边缘
```

访问磁盘的过程，很大一部分时间都花费在了寻道上，那么有哪些策略来节省时间呢？
主要考虑在我们存取磁盘数据时，CPU 处理数据也需要时间，因此在磁盘高速旋转的过程中传输的数据并不一定立马就能使用。
常用的策略有下面两种：

```{list-table}
:header-rows: 1
:widths: 20, 80

* - 磁盘设计策略
  - 注解
* - 交替编号
  - 逻辑上相邻的扇区，物理上有一定的间隔。间隔旋转的这段空档期最好等于处理时间
* - 错位命名
  - 采用 `(柱面号, 盘面号, 扇区号)` 的命名方式，可以在读完一个扇区后，响应下一个盘面号上的对应扇区
```

## 输入输出管理

输入/输出设备，就是指可以与计算机进行数据传输的硬件。

### I/O 的控制方式

#### 程序直接控制方式

以轮询的方式，检查 I/O 设备的状态是否适合传输数据。每次读写一个字。

优点是控制简单，不需要多少硬件支持。
但 CPU 和外设只能串行工作，且 CPU 的大部分时间处于循环测试状态，使 CPU 的利用率大大降低，因此该方式只适用于那些
CPU 执行速度较慢且外设较少的系统。

#### 中断驱动方式

将等待 I/O 的进程阻塞，先切换到别的进程执行，当 I/O 完成后，恢复阻塞进程的运行环境。

注意，CPU 在每个指令周期的末尾会检查中断。

在这种模式下，CPU 和 I/O 设备可以并行工作，但是频繁的中断处理会消耗大量的 CPU 时间。

#### DMA 方式

DMA（直接存储器存取）主要用于块设备的 I/O 控制。

与程序直接控制和中断驱动方式不同的是，数据的传送单位不再是字，而是一个块。
而且，在数据流转的过程中，不再需要 CPU 的干预，内存和设备直接交互，只有在一个或多个数据块开始和结束时，才需要 CPU 干预。

CPU 每发出一条 I/O 指令，只能读/写一个或多个**连续**的数据块。
如果要读/写多个离散的数据块，或者要将数据分别写入到不同的内存区域，CPU 需要分别发出多条 I/O 指令，进行多次中断处理才能完成。

#### 通道控制方式

通道是一种硬件，可以理解为 "弱鸡版的 CPU"。
优点是 CPU、通道、I/O 设备可以并行工作，资源利用率很高。
缺点是实现复杂，需要专门的通道硬件支持。

### I/O 的层次结构

#### 用户层软件

实现与用户交互的接口。用户可以直接使用用户层软件提供的与 I/O 操作相关的库函数。

该层会实现假脱机技术（SPOOLing 技术）。"脱机" 是指脱离主机的控制进行 I/O 操作。
引入脱机技术，可以缓解 CPU 和 I/O 设备之间的速度不匹配问题，它先将慢速设备的数据穿缓冲到快速设备，然后由快速设备与 CPU 交互。
"假脱机" 不是硬件实现，一种软件实现：它将设备的输入数据先暂存到输入缓冲区（位于内存中）然后送到 "输入井"（位于磁盘中）；
输出是一个相反的过程，由 "输出井" 到输入缓冲区，再到输出设备。

假脱机技术的具体应用：共享打印机。
当多个用户进程提出输出打印的请求时，系统会答应它们的请求，但并不是真正把打印机分配给他们，假脱机管理进程会完成下面两件事：

1. 在磁盘输出井中为进程申请一个空闲缓冲区，并将要打印的数据送入其中；
2. 为用户进程申请一张空白的打印请求表，将用户的打印请求填入表中，将表挂到假脱机文件队列上。

#### 设备独立性软件

设备独立性软件又叫设备无关性软件。**与设备的硬件特性无关**的功能几乎都在这一层实现。

1. 向上层提供统一的调用接口（如 `read/write` 系统调用）
2. 设备的保护
3. 差错处理
4. 设备的分配与回收（I/O 调度算法）
5. 数据缓冲区管理（通过缓冲技术屏蔽设备之间的数据交换单位大小和传输速度的差异）
6. 建立逻辑设备名和物理设备名的映射关系，根据设备类型选择调用相应的驱动程序

#### 设备驱动程序

主要负责将上层发出的命令翻译为特定设备能理解的指令。包括设置设备寄存器、检查设备状态等。

#### 中断处理程序

I/O 任务完成后，I/O 控制器发送中断信号给 CPU（CPU 还是总线？），CPU 根据中断信号类型找到相应的中断处理程序。

#### 硬件

执行 I/O 操作。

---

[^cite_ref-1]: <https://hliangzhao.cn/articles/000001632804098b0d15f52e2794eba809f483763f603b1000>
[^cite_ref-2]: <https://draveness.me/system-design-scheduler>
[^cite_ref-3]: <https://www.zhihu.com/question/42962803/answer/120217624>

```{toctree}
:titlesonly:
:glob:
:hidden:

os/*
```