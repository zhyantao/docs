# PIC 汇编示例

## 顺序程序结构

> 将20H单元低4位取出存入21H，高四位取出存入22H
> 要点：ANDLW和SWAPF

```asm
MOVF     20H,0      ;将20H单元的内容送人W
ANDLW    0FH        ;W高四位清零低4位保持不变
MOVWF    21H        ;将拆分后的低4位送21H
SWAPF    20H,0      ;将20H单元内容高、低半字节换位后送W

ANDLW    0FH        ;再将W高四位清0低四位保持不变
MOVWF    22H        ;将拆分后的高四位送22H单元
```

## 分支程序结构

> RAM中20H和21H单元存放2个数，找出大着存入22H单元
> 要点：两数做减法，判断标志位C的值

```asm
STATUS    EQU      03H      ;定义STATUS寄存器地址为03H
C         EQU      0        ;定义进位/借位标志C在STATUS中得地址为0
          MOVF     20H 0    ;将20H单元的内容送人W
          SUBWF    21H 0    ;用21H单元的内容减去W中的内容，结果存在W中
          BTFSS    STATUS,C ;若C=1，没借位，则21H单元中的数大，跳到F21BIG
          GOTO     F20BIG   ;若C=0，有借位，20H单元中得数较大，则跳至F20BIG
    
F21BIG    MOVF    21H,0     ;将21H中的内容存入W寄存器
          MOVWF   22H       ;再将它转存到22H单元
          GOTO    STOP      ;跳过下面两条指令到程序末尾
        
F20BIG    MOVF    20H,0     ;将20H中的内容存入W寄存器
          MOVWF   22H       ;再将它转存到22H单元

STOP      GOTO    STOP      ;任务完成，停机，原地踏步
```

## 循环程序结构

> 数据存储器中，从地址30H开始的50个单元全部写入00H
> 要点：间接寻址寄存器FSR当做地址指针

```asm
COUNT   EQU      20H        ;指定20H单元作为循坏次数计数器（即循环变量）
FSR     EQU      04H        ;定义FSR寄存器地址为04H
INDF    EQU      00H        ;设定INDF寄存器地址为00H
        MOVLW    D50        ;把计数器初值50送入W
        MOVWF    COUNT      ;再把50转入计数器（作为循环变量的操作值）
        MOVLW    30H        ;把30H（起始地址）送入W
        MOVWF    FSR        ;再把30H转入寄存器FSR(用作地址指针)
        
NEXT    CLRF     INDF       ;把以FSR内容为地址所指定的单元清0
        INCF     FSR,1      ;地址指针内容加1，指向下一单元
        DECFSZ   COUNT,1    ;计数值减1，结果为0就跳过到下一条指令到STOP处
        GOTO     NEXT       ;跳转回去并执行下一次循环
STOP    GOTO     STOP       ;循环结束之后执行该语句，实现停机
```

## 子程序结构

> 3个数最大者放入40H单元

```asm
STATUS    EQU        03H
C         EQU        00H
X         EQU        20H
Y         EQU        21H
Z         EQU        22H
```

## 主程序

```asm
MAIN    MOVF    30H,0
        MOVWF   X
        MOVF    21H,0
        MOVWF   Y
        CALL    SUB
        MOVF    Z,0
        MOVWF   X
        MOVF    32H,0
        MOVWF   Y
        CALL    SUB
        MOVF    Z,0
        MOVWF   40H
STOP    GOTO    STOP
```

## 子程序

> 子程序:(入口参数：X和Y，出口参数：Z)

```asm
SUB     MOVF     X,0        ;将X内容送人W
        SUBWF    Y,0        ;Y内容减去W内容，结果存入W
        BTFSS    STATUS,C   ;若C=1，没有发生借位，执行下一条，否则跳转
        GOTO     X_BIG        
        
Y_BIG   MOVF    Y,0         ;将Y中的数据送入W
        MOVWF    Z          ;再将它转存到Z
        GOTO     THEEND     ;跳过下面两条到末尾
        
X_BIG   MOVF    X,0         ;将X中的数据送入W
        MOVWF    Z          ;再将它转存到Z
THEEND  RETURN              ;子程序返回
```
