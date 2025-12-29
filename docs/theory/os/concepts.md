# 基本概念

## 堆和栈

- 堆的生长方向：从低地址向高地址增长
- 栈的生长方向：从高地址向低地址增长

程序的执行方向（由程序计数器(PC)决定）：从低地址向高地址执行

因此，我们可以画出下面的示意图：

```{figure} ../../_static/images/illustration-of-stack-and-heap.svg

```

## 内存映射

```{figure} ../../_static/images/uvmmapping.png

```

## 地址翻译

```{figure} ../../_static/images/address-translation.png

```

## 系统调用流程

:::{mermaid}
graph TB
    subgraph "用户态 (User Mode)"
        U1[用户线程正常执行]
        U2[用户代码任意位置]

        subgraph "系统调用/主动放弃CPU"
            U3[调用 sleep/exit 等<br>系统调用]
        end

        U1 --> U2
    end

    subgraph "Trampoline (跳板页)"
        T1[进入 trampoline<br>保存用户寄存器到 trapframe]
        T2[从 trapframe 恢复用户寄存器]
    end

    subgraph "内核态 (Kernel Mode)"
        subgraph "中断处理"
            K1[usertrap 函数<br>处理中断/异常/系统调用]
            K2[根据 r_scause 和 devintr <br>判断 trap 类型]
        end

        K7[系统调用<br>r_scause == 8<br>如 fork]
        K8[异常<br>r_scause == 15 or 13<br>如缺页异常]
        K9[中断<br>devintr == 2<br>如时间片到]

        subgraph "调度器"
            K3[yield 函数]
            K4[swtch 上下文切换<br>保存到当前线程的寄存器状态<br>恢复到目标线程的寄存器状态]
        end

        subgraph "返回路径"
            K6[usertrapret<br>准备返回用户态]
        end

        K1 --> K2
        K2 --> K9
        K3 --> K4
        K2 --> K7
        K2 --> K8
        K7 --> K3
        K8 --> K3
        K9 --> K3

        K4 -- "返回到 usertrap<br>通过 ra 跳转到目标线程" --> K6
    end

    U2 -- "中断/异常" --> T1
    U3 -- "ecall" --> T1
    T1 --> K1
    K6 --> T2
    T2 --> U1

    %% 样式定义
    classDef userStyle fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef trampolineStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef kernelStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef trapframeStyle fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef contextStyle fill:#ffebee,stroke:#c62828,stroke-width:2px

    class U1,U2,U3 userStyle
    class T1,T2 trampolineStyle
    class K1,K2,K3,K4,K5,K6 kernelStyle
:::
