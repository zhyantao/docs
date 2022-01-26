# PIC16F877XA

## 宏观理解

![asm-advanced.png](https://upload-images.jianshu.io/upload_images/13518408-8ceb9117f53b2461.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 核心助记符

| 助记符 | 功能说明 | 英文全称 |
|-------|--------|----------|
|ADD | 相加|add|
|SUB | 相减|substract|
|RL | 循环左移 |rotate left|
|RR | 循环右移 |rotate right|
|AND | 与| and |
|IOR | 或| inclusive or|
|XOR | 异或|exclusive or|
|COM | 取反|complement|
|INC | 加1|increase|
|DEC | 减1|decrease|
|MOV | 传送|move|
|CLR | 清零|clear
|RET | 返回|return|
|BTF | 位测试|bit test|

## 指令系统补充字符说明

| 字符 | 功能说明 | 英文全称 |
|-------| -------------------|------------|
|W|工作寄存器（即累加器）|-|
|f|寄存器地址（取7位寄存器地址,00H~7FH）|-|
|b|8位寄存器f内位地址（0~7）|bit|
|K|立即数（8位常数或11位地址）、常量或标号|-|
|L|指令操作数中含有8位立即数K|-|
|d|目标地址选择：d=0,结果至W;d=1,结果至f|destination|
|FSZ|寄存器f为0,则间跳|skip if 0|
|FSC|寄存器f的b位为0,则间跳|skip if clear|
|FSS|寄存器f的b位为1,则间跳|skip if set|
|( )|表示寄存器的内容|-|
|(( ))|表示寄存器间接寻址的内容|-|
|→|表示运算结果送入目标寄存器|-|

## 常用指令实例

### 寄存器加1指令：INCF

【格式】 INCF    F,d

【功能】寄存器F加1

【说明】

（1）INCF是Increment F的缩写;

（2）在PIC系列8位单片机中,常用符号F代表片内的各种寄存器和F的序号地址;

（3）d＝0时,结果存入W;d＝1时,结果存入F。

【实例】

```asm
INCF    PORTC,1    ;将PORTC加1
```

### 寄存器减1指令：DECF

【格式】 DECF    F,d

【功能】寄存器F减1

【说明】

（1）DECF是Decrement F的缩写;

（2）d＝0时,结果存入W;d＝1时,结果存入F。

【实例】

```asm
ENCODER     EQU 0X21

            ...
            
            DECF     ENCODER,1 ;将ENCODER减1
```

### 寄存器清零指令：CLRF

【格式】 CLRF    F

【功能】寄存器清零

【说明】

（1）CLRF是Clear F的缩写;

（2）F寄存器被清为全0,使状态位Z＝1。

【实例】

```asm
CLRF    TRISC       ;对TRISC 清零
```

### W清零指令：CLRW

【格式】 CLRW

【功能】寄存器W清零

【说明】

（1）CLRW是Clear W的缩写;

（2）W为PIC单片机的工作寄存器;

（3）W寄存器被清为全0,使状态位Z＝1。

【实例】

```asm
CLRW        ;W＝00H
```

### F寄存器传送指令：MOVF

【格式】 MOVF    F,d

【功能】将F寄存器内容传送到F或W

【说明】

（1）MOVF是Move F的缩写;

（2）当d＝1时,传到F本身;当d＝0时,传到W;

（3）影响状态位Z

【实例】

```asm
MOVF       PORTB,0    ;PORTB口内容送W

MOVWF      PORTA      ;W内容即PORTB口内容送PORTA
```

### W寄存器传送指令：MOVWF

【格式】 MOVWF       F

【功能】 W寄存器传送

【说明】

（1）MOVWF是Move W to F的缩写;

（2）将W寄存器内容传到F,W内容不变;

（3）不影响状态位。

【实例】

```asm
MOVLW   0x0B        ;送0BH送W

MOVWF   PORTB       ;送W内容到PORTB口
```

### 递增跳转指令：INCFSZ

【格式】 INCFSZ     F,d

【功能】 递增跳转

【说明】

（1）INCFSZ是Increment F,Skip if 0的缩写;

（2）F寄存器内容加1后,当d＝1时结果存入F,当d＝0时存入W;

（3）若结果为0则跳过下一条指令,否则顺序执行;

（4）影响状态位Z。

【实例】

```asm
LOOP   INCFSZ     COUNT1,1   ;COUNT1加1,结果存到COUNT1

       GOTO       LOOP       ;结果不为零,循环

       MOVWF      COUNT2     ;结果为零时,执行该语句
```

### 递减跳转指令：DECFSZ

【格式】 DECFSZ      F,d

【功能】递减跳转

【说明】

（1）DECFSZ是Decrement F,Skip if 0的缩写;

（2）F寄存器内容减1,结果存入F本身（d＝1）或W（d＝0）;

（3）如果结果为0则跳过下一条指令,否则顺序执行;

（4）影响状态位Z;

（5）实际指令中,当d=1时,该项常常被略去。

【实例】

```asm
DELAY   MOVLW    25          ;延时子程序

        MOVWF    N           ;给N赋值25

        LOOP     DECFSZ N,1  ;N-1送回N并判结果＝0？是！跳出循环

        GOTO     LOOP        ;否！循环回去

        RETURN               ;返回
```

### 位清零指令：BCF

【格式】 BCF     F,B

【功能】位清0

【说明】

（1）BCF是Bit Clear F的缩写;

（2）符号B是表示片内某个8位数据寄存器F的位号(或位地址);

（3）指令的意思是：将寄存器的第B位清0。

【实例】

```asm
BCF     REG1,2     ;把寄存器REG1的第2位清零
```

### 位置1指令：BSF

【格式】 BSF     F,B

【功能】位置1

【说明】（1）BSF是Bit Set F的缩写;

（2）将寄存器F的第B位置1。

【实例】

```asm
BSF     STATUS,RP0      ;设置文件寄存器的体1
```

### 位测试为零跳转指令：BTFSC

【格式】 BTFSC   F,B

【功能】位测试为0跳转

【说明】

（1）BTFSC是Bit Test,Skip if Clear的缩写;

（2）测试F寄存器的第B位,若F（B）＝0则调到下一条指令,否则顺序执行。

【实例】

```asm
BTFSC       PORTB,0    ;检测PORTB口中的第0位是否为0？是！跳过下一条指令

GOTO       CHECK       ;否！则转到标号为CHECK的语句

CALL       DELAY       ;PORTB的第0位是1则直接执行该语句,调用延时子程序
```

### 位测试为1跳转指令：BTFSS

【格式】 BTFSS       F,B

【功能】位测试位1跳转指令

【说明】

（1）BTFSS是Bit Test F,Skip if Set的缩写;

（2）测试F寄存器的第B位,若F（B）＝1,则跳转到下一条指令,否则顺序执行。

【实例】

```asm
BTFSS       PORTB,0     ;检测PORTB口中的第0位是否为1？是！跳过下一条指令

GOTO        CHECK       ;否！则转到标号为CHECK的语句

CALL        DELAY       ;PORTB的第0位是1则直接执行该句,调用延时子程序
```

### 常数传送指令：MOVLW

【格式】 MOVLW       K

【功能】常数传送

【说明】（1）MOVLW是Move literal to W的缩写;

（2）将8位立即数传送到W寄存器,k表示常数、立即数和标号;

（3）不影响状态位

【实例】

```asm
MOVLW       0x1E    ;常数30送W
```

### 子程序调用指令：CALL

【格式】 CALL    K

【功能】子程序调用

【说明】

（1）CALL是CALL subroutine的缩写;

（2）K为立即地址;

（3）不影响状态位。

【实例】

```asm
CALL    DELAY         ;调用延时子程序

DELAY   ...           ;延时子程序DELAY

        ...

        RETURN
```

### 无条件跳转指令：GOTO

【格式】 GOTO    K

【功能】无条件跳转

【说明】

（1）GOTO是Go to address的缩写;

（2）指令中的K,常与程序中的标号联系起来;

（3）不影响状态位。

【实例】

```asm
STOP    GOTO    STOP    ;循环执行GOTO语句,从而停机
```

### 子程序返回指令：RETURN

【格式】 RETURN

【功能】子程序返回

【说明】

（1）RETURN是Return from Subroutine的缩写;

（2）将堆栈顶端单元内容弹出并送入PC,从而返回主程序断点处;

（3）不影响状态位。

【实例】

```asm
SUB  MOVLW   01H     ;子程序

     ...

     RETURN          ;子程序返回
```

### 空操作指令：NOP

【格式】 NOP

【功能】空操作

【说明】

（1）NOP是No Operation的缩写;

（2）不产生任何操作,仅使PC加1,消耗一个指令周期NOP;

（3）不影响状态位。

【实例】

```asm
MOVLW       0xOF        ;送OFH到W
        
MOVWF       PORTB       ;W内容写入B口
         
NOP                      ;空操作

MOVF        PORTB,W     ;读操作
```

## 常用伪指令实例

### 符号名赋值伪指令：EQU

【格式】符号名 EQU nn

【功能】符号名赋值

【说明】

（1）给符号名或寄存器赋值,符号名一旦由EQU赋值,其值就不能再重新定义;

（2）nn是一个长度不同的二进制数值。

【实例】

```asm
COUNT       EQU     100     ;定义COUNT为常数100
```

### 程序起始地址伪指令：ORG

【格式】 ORG nnnn

【功能】程序起始地址

【说明】

（1）用于指定该伪指令后面的源程序存放的起始地址,也就是汇编后的机器码目标程序在单片机的程序存贮器中开始存放的首地址;

（2）nnnn是一个13为长的地址参数。

【实例】

```asm
ORG 0x00     ;程序汇编地址从00H开始
```

### 程序结束伪指令：END

【格式】 END

【功能】程序结束

【说明】

（1）指令末的伪指令END是通知汇编程序MPASM结束对源程序的汇编,即使后面还有语句,也不再予以汇编;

（2）在一个源程序中必须有END伪指令;

（3）只能有一个END;

（4）放在整个程序的最后。

【实例】直接在程序末尾使用,从而结束程序

### 调入外部函数伪指令：INCLUDE

【格式】 INCLUDE "文件名"

【功能】调入外部函数

【说明】

（1）用来告诉汇编器,将一个预先编好的外部程序文件包含进来,作为本源程序的一部分;

（2）这样可以减少重复劳动,提高编程效率。

## 参考文献

1. <http://technology.niagarac.on.ca/staff/mboldin/18F_Instruction_Set/>
2. <http://ww1.microchip.com/downloads/en/DeviceDoc/39582C.pdf>
