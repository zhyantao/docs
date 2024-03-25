# 汇编指令表

注：MIT6.828 使用的是 AT&T 语法。AT&T 语法始终将 `src` 放在左侧，`dest` 放在右侧。

在汇编指令中，我们注意到 `mov` 指令不仅有 `mov`，还有 `movb`、`movw`、`movl`、`movq`。
那么它们有什么区别呢？这里的后缀 `b`、`w`、`l`、`q` 是 AT&T 语法中的限定词：

- `q`：四字（8 个字节，64 位）
- `l`：双字（4 个字节，32 位）
- `w`：单字（2 个字节，16 位）
- `b`：单字节（1 个字节，8 位）

特殊情况：`ljmp` 中的 `l` 不是后缀，而是前缀，但大概意思没有变，因此这种略微的差异并不影响我们阅读代码。
`ljmp` 表示能够跳转到比 `jmp` 更远的地方，而且为了存储 `ljmp` 需要占用的内存空间更大。

记住一些约定，对我们理解汇编源代码有一定的好处 [^cite_ref-5]：

- 在 AT&T 语法中，前缀 `%` 后紧接寄存器名，前缀 `$` 后是立即数；
- 在 Intel 语法下，寄存器名和立即数前都没有前缀；
- AT&T 中的内存寻址采用的是 `()`，Intel 内存寻址使用的是 `[]`。

但情况也有例外，比如 `out %ax,$0x64` 是一个输出语句，这里的 `$0x64`
就不能看作一个立即数了，它表示一个端口，因此这句话的意思是将 `ax` 寄存器中的内容输出到
`0x64` 对应的设备中。

(assembly_instructions)=

## 传送指令

```{list-table}
:header-rows: 1
:widths: 25, 50, 25

* - 汇编指令
  - 控制 CPU 完成的操作
  - 备注
* - `mov 18,%ax`
  - 将 18 送入寄存器 `%ax`
  - `ax = 18`
* - `push %ax`
  - 将寄存器 `%ax` 中的数压入 `%sp` 寄存器
  - 函数调用
* - `pop %ax`
  - 将 `%sp` 寄存器中的值弹出，存入 `%ax` 寄存器
  - 函数返回
* - `lea 0x1(%ecx),%edx`
  - 将 `%ecx` 中的值自增 1 存入 `%edx` 寄存器 [^cite_ref-3]
  - 载入有效地址
```

## 转移指令

```{list-table}
:header-rows: 1
:widths: 30, 45, 25

* - 汇编指令
  - 控制 CPU 完成的操作
  - 备注
* - `call *%ebx`
  - 执行 `%ebx` 指向的函数
  - 函数调用
* - `jmp 0x90cd`
  - 执行 `0x90cd` 处的指令
  - 无条件跳转
* - `je 0x90cd`
  - 执行 `0x90cd` 处的指令
  - 标志位 `ZF=1` 时跳转
* - `jne 0x90cd`
  - 执行 `0x90cd` 处的指令
  - 标志位 `ZF=0` 时跳转
* - `jb 0x90cd`
  - 执行 `0x90cd` 处的指令
  - 如果小于则跳转
* - `jnb 0x90cd`
  - 执行 `0x90cd` 处的指令
  - 如果不小于则跳转
* - `ja 0x90cd`
  - 执行 `0x90cd` 处的指令
  - 如果大于则跳转
* - `jna 0x90cd`
  - 执行 `0x90cd` 处的指令
  - 如果不大于则跳转
```

## 运算指令

```{list-table}
:header-rows: 1
:widths: 20, 55, 25

* - 汇编指令
  - 控制 CPU 完成的操作
  - 备注
* - `add %ax,%bx`
  - 将 `%ax` 和 `%bx` 中的数值相加，结果存入 `%bx`
  - `bx = ax + bx`
* - `sub $0x2c,%esp`
  - 将 `%esp` 与 `0x2c` 的差存入 `%esp`
  - `esp = esp - 0x2c`
* - `mul 0x16`
  - 将累加器 `ax` 或 `al` 中的数字乘以 `0x16`，存入 `ax`
  - `ax = ax * 0x16`
* - `div 0x16`
  - 将 `dx` 或 `ax` 中的数除以 `0x16`，存入 `ax` 或 `dx`
  - `ax = ax / 0x16`
* - `adc %ax,%bx`
  - 将 `%ax` 和 `%bx` 中的数值相加，结果存入 `%bx`
  - 带进位相加
* - `sbb $0x2c,%esp`
  - 将 `%esp` 与 `0x2c` 的差存入 `%esp`
  - 带借位相减
* - `cmp 0x2f,%ax`
  - 比较立即数 `0x2f` 和寄存器 `%ax` 中的值
  - 设置标志位 `ZF`
* - `or 0x11,%ax`
  - 将 `%ax` 寄存器的位 0 和位 4 置 1
  - 开启位 `i`，求余数
* - `and 0xFFFD,%al`
  - 将 `%al` 寄存器的位 1 和置 0
  - 关闭位 `i`
* - `xor %dx,%dx`
  - 将寄存器 `%dx` 清零
  - 求反位 `i`，求补码
* - `test $0x1,%al`
  - 测试 `%al` 寄存器的位 0 是否置 1
  - `0x1 & %al`
* - `repnz ...`
  - 如果 `ZF=0` 则重复执行串操作 `...`
  - `while()`
```

## 控制指令

```{note}
串操作的含义就是连续的一串相同的操作，通常作用在连续的内存上。
比如把一串字符串常量送入到某个连续地址处，此时如果采用串操作的话，每传一个字节的数据，
串操作可以自动的把源操作数和目的操作数的地址加或减 1。
那么下一个操作就直接作用在下一个空间了 [^cite_ref-4]。
```

```{list-table}
:header-rows: 1
:widths: 20, 55, 25

* - 汇编指令
  - 控制 CPU 完成的操作
  - 备注
* - `nop`
  - 白白消耗 CPU 的时钟周期，什么都不干
  - 延时操作
* - `cli`
  - 关中断指令
  - 保证操作的原子性
* - `cld`
  - 方向标志位清零：`DF=0`，方向标志位决定了地址指针的生长方向
  - `es:di` 递增或递减
* - `out %ax,$0x70`
  - 把 `%ax` 的值写入端口 `$0x70` 连接的外部设备 [^cite_ref-1] 中
  - CPU 与外部设备通信
* - `in $0x71,%ax`
  - 把端口 `$0x71` 连接的外部设备 [^cite_ref-1] 中的值写入 `%ax`
  - CPU 与外部设备通信
* - `lidtw %cs:%ip`
  - 将从 `%cs:%ip` 开始的 6 个字节读入中断向量表中 [^cite_ref-2]
  - 进程间切换
* - `lgdtw %cs:%ip`
  - 将从 `%cs:%ip` 开始的 6 个字节读入全局描述符表中
  - 保护模式下的隔离措施
```

---

以上是常用的汇编指令，如果想要查看更多详细的介绍，可以参考
*[PC 汇编语言](https://kdocs.cn/l/cq5FqOlocImF)* 的 *附录A 80x86 指令*。

---

[^cite_ref-1]: <https://bochs.sourceforge.io/techspec/PORTS.LST>
[^cite_ref-2]: <http://wiki.osdev.org/Interrupt_Descriptor_Table>
[^cite_ref-3]: <http://adam8157.info/blog/2011/01/interesting-opcode-lea>
[^cite_ref-4]: <https://www.cnblogs.com/fatsheep9146/p/5115086.html>
[^cite_ref-5]: <https://binhack.readthedocs.io/zh/latest/assembly/diff.html>
