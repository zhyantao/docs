# 第六章 函数与函数编程

为便于代码维护，绝大多数子程序都被分解并重新组织为函数以使代码模块化。 在Python中定义一个函数很简单,Python从其它函数编程语言中借鉴了很多有用的思路用来简化某些特定任务。本章的主题是函数,匿名函数,函数编程特性及eval()与execfile() 函数和exec语句.还详细描述了列表内涵(list comprehensions),一个强大的列表构建方法.

## 函数

函数使用def语句定义:

```python
def add(x,y):
    return x+y
```

要调用一个函数,只要使用函数名加上小括号括起来的参数表就可以了,例如 `a = add(3,4)`. 参数的顺序和个数必须和函数定义中的相匹配.否则会引发`TypeError`异常.

定义函数的时可以使用参数默认值，如:

```
def foo(x,y,z = 42):
```

若函数定义中有存在默认值的参数,这个参数就是可选参数.

默认参数的值在函数定义的时候就被决定,并且不会改变,例如:

```python
a = 10
def foo(x = a):
    print x
a = 5               # Reassign 'a'.
foo()               # Prints '10' (默认值没有改变)
```

但是,若使用可变对象作为默认参数值,则会有意料之外的情况发生:

```python
a = [10]
def foo(x = a):
    print x
a.append(20)
foo()              # Prints '[10, 20]'
```

如果最后一个参数名前有星号(*),函数就可以接受可变数量的参数,这些不定数量的参数将做为一个元组传递给函数:

```python
def fprintf(file, fmt, *args):
    file.write(fmt % args)

# fprintf.args 被赋值为 (42, "hello world", 3.45)
fprintf(out,"%d %s %f", 42, "hello world", 3.45)
```

在这个例子中,所有剩下的参数都被放入一个元组,赋值给args. 使用*args还可以把元组args传递给另个函数:

```python
def printf(fmt, *args):
        # Call another function and pass along args
        fprintf(sys.stdout, fmt, *args)
```

你也可以明确给每个形参名字绑定一个特定值(这称为关键字参数),然后传递给一个函数，如下:

```python
def foo(w,x,y,z):
    print w,x,y,z

#以关键字参数形式调用函数
foo(x=3, y=22, w='hello', z=[1,2])
```

使用这种方式调用函数,参数可以是任意顺序(不必与定义时顺序相同).但是,除非你省略的参数有默认值,否则你必须显式的给函数中所有形参名字指定一个值.如果是省略了某个必须的参数或你提供了一个函数定义中不存在的形参名字,就会引发`TypeError`异常.

传统的参数与关键字参数可以在同一个函数调用中混合使用,一个前提是必须先给出固定位置的参数,例如:

```
foo('hello', 3, z=[1,2], y=22)
```

如果一个函数定义中的最后一个形参有 ** （双星号）前缀,所有正常形参之外的其他的关键字参数都将被放置在一个字典中传递给函数,例如:

```python
def spam(**parms):
    print "You supplied the following args:"
    for k in parms.keys():
        print "%s = %s" % (k, parms[k])
spam(x=3, a="hello", foobar=(2, 3))
```

常规参数，*参数及**参数可以同时使用，这时**参数必须位于参数表的最后:

```python
# Accept variable number of positional or keyword arguments
def spam(x, *args, **keywords):
    print x, args, keywords
```

使用**关键字语法也可以把关键字参数传递给另一个函数，如:

```python
def callfunc(func, *args, **kwargs):
    print args
    print kwargs
    func(*args, **kwargs)
```

从Python 2.1开始,函数和方法可以拥有任意的属性,例如:

```python
def foo():
    print "Hello world"

foo.secure = 1
foo.private = 1
```

```
       注意：这仅仅是自定义函数的特权，内建函数或者类的方法是没有这种行为的。 --WeiZhong
```

函数的属性被储存在一个字典中(函数的 `__dict__` 属性).

某些特定应用程序如语法分析器或网络应用程序需要在一个函数中携带附加信息，函数属性完美的满足了这一需求.在Python2.1之前,只能用文档字符串来储存这些信息（这有很大的局限性，比如只能存储字符串对象，并且有违文档字符串功能的初衷).

## 参数传递和返回值

当调用一个函数时,它的参数是按引用传递给.如果函数的实参一个可变对象(如列表或字典)，则函数内对该对象的修改将会影响到函数之外。例如:

```python
a = [1,2,3,4,5]
def foo(x):
    x[3] = -55    # 修改 x 中的一个元素

foo(a)            # 传递 a
print a           # 显示 [1,2,3,-55,5]
```

return语句用于从函数中返回一个对象。如果没有指定返回对象或者return语句被省略,则会返回一个None对象.如果要返回多个值，可以通过返回一个元组或其它包含对象来完成。

```python
def factor(a):
    d = 2
    while (d <= (a/2)):
        if ((a/d)*d == a):
              return ((a/d),d)
        d = d + 1
    return (a,1)
```

如果返回值是一个元组，可以通过下面的方式来将返回值一次赋给多个独立变量:

```python
x,y = factor(1243)    # 返回的值被赋值给 x 和 y.
(x,y) = factor(1243)  # 同样的效果 
```

## 作用域规则

当一个函数开始运行,就会创建一个新的局部名字空间。该名字空间用来存放函数的形参名字及该函数中所使用的全部局部变量名。当解析一个变量名时,解释器首先在这个局部名字空间中搜索.如果没有找到,再接着搜索全局名字空间.一个函数的全局名字空间就是定义该函数的模块.如果在全局名字空间中还没有找到匹配,解释器接着在内建名字空间中搜索.若仍然找不到这个变量名,则引发`NameError`异常.

名字空间的一个特性是：在函数内部即使有一个变量与一个全局变量同名，也各不相干（因为它们位于不同的名字空间）.例如下边的代码:

```python
a = 42
def foo():
    a = 13
foo()
print a 
```

尽管我们在函数 foo 中修改了变量 a 的值,这个例子返回的结果仍然是 42 .如果一个变量在函数内部被赋值,则它一定是这个函数的局部变量(除非事先使用了 global 关键字)。在函数foo中的变量 a 其实是一个全新的值为 13 的对象，与函数外的 a 是不同的对象. 要在函数内部使用全局变量, 你应该在函数内使用global语句. global语句明确的声明一个或多个变量(如果有多个变量，以逗号分隔这些变量)属于全局名字空间. 例如:

```python
a = 42
def foo():
    global a        # 'a' 在全局名字空间
    a = 13
foo()
print a
```

所有的Python版本都允许嵌套的函数定义.但在Python 2.1之前的版本,嵌套函数并未提供嵌套作用域.因此在老版本的Python中，嵌套函数的运行结果有可能与你的预期不同。比如下面这个例子,虽然它是合法的,但在Python2.0中，它的执行并不象你想象的那样:

```python
def bar():
  x = 10
  def spam():            # 嵌套函数定义
       print 'x is ', x  # 在bar()的全局名字空间中寻找x
  while x > 0:
       spam()            # 若在Python2.0中运行该代码 程序会报错 : NameError on 'x'
       x -= 1
```

在Python2.1之前的版本中,当嵌套函数spam()运行时,它的全局名字空间会与bar()相同,都是函数被定义的模块.所以spam()无法得到它希望得到的bar()名字空间中的变量,这就引发了`NameError`异常.

从Python 2.1开始支持嵌套作用域(这样,上边的例子就会正常运行)：解释器将首先在局部名字空间中搜索变量名,然后一层层向外搜索，最后搜索全局名字空间和内建名字空间。注意嵌套范围在Python 2.1是一个可选的功能,只有当你的程序包含` from __future__ import nested_scopes `时才启用该功能.(具体细节参见在第十章--运行环境).另外,如果你需要考虑和较老Python版本的兼容性,那么就应该避免使用嵌套函数.

```
        注：Python 2.4中该功能已经是内建功能，不需要做那个 from __future__ import nested_scopes 操作了 --WeiZhong
```

如果一个局部变量在它被赋值之前使用,会引发一个`UnboundLocalError`异常,例如:

```python
def foo():
    print i       # 导致UnboundLocalError exception异常
    i = 0
```

## 递归

Python对递归函数调用的次数作了限制.函数 sys.getrecursionlimit()返回当前允许的最大递归次数,而函数sys.setrecursionlimit()可以改变该函数的返回值.默认的最大递归次数为1000.当一个函数递归次数超过最大递归次数时,就会引发`RuntimeError`异常.

## apply()函数

`apply(func [, args [, kwargs ]])` 函数用于当函数参数已经存在于一个元组或字典中时间接的调用函数. args是一个包含将要提供给函数的按位置传递的参数的元组. 如果省略了args,任何参数都不会被传递. kwargs是一个包含关键字参数的字典.下面的语句效果是一样的:

```python
foo(3,"x", name='Dave', id=12345)
apply(foo, (3,"x"), { 'name': 'Dave', 'id': 12345 })
```

在Python较老的版本里, apply()是在当参数已经位于元组或字典中时调用函数的唯一机制.不过现在,你还可以使用更直接更简单的方式,如下:

```python
a = (3,"x")
b = { 'name' : 'Dave', 'id': 12345 }
foo(*a,**b)     # 与上边的代码相同
```

## lambda操作符

lambda语句用来创建一个匿名函数(没和名字绑定的函数):

```
lambda args: expression
```

args是一个用逗号分隔的参数, expressin是一个调用这些参数的表达式,例如:

```python
a = lambda x,y : x+y
print a(2,3)              # 打印出 5
```

lambda定义的代码必须是一个合法的表达式.多重语句和其他非表达式语句(如print, for, while等)不能出现在lambda语句中. lambda表达式也遵循和函数一样的作用域规则.

```
        lambda 已经是过时的语句，即将被废除。 --WeiZhong
```

## map(), zip(), reduce(), 和filter()

t = map(func, s )函数将序列s中的每个元素传递给func函数做参数, 函数的返回值组成了列表 t. 即t[i] = func(s[i]). 需要注意的是, func函数必须有只有一个参数,例如:

```python
a = [1, 2, 3, 4, 5, 6]
def foo(x):
    return 3*x
b = map(foo,a)   # b = [3, 6, 9, 12, 15, 18]
```

上边的例子中的函数也可以用匿名函数来创建:

```python
b = map(lambda x: 3*x, a)   # b = [3, 6, 9, 12, 15, 18]
```

map ()函数也可以用于多个列表,如 t = map(func, s1, s2, ..., sn ). 如果是这种形式,t中的每个元素 t [i ] = func(s1[i ], s2[i ], ..., sn[i ]) .func函数的形参个数必须和列表的个数(n)相同,结果与s1,s2, ... sn中的最长的列表的元素个数相同.在计算过程中,短的列表自动用None扩充为统一长度的列表.

如果函数func为None,则func就被当成是恒等函数处理。这样函数就返回一个包含元组的列表:

```python
a = [1,2,3,4]
b = [100,101,102,103]
c = map(None, a, b)   # c = [(1,100), (2,101), (3,102), (4,103)]
```

上边这个例子也可以用 zip(s1 , s2 , ..., sn ) 函数来完成. zip()用来将几个序列组合成一个包含元组的序列,序列中的每个元素t[i ] = (s1[i ], s2[i ], ..., sn[i ]). 与map()不同的是, zip()函数将所有较长的序列序列截的和最短序列一样长:

```python
d = [1,2,3,4,5,6,7]
e = [10,11,12]
f = zip(d,e)   # f = [(1,10), (2,11), (3,12)]
```

reduce(func , s )函数从一个序列收集信息,然后只返回一个值(例如求和,最大值,等).它首先以序列的前两个元素调用函数,再将返回值和第三个参数作为参数调用函数,依次执行下去,返回最终的值. func函数有且只有两个参数.例如:

```python
def sum(x,y):
    return x+y

b = reduce(sum, a)   # b = (((1+2)+3)+4) = 10
```

filter(func ,s)是个序列过虑器，它使用func()函数来过滤s中的元素。使func返回值为false的元素被丢弃，其它的存入filter函数返回的列表中,例如:

```python
c = filter(lambda x: x < 4, a)   # c = [1, 2, 3]
```

如果函数func为None,则func就被当成是恒等函数处理。这样,函数就返回序列s中值为True的元素.

## 列表内涵

列表内涵可以代替许多调用map()和filter()函数的操作.列表内涵的一般形式是:

```
[表达式 for item1 in 序列1
            for item2 in 序列2
            ...
            for itemN in 序列N
            if 条件表达式]
```

上边的例子等价于:

```python
s = []
for item1 in sequence1:
    for item2 in sequence2:
        ...
           for itemN in sequenceN:
               if condition: s.append(expression)
```

Listing 6.1 中的例子可以帮助你理解列表内涵

**Listing 6.1 列表内涵**

```python
import math
a = [-3,5,2,-10,7,8]
b = 'abc'
c = [2*s for s in a]          # c = [-6,10,4,-20,14,16]
d = [s for s in a if s >= 0]  # d = [5,2,7,8]
e = [(x,y) for x in a         # e = [(5,'a'),(5,'b'),(5,'c'),
           for y in b         #      (2,'a'),(2,'b'),(2,'c'),
           if x > 0]          #      (7,'a'),(7,'b'),(7,'c'),
                              #      (8,'a'),(8,'b'),(8,'c')]
f = [(1,2), (3,4), (5,6)]
g = [math.sqrt(x*x+y*y)       # f = [2.23606, 5.0, 7.81024]
     for x,y in f]
h = reduce(lambda x,y: x+y,   # 平方根的和
           [math.sqrt(x*x+y*y)
            for x,y in f])
```

提供给列表内涵的序列不必等长，因为系统内部使用嵌套的一系列for循环来迭代每个序列中的每个元素，然后由if从句处理条件表达式,若条件表达式为真,计算表达式的值并放入到列表内涵返回的序列中. if从句是可选的.

当使用列表内涵来构建包含元组的列表时,元组的值必须放在括号里.例如 `[(x,y) for x in a for y in b]`是一个合法的语句,而`[x,y for x in a for y in b]`则不是.

最后,你应该注意在一个列表内涵中定义的变量是与列表内涵本身有同样的作用域,在列表内涵计算完成后会继续存在.例如 [x for x in a] 会覆盖内涵外先前定义的x ,最终 x 的值会是 a 中的最后一个元素的值.

## eval(), exec, execfile(),和compile()

eval(str [,globals [,locals ]])函数将字符串str当成有效Python表达式来求值，并返回计算结果。

同样地, exec语句将字符串str当成有效Python代码来执行.提供给exec的代码的名称空间和exec语句的名称空间相同.

最后，execfile(filename [,globals [,locals ]])函数可以用来执行一个文件,看下面的例子:

```
        >>> eval('3+4')
        7
        >>> exec 'a=100'
        >>> a
        100
        >>> execfile(r'c:\test.py')
        hello,world!
        >>> 
```

默认的，eval(),exec,execfile()所运行的代码都位于当前的名字空间中. eval(), exec,和 execfile()函数也可以接受一个或两个可选字典参数作为代码执行的全局名字空间和局部名字空间. 例如:

```python
globals = {'x': 7,
           'y': 10,
           'birds': ['Parrot', 'Swallow', 'Albatross']
          }
locals = { }

# 将上边的字典作为全局和局部名称空间
a = eval("3*x + 4*y", globals, locals)
exec "for b in birds: print b" in globals, locals   # 注意这里的语法
execfile("foo.py", globals, locals)
```

如果你省略了一个或者两个名称空间参数,那么当前的全局和局部名称空间就被使用.如果一个函数体内嵌嵌套函数或lambda匿名函数时,同时又在函数主体中使用exec或execfile()函数时， 由于牵到嵌套作用域，会引发一个[SyntaxError](https://wiki.woodpecker.org.cn/moin/SyntaxError)异常.（此段原文:If you omit one or both namespaces, the current values of the global and local namespaces are used. Also,due to issues related to nested scopes, the use of exec or execfile() inside a function body may result in a [SyntaxError](https://wiki.woodpecker.org.cn/moin/SyntaxError) exception if that function also contains nested function definitions or uses the lambda operator.）

```
        在Python2.4中俺未发现可以引起异常 --WeiZhong
```

注意例子中exec语句的用法和eval(), execfile()是不一样的. exec是一个语句(就象print或while), 而eval()和execfile()则是内建函数.

```
        exec(str) 这种形式也被接受，但是它没有返回值。 --WeiZhong
```

当一个字符串被exec,eval(),或execfile()执行时,解释器会先将它们编译为字节代码，然后再执行.这个过程比较耗时,所以如果需要对某段代码执行很多次时,最好还是对该代码先进行预编译,这样就不需要每次都编译一遍代码，可以有效提高程序的执行效率。

compile(str ,filename ,kind )函数将一个字符串编译为字节代码, str是将要被编译的字符串, filename是定义该字符串变量的文件，kind参数指定了代码被编译的类型-- 'single'指单个语句, 'exec'指多个语句, 'eval'指一个表达式. cmpile()函数返回一个代码对象，该对象当然也可以被传递给eval()函数和exec语句来执行,例如:

```python
str = "for i in range(0,10): print i"
c = compile(str,'','exec')      # 编译为字节代码对象
exec c                          # 执行

str2 = "3*x + 4*y"
c2 = compile(str2, '', 'eval')  # 编译为表达式
result = eval(c2)               # 执行  
```