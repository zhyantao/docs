# perf

perf 是一个事件驱动的性能采集工具，本文是 <https://www.brendangregg.com/perf.html> 的摘抄版本。

- <https://jvns.ca/perf-cheat-sheet.pdf>
- <https://www.linuxtrainingacademy.com/linux-commands-cheat-sheet/>

## 事件类型

```bash
# 列出当前所有已知的事件
perf list

# 列出调度相关的 tracepoints
perf list 'sched:*'
```

## 计数事件

```bash
# 对指定命令进行 CPU 计数器统计
perf stat command

# 对指定命令进行详细的 CPU 计数器统计（包括额外信息）
perf stat -d command

# 对指定 PID 进行 CPU 计数器统计，直到按下 Ctrl-C
perf stat -p PID

# 对整个系统进行 CPU 计数器统计，持续 5 秒钟
perf stat -a sleep 5

# 对整个系统进行多种基本 CPU 统计，持续 10 秒钟
perf stat -e cycles,instructions,cache-references,cache-misses,bus-cycles -a sleep 10

# 对指定命令进行 CPU 一级数据缓存统计
perf stat -e L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores command

# 对指定命令进行 CPU 数据 TLB 统计
perf stat -e dTLB-loads,dTLB-load-misses,dTLB-prefetch-misses command

# 对指定命令进行 CPU 最后一级缓存统计
perf stat -e LLC-loads,LLC-load-misses,LLC-stores,LLC-prefetches command

# 使用原始 PMC 计数器，例如统计未停止的核心周期数
perf stat -e r003c -a sleep 5

# 使用 PMC 计数器，通过原始定义统计周期和前端停顿
perf stat -e cycles -e cpu/event=0x0e,umask=0x01,inv,cmask=0x01/ -a sleep 5

# 统计整个系统的每秒系统调用数
perf stat -e raw_syscalls:sys_enter -I 1000 -a

# 按类型统计指定 PID 的系统调用数，直到按下 Ctrl-C
perf stat -e 'syscalls:sys_enter_*' -p PID

# 按类型统计整个系统的系统调用数，持续 5 秒钟
perf stat -e 'syscalls:sys_enter_*' -a sleep 5

# 统计指定 PID 的调度事件数，直到按下 Ctrl-C
perf stat -e 'sched:*' -p PID

# 统计指定 PID 的调度事件数，持续 10 秒钟
perf stat -e 'sched:*' -p PID sleep 10

# 统计整个系统的 ext4 事件数，持续 10 秒钟
perf stat -e 'ext4:*' -a sleep 10

# 统计整个系统的块设备 I/O 事件数，持续 10 秒钟
perf stat -e 'block:*' -a sleep 10

# 统计所有的 vmscan 事件，每秒打印一次报告
perf stat -e 'vmscan:*' -a -I 1000
```

## 性能采样

```bash
# 对指定命令的 CPU 上运行的函数进行采样，频率为 99 赫兹
perf record -F 99 command

# 对指定 PID 的 CPU 上运行的函数进行采样，频率为 99 赫兹，直到按下 Ctrl-C
perf record -F 99 -p PID

# 对指定 PID 的 CPU 上运行的函数进行采样，频率为 99 赫兹，持续 10 秒钟
perf record -F 99 -p PID sleep 10

# 对指定 PID 的 CPU 堆栈跟踪进行采样（通过帧指针），频率为 99 赫兹，持续 10 秒钟
perf record -F 99 -p PID -g -- sleep 10

# 对指定 PID 的 CPU 堆栈跟踪进行采样，使用 dwarf（调试信息）展开堆栈，频率为 99 赫兹，持续 10 秒钟
perf record -F 99 -p PID --call-graph dwarf sleep 10

# 对整个系统的 CPU 堆栈跟踪进行采样，频率为 99 赫兹，持续 10 秒钟（Linux 版本低于 4.11）
perf record -F 99 -ag -- sleep 10

# 对整个系统的 CPU 堆栈跟踪进行采样，频率为 99 赫兹，持续 10 秒钟（Linux 版本大于等于 4.11）
perf record -F 99 -g -- sleep 10

# 如果上一条命令不起作用，请尝试强制 perf 使用 cpu-clock 事件
perf record -F 99 -e cpu-clock -ag -- sleep 10

# 对由 /sys/fs/cgroup/perf_event cgroup 标识的容器进行 CPU 堆栈跟踪采样
perf record -F 99 -e cpu-clock --cgroup=docker/1d567f4393190204...etc... -a -- sleep 10

# 对整个系统的 CPU 堆栈跟踪进行采样，使用 dwarf 展开堆栈，频率为 99 赫兹，持续 10 秒钟
perf record -F 99 -a --call-graph dwarf sleep 10

# 对整个系统的 CPU 堆栈跟踪进行采样，使用最后分支记录（LBR）来获取堆栈，持续 10 秒钟（Linux 版本大于等于 4.?）
perf record -F 99 -a --call-graph lbr sleep 10

# 对 CPU 堆栈跟踪进行采样，每次触发 10,000 次一级数据缓存未命中时采样一次，持续 5 秒钟
perf record -e L1-dcache-load-misses -c 10000 -ag -- sleep 5

# 对 CPU 堆栈跟踪进行采样，每次触发 100 次最后一级缓存未命中时采样一次，持续 5 秒钟
perf record -e LLC-load-misses -c 100 -ag -- sleep 5

# 对内核指令进行 CPU 采样，持续 5 秒钟
perf record -e cycles:k -a -- sleep 5

# 对用户空间指令进行 CPU 采样，持续 5 秒钟
perf record -e cycles:u -a -- sleep 5

# 精确地对用户空间指令进行 CPU 采样（使用 PEBS），持续 5 秒钟
perf record -e cycles:up -a -- sleep 5

# 执行分支追踪（需要硬件支持），持续 1 秒钟
perf record -b -a sleep 1

# 以 49 赫兹频率采样 CPU，并实时显示顶部地址和符号（不生成 perf.data 文件）
perf top -F 49

# 以 49 赫兹频率采样 CPU，并实时显示进程名称和模块信息
perf top -F 49 -ns comm,dso
```

## 静态追踪

```bash
# 追踪新创建的进程，直到按下 Ctrl-C
perf record -e sched:sched_process_exec -a

# 采样（取子集）上下文切换，直到按下 Ctrl-C
perf record -e context-switches -a

# 追踪所有上下文切换，直到按下 Ctrl-C
perf record -e context-switches -c 1 -a

# 显示使用的原始设置（参见man perf_event_open）
perf record -vv -e context-switches -a

# 通过 sched tracepoint 追踪所有上下文切换，直到按下 Ctrl-C
perf record -e sched:sched_switch -a

# 采样上下文切换并包含堆栈跟踪，直到按下 Ctrl-C
perf record -e context-switches -ag

# 采样上下文切换并包含堆栈跟踪，持续 10 秒钟
perf record -e context-switches -ag -- sleep 10

# 采样上下文切换、堆栈跟踪，并显示时间戳（Linux 3.17 及更早版本，-T 已默认启用）
perf record -e context-switches -ag -T

# 采样 CPU 迁移事件，持续 10 秒钟
perf record -e migrations -a -- sleep 10

# 追踪带有堆栈跟踪的所有 connect() 调用（即传出连接），直到按下 Ctrl-C
perf record -e syscalls:sys_enter_connect -ag

# 追踪带有堆栈跟踪的所有 accept() 调用（即传入连接），直到按下 Ctrl-C
perf record -e syscalls:sys_enter_accept* -ag

# 追踪带有堆栈跟踪的所有块设备（磁盘 I/O）请求，直到按下 Ctrl-C
perf record -e block:block_rq_insert -ag

# 每秒最多采样 100 个块设备请求，直到按下 Ctrl-C
perf record -F 100 -e block:block_rq_insert -a

# 追踪所有块设备请求的插入、发出和完成事件（包含时间戳），直到按下 Ctrl-C
perf record -e block:block_rq_issue -e block:block_rq_complete -a

# 追踪所有块设备完成事件，且大小至少为 100 KB，直到按下 Ctrl-C
perf record -e block:block_rq_complete --filter 'nr_sector > 200'

# 追踪所有块设备完成事件中的同步写操作，直到按下 Ctrl-C
perf record -e block:block_rq_complete --filter 'rwbs == "WS"'

# 追踪所有块设备完成事件中的各种写操作，直到按下 Ctrl-C
perf record -e block:block_rq_complete --filter 'rwbs ~ "*W*"'

# 采样次要缺页异常（RSS 增长）并包含堆栈跟踪，直到按下 Ctrl-C
perf record -e minor-faults -ag

# 追踪所有次要缺页异常并包含堆栈跟踪，直到按下 Ctrl-C
perf record -e minor-faults -c 1 -ag

# 采样缺页异常并包含堆栈跟踪，直到按下 Ctrl-C
perf record -e page-faults -ag

# 追踪所有 ext4 调用，并将结果写入非 ext4 文件系统上的文件，直到按下 Ctrl-C
perf record -e 'ext4:*' -o /tmp/perf.data -a

# 追踪 kswapd 唤醒事件，直到按下 Ctrl-C
perf record -e vmscan:mm_vmscan_wakeup_kswapd -ag

# 添加 Node.js USDT 探针（适用于 Linux 4.10+）
perf buildid-cache --add `which node`

# 追踪 node http__server__request USDT 事件（适用于 Linux 4.10+）
perf record -e sdt_node:http__server__request -a
```

## 动态追踪

```bash
# 添加一个用于追踪内核 tcp_sendmsg() 函数入口的 tracepoint（“--add” 是可选的）
perf probe --add tcp_sendmsg

# 删除 tcp_sendmsg() 的 tracepoint（或使用 “--del”）
perf probe -d tcp_sendmsg

# 添加一个用于追踪内核 tcp_sendmsg() 函数返回的 tracepoint
perf probe 'tcp_sendmsg%return'

# 显示内核 tcp_sendmsg() 函数可用的变量（需要 debuginfo）
perf probe -V tcp_sendmsg

# 显示内核 tcp_sendmsg() 函数可用的变量以及外部变量（需要 debuginfo）
perf probe -V tcp_sendmsg --externs

# 显示 tcp_sendmsg() 的可用行号探测点（需要 debuginfo）
perf probe -L tcp_sendmsg

# 显示 tcp_sendmsg() 在第 81 行可用的变量（需要 debuginfo）
perf probe -V tcp_sendmsg:81

# 添加一个用于追踪 tcp_sendmsg() 的 tracepoint，并记录三个寄存器参数（平台相关）
perf probe 'tcp_sendmsg %ax %dx %cx'

# 添加一个用于追踪 tcp_sendmsg() 的 tracepoint，并为 %cx 寄存器起别名（平台相关）
perf probe 'tcp_sendmsg bytes=%cx'

# 当 bytes（别名）变量大于 100 时，追踪之前创建的 probe
perf record -e probe:tcp_sendmsg --filter 'bytes > 100'

# 添加一个用于追踪 tcp_sendmsg() 返回值的 tracepoint，并捕获返回值
perf probe 'tcp_sendmsg%return $retval'

# 添加一个用于追踪 tcp_sendmsg() 入口参数的 tracepoint，并捕获 size 参数（可靠方式，但需要 debuginfo）
perf probe 'tcp_sendmsg size'

# 添加一个用于追踪 tcp_sendmsg() 入口参数的 tracepoint，并捕获 size 和 socket 状态（需要 debuginfo）
perf probe 'tcp_sendmsg size sk->__sk_common.skc_state'

# 显示如何执行上述操作，但不实际执行（需要 debuginfo）
perf probe -nv 'tcp_sendmsg size sk->__sk_common.skc_state'

# 当 size 不为零且状态不是 TCP_ESTABLISHED（状态码 1）时，追踪之前的 probe（需要 debuginfo）
perf record -e probe:tcp_sendmsg --filter 'size > 0 && skc_state != 1' -a

# 添加一个用于追踪 tcp_sendmsg() 第 81 行的 tracepoint，并捕获局部变量 seglen（需要 debuginfo）
perf probe 'tcp_sendmsg:81 seglen'

# 添加一个用于追踪 do_sys_open() 的 tracepoint，并捕获文件名为字符串（需要 debuginfo）
perf probe 'do_sys_open filename:string'

# 添加一个用于追踪 myfunc() 返回值的 tracepoint，并捕获返回值作为字符串
perf probe 'myfunc%return +0($retval):string'

# 添加一个用于追踪用户空间 malloc() 函数的 tracepoint（来自 libc）
perf probe -x /lib64/libc.so.6 malloc

# 添加一个用于追踪用户空间静态探针（USDT，也称为 SDT 事件）的 tracepoint
perf probe -x /usr/lib64/libpthread-2.24.so %sdt_libpthread:mutex_entry

# 列出当前可用的动态探针
perf probe -l
```

## 混合

```bash
# 按进程追踪系统调用，每 2 秒刷新一次摘要
perf top -e raw_syscalls:sys_enter -ns comm

# 按正在运行的 CPU 进程追踪发送的网络包，输出实时滚动（不清屏）
stdbuf -oL perf top -e net:net_dev_xmit -ns comm | strings

# 以 99 赫兹频率采样堆栈信息，并同时采样上下文切换事件
perf record -F99 -e cpu-clock -e cs -a -g

# 限制堆栈深度CPU 堆栈最多 2 层，上下文切换堆栈最多 5 层（需要 Linux 4.8 及以上版本）
perf record -F99 -e cpu-clock/max-stack=2/ -e cs/max-stack=5/ -a -g
```

## 特殊功能

```bash
# 记录缓存行争用事件（适用于 Linux 4.10+）
perf c2c record -a -- sleep 10

# 根据之前的记录生成缓存行事件报告（适用于 Linux 4.10+）
perf c2c report
```

## 生成报告

```bash
# 在支持的情况下使用 ncurses 界面（TUI）浏览 perf.data 文件
perf report

# 显示 perf.data 报告，并包含样本计数列
perf report -n

# 将 perf.data 以文本形式输出，合并数据并显示百分比
perf report --stdio

# 输出报告，并将堆栈折叠为单行格式每一行为一个堆栈（需要 Linux 4.4 及以上版本）
perf report --stdio -n -g folded

# 列出 perf.data 中的所有事件
perf script

# 列出 perf.data 中的所有事件，并包含数据头信息（适用于较新内核；旧版本默认包含）
perf script --header

# 列出 perf.data 中的所有事件，并自定义字段输出（适用于 Linux 4.1 以下版本）
perf script -f time,event,trace

# 列出 perf.data 中的所有事件，并自定义字段输出（适用于 Linux 4.1 及以上版本）
perf script -F time,event,trace

# 推荐字段组合列出 perf.data 事件（需配合 perf record -a 使用，适用于较新内核）
perf script --header -F comm,pid,tid,cpu,time,event,ip,sym,dso

# 推荐字段组合列出 perf.data 事件（需配合 perf record -a 使用，适用于旧内核）
perf script -f comm,pid,tid,cpu,time,event,ip,sym,dso

# 将 perf.data 的原始内容以十六进制形式转储（用于调试）
perf script -D

# 反汇编代码并标注指令执行比例（需要部分调试信息）
perf annotate --stdio
```
