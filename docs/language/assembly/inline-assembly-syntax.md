# 内联汇编语法

(inline_assembly_syntax)=

## 基本介绍

**内联汇编** 是指在高级语言（如 C 语言）中混入汇编语法。本文以
[Brennan's Guide to Inline Assembly](http://www.delorie.com/djgpp/doc/brennan/brennan_att_inline_djgpp.html)
为基础，进行相关整理，方便后续查阅。

不同的编译器支持的汇编语法会有所差异，比如 NASM 支持 Intel 风格，而 GAS 支持 AT&T 风格。
由于 MIT6.828 项目需要，我们重点学习 AT&T 风格的语法，并与另一种风格进行相关对比。

书写 AT&T 风格的汇编语言，可以使用的编译器是 DJGPP（基于 GCC 开发）。

## AT&T 和 Intel 风格对比

### 寄存器的命名方式

以 `%` 开头来标识寄存器 `eax`。

AT&T：`%eax`

Intel：`eax`

### src/dest 的书写顺序

AT&T 语法始终将 `src` 放在左侧，`dest` 放在右侧。

将 `eax` 寄存器中的值赋值给 `ebx`。

AT&T：`movl %eax, %ebx`

Intel：`mov ebx, eax`

### 常量值/立即数的格式

常量或立即数必须以 `$` 开头。

将 C 语言中的 `static` 变量 `booga` 的内存地址赋值给 `eax` 寄存器。

AT&T：`movl $_booga, %eax`

Intel：`mov eax, _booga`

将 `0xd00d` 赋值给 `eax` 寄存器。

AT&T：`movl $0xd00d, %ebx`

Intel：`mov ebx, d00dh`

### 指定操作数据的大小

使用前缀 `b`、`w` 或 `l` 来指定目标寄存器的宽度是 `byte`、`word` 还是 `longword`。
如果你省略了前缀 GAS（GNU Assembler）会去猜需要多大的存储空间，这种不可控的局面可能会导致错误发生。

AT&T：`movw %ax, %bx`

Intel：`mov bx, ax`

### 汇编寻址方式汇总

DJGPP 使用 386 保护模式，所以你不用在乎实模式下寻址方式（哪个寄存器中保存了哪个默认段，哪个是基地址寄存器，哪个是指针寄存器）。
因此，我们只考虑 6 个通用寄存器（如果算上 `ebp` 那就是 7 个，但是如果要使用这个寄存器的时候，记得手动恢复，或者编译时带上
`-fomit-frame-pointer` 这个参数）

AT&T：`immed32(basepointer, indexpointer, indexscale)`

Intel：`[basepointer + indexpointer * indexscale + immed32]`

使用段地址和偏移地址计算物理地址的方式如下：

`immed32 + basepointer + indexpointer * indexscale`

你可能用不到上面全部的参数，但是必须包含 `immed32` 和 `basepointer` 的其中一个。
并且，你必须把 size 后缀添加到操作符上。

寻址一个指定的 C 变量：

AT&T：`_booga`

Intel：`[_booga]`

通过使用下划线可以拿到一个 `static` (global) C 变量。
*这种取数据的方式仅对全局变量起作用。*
另外，你可以使用扩展的 asm 语法把需要用到的变量预加载到寄存器中，下面将介绍这种方式。

直接以寄存器中的值作为目标地址，进行寻址：

AT&T：`(%eax)`

Intel：`[eax]`

以变量名的地址作为基地址，寄存器中的值作为偏移地址，进行寻址：

AT&T：`_variable(%eax)`

Intel：`[eax + _variable]`

以数组名作为基地址，寄存器中的值作为偏移地址，步长指定为 4 字节，进行寻址：（**冲突**）

AT&T：`_array(, %eax, 4)`

Intel：`[eax * 4 + array]`

以 `eax` 中的值作为基地址，立即数作为偏移地址，进行寻址：

C code：`*(p+1)` where `p` is a `char *`

AT&T：`1(%eax)` where `eax` has the value of `p`

Intel：`[eax + 1]`

也可以在立即数进行一些简单的数学运算：

AT&T：`_struct_pointer + 8`

在字符数组中（含有 8 个字符）中寻址指定的字符：

eax 保存的是数组元素的数量（这里是 8 个），ebx 保存的是字符的偏移地址。（**冲突**）

AT&T：`_array(%ebx, %eax, 8)`

Intel：`[ebx + eax * 8 + _array]`

## 基本的内联语句

基本的汇编语句

```{code-block} c
asm ("statements");
asm ("nop");            // 不做任何事情
asm ("cli");            // 结束中断
asm ("sti");            // 开启中断
```

如果使用 `asm` 作为关键字和 C 代码有冲突，可以尝试换成 `__asm__`。

使用下面的语句，你甚至可以把寄存器压栈，然后弹栈，就和正常的函数调用一样：

```{code-block} c
asm ("pushl %eax\n\t"
     "movl $0, %eax\n\t"
     "popl %eax");
```

当你在一个 `asm` 函数中需要书写多行汇编语句时，需要用 `\n` 和 `\t` 来结尾。
只有这样，由 GCC 生成的 `.s` 文件在传递给 GAS 时才能够保持语法正确。

因为 C 语言和汇编语言之间并没有一个完全一对一的转化关系，所以，在汇编指令中，不要轻易触碰寄存器。

如果你非要使用寄存器，那么不要把程序写死，把每一个寄存器都安排的明明白白的，就像下面这样：

```{code-block} c
asm ("movl %eax, %ebx");
asm ("xorl %ebx, %edx");
asm ("movl $0, _booga");
```

上面这样写，很容易让你的程序崩掉。
因为这几个 asm 语句说明程序需要占用 `ebx`、`edx`、`booga` 这几个寄存器，但是可能不会立马使用。
进而导致其他程序由于无法使用寄存器而阻塞，而这个原因是 GCC 不会告诉你的。

那更好的方式应该时用下面介绍的格式来进行书写：不特别指定寄存器，让 GCC 自动优化，决定使用哪个寄存器。
我们使用 `$1`、`$2`、`$3` 这种方式来让程序更由弹性。

## 高级的内联语句

基本格式和前面保持一致，但是我们现在使用 Watcom-like 的扩展来支持输入和输出参数：

```{code-block} c
asm ( "statements" : output_registers : input_registers : clobbered_registers);
```

这个语法，我们的阅读顺序（或执行顺序）应该是这样的：

1. `input_registers` 输入寄存器列表，表示将 C 语言中的变量如何赋值给 CPU 中的寄存器。
2. `statements` 函数具体实现，表示需要执行的汇编语言函数体。
3. `clobbered_registers` 易失性寄存器列表，声明哪些寄存器可能会发生改变，让 GCC 特别留意。
4. `output_registers` 输出寄存器列表，表示将程序计算的结果保存到哪里。

现在直接看一个例子，后面再解释：

```{code-block} c
asm ("cld\n\t"      // 清除寄存器中的 direction 标志位，这个语句消耗 1-2 个时钟周期
     "rep\n\t"      // GAS 要求 rep 前缀独占一行，表示循环语句的开始
     "stosl"        // 注意 stos 有一个 l 后缀，表示我们要操作 longwords
     : /* no output registers */
     : "c" (count), "a" (fill_value), "D" (dest)
     : "%ecx", "%edi");
```

上面这段代码的意思是说，将 C 语言中的 `fill_value` 变量的值保存 `count` 次，每次都保存到 `dest` 中。

`: "c" (count), "a" (fill_value), "D" (dest)`

上面这个语句表示将 C 语言中的 `count` 保存到 `ecx` 寄存器，将 `fill_value` 保存到 `eax` 寄存器，将
`dest` 保存到 `edi` 寄存器。为什么这个工作要给 GCC 来做，而不是我们手动分配呢？
这是因为 GCC 分配寄存器的时候，如果它发现 `fill_value` 已经在 `eax`
寄存器中了，那它就会继续保留这个值，而不是重新载入。
这样，如果是在循环语句中，每次循环都能节省一个 movl 操作。

`: "%ecx", "%edi");`

上面这个语句表示，我们告诉了 GCC，你不能完全信任 ecx 和 edi 这两个寄存器中的值是有效的。
这并不是说每次都需要重新加载，只是告诉它这个值是可能会被改变的。

这种声明方式在 GCC 做优化的时候是有帮助的，因为这告诉了 GCC 你的意图。
它甚至能够智能地推断出，如果你想找到 `(x+1)` 寄存器中的值，且你没有更改这个寄存器的值，后面 C
代码需要使用这个寄存器中的值的时候，就可以直接复用前面的计算结果了。

下面是一个关于如何加载寄存器的代码，你可能在未来会用到：

```{code-block} text
a        eax
b        ebx
c        ecx
d        edx
S        esi
D        edi
I        constant value (0 to 31)
q,r      dynamically allocated register (see below)
g        eax, ebx, ecx, edx or variable in memory
A        eax and edx combined into a 64-bit integer (use long longs)
```

用上面的方式，你不能直接指向寄存器中的某个字节（`ah`，`al` 等）或某个字（`ax`，`bx` 等）。
如果你实现这样的效果，你需要特别指明 `ax` 或 `ah`。

使用寄存器的时候，在源代码中需要使用双引号，在表达式中需要用圆括号。

当你构造一个易失性寄存器列表的时候，你可以像上面一样，用 `%` 前缀指定寄存器。
如果你正在写一个变量，那么你必须在易失性寄存器列表中包含 `"memory"` 字样，这样写是为了以防万一，当你写一个变量时，而 GCC 认为它已经在寄存器中了。

当然，还有更多，比如用 `cc` 表示条件易变（`flags` 寄存器容易发生改变，这个寄存器 `jnz`、`je`
指令会经常用到），也可以把 `cc` 放到易失性寄存器列表中。

现在，我们加载特定的寄存器都是没什么问题的。
但是有一种情况，如果说现在需要使用 `ebx` 和 `ecx`，但是这两个寄存器正在被其他程序使用，在前面的变量没有压栈的情况下，GCC
无法重新给这两个寄存器重新分配值，这就会导致程序的效率低下。

解决这个问题的方案就是，我们不再手工给程序指定需要使用哪个寄存器，而是让 GCC 帮助我们选择：

```{code-block} c
asm ("leal (%1,%1,4), %0"
     : "=r" (x)
     : "0" (x) );
```

上面的例子可以快速地计算 `x` 的 5 倍（在 Pentium 上只需要 1 个周期）。

但是，除非我们真的需要指定需要使用哪些寄存器，比如 `rep movsl` 或 `rep stosl` 需要硬编码地使用
`ecx`、`edi` 或 `esi` 寄存器，这是万不得已的情况。那么一般情况下，我们为什么不让 GCC 帮我们选择呢？
所以，当 GCC 通过编译出能够供 GAS 使用的代码后，`%0` 就会被真实的寄存器替换掉了，这个寄存器时 GCC 选出来的。

`"q"` 和 `"r"` 从哪里来？`"q"` 让 GCC 可以从 `eax`、`ebx`、`ecx` 和 `edx` 中做选择，`"r"` 让 GCC
可以考虑 `esi` 和 `edi`。所以，如果你用 `"r"`，那么程序就可能会使用指令寄存器，否则建议你使用 `"q"`。

现在，你可能想知道，如何知道 `%n` 将会具体被哪些寄存器取代呢？
这其实是先来先服务的模型，对于 `"q"` 和 `"r"` 代表的那些寄存器。
如果你想将某个 `%n` 和特定的寄存器绑定，来保证能够复用结果，那么就用 `0`、`1`、`2` 来代替这里的 `n`。
在这种情况下，就不用指定易失性寄存器列表了，因为你肯定不会知道应该如何指定，这是由 GCC 决定的。

现在，对于 output_registers：

```{code-block} c
asm ("leal (%1,%1,4), %0"
     : "=r" (x_times_5)
     : "r" (x) );
```

注意，我们用 `=` 来指定输出寄存器。

如果你想让某个变量的输出和输出始终保持在同一个寄存器中，你可以用如下的方式：

```{code-block} c
asm ("leal (%0,%0,4), %0"
     : "=r" (x)
     : "0" (x) ); // 这里用 0 来指定
```

当然，下面的方式也可以奏效，显式地指明需要使用哪个寄存器：

```{code-block} c
asm ("leal (%%ebx, %%ebx, 4), %%ebx"
     : "=b" (x)
     : "b" (x) );
```

注意两点：

- 不用在易失性寄存器列表中指明包含 `ebx`，因为 GCC 知道 `ebx` 的值可以直接被 `x` 使用。
- 在扩展的 asm 语法中，你需要使用两个百分号来指明寄存器。

````{important}
如果汇编语句必须作为一个整体被执行，而不希望被编译器优化，需要使用 `__volatile__` 关键字。

```{code-block} text
__asm__ __volatile__ (函数体);
```

当然，一般情况下，我们并不建议使用 `volatile` 关键字，因为它妨碍了编译器的优化。
````

## 一些有用的例子

```{code-block} c
#define disable() __asm__ __volatile__ ("cli");

#define enable() __asm__ __volatile__ ("sti");
```

当然，`libc` 也有类似的定义：

```{code-block} c
#define times3(arg1, arg2) \
__asm__ ( \
  "leal (%0,%0,2),%0" \
  : "=r" (arg2) \
  : "0" (arg1) );

#define times5(arg1, arg2) \
__asm__ ( \
  "leal (%0,%0,4),%0" \
  : "=r" (arg2) \
  : "0" (arg1) );

#define times9(arg1, arg2) \
__asm__ ( \
  "leal (%0,%0,8),%0" \
  : "=r" (arg2) \
  : "0" (arg1) );
```

上面这些函数分别是对 `arg1` 乘以了 3、5、9，然后把结果放在了 `arg2` 中。当然，你可以下面这样做：

```{code-block} c
times5(x, x);
```

温馨提示：如果你用固定长度的参数调用 `memcpy()`，GCC 会将它内联成 `rep movsl` 格式，如下所示：

```{code-block} c
#define rep_movsl(src, dest, numwords) \
__asm__ __volatile__ ( \
  "cld\n\t" \
  "rep\n\t" \
  "movsl" \
  : : "S" (src), "D" (dest), "c" (numwords) \
  : "%ecx", "%esi", "%edi" )
```

但是，如果需要一个变长的参数来内联，且你总是需要操作 `dwords`，那么可以按照如下的方式来操作：

```{code-block} c
#define rep_stosl(value, dest, numwords) \
__asm__ __volatile__ ( \
  "cld\n\t" \
  "rep\n\t" \
  "stosl" \
  : : "a" (value), "D" (dest), "c" (numwords) \
  : "%ecx", "%edi" )
```

和上面的代码段类似，我们来实现 `memset()`，但是并没有写成内联格式，如下所示：

```{code-block} c
#define RDTSC(llptr) ({ \
__asm__ __volatile__ ( \
        ".byte 0x0f; .byte 0x31" \
        : "=A" (llptr) \
        : : "eax", "edx"); })
```

阅读 Pentium 中的 `TimeStampCounter`，把 64 位的结果放入 `llptr` 中。
