# 第五章 控制流

本章描述程序中与控制流有关的语句.主题包括条件语句,循环及异常.

## 条件语句

if,else,以及elif语句用来控制条件代码的执行.条件语句的通常格式如下:

```
if expression:
    statements
elif expression:
    statements
elif expression:
    statements
...
else:
    statements
```

如果不需要判断if条件外的其它情形，条件语句中的else从句和elif从句可以省略. pass语句用于不需要做任何事的特殊情形:

```
if expression:
    pass            # 不做任何事
else:
    statements 
```


```
    注：上面的语句等价于
if !expression:
    statements
```


## 循环

可以使用for或while语句实现循环:

```
while expression:
    statements

for i in s:
    statements
```

while语句循环执行块中的语句,直到表达式为假. for语句反复迭代一个序列中的元素,直到迭代完序列中最后一个元素。如果序列中的每个元素都是元素个数统一的元组,你可以以下面这样的形式应用for语句:

```
for x,y,z in s:
    statements
```

在这个例子中, s必须为一个元组的序列,每个元组有三个元素.每次循环中,元组的三个元素的值被分别赋值给 x,y,和z.

break语句用于立刻中止循环.下边的例子从用户输入中读入内容,当输入为空时退出循环:

```
while 1:
   cmd = raw_input('Enter command > ')
   if not cmd:
      break            # 无输入,退出循环
   # 运行命令
    ...
```

continue语句用于直接进入下一次循环(忽略当前循环的剩余语句)。这个语句可以使循环跳过不必要的语句.下列这个例子打印出一个序列中的非负元素:

```python
for a in s:
    if a < 0:
       continue       # 忽略负值元素
    print a
```

break和continue语句只用于语句所在的当前循环,如果你需要退出一个多重循环,你应该使用异常。Python不提供goto语句.

你可以在一个循环结构中使用else语句:

```python
# while-else
while i < 10:
     do something
     i = i + 1
else:
     print 'Done'

# for-else
for a in s:
     if a == 'Foo':
          break
else:
     print 'Not found!'
```

循环中的else语句只在循环正常完成后运行(for或while循环),或者在循环条件不成立时立即运行(仅while循环),或者迭代序列为空时立即执行(仅for循环).如果循环使用break语句退出的话,else语句将被忽略.

## 异常

异常意味着错误,未经处理的异常会中止程序运行. raise语句用来有意引发一个异常. raise语句的通常格式是raise exception [, value ] , exception是异常类型, value是对于这个异常的特定描述.例如:

```
raise RuntimeError, 'Unrecoverable Error'
```

如果raise语句没有使用任何参数,最近一次发生的异常将被再次引发(尽管它只能用于处理一个刚刚发生的异常)

我们可以使用try和except语句来处理异常:

```python
try:
    f = open('foo')
except IOError, e:
    print "Unable to open 'foo': ", e
```

当一个异常发生时,解释器停止运行try块中的语句并寻找相应的except异常处理从句.若找到,控制就被传递到except块的第一条语句.否则,异常就被传递到上一级try语句语句块。try-except语句可以嵌套.如果异常被传递到整个程序的最顶层依然没有被处理,解释器就会终止程序运行,并显示出错信息。如果需要,不可捕获的错误也可以传递给用户定义函数 sys.excepthook() 处理.(参见附录A,The Python Library)

except语句中可选的第二个参数代表异常的说明,相当于raise语句的第二个可选参数.异常处理语句可以从这个值中得到关于异常原因的有用信息.

多个except语句可处理多种不同的异常，参见下例:

```
try:
   do something
except IOError, e:
   # 处理 I/O error
   ...
except TypeError, e:
   # 处理 Type error
   ...
except NameError, e:
   # 处理 Name error
   ...
```

一个except语句也可以处理多个异常:

```
try:
   do something
except (IOError, TypeError, NameError), e:
   # 处理 I/O, Type, 或 Name errors
   ...
```

pass语句可以用来忽略异常:

```
try:
   do something
except IOError:
   pass              # 不做任何事
```

省略异常名和值就可以捕获所有异常:

```
try:
   do something
except:
   print 'An error occurred'
```

**Table 5.1. 内建异常类型**

```
异常                      描述
Exception               所有内建异常
SystemExit              由sys.exit()产生
StandardError           除SystemExit外所有内建异常
ArithmeticError         所有运算异常
FloatingPointError      浮点数运算异常
OverflowError           数值溢出
ZeroDivisionError       被零除
AssertionError          assert语句引起的异常
AttributeError          属性名称不可用时引起
EnvironmentError        Python外部错误
IOError                 I/O 或与文件有关的错误(输入/输出错误)
OSError                 操作系统错误
WindowsError            Windows错误
EOFError                当到达一个文件的末尾时引起
ImportError             import语句失败
KeyboardInterrupt       键盘中断(通常是 Ctrl+C)
LookupError             索引或关键字错误
IndexError              超出序列的范围
KeyError                不存在的字典关键字
MemoryError             内存不足
NameError               寻找局部或全局变量时失败
UnboundLocalError       未绑定变量
RuntimeError            一般运行时错误
NotImplementedError     不可实现的特征
SyntaxError             语法错误
TabError                不一致的制表符使用 (由 -tt 选项产生)
IndentationError        缩进错误
SystemError             解释器致命错误
TypeError               给一个操作传递了一个不适当的类型
ValueError              值错误(不合适或丢失)
UnicodeError            Unicode编码错误
```

try语句也支持else从句. else从句必须放在最后一个except从句后. 这块代码只在try块中的语句没有引发异常的时候运行.例如:

```python
try:
   f = open('foo', 'r')
except IOError:
   print 'Unable to open foo'
else:
   data = f.read()
   f.close()
```

finally语句定义了在try块中代码的结束操作,例如:

```python
f = open('foo','r')
try:
   # Do some stuff
   ...
finally:
   f.close()
   print "File closed regardless of what happened."
```

finally语句并不用于捕获异常.它用来指示无论是否发生异常都要执行的语句块。如果没有引起异常,finally块中的语句将在try块中语句执行完毕后执行;如果有异常发生,控制将先传递到finally块中的第一条语句.在这块语句执行完后,异常被自动再次引发,然后交由异常处理语句处理. finally和except语句不能在同一个try语句中出现. Table 5.1列出了Python中定义的全部内建异常类型.(关于异常的更多细节,参见附录A)

可以通过异常名称来访问一个异常。例如:

```
try:
     statements
except LookupError:     # 捕获 IndexError 或 KeyError
     statements
或
try:
     statements
except StandardError:   # 捕获任何内建的异常类型
     statements
```


## 定义新的异常

所有的内建异常类型都是使用类来定义的.要定义一个新的异常，就创建一个父类为`exceptions.Exception`的新类:

```python
import exceptions
# Exception class
class NetworkError(exceptions.Exception):
     def __init__(self,args=None):
         self.args = args
```

args应该像上面那样使用.这样就可以使用raise语句来引发这个异常,并显示出错误返回信息以及诊断,如:

```
raise NetworkError, "Cannot find host."
```

通过调用[NetworkError](https://wiki.woodpecker.org.cn/moin/NetworkError)("Cannot find host.")可以创建一个[NetworkError](https://wiki.woodpecker.org.cn/moin/NetworkError)异常的实例. 如：

```python
a=NetworkError("Cannot find host.")
print a                 #得到 Cannot find host.
```

如果你使用一个不是 self.args 的属性名或你根本没有这个属性, 异常实例就没有这种行为.

当使用 raise 语句有意引发一个异常时, raise语句的可选参数将做为该异常的构造函数(`__init__()`方法)参数.如果异常的构造函数需要一个以上参数,有两种方法可以用来引发这种异常:

```python
import exceptions
# Exception class
class NetworkError(exceptions.Exception):
     def _ _init_ _(self,errno,msg):
     self.args = (errno, msg)
     self.errno = errno
     self.errmsg = msg

# 方法一
raise NetworkError(1, 'Host not found')

# 方法二
raise NetworkError, (1, 'Host not found')
```

基于类的这种异常体制让你能够轻易创建多级异常.例如,前边定义的 `NetworkError`异常可以用做以下异常的基类:

```python
class HostnameError(NetworkError):
    pass

class TimeoutError(NetworkError):
    pass

def error3():
    raise HostnameError

def error4():
    raise TimeoutError

try:
    error3()
except NetworkError:
    import sys
    print sys.exc_type    # 打印出异常类型
```

在这个例子中`except NetworkError` 语句能捕获任何从`NetworkError`中继承而来的异常. 通过变量 sys.exc_type可以得到这个特殊异常的名称. sys.exc_info()函数用于返回最近一个异常的信息(不依靠全局变量,属于安全线程).

## 断言和__debug__

assert语句用来断言某个条件是真的,常用于程序调试. assert语句的一般格式为：

assert test [, data]

test是一个表达式，它返回True或False. 如果test的值为假, assert语句就引发[AssertionError](https://wiki.woodpecker.org.cn/moin/AssertionError)异常, 可选的data字符串将被传递给这个异常.例如:

```python
def write_data(file,data):
    assert file, "write_data: file is None!"
    ...
```

实际上assert语句在执行时会被实时翻译为下面的代码:

```python
if __debug__:
   if not (test):
      raise AssertionError, data
```

`__debug__`是一个内建的只读值,除非解释器运行在最佳化模式(使用 -O 或 -OO 选项)，否则它的值总是 True. 虽然`__debug__`被设计为供 assert 语句使用,你仍然可以在任何自定义调试代码中使用它.

assert语句不能用于用来确保程序执行正确的场合,因为该语句在最佳化模式下会被忽略掉.尤其不要用assert来检查用户输入. assert语句用于正常情况下应该总是为真的场合;若assert语句引发了异常,那就代表程序中存在bug,是程序员出了问题而不是用户出现了问题.

如果打算将上边的 write_data() 函数交付给最终用户使用, assert语句就应该使用if语句和错误处理语句来重写.