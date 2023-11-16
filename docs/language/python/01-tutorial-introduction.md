# 第一章 Python快速入门

本章是 Python 的快速入门，在这一章并不涉及 Python 的特殊规则和细节，目标是通过示例使你快速了解 Python 语言的特点。本章简要介绍了变量、表达式、控制流、函数以及输入/输出的基本概念。在这一章不涉及 Python 语言的高级特性。尽管如此，有经验的程序员还是能够通过阅读本章的材料创建高级程序。

## 运行 Python

Python 程序通过解释器执行。如果你的机器已经装好了 python，简单地在命令行键入 python 即可运行 python 解释器。在解释器运行的时，会有一个命令提示符 `>>>`，在提示符后键入你的程序语句，键入的语句将会立即执行。在下边的例子中，我们在 `>>>` 提示符后边键入最常见的显示 "Hello World" 的命令:

```python
Python 2.4.2 (#67, Sep 28 2005, 12:41:11) [MSC v.1310 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> print "Hello World"
Hello World
>>>
```

程序也可以像下面一样放置在一个文件中

```python
# helloworld.py
print "Hello World"
```
Python源代码文件使用.py后缀. '#' 表示注释(到行末结束)

执行文件helloworld.py

```bash
% python helloworld.py
Hello World
%
```

在Windows 下，只需双击一个.py文件就能执行这个python程序。windows会自动调用python解释程序，然后启动一个终端窗口(类DOS窗口)来执行它。在这种情况下,终端窗口会在程序执行完毕后立即关闭(经常是在你看到它的输出之前)。为避免这个问题,你可以使用python集成开发环境,例如IDLE或Pythonwin。另一个可行的方法是建立一个 bat 文件,在文件写入这样一行语句，如 python -i helloworld.py。运行这个批处理，程序在执行完成后会自动进入python解释器。

在解释器中,也可以通过函数execfile()来运行一个保存在磁盘上的程序,如下例:

```python
>>> execfile("helloworld.py")
Hello World
```

在UNIX下,你可以在程序的首行写入 #! 魔法字符串 来自动调用python解释器执行你的脚本。

```python
print "Hello World"
```

解释器会一直运行直到文件结束。如果在交互模式下,键入 EOF字符退出解释器。在UNIX下,EOF字符是Ctrl+ D;在Windows下,EOF字符是Ctrl+Z.也可以在程序中使用sys.exit()函数或者通过引发`SystemExit`异常来退出程序:

```python
>>> import sys
>>> sys.exit()
```

或者

```python
>>> raise SystemExit
```

## 变量和表达式

通过Listing 1.1所示的程序示例变量和表达式的用法

Listing 1.1 复利计算器(Simple Compound-Interest Calculation)

```python
principal = 1000        # Initial amount (本金)
rate = 0.05             # Interest rate (利率)
numyears = 5            # Number of years (期数,年)
year = 1
while year <= numyears:
        principal = principal*(1+rate)
        print year, principal
        year += 1
```

程序输出:

```python
1 1050.0
2 1102.5
3 1157.625
4 1215.50625
5 1276.2815625
```

Python 是一种动态语言,在程序运行过程中，同一变量名可以（在程序运行的不同阶段）代表不同形式的值(整型,浮点,列表,元组...)。事实上，程序中使用的变量名只是各种数据及对象的引用。这与C语言不同,C语言中变量名代表的是用来存放结果的一个固定位置及长度的内存片段。从例子Listing 1.1中的变量principal可以看出Python语言的动态特性.最初,它被赋值为一个整数,但是稍后程序将它再次赋值:

```python
principal = principal*(1+rate)
```

这个语句计算表达式的值，然后将计算结果赋给 principal 变量做为它的新值。当赋值动作发生时,principal最初绑定的值1000被丢弃。赋值结束，不但 principal 绑定的值发生了变化，它的类型也随着赋值动作发生了相应的变化。在这个例子中，由于rate是一个浮点数,所以在赋值完成后,principal也变成一个浮点数。

Python中每个语句以换行结束,当然你也可以在一行中写多个语句，这时语句之间必须使用用分号分隔，就象下面这样:

```python
principal = 1000; rate = 0.05; numyears = 5;
```

（建议这样的写法仅仅用于调试语句，因为可以很方便的只删一行就删掉全部调试语句)

while 语句首先检查在它后边的循环条件,若条件表达式为真,它就执行冒号后面的语句块，然后再次测试循环条件，直至为假。冒号后面的缩近语句块为循环体。注意，Python语言使用缩进块来表示程序逻辑（其它大多数语言使用大括号等）。在Listing 1.1中while语句后的三条语句为循环体，在每次循环中均执行。Python并未指定缩进的空白(空格和制表符)数目，唯一的要求是同一层次的语句必须有相同的缩进空白。（注意，要么都是空格，要是么都制表符，千万别混用)

Listing 1.1中的程序美中不足的就是输出不是很好看，为了让它美观一点,可以用格式字符串将计算结果只保留小数点后两位：

```python
print "%3d %0.2f" % (year, principal)

这样,程序的输出就变为:

1 1050.00
2 1102.50
3 1157.63
4 1215.51
5 1276.28
```

格式字符串包含普通文本及格式化字符序列(例如"%d", "%s", 和 "%f"),这些序列决定特定类型的数据(如整型,字符串,浮点数)的输出格式.'%3d'将一个整数在宽度为3个字符的栏中右对齐,'%0.2f'将一个浮点数的小数点后部分转换为2位。格式字符串的作用和C语言中的sprintf()函数基本相同。详细内容请参阅第四章--操作符及表达式。

## 条件语句

if和else语句用来进行简单的测试，如:

```python
# Compute the maximum (z) of a and b (得到a与b中较大的一个)
if a < b:
        z = b
else:
        z = a
```

if和else的语句块用缩近来表示，else从句在某些情况下可以省略。 如果if或else语句块只有一个语句，也可以不使用缩近。也就是说:

```python
if a<b: z=a
else: z=b
```

这样的写法也是合法的，但这不是推荐的作法。一直使用缩近可以让你方便的在语句体中添加一个语句，而且读起来更清晰。 若某个子句不需任何操作,就使用pass语句，如:

```python
if a < b:
        pass      # Do nothing
else:
        z = a
```

通过使用 or,and 和 not 关键字你可以建立任意的条件表达式:

```python
if b >= a and b <= c:
        print "b is between a and c"
if not (b < a or b > c):
        print "b is still between a and c"
```

用 elif 语句可以检验多重条件(用于代替其它语言中的switch语句):

```python
if a == '+':
        op = PLUS
elif a == '-':
        op = MINUS
elif a == '*':
        op = MULTIPLY
else:
        raise RuntimeError, "Unknown operator"
```

## 文件输入/输出

下面的程序打开一个文件,然后一行行地读出并显示文件内容:

```python
f = open("foo.txt")        # Returns a file object
line = f.readline()        # Invokes readline() method on file
while line:
        print line,        # trailing ',' omits newline character
        line = f.readline()
f.close()
```

`open()`函数返回一个新文件对象(file object)。通过调用此对象的不同方法可以对文件进行不同的操作。`readline()`方法读取文件的一行(包括换行符'\n')。如果读到文件末尾，就返回一个空字符串。要将程序的输出内容由屏幕重定向到文件中，可以使用'>>'运算符，如下例:

```python
f = open("out","w")     # Open file for writing
while year <= numyears:
        principal = principal*(1+rate)
        print >>f,"%3d %0.2f" % (year,principal)  #将格式文本输出到文件对象 f
        year += 1
f.close()
```

当然,文件对象也拥有`write()`方法，通过它可以向文件对象写入新的数据。例如上边例子中的print的语句也可以写成这样:

```python
f.write("%3d  %0.2f\n" % (year,principal)) 
```

## 字符串

要创建一个字符串，你使用单引号,双引号或三引号将其引起来，如下例:

```python
a = 'Hello World'
b = "Python is groovy"
c = """What is footnote 5?"""
```

一个字符串用什么引号开头，就必须用什么引号结尾。单引号与双引号只能创建单行字符串，两个三引号之间的一切字符(包括换行)都是字符串的内容, 因此三引号能够创建多行字符串 。如下例：

```python
print '''Content-type: text/html

<h1> Hello World </h1>
Click <a href="http://www.python.org">here</a>.
'''
```

字符串是一个以0开始，整数索引的字符序列,要获得字符串 s 中的第 i+1 个字符(别忘了0是第一个),使用索引运算符 s[i]:

```python
a = "Hello World"
b = a[4]                # b = 'o'
```

要获得一个子串,使用切片运算符 s[i:j]。 它返回字符串 s 中从索引 i (包括i)到 j (不包括 j)之间的子串。若 i 被省略，python就认为 i=0，若 j 被省略，python就认为 j=len(s)-1:

```python
c = a[0:5]              # c = "Hello"
d = a[6:]               # d = "World"
e = a[3:8]              # e = "lo Wo"
```

可以用加(+)运算符来连结字符串:

```python
g = a + " This is a test"
```

通过使用str()函数,repr()函数或向后的引号(`)可以将其他类型的数据转换为字符串:

```python
s = "The value of x is " + str(x)
s = "The value of y is " + repr(y)
s = "The value of y is " + `y`
```

repr()函数用来取得对象的规范字符串表示，向后的引号(`)是repr()函数的快捷版。

在大多情况下str()和repr()函数会返回同一个结果,但是它们之间有很微妙的差别,后边的章节对此将有详细描述。

## 列表和元组(Lists & Tuples)

就如同字符串是字符的序列,列表和元组则是任意对象的序列。象下面这样就可以创建一个列表:

```python
names = [ "Dave", "Mark", "Ann", "Phil" ]
```

列表和元组都是以整数0来开始索引的序列,你可以用索引操作符来读取或者修改列表中特定元素的值:

```python
a = names[2]             # Returns the third item of the list, "Ann"
names[0] = "Jeff"        # Changes the first item to "Jeff"

用len()函数得到列表的长度:

print len(names)        # prints 4

append()方法可以把一个新元素插入列表的末尾:

names.append("Kate")

aList.insert(index,aMember)方法可以把新元素 aMember 插入到列表 aList[index] 元素之前:

names.insert(2, "Sydney")

用切片操作符可以取出一个子列表或者对子列表重新赋值:

b = names[0:2]                      # Returns [ "Jeff", "Mark" ]
c = names[2:]                       # Returns [ "Sydney", "Ann", "Phil", "Kate" ]
names[1] = 'Jeff'                   # Replace the 2nd item in names with "Jeff"
names[0:2] = ['Dave','Mark','Jeff'] # 用右边的 list 替换 names 列表中的前两个元素
    
加(+)运算符可以连结列表:

a = [1,2,3] + [4,5]     # Result is [1,2,3,4,5]

列表元素可以是任意的 Python 对象,当然也包括列表:

a = [1,"Dave",3.14, ["Mark", 7, 9, [100,101]], 10]

子列表的元素用下面的方式调用:

a[1]            # Returns "Dave"
a[3][2]         # Returns 9
a[3][3][1]      # Returns 101
```

Listing 1.2中代码从一个文件中读取一系列数字，然后输出其中的最大值和最小值。 通过这个示例我们可以了解到列表的一些高级特性：

Listing 1.2 列表的高级特性

```python
import sys                       # Load the sys module (导入sys模块)
f = open(sys.argv[1])            # Filename on the command line (从命令行读取文件名)
svalues = f.readlines()          # Read all lines into a list (读出所有行到一个列表)
f.close()

# Convert all of the input values from strings to floats (把输入的值转换为浮点数)
fvalues = [float(s) for s in svalues]

# Print min and max values (输出最大值和最小值)
print "The minimum value is ", min(fvalues)
print "The maximum value is ", max(fvalues)
```

程序第一行用import语句从Python library中导入sys模块。

你需要在命令行提供一个文件名给上面的程序，该文件名参数保存在sys.argv 列表中，open方法通过读取sys.argv[1]得到这个文件名参数。

readlines()方法读取文件中的所有的行到一个列表中。

表达式 [float(s) for s in svalues] 通过循环列表svalues中的所有字符串并对每个元素运行函数float()来建立一个新的列表,这种特殊的建立列表的方法叫做列表包含( list comprehension)。 在列表中所有的字符串都转换为浮点数之后,内建函数min()和max()计算出列表中的最大值及最小值。

元组(tuple)类型和列表关系很密切,通过用圆括号中将一系列逗号分割的值括起来可以得到一个元组:

```python
a = (1,4,5,-9,10)
b = (7,)                                 # 一个元素的元组 (注意一定要加一个额外的逗号！)
person = (first_name, last_name, phone)
```

在某些时候，即使没有圆括号, Python仍然可以根据上下文认出这是一个元组，如: (为了写出更清晰可读的程序，建议你不要依赖 Python 的智能)

```python
a = 1,4,5,-9,10
b = 7,
person = first_name, last_name, phone
```

元组支持大多数列表的操作,比如索引,切片和连结。一个关键的不同是你不能在一个tuple创建之后修改它的内容。也就是说,你不能修改其中的元素,也不能给tuple添加新的元素。

## 循环

通过使用while语句，我们在前面已经简单介绍了 while 循环。在Python中另一种循环结构是 for 循环，它通过 迭代 一个序列(例如字符串,列表,或者tuple等)中的每个元素来建立循环。下边是一个例子:

```python
for i in range(1,10):
        print "2 to the %d power is %d" % (i, 2**i)
```

range(i,j)函数建立一个整数序列,这个序列从第 i 数开始(包括 i )到第 j 数为止(不包括 j)。若第一个数被省略，它将被认为是0。该函数还可以有第三个参数，步进值，见下面的例子:

```python
a = range(5)         # a = [0,1,2,3,4]
b = range(1,8)       # b = [1,2,3,4,5,6,7]
c = range(0,14,3)    # c = [0,3,6,9,12]
d = range(8,1,-1)    # d = [8,7,6,5,4,3,2]
```

for语句可以迭代任何类型的序列:

```python
a = "Hello World"
# Print out the characters in a
for c in a:
        print c
b = ["Dave","Mark","Ann","Phil"]
# Print out the members of a list
for name in b:
        print name
```

range()函数根据起始值，终止值及步进值三个参数在内存中建立一个列表，当需要一个很大的列表时,这个既占内存又费时间。为了克服它的缺点,Python提供了xrange()函数:

```python
for i in xrange(1,10):
        print "2 to the %d power is %d" % (i, 2**i)

a = xrange(100000000)       # a = [0,1,2, ..., 99999999]
b = xrange(0,100000000,5)   # b = [0,5,10, ...,99999995]
```

xrange()函数只有在需要值时才临时通过计算提供值，这大大节省了内存。

## 字典

字典就是一个关联数组(或称为哈希表)。它是一个通过关键字索引的对象的集合。使用大括号{}来创建一个字典，如下 例:

```python
a = {
       "username" : "beazley",
       "home" : "/home/beazley",
       "uid" : 500
    }

用关键字索引操作符可以访问字典的某个特定值:

u = a["username"]
d = a["home"]

用下面的方式插入或者修改对象:

a["username"] = "pxl"
a["home"] = "/home/pxl"
a["shell"] = "/usr/bin/tcsh"
```

尽管字符串是最常见的 关键字(key) 类型，你还是可以使用很多其它的 python 对象做为字典的关键字，比如 数字 和 tuple，只要是不可修改对象，都可以用来做字典的key。有些对象,例如列表和字典,不可以用来做字典的key,因为他们的内容是允许更改的。

我们可以使用 has_key() 方法来检验一个键/值对是否存在(或者in操作符):

```python
if a.has_key("username"):
     username = a["username"]
else:
     username = "unknown user"

上边的操作还可以用更简单的方法完成:

username = a.get("username", "unknown user")

字典的keys() 方法返回由所有关键字组成的列表:

k = a.keys()         # k = ["username","home","uid","shell"]

del语句可以删除字典中的特定元素:

del a["username"]
```

## 函数

在Python中，使用def语句来创建函数，如下例:

```python
def remainder(a,b):
        q = a/b
        r = a - q*b
        return r
```

要调用一个函数，只要使用函数名加上用括号括起来的参数就可以了。比如result = remainder(37,15),如果你打算让函数返回多个值，就让它返回一个元组好了。（当然，只要你愿意，让它返回一个列表我们也不会介意)

```python
def divide(a,b):
        q = a/b        # If a and b are integers, q is an integer
        r = a - q*b
        return (q,r)
```

当返回一个 tuple 时，你会发现象下面这样调用函数会很有用:

```python
quotient, remainder = divide(1456,33)
```

你也可以象下面这样给函数的参数指定一个默认值:

```python
def connect(hostname,port,timeout=300):
      # Function body
```

若在函数定义的时候提供了默认参数，那么在调用函数时就允许省略这个参数：

```python
connect('www.python.org', 80)
```

你也可以使用关键字参数来调用函数,这样你的参数就可以使用任意顺序:

```python
connect(port=80,hostname="www.python.org")
```

函数内部定义的变量为局部变量，要想在一个函数内部改变一个全局变量的值，在函数中使用global语句:

```python
a = 4.5
...
def foo():
        global a
        a = 8.8             # 改变全局变量 a
```

## 类

Python支持面向对象编程，在面向对象编程中，class语句用于定义新类型的对象。例如，下面这个类定义了一个简单的堆栈：

```python
class Stack(object):
        def __init__(self):              # 初始化栈
                self.stack = [ ]
        def push(self,object):
                self.stack.append(object)
        def pop(self):
                return self.stack.pop()
        def length(self):
                return len(self.stack)
```

在类定义中,方法用 def 语句定义。类中每个方法的第一个参数总是引用类实例对象本身，大家习惯上使用 self 这个名字代表这个参数。不过这仅仅是个习惯而已，如果你愿意也可以用任意的别的名字。不过为了别人容易看懂你的程序，最好还是跟随大家的习惯。类的方法中若需要调用实例对象的属性则必须显式使用self变量(如上所示)。方法名中若前后均有两个下划线，则表示这是一个特殊方法，比如init方法被用来初始化一个对象(实例)。

象下面这样来使用一个类:

```python
s = Stack()           # Create a stack (创建)
s.push("Dave")        # Push some things onto it (写入)
s.push(42)
s.push([3,4,5])
x = s.pop()           # x gets [3,4,5] (读取)
y = s.pop()           # y gets 42
del s                 # Destroy s (删除)
```

## 异常

如果在你的程序发生了一个错误，就会引发异常(exception),你会看到类似下面的错误信息:

```python
Traceback (most recent call last):
 File "<interactive input>", line 42, in foo.py
NameError: a
```

错误信息指出了发生的错误类型及出错位置，通常情况下，错误会导致程序终止。不过你可以使用 try 和 except 语句来捕获并处理异常:

```python
try:
    f = open("file.txt","r")
except IOError, e:
    print e
```

上面的语句表示：如果有 IOError 发生，造成错误的详细原因将会被放置在对象 e 中，然后运行 except 代码块。 若发生其他类型的异常，系统就会将控制权转到处理该异常的 except 代码块，如果没有找到该代码块，程序将运行终止。若没有异常发生，except代码块就被忽略掉。

raise语句用来有意引发异常，,你可以使用内建异常来引发异常，如下例:

```python
raise RuntimeError, "Unrecoverable error"
```

当然，你也可以建立你自己的异常，这将在 第五章--控制流中的定义新的异常中详细讲述。

## 模块

当你的程序变得越来越大，为了便于修改和维护，你可能需要把它们分割成多个相关文件。 Python允许你把函数定义或公共部分放入一个文件，然后在其他程序或者脚本中将该文件作为一个模块导入。要创建一个模块，把相应的语句和定义放入一个文件，这个文件名就是模块名。(注意:该文件必须有.py后缀)：

```python
# file : div.py
def divide(a,b):
    q = a/b        # If a and b are integers, q is an integer
    r = a - q*b
    return (q,r)
```

要在其它的程序中使用这个模块，使用import语句:

```python
import div
a, b = div.divide(2305, 29)
```

import语句创建一个新的名字空间，该空间包含模块中所有定义对象的名称。要访问这个名字空间，把模块名作为一个前缀来使用这个模块内的对象，就像上边例子中那样:`div.divide()`

如果你希望使用一个不同的模块名字访问这个模块，给import语句加上一个 as 模块名 部分就可以了:

```python
import div as foo
a,b = foo.divide(2305,29)

如果你只想导入指定的对象到当前的名称空间,使用 from 语句:

from div import divide
a,b = divide(2305,29)       # No longer need the div prefix (不再需要div前缀)

导入一个模块中的所有内容到当前的名称空间:

from div import *

最后，内建函数dir()可以列出一个模块中的所有可访问内容。当你在python交互环境中测试一个模块的功能时，这会是一个很有用的工具，因为它可以提供一个包含可用函数及变量的列表:

>>> import string
>>> dir(string)
['_ _builtins_ _', '_ _doc_ _', '_ _file_ _', '_ _name_ _', '_idmap',
 '_idmapL', '_lower', '_swapcase', '_upper', 'atof', 'atof_error',
 'atoi', 'atoi_error', 'atol', 'atol_error', 'capitalize',
 'capwords', 'center', 'count', 'digits', 'expandtabs', 'find',
...
>>> 
```