=========
类型信息
=========

Java 在运行时识别对象和类的信息，主要有两种方式：

- RTTI（Runtime Type Identification）运行时类型识别
- 反射：允许在运行时发现和使用类的信息

如果你的程序代码处于同一块程序空间，但是不知道某个对象的确切类型，RTTI 可以告诉你。
但是有一个限制：这个类型在编译时必须已知，这样才能使用 RTTI 识别它，并利用这些信息做一些有用的事情。

但是，假设你获取了一个指向某个并不在你的程序空间中的对象的引用，
事实上，在编译时你的程序根本没法获知这个对象所属的类。
例如，假设你从磁盘文件或网络连接中获取了一串字节。

RTTI 和 反射在使用类之前都必须获取到那个类的 Class 对象，因此，那个类的 ``.class`` 文件对于 JVM 来说必须是可获取的。
要么在本地机器上，要么可以通过网络获得。

RTTI 和 反射的唯一不同就是，对 RTTI 来说，编译器在编译时打开和检查 ``.class`` 文件，而对于反射来说，
``.class`` 文件在编译时是不可获取的，所以是在运行时打开和检查 ``.class`` 文件。

为什么需要 RTTI
----------------

面向对象的基本目的：让代码只操纵对基类的引用。

这样，如果要添加一个新类来扩展程序，就不会影响到原来的代码。

.. uml::

    @startuml

    class Shape
    class Circle
    class Square
    class Triangle

    Shape <|-- Circle
    Shape <|-- Square
    Shape <|-- Triangle

    @enduml

比如，当把元素放入数组 ``List<Shape>`` 中时，会丢失 ``Shape`` 类型信息，向上转型为 ``Object`` 。

当从数组 ``List<Shape>`` 中取出元素时，容器 ``List`` 会自动将结果转型回 ``Shape`` 。

这是 RTTI 最基本的使用形式，因为在 Java 中，所有的类型转换都是在运行时进行正确性检查的。

但是，这个例子 RTTI 转型并不彻底， ``Object`` 被转型为 ``Shape`` ，并没有转型为 ``Circle`` 、 ``Square`` 或者 ``Triangle`` 。
这是因为目前我们只知道这个 ``List<Shape>`` 保存的都是 ``Shape`` 。这是由 **容器** 和 **泛型** 来保证这种机制的。

接下来是由 **多态** 进行动态绑定，将 ``Shape`` 转型为 ``Circle`` 、 ``Square`` 或者 ``Triangle`` 。

Class 对象
-----------

类型信息在运行时是如何表示的？

- 加载。每编写并编译了一个新类，类加载器查找字节码，并从字节码中创建一个 Class 对象。
  
  - 每个类都有一个 Class 对象，被保存在同名 ``.class`` 文件中。
  - Java 使用 Class 对象来创建所有普通类的对象（执行 RTTI），Class 对象包含了与类有关的信息。
  - 一旦某个类的 Class 对象被载入内存，它就被用来创建这个类的所有对象。

- 链接。验证类中的字节码，为静态域分配存储空间，并且若必须的话，将解析这个类创建的对其他类的所有引用。
- 初始化。如果该类具有超类，则对其初始化，执行静态初始化器和静态初始化块。

.. code-block:: java

    //: typeinfo/SweetShop.java
    // Examination of the way the class loader works.
    import static net.mindview.util.Print.*;

    class Candy {
        static { print("Loading Candy"); }
    }

    class Gum {
        static { print("Loading Gum"); }
    }

    class Cookie {
        static { print("Loading Cookie"); }
    }

    public class SweetShop {
        public static void main(String[] args) {	
            print("inside main");
            new Candy();
            print("After creating Candy");
            try {
                Class.forName("Gum");
            } catch(ClassNotFoundException e) {
                print("Couldn't find Gum");
            }
            print("After Class.forName(\"Gum\")");
            new Cookie();
            print("After creating Cookie");
        }
    } /* Output:
    inside main
    Loading Candy
    After creating Candy
    Loading Gum
    After Class.forName("Gum")
    Loading Cookie
    After creating Cookie
    *///:~

Class 对象常用的方法：

- ``Class.forName()`` 查找相应类的对象的 Class 对象引用
- ``Class.getClass()`` 获取 Class 对象的引用
- ``Class.getInterfaces()`` 获取感兴趣的对象所包含的接口
- ``Class.getSuperclass()`` 查找基类

普通对象 object 的常用方法：

- ``object.getSimpleName()`` 产生不包含包名的类名
- ``object.getCanonicalName()`` 产生全限定的类名

.. note:: 

    Java 虚拟机使用类加载器生成 Class 对象（首先检查是否已经生成，若未生成，就根据类名查找 ``.class`` 文件）。
    
    类加载器子系统实际上包含一条类加载器链，但是只有一个原生类加载器，它是 JVM 实现的一部分。
    原生加载器加载的是可信类，包括从本地盘加载的 Java API 类（若从网络中加载类需要手动挂接）。
    
    所有的类都是在对其第一次使用时，动态加载到 JVM 中的。当程序创建第一个对类的静态成员的引用时，就会加载这个类。
    因此，当用 ``new`` 创建对象时，就是在创建类的构造器的引用，这说明构造器就是 ``static`` 的。

    但是，Java 程序在它开始运行之前，并未完全加载，其余各个部分是在需要时才加载的。

类字面常量
~~~~~~~~~~

使用类字面常量生成对 Class 对象的引用：

.. code-block:: java

    FancyToy.class

这样做比用 ``forName()`` 更简单、更安全。

类字面常量可以用于：

- 普通类
- 接口
- 数组
- 基本数据类型
- 基本数据类型的包装器类

.. note:: 

    使用 ``.class`` 创建对 Class 对象的引用时，不会自动初始化该 Class 对象，而使用 ``forName()`` 会初始化对象。

泛化的 Class 引用
~~~~~~~~~~~~~~~~~

Class 引用总是指向某个 Class 对象，它可以创建类的对象，并包含可作用于这些对象的所有方法代码。
它还包含该类的静态成员，因此，Class 引用表示的就是它所指向的对象的确切类型，而该对象便是 Class 类的一个对象。

普通的类的引用可以被重新赋值为指向任何其他的 Class 对象，这是不安全的。
可以使用泛型语法对 Class 引用所指向的 Class 对象的类型进行限定。为了放宽这种限定，可以使用通配符，比如 ``Class<?>`` 。
向 Class 引用添加泛型语法的原因仅仅是为了提供编译期类型检查。

.. code-block:: java
    :emphasize-lines: 6

    //: typeinfo/GenericClassReferences.java

    public class GenericClassReferences {
        public static void main(String[] args) {
            Class intClass = int.class;
            Class<Integer> genericIntClass = int.class;
            genericIntClass = Integer.class; // Same thing
            intClass = double.class;
            // genericIntClass = double.class; // Illegal
        }
    } ///:~

类型转换前先做检查
------------------

为了确保类型转换是正确的，一般来讲由 RTTI 确保类型转换的正确性，如果执行了一个错误的类型转换，就抛出 ``ClassCastException`` 异常。
RTTI 通过查询 Class 对象获取运行时所需要的信息，但是在编译期，编译器不知道确定的类型，需要人为指定向下转型的具体类型。
因此，引出关键字 ``instanceof`` ，使用提问的方式，如下

.. code-block:: java

    if (x instanceof Dog)
        ((Dog)x).bark()

动态的 instanceof
~~~~~~~~~~~~~~~~~~

``Class.isInstance()`` 方法提供了一种动态地测试对象的途径。

.. code-block:: java

    objA.isInstance(objB)

instanceof 与 Class 的等价性
----------------------------

查询类型信息时，通过比较获取到的对象引用，发现：

- ``instanceof`` 或 ``isInstance()`` 考虑继承关系，子类属于父类
- ``==`` 不考虑继承关系
- ``getClass()`` 获取到的是最具体的类型信息

.. code-block:: java

    //: typeinfo/FamilyVsExactType.java
    // The difference between instanceof and class
    package typeinfo;
    import static net.mindview.util.Print.*;

    class Base {}
    class Derived extends Base {}	

    public class FamilyVsExactType {
        static void test(Object x) {
            print("Testing x of type " + x.getClass());
            print("x instanceof Base " + (x instanceof Base));
            print("x instanceof Derived "+ (x instanceof Derived));
            print("Base.isInstance(x) "+ Base.class.isInstance(x));
            print("Derived.isInstance(x) " + Derived.class.isInstance(x));
            print("x.getClass() == Base.class " + (x.getClass() == Base.class));
            print("x.getClass() == Derived.class " + (x.getClass() == Derived.class));
            print("x.getClass().equals(Base.class)) "+ (x.getClass().equals(Base.class)));
            print("x.getClass().equals(Derived.class)) " + (x.getClass().equals(Derived.class)));
        }
        public static void main(String[] args) {
            test(new Base());
            test(new Derived());
        }	
    } /* Output:
    Testing x of type class typeinfo.Base
    x instanceof Base true
    x instanceof Derived false
    Base.isInstance(x) true
    Derived.isInstance(x) false
    x.getClass() == Base.class true
    x.getClass() == Derived.class false
    x.getClass().equals(Base.class)) true
    x.getClass().equals(Derived.class)) false
    Testing x of type class typeinfo.Derived
    x instanceof Base true
    x instanceof Derived true
    Base.isInstance(x) true
    Derived.isInstance(x) true
    x.getClass() == Base.class false
    x.getClass() == Derived.class true
    x.getClass().equals(Base.class)) false
    x.getClass().equals(Derived.class)) true
    *///:~

反射：运行时的类信息
---------------------

在大规模的编程世界中，比如基于构件的编程，可以通过将代表不同组件的图标拖拽到表单来创建程序。
然后，在编程时通过设置构件的属性值来配置它们。这种设计要求继承开发环境能够发现构件暴露出来的方法。

反射，提供了一种机制，用来检查可用的方法，并返回方法名。Java 通过 JavaBeans 提供了基于构件的编程架构。

人们想要在运行时获取类的信息的另一个动机，是希望提供在跨网络的远程平台上创建和运行对象的能力。
这被称为 **远程方法调用（RMI）** ，它允许一个 Java 程序对象分布到多台机器上。

- 将大的计算任务分成小的计算单元，分布到不同机器上（分布式计算）
- 将处理特定类型任务的代码分布到不同的机器上（多层的 C/S 架构）

Class 类与 ``java.lang.reflect`` 类库一起，对反射的概念提供了支持，该类库包含了 Field、Method、Constructor 类。
可以在 IDE 中使用一系列的 ``get()`` ， ``set()`` 方法。

类方法提取器
~~~~~~~~~~~~

通常，你不需要直接使用反射工具。反射在 Java 中是用来支持其他特性的，例如对象序列化和 JavaBean。

查找类定义的源代码或 JDK 文档是费时的， **类方法提取器帮助我们快速地提取某个类的信息** ，使我们能够编写自动展示完整接口的简单工具。

.. code-block:: java

    //: typeinfo/ShowMethods.java
    // Using reflection to show all the methods of a class,
    // even if the methods are defined in the base class.
    // {Args: ShowMethods}
    import java.lang.reflect.*;
    import java.util.regex.*;
    import static net.mindview.util.Print.*;

    public class ShowMethods {
        private static String usage =
            "usage:\n" +
            "ShowMethods qualified.class.name\n" +
            "To show all methods in class or:\n" +
            "ShowMethods qualified.class.name word\n" +
            "To search for methods involving 'word'";
        private static Pattern p = Pattern.compile("\\w+\\.");
        public static void main(String[] args) {
            if(args.length < 1) {
                print(usage);
                System.exit(0);
            }
            int lines = 0;
            try {
                Class<?> c = Class.forName(args[0]);
                Method[] methods = c.getMethods();
                Constructor[] ctors = c.getConstructors();
                if(args.length == 1) {
                    for(Method method : methods)
                        print(
                            p.matcher(method.toString()).replaceAll(""));
                    for(Constructor ctor : ctors)
                        print(p.matcher(
                            ctor.toString()).replaceAll(""));
                    lines = methods.length + ctors.length;
                } else {
                    for(Method method : methods)
                        if(method.toString().indexOf(args[1]) != -1) {
                            print(
                                p.matcher(method.toString()).replaceAll(""));
                            lines++;
                        }
                    for(Constructor ctor : ctors)
                        if(ctor.toString().indexOf(args[1]) != -1) {
                            print(p.matcher(
                                ctor.toString()).replaceAll(""));
                            lines++;
                        }
                }
            } catch(ClassNotFoundException e) {
                print("No such class: " + e);
            }
        }
    } /* Output:
    public static void main(String[])
    public native int hashCode()
    public final native Class getClass()
    public final void wait(long,int) throws InterruptedException
    public final void wait() throws InterruptedException
    public final native void wait(long) throws InterruptedException
    public boolean equals(Object)
    public String toString()
    public final native void notify()
    public final native void notifyAll()
    public ShowMethods()
    *///:~

动态代理
--------

代理是基本的设计模式之一，它是为了提供额外的或不同的操作，而插入的用来代替“实际”对象的对象。

这些操作通常涉及与“实际”对象的通信，因此，代理通常充当中间人的角色。代理可以帮你做一些事情，但是你又不知道是谁做的。

.. uml::

    @startuml
    interface Interface
    class RealObject
    class SimpleProxy
    Interface <|.. RealObject
    Interface <|.. SimpleProxy
    @enduml

.. code-block:: java

    //: typeinfo/SimpleProxyDemo.java
    import static net.mindview.util.Print.*;

    interface Interface {
        void doSomething();
        void somethingElse(String arg);
    }

    class RealObject implements Interface {
        public void doSomething() { print("doSomething"); }
        public void somethingElse(String arg) {
            print("somethingElse " + arg);
        }
    }	

    class SimpleProxy implements Interface {
        private Interface proxied;
        public SimpleProxy(Interface proxied) {
            this.proxied = proxied;
        }
        public void doSomething() {
            print("SimpleProxy doSomething");
            proxied.doSomething();
        }
        public void somethingElse(String arg) {
            print("SimpleProxy somethingElse " + arg);
            proxied.somethingElse(arg);
        }
    }	

    class SimpleProxyDemo {
        public static void consumer(Interface iface) {
            iface.doSomething();
            iface.somethingElse("bonobo");
        }
        public static void main(String[] args) {
            consumer(new RealObject());
            consumer(new SimpleProxy(new RealObject()));
        }
    } /* Output:
    doSomething
    somethingElse bonobo
    SimpleProxy doSomething
    doSomething
    SimpleProxy somethingElse bonobo
    somethingElse bonobo
    *///:~

动态代理可以动态地创建代理并动态地处理对所代理方法的调用。
在动态代理上所做的所有调用都会被重定向到单一的调用处理器上。
调用处理器的工作是揭示调用的类型并确定相应的对策。

.. uml::

    @startuml
    interface InvocationHandler
    class DynamicProxyHandler
    InvocationHandler <|.. DynamicProxyHandler
    @enduml

.. code-block:: java

    //: typeinfo/SimpleDynamicProxy.java
    import java.lang.reflect.*;

    class DynamicProxyHandler implements InvocationHandler {
        private Object proxied;
        public DynamicProxyHandler(Object proxied) {
            this.proxied = proxied;
        }
        public Object
        invoke(Object proxy, Method method, Object[] args)
        throws Throwable {
            System.out.println("**** proxy: " + proxy.getClass() +
                ", method: " + method + ", args: " + args);
            if(args != null)
                for(Object arg : args)
                    System.out.println("    " + arg);
            return method.invoke(proxied, args);
        }
    }	

    class SimpleDynamicProxy {
        public static void consumer(Interface iface) {
            iface.doSomething();
            iface.somethingElse("bonobo");
        }
        public static void main(String[] args) {
            RealObject real = new RealObject();
            consumer(real);
            // Insert a proxy and call again:
            Interface proxy = (Interface)Proxy.newProxyInstance(
                Interface.class.getClassLoader(),
                new Class[]{ Interface.class },
                new DynamicProxyHandler(real));
            consumer(proxy);
        }
    } /* Output: (95% match)	
    doSomething
    somethingElse bonobo
    **** proxy: class $Proxy0, method: public abstract void Interface.doSomething(), args: null
    doSomething
    **** proxy: class $Proxy0, method: public abstract void Interface.somethingElse(java.lang.String), args: [Ljava.lang.Object;@42e816
        bonobo
    somethingElse bonobo
    *///:~

通过静态方法 Proxy.newProxyInstance() 可以创建动态代理，这个方法需要：

- 一个类加载器（通常从已经被加载的对象中获取其类加载器，然后传递给它）
- 一个你希望该代理实现的接口列表（不是类或抽象类）
- 一个 InvocationHandler 接口的实现

动态代理可以将所有调用重定向到调用处理器，因此通常会向调用处理器的构造器传递一个“实际”对象的引用，
从而使得调用处理器在执行其中介任务时，可以将请求转发。

空对象
------

.. code-block:: java

    public interface Null {}

模拟对象与桩
~~~~~~~~~~~~

桩只是返回桩数据。
