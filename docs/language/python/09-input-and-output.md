# 第九章 输入输出

本章的主题是Python的输出输出细节：命令行参数、环境变量、文件I/O、Unicode及对象持久化。

## 读取参数及环境变量

当解释器启动时，命令行参数就被放入 sys.argv 这个列表中。列表的第一个元素是程序的名字，后面的元素是你提供的命令行参数。下面的程序展示了如何访问命令行参数:

```python
# printopt.py 
# 打印出所有命令行参数
import sys 
for i in range(len(sys.argv)): 
    print "sys.argv[%d] = %s" % (i, sys.argv[i]) 
```

运行该程序，结果如下:

```
% python printopt.py foo bar -p 
sys.argv[0] = printopt.py 
sys.argv[1] = foo 
sys.argv[2] = bar 
sys.argv[3] = -p 
% 
```

通过访问os.envirom字典可以访问环境变量，如下例：

```python
import os 
path = os.environ["PATH"] 
user = os.environ["USER"] 
editor = os.environ["EDITOR"] 
```

要更改环境变量， 直接设定 os.environ 变量或使用 os.putenv() 函数。如下例：

```python
os.environ["FOO"] = "BAR" 
os.putenv("FOO","BAR") 
```

## 文件

内建函数 open(name [,mode]) 打开或创建文件，就象下面这样：

```python
f = open('foo')        # 以读取模式打开 'foo'
f = open('foo','w')    # 以写模式打开 'foo' 
```

文件模式 'r' 表示读， 'w' 表示写， 'a' 表示在文件末尾添加内容。 模式字符后面允许跟一个 'b' 表示访问的是二进制数据，比如 'rb' 或 'wb'。对 UNIX(或Linux)这个'b'有没有无关紧要，对 Windows 平台则有积极意义。如果你很关心代码的可移植性，那就最好总是加上这个'b'。另外，还有一种更新模式，你只要在读写模式后增加一个'+'就可以使用这种模式，如'r+' 或 'w+'。当一个文件以更新模式打开，你就可以对这个文件进行读写操作。只要在任何读取操作之前刷新所有的输出缓冲就不会有问题。如果一个文件以 'w+' 模式打开，它的长度就度截为 0。

open() 返回一个文件对象，它支持下表中列出的方法

**表 9.1. 文件方法**

```
方法                      描述
f.read([n])               读取至多 n 字节
f.readline([n])           读取一行中的前 n 字符。如果 n 被省略，就读取整行
f.readlines()             读取所有的行并返回一个包含所有行的列表
f.xreadlines()            返回一个迭代器，每次迭代返回文件的一个新行
f.write(s)                将字符串 s 写入文件
f.writelines(l)           将列表 l 中的所有字符串写入文件
f.close()                 结束文件
f.tell()                  返回当前的文件指针
f.seek(offset [, where])  定位到一个新的文件位置
f.isatty()                如果 f 是一个交互式终端则返回 1
f.flush()                 刷新输出缓冲区
f.truncate([size])        如果文件长于 size 就截短它至 size 大小
f.fileno()                返回一个整型的文件描述符
f.readinto(buffer ,nbytes)读取 n 字节数据至一个 buffer 对象。
```

除非给 read() 方法一个可选的长度参数，它就会读取整个文件并将文件内容作为一个字符串返回。 readline() 返回下一行，包含换行字符。如果在调用 readline() 方法时提供一个长度参数 n，若 n 大于该行长度，则返回前 n 个字节。该行剩下的部分并不会被丢弃，在下次读取操作时会被返回。 readlines() 方法读取所有行，并将这些行作为一个 list 返回。readline() 和 readlines() 会自动处理换行在不同平台的表示。(众所周知的 '\n','\r','\r\n') xreadlines() 返回一个迭代器，允许用迭代的方式得到文件的每一行。下面是一个使用 xreadlines()的例子：

```python
for line in f.xreadlines(): 
    # Do something with line 
   ... 
```

write() 方法将一个字符串写入文件。 writelines() 将一个字符串列表中的所有元素顺序写入文件。以上所有操作，字符串中均可包含二进制数据。 seek(offset[,where])用来随机存取文件的任一部分。offset是偏移量，where是可选的位置参数(默认值为0，表示文件开始位置)。 如果where的值是1，表示当前位置。如果where是2表示文件结束位置。fileno()返回一个打开文件的整型文件描述编号，有些模块在进行低层次I/O操作时会用到。在支持单个文件超过2GB容量的机器上，seek() 和 tell() 使用长整数. 不过要允许这个特性可能需要重新配置并重新编译Python解释器。

文件对象还有下面的数据属性：

属性 描述 f.closed 表示文件状态的布尔值: 0 表示文件打开， 1 表示已关闭。 f.mode 文件打开模式 f.name open()函数打开的文件名 否则，它就是一个表示文件来源的字符串 f.softspace 这是一个布尔值 在使用 print 语句时表示在打印另一个值之前，是否要先打印一个空白符。若用类来模仿文件操作则必须提供这样一个可写的属性，并将其初始化为0。

## 标准输入,标准输出和标准错误

Python解释器提供三种标准文件对象,标准输入,标准输出,以及标准错误。(即sys模块中的sys.stdin, sys.stdout和 sys.stderr对象). stdin对象为解释器提供输入字符流。stdout对象接收 print 语句产生的输出. stderr对象接收出错信息. 通常stdin被映射到用户键盘输入,而stdout和stderr产生屏幕输出.

用上一节介绍的方法就可以实现原始的用户输入/输出.下边的函数从标准输入读取一行文本，然后返回这行文本:

```python
def gets():
    text = ""
    while 1:
       c = sys.stdin.read(1)
       text = text + c
       if c == '\n': break
    return text
```

内建函数raw_input(prompt)也可以从stdin中读取并保存内容:

```python
s = raw_input("type something : ")
print "You typed '%s'" % (s,)
```

最后要说的是，键盘中断(通常是Ctrl+C)会引发`KeyboardInterrupt`异常,该异常可以被异常处理语句捕获并处理。

只要需要，sys.stdout、 sys.stdin及sys.stderr的值均可以使用其它文件对象进行替换。这样 print 语句和 raw_input 函数都会使用新值。在解释器启动时，sys.stdout, sys.stdin及sys.stderr可以分别使用sys.stdout, sys.stdin, 和 sys.stderr这三个名字来访问。

注意某些场合 sys.stdout, sys.stdin及sys.stderr的默认值会被改变(通常程序运行在一个集成环境时).例如,当在IDLE下运行Python代码时, sys.stdin会被开发环境提供的一个行为类似文件对象的对象代替.在这样的场合,低层方法如read(),seek()可能会失效.

```
《Python In a Nutshell》(2003)
10.7.1 标准输出及标准错误
sys 模块有 stdout 和 stderr 属性, 这是用于输出的两个文件对象。 除非你使用某种 shell 重定向，输出内容将总是发送到执行脚本的终端上。当然现在几乎没有什么真正的终端了:这个所谓的终端通常是一个支持文本输入输出的窗口(比方windows下的一个 控制台 或unix下 一个 xterm 窗口).
```

## print语句

print语句将一个或多个对象的字符串表示输出到stdout对象. print可以能用逗号分割的一系列对象:

```
print "The values are", x, y, z
```

解释器对每个对象调用str()函数来产生最终输出内容，然后再将这些字符串用空格连接起来,并在字符串最后添加一个换行符，最后输出到stdout对象.不过当 print 语句的最后有一个逗号时，就会用一个空格代替输出字符串最后的换行。

```python
print "The values are ", x, y, z, w
# 也可以使用两个print语句来打印出相同的字符
print "The values are ", x, y,   # Omits trailing newline
print z, w
```

在第四章--操作符和表达式中介绍过的字符格式运算(%)能够实现字符串格式输出:

```
print "The values are %d %7.5f %s" % (x,y,z) # 格式化输出/输入
```

通过对 print 语句添加 >>file 修饰能够将输出内容重定向到 file 文件对象.(file是一个可写的文件对象):

```python
f = open("output","w")
print >>f, "hello world"
...
f.close()
```

将格式输出与三引号字符串相结合是输出特殊文本的有效方式。假设你需要批量发送一些固定格式的短小信件,包含姓名,项目名,以及一个数字，象下面这样:

```
Dear Mr. Bush,
Please send back my blender or pay me $50.00.

                                     Sincerely yours,

                                     Joe Python User
```

象下面这样做就OK:

```python
form = """\
Dear %(name)s,
Please send back my %(item)s or pay me $%(amount)0.2f.

                                     Sincerely yours,

                                     Joe Python User
"""
print form % { 'name': 'Mr. Bush',
               'item': 'blender',
               'amount': 50.00,
             }
```

在输出多行多项目文本时,该方法简单有效,并且条理清晰。

## 对象持久化

将一个对象内容保存到一个文件中，当再次需要该对象时通过读取这个文件重新生成该对象是很用的。你可以写一对函数通过读取和写入特定格式数据实现该功能，不过Python提供的 Pickle 和 shelve 模块可能是更好的选择.

Pickle 模块的 dump 方法可以方便的把一个对象保存到一个文件中.例如:

import Pickle object = someObject() f = open(filename,'w') Pickle.dump(object, f) # 保存对象

之后可以用 load 方法重新得到该对象:

import Pickle f = open(filename,'r') object = Pickle.load(f) # 恢复对象

shelve模块与Pickle做类似的工作,不过它将对象数据保存在一个字典格式的文本数据库中:

```python
import shelve
object = someObject()
dbase = shelve.open(filename)    # 打开数据库
dbase['key'] = object            # 将对象保存在数据库中
...
object = dbase['key']            # 恢复对象
dbase.close()                    # 关闭数据库
```

*注意*:只有支持序列化的对象才可以被保存在文件中。绝大多数Python对象都支持序列化。某些用于特殊目的的对象,例如用来维护系统内部状态的文件等，这样的对象是不能用这种方法来恢复的。关于Pickle和shelve模块的更多细节，参见附录A.

## Unicode I/O

在系统内部，Unicode 字符串被表示为一个16位整数序列，8-bit 字符串则是一个字节序列, 绝大多数字符串操作被扩展为能够处理更宽范围的字符值。只要 Unicode 字符串被转换为字节流，就必然会产生一系列问题(需要解决)。首先,要考虑现有软件的兼容性, 对那些仅支持 ASCII或其它 8-bit的软件来说，将 Unicode字符串转化为 ASCII字符串是较好的方法。其次, 16-bit 字符占用两个字节，字节顺序问题虽然比较无聊但必须考虑。对一个Unicode字符 U+HHLL 来说, 小端法编码方案将低位字节放在前面, 即 LL HH；大端法编码方案则将高位字节放在前面,即 HH LL. 就因为这么点问题, 不指定编码方案，你就无法将原始 Unicode 数据写入文件.

要解决这些问题, 只能根据特定的编码规则将 Unicode 字符串进行客观表示。这些规则定义了如何将 Unicode 字符表示为字节序列。在第四章, 针对 unicode()及 s.encode() 首先介绍了编码规则。举例来说：

```python
a = u"M\u00fcller" 
b = "Hello World" 
c = a.encode('utf-8')     # Convert a to a UTF-8 string 
d = unicode(b)            # Convert b to a Unicode string 
```

codecs 模块用类似的技术解决了 Unicode 的输入输出问题。 codecs 模块拥有一系列转换函数依据不同的编码方案完成字节数据和 Unicode 字符串的转换。通过调用 codecs.lookup(encoding) 函数来选择一种编码方案。这个函数返回一个包括四个元素的 tuple (enc_func, decode_func, stream_reader, stream_writer ). 举例来说:

```python
import codecs 
(utf8_encode, utf8_decode, utf8_reader, utf8_writer) = \ 
          codecs.lookup('utf-8') 
```

enc_func (u [,errors ]) 函数接受一个 Unicode 字符串 u ，返回值是tuple(s , len).其中 s 是转码后的 8-bit 字符串(内容为 u 的一部分或全部), len 是被成功转换的 Unicode 字符数. decode_func(s [,errors]) 函数接受一个 8-bit 字符串，返回值是 tuple(u, len)。其中 u 是一个 Unicode字符串(内容为 s 的一部分或全部)，len 是被成功转换的字符数。errors 决定转化过程中的错误如何处理，它的值可能是 'strict' 或 'ignore' 或 'replace'。若是 'strict'模式, 编码错误将引发` UnicodeError` 异常。 若是 'ignore' 模式, 编码错误将被忽略。若是 'replace' 模式，无法转换的编码将被替换为 '?' 字符(Unicode字符U+FFFD或8-bit字符 '?')。

stream_reader 用来对文件对象进行封装，以支持 Unicode 数据读取. 调用 stream_reader (file) 返回封装后的文件对象，它的 read(), readline(), 及 readlines() 方法支持读取 Unicode 字符串数据. stream_writer 用来对文件对象进行封装，以支持将 Unicode 字符串写入文件。调用 stream_writer(file) 返回封装后的文件对象，它的 write() 和 writelines() 方法将 Unicode 字符串按给定的编码转换为字节流写入文件中。

下面的例子演示了如何使用这些方法处理 UTF-8 编码的 Unicode 数据:

```python
# 输出 Unicode 数据到文件
ustr = u'M\u00fcller'         # 一个Unicode 字符串

outf = utf8_writer(open('foo','w'))   # 创建 UTF-8 字节流
outf.write(ustr) 
outf.close() 

# 从一个文件读取 unicode 数据 
infile = utf8_reader(open('bar')) 
ustr = infile.read() 
infile.close() 
```

当处理 Unicode文件时, 数据编码通常内嵌在文件本身当中。举例来说，XML 解析器根据文件的前几个字节'<?xml ...>' 来判断文件编码. 如果最初的四个值是 3C 3F 78 6D ('<?xm'), 就认为编码是 UTF-8. 如果最初的四个值是 00 3C 00 3F 或 3C 00 3F 00, 就认为编码是 UTF-16 大端表示方案 或 UTF-16 小端表示方案。 文档编码可能出现在 MIME 头或者做为其它文档元素的一个属性。举例来说：

```
<?xml ... encoding="ISO-8859-1" .... ?> 
```

用类似下面的代码来读取文档的编码：

```python
f = open("somefile") 
# Determine encoding 
... 
(encoder,decoder,reader,writer) = codecs.lookup(encoding) 
f = reader(f)    # Wrap file with Unicode reader 
data = f.read()  # Read Unicode data 
f.close()
```

### Unicode 数据编码

表 9.2 列出了codecs模块中目前正在使用的所有编码

**表 9.2. codecs 模块中的全部编码器**

```
编码                              描述
'ascii'                         ASCII 编码
'latin-1', 'iso-8859-1'         Latin-1 或 ISO-8859-1 编码
'utf-8'                         8-bit 变长编码
'utf-16'                        16-bit 变长编码
'utf-16-le'                     UTF-16, 显式小端编码方案
'utf-16-be'                     UTF-16, 显式大端编码方案
'unicode-escape'                和 u"string " 格式相同
'raw-unicode-escape'            和 ur"string "格式相同
```

下面的段落描述了各种编码的细节：

'ascii' 编码:

'ascii' 编码, 字符值的范围被限制在[0,0x7f] 和 [U+0000, U+007F]。超出这个范围的任何字符都是非法的。

'iso-8859-1' 或 'latin-1' 编码:

字符可以是任意的 8-bit 值([0,0xff] 及 [U+0000, U+00FF]). 取值范围 [0,0x7f] 内的字符对应 ASCII 字符集，取值范围 [0x80,0xff] 内的字符对应 ISO-8859-1 或 扩展 ASCII 字符集。超出 [0,0xff] 取值范围的任何字符都会造成错误。

'utf-8' 编码:

UTF-8 是一种变长编码，它能表示所有的Unicode字符。一个单独的字节用来表示值为 0–127 的 ASCII 字符。所有其它字符均被表示为多字节序列(双字节或3字节)。这些字节的编码见下表

```
Unicode 字符              Byte 0                    Byte 1                  Byte 2
U+0000 - U+007F          0nnnnnnn 
U+007F - U+07FF          110nnnnn                  10nnnnnn 
U+0800 - U+FFFF          1110nnnn                  10nnnnnn                 10nnnnnn 
```

对两字节序列, 第一个字节的前三个比特总是 110. 对三字节序列, 第一个字节的前三个比特总是 1110. 多字节序列的所有后来字节的前两个比特都是 10。

UTF-8 格式一个字符最多可以使用六个字节。 Python 中, 四字节 UTF-8 序列被称为代理对，用来对一对 Unicode 字符进行编码。 这一对字符的取值都在[U+D800, U+DFFF]范围内并组合成一个 20-bit 的值. 代理对这样编码:四字节序列 111100nn 10nnnnnn 10nnmmmm 10mmmmmm 被编码成这样一对： U+D800 + N , U+DC00 + M , 其中 N 是高10位， M 是低十位。五字节和六字节 UTF-8 序列(开始位分别为 111110 和 1111110) 用来对32比特值的Unicode字符进行编码。Python目前不支持五字节和六字节UTF-8序列。如果数据流中存在这样的数据会引发 `UnicodeError` 异常。

UTF-8 编码对旧程序支持的相当好. 首先，标准 ASCII 字符的编码没有发生任何改变。这意味着 UTF-8 编码的 ASCII 字符串与传统的 ASCII 字符串完全相同。其次， UTF-8 编码的多字节序列未内嵌 null 字节。这样现有的基于 C 库的软件和程序所使用的 null-结尾的 8-bit 字符串可以与 UTF-8 字符串相容. 最后，UTF-8 编码 保留了字符串的字典顺序。也就是说如果 a 和 b 是 Unicode 字符串并且 a < b, 则当 a 和 b被转化为UTF-8编码后， a < b 仍然成立。因此，写给 ASCII 字符串的排序算法及其它与顺序有关的算法也一样可以工作在 UTF-8 编码上。

'utf-16' , 'utf-16-be' , and 'utf-16-le' 编码:

UTF-16 是一种变长16位编码，其中 Unicode 被记录为 16-bit 值。如果未指定字节顺序，则默认为大端法编码方案。另外，一个特殊的字符 U+FEFF 可以用来显式的标记UTF-16 数据流的字节顺序。.大端编码方案, U+FEFF 字符表示 zero-width nonbreaking space, 而 U+FFFE 则是一个非法的 Unicode字符。因此，编码器可以使用这个字节顺序 FE FF 或 FF FE 来判断字节顺序。当读取 Unicode 数据时,Python会自动移去这个标志。

'utf-16-be' 编码 显式指定届UTF-16 大端编码(big endian), 'utf-16-le' 显式指定 UTF-16 小端编码(little ending)。

尽管已经有多种 UTF-16 的扩展以支持更多字符，目前的 Python 并不支持任何这样的扩展。

'unicode-escape' 及 'raw-unicode-escape' 编码:

这些编码方法被用来转换 Unicode 字符串到 Python使用的 Unicode 字符串及原始Unicode字符串。举例来说：

```python
s = u'\u14a8\u0345\u2a34' 
t = s.encode('unicode-escape')   #t = '\u14a8\u0345\u2a34' 
```

### Unicode 字符属性

除了实现输入输出之外, 使用 Unicode 的程序必然会有测试 Unicode 字符属性的需要（是否大小写、是否数字、是否空白等等）。 unicodedata 模块提供了这些 unicode字符数据库。. 常规字符属性可以通过 unicodedata.category(c) 函数得到. 例如, unicodedata.category(u"A") 返回 'Lu', 表示这个字符是一个大写字符。更多关于Unicode 字符数据库及 unicodedata 模块的细节，请参阅附录A。