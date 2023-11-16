# 第三章 类型和对象

Python 程序中的一切数据都是对象。对象包括自定义对象及基本的数据类型如数值、字符串、列表、字典等。你能够以类或扩展类型的方式创建自定义对象。本章主要描述 Python对象模型及第四章--运算符与表达式中要用到的一些预备知识。

## 术语

程序中的一切数据都是对象，每个对象都有三个基本属性，即标识(类似人的标识证号)、类型和值。

例如，当你写下 `a = 42` 这行代码，你就创建了一个值为 42 的整数对象。 `type()`和`id()`函数用来查看对象的类型标识。`id(a)`可以查看该对象的标识(当前的实现是该对象在内存中的位置)。在这个例子中，a就是这个位置的引用。

一个对象的类别决定了可以对该对象进行何种操作(如，这个对象有长度吗?)。当一个特定类型的对象被创建时，这个对象被称为该类型的一个实例(注意：不要将类型的的实例和用户自定义类的实例混淆)。在一个对象被创建之后，它的标识和类型就再不能被改变。某些对象的值是可变的，这些对象就被称为可变对象(mutable);另一些对象的值是不可变的，那就被称为不变对象`(immutable)`。某类对象可以包含其它对象的引用，我们称这类对象为容器。

```
注1:关于类型的不可改变
从python2.2开始，Python开发小组开始有步骤的合并某些类别和类，因此书中的某些结论可能不是百分之百精确和完整。在某些特定条件下，有可能允许改变一个对象的类型。但是，在本手册扩展修订之前，我们就应该一如既往的认为这些经典类型是不可改变的。考虑到兼容性，python2.2和2.3也是这样默认处理的。

注2:不变对象的不可变并不是绝对的，当一个不变容器对象包含一个可变对象的引用时，可变对象的值变化会引起该不变容器对象的值发生变化。这种情况下，我们仍然认为该容器对象为不变对象，因为该容器所包含并不是引用对象的值，而仅仅是该对象的引用，这里的引用可以理解为该对象的内存地址。不管被包含对象的值如何变化，被包含对象的引用确实是始终不变的)。一个对象是否可变取决于它的类型，举例来说，数字、字符串、tuple类型是不可变类型，字典与列表是可变类型。

--WeiZhong
```

除了保存值以外，许多对象还拥有一系列的属性`(attribute)`。广义的属性是指对象的相关数据或者该对象能够具有的行为（如狗对象拥有颜色体重等相关数据，还拥有叫、吃、跑等行为，这些都是对象的广义的属性），狭义的属性只包含对象的相关数据，对于对象的行为，更常用的叫法是方法`(method)`。方法是对象可调用的属性，一个对象有多少个方法`(method)`，它就具有多少种行为。要访问一个对象的属性或者调用一个对象方法，使用点(.)操作符：

```
a = 3 + 4j              # 创建一个复数
r = a.real              # 取得一个复数的实部，访问该对象的一个属性

b = [1, 2, 3]           # 创建一个列表)
b.append(7)             # 使用 append 方法为列表加入新的元素
```

## 对象的标识与类型

内建函数id()返回一个对象的标识。该返回值是一个整数，目前的实现该整数通常就是对象在内存中的位置。is 运算符用来比较两个对象的标识。内建函数type()返回一个对象的类型:

```python
# 比较两个对象
def compare(a,b):
    print 'The identity of a is ', id(a)
    print 'The identity of b is ', id(b)
    if a is b:
        print 'a and b are the same object'
    if a == b:
        print 'a and b have the same value'
    if type(a) is type(b):
        print 'a and b have the same type'
```

对象的类型也是对象，这个对象具有唯一性。对同一类型的所有实例应用`type()`函数总是会返回同一个类型对象。因此，类型之间可以使用 `is` 运算符来进行比较。标准模块 types 内包含所有内建类型对象，我们可以通过它来完成类型检查工作:

```python
import types
if type(s) is types.ListType:
    print 'Is a list'
else:
    print 'Is not a list'
```

若要比较两个自定义类实例对象的类型，最好是使用`isinstance()`函数。 函数 `isinstance(s,C)`用于测试 s 是否是 C 或 C 的子类的实例。详细内容请参阅第七章--类和面向对象的编程。

## 引用计数与垃圾收集

一切对象都是引用计数的。当分配一个新的名字给一个对象，或者其将放入到一个容器比如列表、元组、或者字典中，该对象的引用计数就会增加1次。如:

```python
a = 3.4      # 创建一个对象 '3.4'，引用计数为 1
b = a        # 对象 '3.4' 引用计数增加 1，此时对象 '3.4' 的引用计数为 2
c = []
c.append(b)  # 对象 '3.4' 引用计数增加 1，此时对象 '3.4' 的引用计数为 3
```

例子中创建了一个包含值3.4的一个对象。变量 a 是一个指向该对象的名字。当用 a 来为 b 赋值时，b 成为同一个对象新的名称，此时对象的引用计数就会增1。同样地， 当你把 b 放入一个列表中时，对象的引用计数再次增1。在例子中，自始至终只有一个值为 3.4 的整数对象，b 与 c[0] 都仅仅是该对象的引用。

del语句、脱离变量作用域或者变量被重新定义，都会使对象的引用计数减少。

```python
del a           # 直接删除一个引用，对象 3.4 引用减1
b = 7.8         # 某个引用被赋新值，对象 3.4 引用减1
c[0]=2.0        # 某个引用被赋新值，对象 3.4 引用减1
```

当一个对象的引用计数减少至零时，它就会在适当时机被垃圾回收车拉走。然而，特定情况(循环引用)会阻止垃圾回收车销毁不再使用的对象，看下面的例子：

```python
a = { }         # a 的引用为 1
b = { }         # b 的引用为 1
a['b'] = b              # b 的引用增 1，b的引用为2
b['a'] = a              # a 的引用增 1，a的引用为 2
del a           # a 的引用减 1，a的引用为 1
del b           # b 的引用减 1,  b的引用为 1
```

在这个例子中,del语句减少了 a 和 b 的引用计数并删除了用于引用的变量名，可是由于两个对象各包含一个对方对象的引用，虽然最后两个对象都无法通过名字访问了，但引用计数并没有减少到零。因此这个对象不会被销毁，它会一直驻留在内存中，这就造成了内存泄漏。为解决这个问题，Python解释器会定期的运行一个搜索器，若发现一个对象已经无法被访问，不论该对象引用计数是否为 0 ，都销毁它。这个搜索器的算法可以通过 gc 模块的函数来进行调整和控制。具体内容参阅附录A：Python 库。

## 引用与副本

当运行语句 `a = b` 时，就创建了对象 b 的一个新引用a。对于不可变对象(数字或字符串等)，改变对象的一个引用就会创建一个新对象。

```python
a=100                   #创建一个新对象 100
b=a                     #对象 100 增加了一个新的引用 b
print id(a),id(b)       #打印 a 和 b 的标识，你会发现两个标识是相同的
b=20                    #现在 b 不再是 a 的引用，变成新对象 20 的一个引用了
print id(a),id(b)       #现在 a 和 b 的标识不再相同
```

对于可变对象(列表或字典等)，改变对象的一个引用就等于改变了该对象所有的引用，见下例:

```python
b = [1,2,3,4]
a = b                   # a 是 b 的一个引用
a[2] = -100             # 改变 a 中的一个元素
print b                 # b的值也随之改变为 '[1, 2, -100, 4]'
```

因为 a 和 b 指向相同的对象，所以改变了 a 就等于改变了 b 。为了避免这种情况，你应该创建一个可变对象的副本，然后对该副本进行操作。这样就不会影响到原始对象了。

有两种方法用来创建可变对象的副本：浅复制`(shallow copy)`和深复制`(deep copy)`。浅复制创建一个新对象，但它包含的子元素仍然是原来对象子元素的引用:

```python
b = [ 1, 2, [3,4] ]
a = b[:]                # 创建b的一个 浅拷贝 a
a.append(100)           # a 对象添加一个新元素
print b                 # 打印 b 的值，得到 '[1,2, [3,4]]'， b 没有改变
a[0]=-100               # 改变 a 的一个不可变子对象
print b                 # 打印 b 的值，得到 '[1,2, [3,4]]'， b 没有改变
a[2][0] = -100          # 改变 a 的一个可变子对象
print b                 # 打印 b 得到 '[1,2, [-100,4]]'，b 被改变了
```

a 和 b 虽然是彼此独立的对象，但他们包含的元素却是共享的。这样，修改 a 中的一个可变元素也会影响 b 中的这个可变元素。

深复制创建一个新对象，并递归复制所有子对象。python并没有内建的深复制函数，不过在标准库中提供有一个copy模块，该模块有一个deepcopy()函数可以漂亮的干这件事：

```python
import copy
b = [1, 2, [3, 4] ]
a = copy.deepcopy(b)
```

## 内建类型

Python的解释器内建数个大类，共二十几种数据类型，表 3.1列出了全部内建类型。一些类别包含最常见的对象类型，如数值、序列等，其它类型则较少使用。后面几节将详细描述这些最常用的类型。

```
表 3.1 Python内建类型
分类                            类型名称                        描述
None                            NoneType                        null 对象
数值                            IntType                         整数
                                LongType                        任意精度整数
                                FloatType                       浮点数
                                ComplexType                     复数
序列                            StringType                      字符串
                                UnicodeType                     Unicode字符串
                                ListType                        列表
                                TupleType                       元组
                                XRangeType                      xrange()函数返回的对象
                                BufferType                      buffer()函数返回的对象
映射                            DictType                        字典
可调用类型                      BuiltinFunctionType             内建函数
                                BuiltinMethodType               内建方法
                                ClassType                       类
                                FunctionType                    用户定义函数
                                InstanceType                    类实例
                                MethodType                      Bound class method
                                UnboundMethodType               Unbound class method
模块                            ModuleType                      模块
类                              ClassType                       类定义
类实例                          InstanceType                    类实例
文件                            FileType                        文件对象
内部类型                        CodeType                        字节编译码
                                FrameType                       执行框架
                                TracebackType                   异常的堆栈跟踪
                                SliceType                       由扩展切片操作产生
                                EllipsisType                    在扩展切片中使用
```

注意: [ClassType](https://wiki.woodpecker.org.cn/moin/ClassType)和[InstanceType](https://wiki.woodpecker.org.cn/moin/InstanceType)在表中之所以出现两次，是因为在特定环境下类及类实例都能被调用。

### None类型

None表示空对象。如果一个函数没有显式的返回一个值，None就被返回。None经常被用做函数中可选参数的默认值。None对象没有任何属性。None的布尔值为假。

### 数值类型

Python拥有四种数值类型:整型,长整型,浮点类型,以及复数类型。所有数值类型都是不可变类型。

整数类型用来表示从-2147483648 到 2147483647之间的任意整数(在某些电脑系统上这个范围可能会更大，但绝不会比这个更小)。在系统内部，一个整数以一个32位或者更多位的二进制补码形式储存。如果某次整数运算的结果超出了这个表示范围，一般情况下Python会自动将运算结果由整型升级为长整型返回，不过在有些情况下会引发一个溢出异常，我们正在努力彻底消灭这个异常`(OverflowError)`。

长整数可以表示任意范围的整数(只要你的内存足够大就行)。

Python中只有双精度浮点数(64位)，它提供大约17个数字的精确度和-308到308的指数，这与C中的double类型相同。Python不支持32位单精度的浮点数。如果你的程序很关心精确度和存储空间，推荐你使用`Numerical Python (`[http://numpy.sourceforge.net](http://numpy.sourceforge.net/)`)`。

复数使用一对浮点数表示，虚数 z 的实部和虚部分别用 z.real 和 z.imag 访问。

### 序列类型

序列是由非负整数索引的对象的有序集合。它包括字符串、Unicode字符串、列表、元组、xrange对象以及缓冲区对象。字符串和缓冲区对象是字符序列，xrange对象是整数的序列，列表和元组是任意Python对象的序列。字符串、Unicode字符串及元组是不可变序列，列表是可变序列，允许插入，删除，替换元素等操作。缓冲区对象将在本节后面详细描述。

Table 3.2列出所有序列对象均支持的操作及方法。序列 s 中的元素 i 使用索引运算符 s[i] 来访问，通过切片运算符 s[i:j] 可以得到一个序列的子序列(这些运算符在第四章有详细介绍)。内建函数 `len(s) 可以返回任意序列 s 的长度。你还能使用内建函数 min(s) 和 max(s) `来获得一个序列的最大值和最小值。不过，这两个函数必须使用在元素可排序的序列中(典型的可排序序列是数值和字符串)。

Table 3.3介绍了可变序列(如列表)支持的其它操作

**Table 3.2. 所有序列类型都支持的操作和方法**

```
项目            描述
s [i ]          返回序列s的元素i
s [i :j ]       返回一个切片
len(s )         序列中元素的个数
min(s)          s 中的最小值
max(s)          s 中的最大值
```

**Table 3.3. 可变序列适用的操作**

```
项目            描述
s [i] = v       给某个元素赋新值
s [i:j] = t     用 序列 t 中的所有元素替换掉 s 序列中的索引从 i 至 j 的元素。
del s[i]        删除序列 s 中索引为 i 的元素。
del s [i :j ]   删除序列 s 中的索引从 i 至 j 的元素
```

除此之外，列表还支持Table 3.4中的方法。内建函数` list(s) `把可以把任意一个序列对象转换为一个列表。如果 s 本身是一个列表，这个函数就创建一个 s 的浅拷贝。 `s.append(x) `方法可以在列表的末尾加入一个元素 `x`。 `s.index(x)` 方法在列表中查找值 `x` 第一次出现时的索引，若没有找到就引发一个`ValueError`异常。同样地，`s.remove(x)`方法删除第一次出现的值 `x`。` s.extend(t)`方法通过将链表 t 的所有元素添加到 s 的末尾来扩充列表s。` s.sort()`方法会将列表中的元素进行排序，该方法接受自定义比较函数，自定义比较函数必须有两个参数，若参数1小于参数2，则返回-1，若参数1等于参数2，返回0，否则就返回1。` s.reverse()`方法反转列表中的所有元素。`sort()和reverse()`方法都是直接操作列表中元素并返回None。

**Table 3.4. 列表的方法**

```
方法                    描述
list(s )                把序列s转换为一个列表
s.append(x)             把一个元素添加到列表的结尾,相当于` s[len(s):] = [x]`
s.extend(t)             将链表 t 的所有元素添加到 s 的末尾来扩充列表 s，相当于 `s[len(s):] = t`
s.count(x)              返回值 x 在列表 s 中出现的次数
s.index(x)              返回列表s中第一个值为 x 的元素的索引值
s.insert(i,x)           在 s[i] 前插入一个元素 x
s.pop([i])              返回 s[i] 的值并将 s[i] 元素从列表中删除。如果 i 被省略，` s.pop()` 就对最后一个元素进行操作。
s.remove(x )            删除列表中值为 x 的第一个元素
s.reverse()             翻转 s 中的全部元素
s.sort([cmpfunc ])      对列表 s 中的元素进行排序，cmpfunc 是一个可选的比较函数
```

### 字符串类型

Python拥有两种字符串类型。标准字符串是单字节字符序列，允许包含二进制数据和嵌入的null字符。 Unicode 字符串是双字节字符序列，一个字符使用两个字节来保存，因此可以有最多65536种不同的unicode字符。尽管最新的Unicode标准支持最多100万个不同的字符，Python现在尚未支持这个最新的标准。

标准字符串和Unicode字符串都支持表 3.5中的方法。虽然这些方法都是用于操作一个字符串实例，但所有的字符串方法都不会改变原始字符串。它们有的返回一个新得字符串，如` s.capitalize(), s.center(), s.expandtabs()`。有的返回True或者False,如特征测试方法 `s .isalnum() 和 s .isupper()`，值得一提的是，这些方法当字符串长度为零时返回False。` s .find()、 s .rfind()、s .index()、 s .rindex()` 方法被用来在 s 中寻找一个子串，如果找到子串，这些函数都返回s的整数索引值。 当找不到子串时,find()方法返回-1，而index()方法则引发一个 `ValueError` 异常。有很多数字符串方法接受两个可选的参数：`start 和` end` ，用于指定 s 中开始位置和结束位置的索引。`s.translate()`方法根据一个字典来转换原始字符串，该函数在附录A中的` string`模块中有详细描述。` s.encode()` 方法用来将字符串转换为指定的字符集，如'ascii'、 'utf-8' 或 'utf-16'等。这个方法主要用于将 Unicode字符串转换为适合输入输出的字符编码，关于此方法的的详细介绍在第九章--输入和输出。要了解更多关于字符串方法的细节请参阅附录A中的 string 模块。

**Table 3.5. 字符串方法**

```
方法                                    描述
s.capitalize()                          第一个字母变大写
s.count(sub [,start [,end ]])           子串sub出现的次数
s.encode([encoding [,errors ]])         改变字符串的编码                
s.startswith(prefix [,start [,end ]])   检查字符串的开头是否为prefix
s.endswith(suffix [,start [,end ]])     检查字符串的结尾是否是suffix       
s.expandtabs([tabsize ])                将制表符转换为一定数量的空格
s.find(sub [,start [,end ]])            返回子串 sub 首次出现的位置或者 -1
s.rfind(sub [,start [,end ]])           返回子串 sub 末次出现的位置或者 -1
s.index(sub [,start [,end ]])           返回子串 sub 首次出现的位置或者引起异常
s.rindex(sub [,start [,end ]])          返回子串 sub 末次出现的位置或者引发异常
s.isalnum()                             字符是否都为字母或数字
s.isalpha()                             字符是否都为字母
s.isdigit()                             字符是否都为数字
s.islower()                             字符是否都为小写
s.isspace()                             字符是否都为空白
s.istitle()                             检查字符是否为标题格式(每个单词的第一个字母大写)
s.isupper()                             字符是否都为大写
s.join(t)                               用 s 连接 t 中的所有字符串
s.center(width)                         在长度为 width 范围内将字符串置中
s.ljust(width )                         在宽度为 width 内左对齐
s.rjust(width )                         在宽度为 width 内右对齐
s.lower()                               s 中所有字符小写
s.upper()                               s 中所有字符大写
s.replace(old , new [,maxreplace ])     将子串 old 替换为 new
s.lstrip()                              删去字符串s开头的空白
s.rstrip()                              删去字符串s末尾的空白
s.strip()                               删去字符串s开头和末尾的空白
s.split([sep [,maxsplit ]])             将字符串 s 分割成一个字符串列表，其中 sep 为分隔符，maxsplit是最大分割次数
s.splitlines([keepends ])               将字符串按行分割为一个字符串列表，若keepends为1，则保留换行符'\n'
s.swapcase()                            串内字符大写变小写，小写变大写，没有大小写的不变
s.title()                               s 转换为标题格式(每个单词的第一个字母大写)
s.translate(table [,deletechars ])      使用字符转换表转换一个字符串
```

### XRangeType 类型

内建函数`range([i,]j[,stride])`建立一个整数列表，列表内容为`k(i <= k < j)`。第一个参数i和第三个参数stride是可选的，默认值分别为 0 和 1 。内建函数`xrange([i,]j[,stride])`与 `range` 有相似之处，但`xrange`返回的是一个不可改变的`XRangeType`对象。这是一个迭代器，也就是只有用到那个数时才临时通过计算提供值。当 j 值很大时，xrange能更有效地利用内存。`XRangeType`提供一个方法 `s.tolist()`，它可以将自己转换为一个列表对象返回。

### 缓冲区类型

缓冲区对象将内存的一个连续区域模拟为一个单字节字符序列。Python没有直接创建缓冲区对象的语句，你可以使用内建函数`buffer(obj[,offset[,size]])`来创建此类对象。 缓冲区对象与对象 obj 共享相同的内存，对于字符串切片操作或者其他字节数据操作来说，这样会有非常高的效率。另外， 缓冲区对象还可以用来访问其他Python类型储存的原始数据，比如`array`模块中的数组、 `Unicode`字符串等。缓冲器对象是否可变，取决于 obj 对象。

### 映射类型

映射类型用来表示通过关键字索引的任意对象的集合。和序列不同， 映射类型是无序的。映射类型可以使用数字、字符串、或其他不可变对象来索引。映射类型是可变类型。

字典是唯一的内建的映射类型。可以使用任何不可变的对象作为字典的关键字(如字符串、数字、元组等)。列表、字典、及包含可变对象的元组不可以作为关键字。(字典类型需要关键字的值保持不变)

使用索引运算符m[k](k为关键字)可以访问映射对象 m 中索引为 k 的元素。如果映射对象中没有 k 这个关键字，则引发`KeyError`异常。 len(m)函数返回一个映射对象的元素个数。表 3.6列出了映射对象可用的方法及操作。

**Table 3.6. 映射对象的方法和操作**

```
项目                    描述
len(m)                  返回m中的条目个数
m[k]                    返回关键字k索引的元素
m[k] = x                设置关键字k索引的值为x
del m[k]                删除一个元素
m.clear()               删除所有元素
m.copy()                返回m的一个浅拷贝
m.has_key(k)            若 m 中存在 key k 返回True,否则返回False
m.items()               返回包含所有关键字和对应值(key ,value )的列表
m.keys()                返回由所有关键字组成的列表
m.update(b)             将字典b中的所有对象加入m
m.values()              返回一个包含m中所有对应值的列表
m.get(k[,v])            返回m[k]，若m[k]不存在时，返回 v
m.setdefault(k[,v])     返回m[k]，若m[k]不存在时，返回 v 并设置m[k] = v
m.popitem()             从 m 中随机删除一个元素，并以元组的形式返回其关键字和值
```

### 可调用类型

可调用类型表示所有允许以函数方式调用的对象。它包括用户定义函数、用户定义方法，内建函数、内建方法、classic类及其实例、new-style 类及其实例。

#### 用户定义函数

用户定义函数是在module 层使用 def 语句或者 lambda 操作符创建的可调用对象(在类层次定义的函数有专门的名字叫做方法)。函数是一类对象，用法和其它内建对象相似，允许将函数赋值给变量，也可以把函数放入列表、元组和字典中。看下面的例子:

```python
def foo(x,y):
    print '%s + %s is %s' % (str(x), str(y), str(x+y))
 
# 指定为一个新的变量
bar = foo
bar(3,4)            # 调用上边定义好的foo
 
# 放入一个字典中
d = { }
d['callback'] = foo
d['callback'](3,4)  # 调用foo
```

**用户定义函数 f 有如下属性:**

- 

  

  

  

  

  

  

  

  

  

  ```
  属性                                    描述
  f.__module__                            函数定义所在的模块名
  f.__doc__ 或 f.func_doc                 文档字符串
  f.__name__ 或 f.func_name               函数名 (从2.4版开始该属性由只读变为可写)
  f.__dict__ 或 f.func_dict               支持任意函数属性的函数名字空间
  f.func_code                             (函数编译后产生的)字节码
  f.func_defaults                         包含所有默认参数的元组
  f.func_globals                          函数所在模块的全局名称空间的字典(只读)
  f.func_closure                          None or a tuple of cells that contain bindings for the function's free variables. Read-only 
  ```

  

用户定义函数对象也支持任意属性(设定值或取出值)，举个例子来说，它可以用来夹带函数的元数据。用`(.)`操作符来存取这类属性。注意目前只有用户定义函数支持任意属性，内建函数是不支持任意属性这个特性的。(也许将来我们会考虑让内建函数也支持这个特性，也许....)

**用户自定义函数任意属性示例**

```
>>> def abc(x,y):
...     print x,y
...     
>>> abc.a=100
>>> abc.a
100
```

#### 用户定义方法

用户定义方法是仅作用于对象实例的函数。通常方法在一个类定义中定义，如Listing 3.1:

**Listing 3.1 定义一个方法**

```python
# 按优先级排序的队列
class PriorityQueue:
    def __init__(self):
          self.items = []           # 包含(priority, item)的列表
    def insert(self,priority,item):
          for i in range(len(self.items)):
                if self.items[i][0] > priority:
                        self.items.insert(i,(priority,item))
                        break
          else:
                self.items.append((priority,item))
    def remove(self):
          try:
                return self.items.pop(0)[1]
          except IndexError:
                raise RuntimeError, 'Queue is empty'
```

非绑定方法(unbound method)是类中定义方法的引用，它没有被绑定到具体的类实例。

```
m = PriorityQueue.insert        # m是一个非绑定方法
```

要调用一个非绑定方法，需要将一个类实例做为该方法的第一个参数来调用：

```python
pq = PriorityQueue()            #pq 是一个类实例
m = PriorityQueue.insert        #m 是一个非绑定方法
m(pq,5,"Python")                #等于调用 pq.insert(5,"Python")
```

绑定方法(bound method)就是实例方法的别名。

```python
pq = PriorityQueue()    # 创建 PriorityQueue 实例
n = pq.insert           # n 是一个绑定到 pq 实例的方法
```

绑定方法暗含了实例的引用，所以调用绑定方法时要象下面这样调用:

```
n(5,"Python")           # 等于调用 pq.insert(5,"Python")
```

绑定和非绑定方法无非是略略封装了一下常规函数，下表列出了方法对象的属性:

```
属性                      描述
m.im_self               引用类实例对象，如果是非绑定方法，im_self通常为 None(见下面小注)
m.im_func               引用类中定义的方法对象
m im_class              引用定义该方法的类
m.__doc__               等于 m.im_func.__doc__
m.__name__              等于 m.im_func.__name__
m.__module__            等于 m.im_func.__module__

小注: 当一个用户定义方法引用的是一个类方法时，不论是否绑定到类实例，它的 im_self属性都等于其 im_class 属性。 --WeiZhong
```

```
注意： 每次访问一个类或类实例的属性时都会有一次从函数对象到方法对象的转换。这个转换要占用CPU时间。在某些情况(对效率要求比较高的情况下)下，一个很有效的优化手段就是，用一个局部变量引用这个经常用到的类属性，然后调用这个局部变量。还要注意的是，只有类中的用户定义方法才会发生这种转换，其它可调用对象或不可调用对象不存在这种转换。另外需要注意的一点就是类实例的私有方法不需要这种转换。
```

#### 类和可调用的类实例

到现在为止，我们集中讨论了函数和方法。类和类实例也是可调用对象。当一个类被调用时,，就生成该类的一个实例。如果该类定义了一个`__init__()`方法，则这个方法就用来初始化新建的实例。上边例子中的`PriorityQueue`的创建就演示了这个行为。

如果一个类定义有一个特殊的方法`__call__()`，那么该类的实例也可以被调用。假设 x 是一个可调用的类实例，`x(args)`调用就等同于调用`x.__call__(args)`。

#### 内建函数及内建方法

可调用类型还有内建函数和内建方法。内建函数和内建方法的代码一般位于用C或C++写的扩展模块中。下表列出了内建方法可用的属性:

```
属性            方法
b.__doc__       文档字符串
b.__name__      函数/方法名
b.__self__      方法所绑定的实例(未绑定时，返回None)
b.__members__   方法的属性名(返回列表)
```

对于内建函数比如len()，它的`__self__是None`。这表示这个函数并没有绑定给任何特殊对象。而对于内建函数 `x.append()` 来说( x 是一个列表)，`__self__返回 x`。

### 模块类型

模块是容器对象。import语句用来将其它模块中包含的对象导入当前模块。举例来说，语句 import foo 中的 foo 就是一个模块对象。模块拥有自己的名字空间，这是通过模块的一个字典属性来实现的。这个名字空间可以通过模块对象的dict属性来访问。当一个模块的属性被访问(使用点操作符)时，比如访问 `m.x，Python 会自动的去访问 m.__dict__["x"]`。同样的，赋值操作 `m[x]=y 在内部被执行的其实是 m.__dict__[x]=y`。 模块对象拥有以下属性：

```
属性            描述
m.__dict__      保存模块名字空间的字典
m.__doc__       模块的文档字符串
m.__name__      模块名字
m.__file__      模块的文件名
m.__path__      当一个模块通过一个包被引用时，__path__是包的名字
```

```
注1:所有内建模块拥有没有__file__ 属性的特权。
注2:如果一个模块拥有 __path__ 属性，import 语句就会认为它是一个包(package)。当从一个包中 import 一个子模块时，将使用包的__path__属性而不是sys.path。
        --WeiZhong
```

### 类 类型

class语句用来创建类，第七章详细介绍了类。和模块类似，类也使用一个字典属性来维护自己的名称空间。访问类的属性时，比如 c.x 在执行行将被翻译成` c.__dict__["x"]`。如果在类的 `__dict__`里没有找到属性x，那么就会到该类的父类中寻找。如果有多个父类，则搜索按照父类`(base class)`在类定义中顺序从左至右，深度优先。属性赋值如 `c.y = 5，则总是更新 c 的__dict__`属性，而不会更新某个父类的字典。

**class对象定义的属性:**

```
属性            描述 
c.__dict__      类 c 的名字空间
c.__doc__       类 c 的文档字符串
c.__name__      类 c 的名字
c.__module__    类 c 的定义所在的模块
c.__bases__     类 c 的所有父类（这是一个元组）
```

### 类实例 类型

调用一个类就会生成该类的一个实例。每个实例也有独立的名字空间(也是dict字典，注意不要与类的名字空间混淆)。类实例有以下属性:

```
属性            描述
x.__dict__      实例 x 的名字空间
x.__class__     实例 x 所属的类
```

访问一个类实例 x 的属性时，比如 x.a，解释器会先查找 `x.__dict__["a"]，若没有找到，则接着查询 x.__class__.__dict__["a"]`，如果还没找到，则按照上面提到的搜索顺序继续查询该类的父类们的名字空间，如果还是没有找到，就要查看该类是否定义了`__getattr__()`方法，如果有这个方法就使用这个方法继续查找。如果经过以上种种手段仍然没有找到这个属性，就引发`AttributeError`异常。属性赋值如 `x.y = 5`，则总是更新实例 x 的`__dict__`属性，而不会更新其所属的类或其某个父类的`__dict__`字典。

### 文件类型

一个文件对象就是一个打开的文件，调用内建函数open()成功则返回一个文件对象。更多关于文件类型的细节在第九章。

### 内部类型

解释器内部使用的一系列对象，它们属于内部类型（用户通常不会遇到它们，不过必要时使用它们会解决一些棘手问题）。内部使用对象包括调试对象`(traceback objects)`，代码对象 `(code objects)`，`frame objects`，切片对象`(slice objects)`及 省略对象`(Ellipsis object)`。

#### 代码对象

调用内建函数`compile()`返回一个代码对象。它表示原始字节编译码或称为字节码。代码对象和函数对象相似，但它不保存被编译代码的上下文信息（被编译代码所在的名称空间及参数的默认值等)。代码对象是不可变对象，而函数对象是可变对象。一个代码对象 c 拥有如下只读属性:

```
属性                    描述
c.co_argcount           参数的个数(不包括 * 或 ** 参数)
c.co_code               原始字节码字符串
c.co_consts             字节代码用到的常量
c.co_filename           对象 c 所在的文件
c.co_firstlineno        被编译源代码第一行行号
c.co_flags              解释器标志: 1=优化 | 2=newlocals | 4=*arg | 8=**arg
c.co_lnotab             源代码行号=>字节码偏移量 这是一个映射字典
c.co_name               该代码对象的名字
c.co_names              字节代码用到的局部变量名 这是一个元组
c.co_nlocals            字节代码用到的局部变量个数
c.co_stacksize          需要的虚拟机堆践大小(包含内部变量)
c.co_varnames           一个元组，包括全部的局部变量名和参数名
```

#### Frame 对象

Frame 对象表示执行 frame。通常在 traceback对象中会遇到这个对象。 它拥有以下只读属性：

```
属性                    描述
f.f_back                下一个外部frame对象(对当前frame的调用者来说) 如果已到栈底的话 它的值就是 None 
f.f_code                当前frame中正在执行的代码对象
f.f_locals              当前frame可见的局部变量的字典
f.f_globals             当前frame可见的全局变量的字典
f.f_builtins            当前frame可见的内建名字的字典
f.f_restricted          是否在受限模式下运行 0:不受限 | 1:受限
f.f_lineno              源代码当前行号
f.f_lasti               字节码当前指令索引
```

下边是frame对象的可写属性(通过调试器或其他工具可以改变下面属性的值)：

```
f.f_trace               当前frame的跟踪函数(供调试器使用) 或 None
f.f_exc_type            当前frame发生的异常类型 或 None
f.f_exc_value           当前frame发生的异常的值 或 None
f.f_exc_traceback       当前framev发生的 traceback 或 None
```

#### traceback 对象

traceback 对象保存异常的栈追踪信息。只要发生异常就会创建 traceback对象。当一个异常被处理时，可以通过 `sys.exc_info()` 函数输出异常的堆栈追踪信息。traceback 对象 t 有以下只读属性:

```
属性                    描述
t.tb_next               栈追踪的下一级 (对发生异常的 frame 来说) 或 None
t.tb_frame              当前级正在执行的 frame 对象
t.tb_lineno             引发异常的源代码行号
t.tb_lasti              正在执行的指令索引
```

#### 切片对象

切片对象用于表示在扩展切片语法中的切片。如`a [i :j :stride ], a [i :j , n :m ], 或者 a […, i :j ]。切片对象也可以使用内建函数slice([i,] j [,stride])`创建。切片对象有下列只读属性: 属性 描述 s.start 切片的下边界,省略时返回None s.stop 切片的上边界,省略时返回None s.step 切片的步进值,省略时返回None

#### 省略对象

省略对象用于表示在一个切片中出现了省略(...)。这个类型只有一个对象，通过内建名称Ellipsis来访问这个对象。它没有任何属性。它的布尔值为 True。

## 特殊方法

所有内建的数据类型都拥有一些特殊方法。特殊方法的名字总是由两个下划线`(__)`开头和结尾。在程序运行时解释器会根据你的代码隐式调用这些方法来完成你想要的功能。例如运行`z = x + y` 这个代码，解释器内部执行的就是` z= x.__add__(y)。b=x[k] `语句解释器就会执行 `b = x.__getitem__(k)`。每个数据类型的行为完全依赖于这些特殊方法的具体实现。

内建类型的特殊方法都是只读的，所以我们无法改变内建类型的行为。虽然如此，我们还是能够使用类定义新的类型，并让它具有象内建类型那样的行为。要做到这一点也不难，只要你能实现本章介绍的这些特殊方法就可以喽！

### 对象创建、销毁及表示

表 3.7 中列出的方法用于初始化、销毁及表示对象。` __init__()`方法初始化一个对象，它在一个对象创建后立即执行。 `__del__()`方法在对象即将被销毁时调用，也就是该对象完成它的使命不再需要时调用。需要注意的是语句` del x `只是减少对象 x 的引用计数，并不调用这个函数。

**Table 3.7. 对象创建,删除,表示使用的特殊方法**

```
方法                               描述
__init__(self[,args])              初始化self
__del__(self)                      删除self
__repr__(self)                     创建self的规范字符串表示
__str__ (self)                     创建self的信息字符串表示
__cmp__(self,other)                比较两个对象,返回负数,零或者正数
__hash__(self)                     计算self的32位哈希索引
__nonzero__(self)                  真值测试,返回0或者1
```

`__repr__()和__str__()方法都返回一个字符串来表示 self 对象。通常情况，__repr__()`方法会返回的这样一个字符串：通过对该字符串取值(eval)操作将会重新得到这个对象。如果一个对象拥有`__repr__方法，当对该对象使用repr()`函数或后引号(```)操作时，就会调用这个函数做为返回值。例如:

```python
a = [2,3,4,5]           # 创建一个列表
s = repr(a)             # s = '[2, 3, 4, 5]'
                        # 注: 也可以使用 s = `a`
b = eval(s)             # 再转换为一个列表
```

如果`re[r()不能返回这样一个字符串，那它应该返回一个格式为<...message...>的字符串，例如:

```python
f = open("foo")
a = repr(f)             # a = "<open file 'foo', mode 'r' at dc030>"
```

当调用str()函数或执行print语句时，python会自动调用被操作(或打印)对象的`__str__()`方法。与`__repr__()`相比，`__str__()`方法返回的字符快通常更简洁易读，内容一般是该对象的描述性信息。如果一个对象没有被定义该函数，Python就会调用`__repr__()`方法。

`__cmp__(self,other)`方法用于与另一对象进行比较操作。如果 self < other ，它返回一个负值;若self == other，返回零;若self > other，返回一个正数。如果一个对象没有定义该函数，对象就改用对象的标识进行比较。另外，一个对象可以给每个相关操作定义两个比较函数(正向反向)，这通常被称为rich comparisons。`__nonzero__()`方法用于对自身对象进行真值测试，应该返回0或1，如果这个方法没有被定义，Python将调用`__len__()`方法来取得该对象的真值。最后`__hash__()`方法计算出一个整数哈希值以便用于字典操作。(内建函数`hash()`也可以用来计算一个对象的哈希值)。相同对象的返回值是相等的。注意，可变对象不能定义这个方法，因为对象的变化会改变其哈希值，这会造成它不能被定位和查询。一个对象在未定义 cmp() 方法的情况下也不能定义 hash()。

### 属性访问

表 3.8列出了读取、写入、或者删除一个对象的属性的方法.

**Table 3.8. 访问属性的方法**

```
方法                                    描述
__getattr__(self , name)                返回属性 self.name
__setattr__(self , name , value)        设置属性 self.name = value
__delattr__(self , name)                删除属性 self .name
例如:
 
a = x.s       # 调用 __getattr__(x,"s")
x.s = b       # 调用 __setattr__(x,"s", b)
del x.s       # 调用 __delattr__(x,"s")
```

对于类实例，`__getattr__()`方法只在类例字典及相关类字典内搜索属性失败时才被调用。这个方法会返回属性值或者在失败时引发`AttributeError`异常。

### 序列和映射的方法

表 3.9中介绍了序列和映射对象可以使用的方法。

**Table 3.9. 序列和映射的方法**

```
方法                                        描述
__len__(self)                               返回self的长度 len(someObject) 会自动调用 someObject的__len__()
__getitem__(self , key)                     返回self[key]
__setitem__(self , key , value)             设置self[key] = value
__delitem__(self , key)                     删除self[key]
__getslice__(self ,i ,j)                    返回self[i:j]
__setslice__(self ,i ,j ,s)                 设置self[i:j] = s
__delslice__(self ,i ,j)                    删除self[i:j]
__contains__(self ,obj)                     返回 obj 是否在 self 中

例如:
a = [1,2,3,4,5,6]
len(a)               # __len__(a)
x = a[2]             # __getitem__(a,2)
a[1] == 7            # __setitem__(a,1,7)
del a[2]             # __delitem__(a,2)
x = a[1:5]           # __getslice__(a,1,5)
a[1:3] = [10,11,12]  # __setslice__(a,1,3,[10,11,12])
del a[1:4]           # __delslice__(a,1,4)
```

`内建函数len(x)调用对象 x 的__len__()方法得到一个非负整数。如果一个对象没有定义__nonzero__()方法，就由 __len__()这个函数来决定其真值。` `__getitem__(key)`方法用来访问个体元素。对序列类型，key只能是非负整数，对映射类型，关键字可以是任意Python不变对象。 `__setitem__()`方法给一个元素设定新值。`__delitem__()`方法和`__delslice__()`方法在使用del语句时被自动调用。 切片方法用来支持切片操作符 s[i:j]。`__getslice__(self,i,j)`方法返回一个self类型的切片，索引 i 和 j 必须是整数，索引的含义由`__getslice__()`方法的具体实现决定。如果省略 i，i就默认为 0，如果省略 j，j 就默认为 sys.maxint。 `__setslice__()`方法给为一个切片设定新值。`__delslice__()`删除一个切片中的所有元素。`__contains__()`方法用来实现 in 操作符。

除了刚才描述过的方法之外，序列以及映射还实现了一些数学方法，包括`__add__(), __radd__(), __mul__(), 和 __rmul__(),`用于对象连接或复制等操作。下面会对这些方法略作介绍。

Python还支持扩展切片操作，这对于操作多维数据结构(如矩阵和数组)会很方便。你可以这样使用扩展切片:

```python
a = m[0:100:10]          # 步进切片 (stride=10)
b = m[1:10, 3:20]        # 多维切片
c = m[0:100:10, 50:75:5] # 多维步进切片
m[0:5, 5:10] = n         # 扩展切片分配
del m[:10, 15:]          # 扩展切片删除
```

扩展切片的一般格式是i:j [stride](https://wiki.woodpecker.org.cn/moin/stride), srtide是可选的。和普通切片一样，你可以省略每个切片的开始或者结束的值。另外还有一个特殊的对象--省略对象。写做 `(...)`，用于扩展切片中表示任何数字：

```python
a = m[..., 10:20]        # 利用省略进行的扩展切片操作
m[10:20, ...] = n
```

当进行扩展切片操作时，`__getitem__(), __setitem__(), 和 __delitem__()`方法分别用于实现访问、修改、删除操作。然而在扩展切片操作中，传递给这些方法的参数不是一个整数，而是一个包含切片对象的元组(有时还会包括一个省略对象)。例如:

```
a = m[0:10, 0:100:5, ...]
 
上面的语句会以下面形式调用__getitem__():
 
a = __getitem__(m, (slice(0,10,None), slice(0,100,5), Ellipsis))
```

```
        注意：在Python1.4版开始，就一直有扩展切片的语法，却没有任何一个内建类型支持扩展切片操作。
              Python 2.3改变了这个现状。从Python 2.3开始，内建类型终于支持扩展切片操作了，这要感谢 Michael Hudson。
```

### 数学操作

表3.10 列出了与数学运算相关的特殊方法。数学运算从左至右进行，执行表达式 x + y 时，解释器会试着调用 x.add(y)。以 r 开头的特殊方法名支持以反转的操作数进行运算。它们在左运算对象未实现相应特殊方法时被调用，例如 x + y 中的 x 若未提供 `__add__()` 方法，解释器就会试着调用函数 `y.__radd__(x)`。

**表 3.10. 数学操作的方法**

```
Method                          Result
__add__(self ,other)            self + other
__sub__(self ,other)            self - other
__mul__(self ,other)            self * other
__div__(self ,other)            self / other
__mod__(self ,other)            self % other
__divmod__(self ,other)         divmod(self ,other) 
__pow__(self ,other [,modulo]) self ** other , pow(self , other , modulo) 
__lshift__(self ,other)         self << other
__rshift__(self ,other)         self >> other
__and__(self ,other)            self & other
__or__(self ,other)             self | other
__xor__(self ,other)            self ^ other
__radd__(self ,other)           other + self
__rsub__(self ,other)           other - self
__rmul__(self ,other)           other * self
__rdiv__(self ,other)           other / self
__rmod__(self ,other)           other % self
__rdivmod__(self ,other)        divmod(other ,self) 
__rpow__(self ,other)           other ** self
__rlshift__(self ,other)        other << self
__rrshift__(self ,other)        other >> self
__rand__(self ,other)           other & self
__ror__(self ,other)            other | self
__rxor__(self ,other)           other ^ self
__iadd__(self ,other)           self += other
__isub__(self ,other)           self -= other
__imul__(self ,other)           self *= other
__idiv__(self ,other)           self /= other
__imod__(self ,other)           self %= other
__ipow__(self ,other)           self **= other
__iand__(self ,other)           self &= other
__ior__(self ,other)            self |= other
__ixor__(self ,other)           self ^= other
__ilshift__(self ,other)        self <<= other
__irshift__(self ,other)        self >>= other
__neg__(self)                   -self
__pos__(self)                   +self
__abs__(self)                   abs(self) 
__invert__(self)                ~self
__int__(self)                   int(self)
__long__(self)                  long(self)
__float__(self)                 float(self) 
__complex__(self)               complex(self)
__oct__(self)                   oct(self) 
__hex__(self)                   hex(self)
__coerce__(self ,other)         Type coercion
```

`__iadd__(), __isub__()`方法用于实现原地运算`(in-place arithmetic)`，如 a+=b 和 a-=b (称为增量赋值)。原地运算与标准运算的差别在于原地运算的实现会尽可能的进行性能优化。举例来说，如果 self 参数是非共享的，就可以原地修改 self 的值而不必为计算结果重新创建一个对象。

int(), long(), float()和complex() 返回一个相应类型的新对象，oct() 和 hex()方法分别返回相应对象的八进制和十六进制的字符串表示。

x.coerce(self,y) 用于实现混合模式数学计算。这个方法在需要时对参数 self (也就是x) 和 y 进行适当的类型转换，以满足运算的需要。如果转换成功，它返回一个元组，其元素为转换后的 x 和 y ，若无法转换则返回 None。在计算x op y时(op是运算符)，使用以下规则:

```
        1.若 x 有__coerce__()方法,使用x.__coerce__(y)返回的值替换 x 和 y, 若返回None,转到第 3 步。
        2.若 x 有__op __()方法,返回 x.__op __(y)。否则恢复 x 和 y 的原始值，然后进行下一步。
        3.若 y 有__coerce__()方法,使用y.__coerce__(x)返回的值替换 x 和 y。若返回None,则引发异常。
        4.若 y 有__rop __()方法,返回y.__op __(x)，否则引发异常.
```

虽然字符串定义了一些运算操作，但 ASCII字符串和Unicode字符串之间的运算并不使用 coerce()方法。

在内建类型中，解释器只支持少数几种类型进行混合模式运算。常见的有如下几种：

```
·如果 x 是一个字符串, x % y 调用字符串格式化操作,与 y 的类型无关
·如果 x 是一个序列, x + y 调用序列连结
·如果 x 和 y 中一个是序列,另个是整数, x * y调用序列重复
```

### 比较操作

表 3.11 列出了实现分别各种比较操作`(<, >, <=, >=, ==, !=)`的对象特殊方法，这也就是 rich comparisons。这个概念在Python 2.1中被第一次引入。这些方法都使用两个参数，根据操作数返回适当类型对象(布尔型,列表或其他Python内建类型)。举例来说，两个矩阵对象可以使用这些方法进行元素智能比较，并返顺一个结果矩阵。若比较操作无法进行，则引发异常.

**表 3.11. 比较方法**

```
方法                            操作
__lt__(self ,other )            self < other 
__le__(self ,other )            self <= other 
__gt__(self ,other )            self > other 
__ge__(self ,other )            self >= other 
__eq__(self ,other )            self == other 
__ne__(self ,other )            self != other 
```

### 可调用对象

最后，一个对象只要提供 `__call__(self[,args])` 特殊方法，就可以象一个函数一样被调用。举例来说，如果对象 x 提供这个方法，它就可以这样调用：`x(arg1 , arg2 , ...)`。解释器内部执行的则是 `x .__call__(self , arg1 , arg2 , ...)`。

## 性能及内存占用

所有的Python对象至少拥有一个整型引用记数、一个类型定义描述符及真实数据的表示这三部分。对于在32位计算机上运行的C语言实现的Python 2.0，表 3.12 列出了常用内建对象占用内存的估计大小，对于解释器的其它实现或者不同的机器配置，内存占用的准确值可能会有不同。你可能从来不考虑内存占用问题，不过当Python在要求高性能及内存紧张的环境下运行时，就必须考虑这个问题。下边这个表可以有效的帮助程序员更好地规划内存的使用：

**表 3.12. 内建数据类型使用的内存大小**

```
类型              大小

Integer                 12 bytes
Long integer            12 bytes + (nbits/16 + 1)*2 bytes
Floats                  16 bytes
Complex                 24 bytes
List                    16 bytes + 4 bytes(每个元素)
Tuple                   16 bytes + 4 bytes(每个条目)
String                  20 bytes + 1 byte(每个字符)
Unicode string          24 bytes + 2 bytes(每个字符)
Dictionary              24 bytes + 12*2n bytes, n = log2(nitems)+1
Class instance          16 bytes 加一个字典对象
Xrange object           24 bytes
```

由于字符串类型太常用了，所以解释器会特别优化它们。可以使用内建函数intern(s)来暂存一个频繁使用的字符串 s。这个函数首先在内部哈希表中寻找字符串 s 的哈希值，如果找到，就创建一个到该字符串的引用，如果找不到，就创建该字符串对象并将其哈希值加入内部哈希表。只要不退出解释器，被暂存的字符串就会一直存在。如果你关心内存占用，那你就一定不要暂存极少使用的字符串。为了使字典查询更有效率，字符串会缓存它们最后的哈希值。

一个字典其实就是一个开放索引的哈希表。The number of entries allocated to a dictionary is equal to twice the smallest power of 2 that’s greater than the number of objects stored in the dictionary. When a dictionary expands, its size doubles. On average, about half of the entries allocated to a dictionary are unused.

一个Python程序的执行首先是一系列的函数调用(包括前面讲到的特殊方法)，之后再选择最高效的算法。搞懂 Python 的对象模型并尽量减少特殊方法的调用次数，可以有效提高你的程序的性能。特别是改良类及模块的名字查询方式效果卓著。看下面的代码:

```python
import math
d = 0.0
for i in xrange(1000000):
     d = d + math.sqrt(i)
```

在上面的代码中，每次循环调用都要进行两次名称查询。第一次在全局名称空间中定位math模块，第二次是搜寻一个名称是sqrt的函数对象。 我们将代码改成下面这样:

```python
from math import sqrt
d = 0.0
for i in xrange(1000000):
     d = d + sqrt(i)
```

这个代码每次循环只需要进行一次名称查询。就这样一个简单的调整，在作者的 200 MHz PC上运行时,这个简单的变化会使代码运行速度提高一倍多。

```
注:      200 MHz的机器我没有，但在我的2000 MHz机器上效果没有这么明显，不过仍然有10%以上的提高  --Feather
         那时作者用的是 Python 2.0，现在你用的是 2.4。 Python一直在不断进步嘛! --WeiZhong
```

在Python程序设计中，应该仅在必要时使用临时变量，尽可能的避免非必要的序列或字典查询。下面我们看看 Listing 3.2中的这两个类:

**Listing 3.2 计算一个平面多边形的周长**

```python
class Point:
    def __init__(self,x,y,z):
          self.x = x
          self.y = y
#低效率的示例
class Poly:
    def __init__(self):
          self.pts = []
    def addpoint(self,pt):
          self.pts.append(pt)
    def perimeter(self):                   #计算周长
          d = 0.0
          self.pts.append(self.pts[0])     # 暂时封闭这个多边形
          for i in xrange(len(self.pts)-1):
               d2 = (self.pts[i+1].x - self.pts[i].x)**2 + (self.pts[i+1].y - self.pts[i].y)**2
               d = d + math.sqrt(d2)
          self.pts.pop()                   # 恢复原来的列表
          return d
```

Poly类中的 perimeter() 方法，每次访问 self.pts[i]都会产生两次查询--一次查询名字空间字典,另一次查询 pts 序列。

下面我们改写一下代码，请看 Listing 3.3:

**Listing 3.3 Listing 3.2的改良版本**

```python
class Poly:
      ...
      def perimeter(self):
          d = 0.0
          pts = self.pts                #提高效率的关键代码
          pts.append(pts[0])
          for i in xrange(len(pts)-1):
                p1 = pts[i+1]
                p2 = pts[i]
                d += sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
          pts.pop()
          return d
```

这个代码的关键之处在于用一个局部变量引用了一个类属性，尽管这样的修正对效率提高的并不是很多(15-20%)，了解这些并在你的常规代码中留意这些细节就能够帮助你写出高效的代码。当然，如果对性能要求极高，你也可以 C 语言编写 Python 扩展。