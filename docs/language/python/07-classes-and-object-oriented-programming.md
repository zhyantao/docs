# 第七章 类及面向对象编程

类是用来创建数据结构和新类型对象的主要机制.本章的主题就是类,面向对象编程和设计不是本章的重点。本章假定你具有数据结构的背景知识及一定的面向对象的编程经验(其它面向对象的语言，比如java,c++).(参见第三章,类型和对象 了解对象这个术语及其内部实现的附加信息)

```
WeiZhong补充：
    这本书出版于2001年，虽然Python有极佳的向下兼容性，但我们应该学习最新的知识。本章很多地方已经明显过时，为了保证大家学到新的知识并维持这本书的完整性，我会在必要的地方说明哪些地方已经过时，哪些地方新增了功能。
    Python从2.2起引入了new-style对象模型，以逐步替代已经使用多年的classic对象模型。
    由于 classic class 已经行将废止，所以我对本章的例子均作为了适当的修改以支持 new-style对象模型。 
```

参考文档:《Python In a Nutshell》中的一节[Python中的新型类及其实例](https://wiki.woodpecker.org.cn/moin/PyNewStyleClass)

## class语句

一个类定义了一系列与其实例对象密切关联的属性.典型的属性包括变量(也被称为类变量)和函数(又被称为方法).

class语句用来定义一个类.类的主体中语句在类定义同时执行.(如 Listing 7.1)

**Listing 7.1 类**

```en
class Account(object):
     "一个简单的类"
     account_type = "Basic"
     def __init__(self,name,balance):
         "初始化一个新 Account 实例"
         self.name = name
         self.balance = balance
     def deposit(self,amt):
         "存款"
         self.balance = self.balance + amt
     def withdraw(self,amt):
         "取款"
         self.balance = self.balance - amt
     def inquiry(self):
         "返回当前余额"
         return self.balance
```


## 访问类属性

类对象作为一个名字空间，存放在类定义语句运行时创建的对象.例如,Account里的内容可以这样访问:

```
Account.account_type
Account.__init__
Account.deposit
Account.withdraw
Account.inquiry
```

需要注意的是, class语句并不创建类的实例(例如上边的例子,并没有创建任何帐户).它用来定义所有实例都应该有的属性.

在类中定义的常规方法的第一个参数总是该类的实例,通常这个参数记为self。你也可能用其它任何合法的变量名，不过为了符合惯例，你最好还是用self. 类中定义的变量,即类变量，如account_type, 它被所有该类的实例共享. 虽然类定义了一个名字空间,但这个名字空间并不是为类主体中的代码服务的.因此在类中引用一个类的属性必须使用类的全名:

```en
class Foo(object):
    def bar(self):
        print "bar!"
    def spam(self):
        bar(self)     # 错误,引发NameError
        Foo.bar(self) # 合法的
```

最后，你不能定义一个不操作实例的方法:

```en
class Foo(object):
    def add(x,y):
        return x+y
a = Foo.add(3,4)      # TypeError. 需要一个类实例作为第一个参数
```

=======================================================================================

以下为[WeiZhong](https://wiki.woodpecker.org.cn/moin/WeiZhong)增补部分： **静态方法和类方法(Python2.2以上)**

- 静态方法: 可以直接被类或类实例调用。它没有常规方法那样的特殊行为（绑定、非绑定、默认的第一个参数规则等等）。你完全可以将静态方法当成一个用属性引用方式调用的普通函数。任何时候定义静态方法都不是必须的（静态方法能实现的功能都可以通过定义一个普通函数来实现）. 有些程序员认为，当有一堆函数仅仅为某一特定类编写时，将这些函数包装成静态这种方式可以提供使用上的一致性。

根据python2.4最新提供的新语法，你可以用下面的方式创建一个静态方法：

```
class AClass(object):
    @staticmethod       #静态方法修饰符，表示下面的方法是一个静态方法
    def astatic(  ): print 'a static method'
anInstance = AClass(  )
AClass.astatic(  )                    # prints: a static method
anInstance.astatic(  )                # prints: a static method
```

注:staticmethod是一个内建函数,用来将一个方法包装成静态方法,在2.4以前版本,只能用下面这种方式定义一个静态方法(不再推荐使用):

```
class AClass(object):
    def astatic(  ): print 'a static method'
    astatic=staticmethod(astatic)
```

这种方法在函数定义本身比较长时经常会忘记后面这一行.

- 类方法 一个类方法就可以通过类或它的实例来调用的方法, 不管你是用类来调用这个方法还是类实例调用这个方法,该方法的第一个参数总是定义该方法的类对象。 记住:方法的第一个参数都是类对象而不是实例对象. 按照惯例,类方法的第一个形参被命名为 cls. 任何时候定义类方法都不是必须的（类方法能实现的功能都可以通过定义一个普通函数来实现,只要这个函数接受一个类对象做为参数就可以了）. 你可以象下面这样来生成一个类方法:

```
class ABase(object):
    @classmethod        #类方法修饰符
    def aclassmet(cls): print 'a class method for', cls.__name__
class ADeriv(ABase): pass
bInstance = ABase(  )
dInstance = ADeriv(  )
ABase.aclassmet(  )               # prints: a class method for ABase
bInstance.aclassmet(  )           # prints: a class method for ABase
ADeriv.aclassmet(  )              # prints: a class method for ADeriv
dInstance.aclassmet(  )           # prints: a class method for ADeriv
```

注:classmethod是一个内建函数,用来将一个方法封装成类方法,在2.4以前版本,你只能用下面的方式定义一个类方法:

```
class AClass(object):
    def aclassmethod(cls): print 'a class method'
    aclassmethod=classmethod(aclassmethod)
```

并没有人要求必须封装后的方法名字必须与封装前一致,但建议你总是这样做(如果你使用python2.4版本以下时). 这种方法在函数定义本身比较长时经常会忘记后面这一行.

=======================================================================================

增补部分至此结束

## 类实例

像调用函数一样调用类，可以得到类的实例。生成实例的过程会自动调用类的`__init__`方法（如果你的类定义了这个方法的话）。

```en
# 创建一些帐户
a = Account("Guido", 1000.00)     # 调用 Account.__init__(a,"Guido",1000.00)
b = Account("Bill", 100000000000L)
```

实例创建之后,就可以使用点(.)操作符来访问它的属性和方法:

```en
a.deposit(100.00)        # 调用 Account.deposit(a,100.00)
b.withdraw(sys.maxint)   # 调用 Account.withdraw(b,sys.maxint)
name = a.name            # 得到帐户名称
print a.account_type     # 显示帐户类型
```

在系统内部,每个类实例都拥有一个字典(即实例的 `__dict__` 属性,在第三章中有介绍).这个字典包含每个实例的信息.例如:

```
>>> print a.__dict__
{'balance': 1100.0, 'name': 'Guido'}
>>> print b.__dict__
{'balance': 97852516353L, 'name': 'Bill'}
```

若一个实例的属性被修改,这个字典也随之改变.上例中，属性通过Account类中定义的方法`__init()__`, deposit(),以及withdraw()中对self变量赋值被改变. 不过对于类实例可以随时添加私有属性。

```
a.number = 123456    # 把 'number' 加入到 a.__dict__
```

属性的赋值总是发生在实例字典中,而属性访问则比属性赋值复杂一些。当访问一个属性的时候,解释器首先在实例的字典中搜索，若找不到则去创建这个实例的类的字典中搜索，若还找不到就到类的基类中搜索(在后边 '继承' 一节中会讲到)，如果还找不到最后会尝试调用类的`__getattr__`方法来获取属性值(若类中定义了该方法的话).如果这个过程也失败,则引发`AttributeError`异常

## 引用记数与实例销毁

所有实例都是引用记数的.若一个实例引用记数变成零,该实例就被销毁.当实例将被销毁前,解释器会搜索该对象的 `__del__`方法并调用它。但在实际应用中,极少有需要给一个类定义`__del__`方法, 除非这个对象在销毁前需要执行一些清除操作(如关闭文件,断开网络,或者释放其他系统资源).即使是在这种情况下,依赖`__del__()`来执行清除和关闭操作也是危险的，因为不能保证在解释器关闭时会自动调用这个方法.更好的选择是定义一个close()方法,在需要时显式的调用这个方法来执行这个过程. 最后注意一点, 如果一个实例拥有`__del__`方法，则它永远不会被Python的垃圾收集器回收(这也是不推荐定义 `__del__()`的理由).关于垃圾回收请参阅附录A中的gc模块。

有时会使用del语句来删除对象的引用，如果这导致该对象引用记数变为零,就会自动调用`__del__()`. del语句并不直接调用`__del__()`.

## 继承

继承(Inheritance)是创建新类的机制之一,它通过一个已有类进行修改和扩充来生成新类。这个原始的类被称为基类(base class)或超类(superclass).新生成的类称为该类的派生类(derived class)或子类(subclass).当通过继承创建一个类时,它会自动'继承'在基类中定义的属性。一个子类也可以重新定义父类中已有的属性或定义新的属性.

Python支持多继承，如果一个类有多个父类，在class语句中就使用逗号来分隔这个父类列表。例如:

```en
class D(oject): pass                    #D继承自object
class B(D):                             #B是D的子类
    varB = 42
    def method1(self):
        print "Class B : method1"
class C(D):                             #C也是D的子类
    varC = 37
    def method1(self):
        print "Class C : method1"
    def method2(self):
        print "Class C : method2"  
class A(B,C):                           #A是B和C的子类
    varA = 3.3
    def method3(self):
        print "Class A : method3"
```

当搜索在基类中定义的某个属性时，Python采用深度优先的原则、按照子类定义中的基类顺序进行搜索。**注意**（new-style类已经改变了这种行为）。上边例子中，如果访问` A.varB `,就会按照A-B-D-C-D这个顺序进行搜索，只要找到就停止搜索.若有多个基类定义同一属性的情况,则只使用第一个被找到属性值:

```en
a = A()            # 创建 'A' 的实例
a.method3()        # 调用 A.method3(a)
a.method1()        # 调用 B.method1(c)
a.varB             # 得到 B.varB
```

**重要提示：新旧对象模型的差异:**

```
    注意：Python 中现在有两种对象模型均在使用中即classic对象模型和new-style对象模型，也有两种类：classic class 及 new-style class
    在classic对象模型中,方法和属性按 从左至右 深度优先 的顺序查找（上文中已经提到）.显然,当多个父类继承自同一个基类时,这会产生我们不想要的结果.
    就上例来说,D是一个new-style类（继承自object），B和C是D的子类, 而A是B和C的子类,如果按classic对象模型(原文中的提到的对象模型)的属性查找规则是搜索顺序是 A-B-D-C-D. 由于Python先查找D后查找C,即使C对D中的属性进行了重定义,也只能使用D中定义的版本.这是classic数据模型的固有问题,在实际应用中会造成一些麻烦.为了解决这个及其它一些问题，Python从2.2版本开始引入new-style对象模型。

    在new-style对象模型中,所有内建类型均是object的直接或间接子类. new-style对象模型改变了传统对象模型中的解析顺序,上面的例子我已经改写为new-style类,因此,这个例子实际的搜索顺序是 A-B-C-D.

    每个内建类型及new-style类均内建有一个特殊的只读属性 __mro__,这是一个tuple,它保存着方法解析类型. 只能通过类来引用 __mro__(通过实例无法访问).
                        --WeiZhong Added@20060210
```

如果一个子类定义了一个和基类具有相同名称的属性,则子类的实例将使用子类中定义的属性.如果需要访问原来的属性,则必须使用全名来限制访问区域:

```en
class D(A):
   def method1(self):
       print "Class D : method1"
       A.method1(self)            # 调用基类属性
```

需要注意的一点是子类实例的初始化.当一个子类实例被创建时, 基类的 `__init__()`方法并不会被自动调用.也就是子类必须自力更生来解决实例的初始化.例如:

```en
class D(A):
    def __init__(self, args1):
        # 初始化基类
        A.__init__(self)
        # 初始化自己
        ...
```

`__del__()` 与 `__init__()` 类似.

## 多态

Python通过上文中提到的属性查询规则来实现多态.当使用obj.method() 来访问一个方法时,方法的搜索顺序为:实例的 `__dict__` 属性,实例的类定义,基类. 第一个被找到的方法被执行。

## 数据隐藏

默认情况下,所有的属性都是'公开'的.这意味着一个类的所有属性均可不受任何限制的访问.这也意味着基类中定义的所有内容都能被子类继承。 在面向对象编程实践中，这种行为是我们不希望的。因为它不但暴露了对象的内部实现，而且容易在派生类对象及基类对象之间产生名字空间冲突。

要解决这个问题,只需要在类中将需要隐藏的属性名字以两个下划线开头,例如 `__Foo`。这样系统会自动实时生成一个新的名字 `_Classname__Foo` 并用于内部使用。这样在某种程度上就提供了私有属性(其实这个 `_Classname__Foo` 仍然是不受限制访问的嘿嘿),也解决了名字空间冲突的问题.例如:

```en
class A:
   def __init__(self):
      self.__X = 3        # self._A__X

class B(A):
   def __init__(self):
      A.__init__(self)
      self.__X = 37       # self._B__X
```

这是一个小技巧,并没有真正阻止访问一个类的*私有*属性.如果已知一个类的名称和它某个私有属性的名称,我们还是可以使用`_Classname__Foo` 来访问到这个属性.(这不是bug,因为在某些特定的场合这非常有用,比如调试时,所以系统一直保留这个所谓的*问题*)

## 操作符重载

用户自定义对象可以通过在类中实现特殊方法(第三章中已介绍)来重载Python内建操作符.例如 Listing 7.2 中的类,它使用标准的数学运算符实现了复数的运算及类型转换.

**Listing 7.2 数学运算及类型转换**

```en
class Complex(object):
    def __init__(self,real,imag=0):
        self.real = float(real)
        self.imag = float(imag)
    def __repr__(self):
        return "Complex(%s,%s)" % (self.real, self.imag)
    def __str__(self):
        return "(%g+%gj)" % (self.real, self.imag)
    # self + other
    def __add__(self,other):
        return Complex(self.real + other.real, self.imag + other.imag)
    # self - other
    def __sub__(self,other):
        return Complex(self.real - other.real, self.imag - other.imag)
    # -self
    def __neg__(self):
        return Complex(-self.real, -self.imag)
    # other + self
    def __radd__(self,other):
        return Complex.__add__(other,self)
    # other - self
    def __rsub__(self,other):
        return Complex.__sub__(other,self)
    # 将其他数值类型转换为复数
    def __coerce__(self,other):
        if isinstance(other,Complex):
            return self,other
        try:   # 检测是否可以被转换为浮点数
            return self, Complex(float(other))
        except ValueError:
            pass
```

在这个例子中,有一些值得研究的地方:

- 首先`__repr__()` 用于返回对象的表达式字符串表示,这个返回字符串可以用于再次得到该对象.在本例中,会创建一个类似"Complex(r,i)"的字符串.另外`__str__()`方法创建一个字符串用于较美观的输出。(通常用于print语句)

  然后,要处理复数在运算符左边或右边这两种情况,必须同时提供 `__op__()和 __rop__()`方法.

  最后, `__ceorco__` 方法用于处理混合类型运算.在本例中,其他的数值类型均被转换为复数,这样才可以继续进行复数的运算.

## 类,类型,和成员检测

目前,类型和类是分开的.内建类型,如列表和字典是不能被继承的,类也不能定义一个新类型.事实上,所有的类定义都属于[ClassType](https://wiki.woodpecker.org.cn/moin/ClassType)类型,同样地,类的实例属于[InstanceType](https://wiki.woodpecker.org.cn/moin/InstanceType)类型.所以,下面这个表达式对于两个类永远为真(即使这两个实例是由不同的类创建的): type(a) == type(b)

```
        Python 2.4 已经支持内建类型的继承，类与类型还有差别，但越来越微妙了。
        对 new-style 类来说，类的实例并不是 InstanceType 类型。它的类型与类的名字有关。也因此，对new-style类来说，上面的等式只有同一个类的两个不同实例才为真。 --WeiZhong
```

内建函数isinstance(obj ,cname)用来测试obj对象是否是cname的实例。.如果是,函数就返回True.例如:

```en
class A(object): pass
class B(A): pass
class C(object): pass

a = A()          # 'A'的实例
b = B()          # 'B'的实例 
c = C()          # 'C'的实例 

isinstance(a,A)  # 返回 True
isinstance(b,A)  # 返回 True, B 源自 A
isinstance(b,C)  # 返回 False, C 与 A 没有派生关系
```

同样地,内建函数issubclass(A ,B)用来测试类A是否是类B的子类:

```
issubclass(B,A)   # 返回 True
issubclass(C,A)   # 返回 False
issubclass(A,A)   # 永远返回True
```

isinstance()函数也可以用于检查任意内建类型:

```en
import types
isinstance(3, types.IntType)     # 返回 True
isinstance(3, types.FloatType)   # 返回 False
```

这是一个被推荐的类型检查方法,这样类型和类的差别就可以忽略.