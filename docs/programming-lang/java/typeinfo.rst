========
类型信息
========

为什么需要类型信息
------------------

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

比如，当把元素放入数组 ``List<Shape>`` 中时，会丢失 ``Shape`` 类型信息，向上转型为 ``Object``。

当从数组 ``List<Shape>`` 中取出元素时，容器 ``List`` 会自动将结果转型回 ``Shape``。

这是 RTTI 最基本的使用形式，因为在 Java 中，所有的类型转换都是在运行时进行正确性检查的。

但是，这个例子 RTTI 转型并不彻底， ``Object`` 被转型为 ``Shape``，并没有转型为 ``Circle`` 、 ``Square`` 或者 ``Triangle``。
这是因为目前我们只知道这个 ``List<Shape>`` 保存的都是 ``Shape``。这是由 **容器** 和 **泛型** 来保证这种机制的。

接下来是由 **多态** 进行动态绑定，将 ``Shape`` 转型为 ``Circle`` 、 ``Square`` 或者 ``Triangle``。

获取类型信息的方式
------------------

Java 在 **运行时** 识别对象和类的信息，主要有两种方式：

- RTTI（Runtime Type Identification）运行时类型识别
- 反射：允许在运行时发现和使用类的信息

**相同点：** RTTI 和反射在使用类之前都必须获取到那个类的 Class 对象。
因此，那个类的 ``.class`` 文件对于 JVM 来说必须是可获取的，要么在本地机器上，要么可以通过网络获得。

**不同点：** 对 RTTI 来说，编译器在编译时打开和检查 ``.class`` 文件，而对于反射来说，
``.class`` 文件在编译时是不可获取的，所以是在运行时打开和检查 ``.class`` 文件。

如果你的程序代码处于同一块程序空间，但是不知道某个对象的确切类型，RTTI 可以告诉你。
但是有一个限制：这个类型在编译时必须已知，这样才能使用 RTTI 识别它，并利用这些信息做一些有用的事情。

但是，假设你获取了一个指向某个并不在你的程序空间中的对象的引用，
事实上，在编译时你的程序根本没法获知这个对象所属的类。
例如，假设你从磁盘文件或网络连接中获取了一串字节。
这时候，反射才能解决问题。

类型信息的工作原理
------------------

假如我们编写了一个文件，叫 ``MyType.java``，它会发生下列一系列动作：（RTTI 过程）

1. 运行 ``javac MyType.java`` 得到一堆 ``.class`` 文件，其中有一个叫 ``MyType.class``
2. 运行 ``java MyType`` 后，JVM 类加载器首先将 ``MyType.class`` 加载到内存（\ `动态加载 <https://www.liaoxuefeng.com/wiki/1252599548343744/1264799402020448>`_\ ）
3. 为 ``.class`` 文件中包含的静态域分配空间
4. 为 ``MyType.class`` 创建 ``Class`` 对象 ``Class cls = new Class(MyType)``
5. 用 ``Class`` 对象 ``cls`` 创建这个类的构造器引用
6. 运行到某一句时，如果发现依赖其他类，就搜索对应的 ``.class`` 文件并加载到内存，重复步骤 3 ~ 6

注意，JVM 在执行 Java 程序的时候，并不是一次性把所有用到的 ``.class`` 全部加载到内存，而是第一次需要用到 ``.class`` 时才加载。

.. admonition:: 示例代码
    :class: dropdown

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
                    Class.forName("Gum"); // 对象调用方法
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

如何获取类型信息
----------------

获取某个类的 Class 实例的方式有三个方法：

- 对完整类名应用 Class 类的静态方法： ``Class.forName("完整类名")``
- 对实例对象应用 Class 类的静态方法： ``实例对象.getClass()``
- 通过类字面常量： ``类名.class``

使用类字面常量生成对 ``Class`` 对象的引用，这样做比用 ``forName()`` 更简单、更安全。

使用 ``.class`` 创建对 ``Class`` 对象的引用时，不会自动初始化该 ``Class`` 对象，而使用 ``forName()`` 会初始化对象。

类字面常量可以用于：普通类、接口、数组、基本数据类型、基本数据类型的包装器类。

补充 ``Class`` 对象常用的方法：

- ``Class.forName()`` 查找相应类的对象的 ``Class`` 对象引用
- ``Class.getClass()`` 获取 ``Class`` 对象的引用
- ``Class.getInterfaces()`` 获取感兴趣的对象所包含的接口
- ``Class.getSuperclass()`` 查找基类

实例对象 object 的常用方法：

- ``object.getSimpleName()`` 产生不包含包名的类名
- ``object.getCanonicalName()`` 产生全限定的类名

如何检查类型信息
----------------

``Class`` 引用总是指向某个 ``Class`` 对象，它可以用于创建类的对象。
创建出来的对象包含可作用于这些对象的所有方法代码，它还包含该类的静态成员。

普通的类的引用可以被重新赋值为指向任何其他的 ``Class`` 对象，但这是不安全的。
因此，可以使用泛型语法对 ``Class`` 引用所指向的 ``Class`` 对象的类型进行限定。

为了放宽这种限定，可以使用通配符，比如 ``Class<?>``。

向 ``Class`` 引用添加泛型语法的原因仅仅是为了提供编译期类型检查。

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

为了确保类型转换是正确的，一般来讲由 RTTI 确保类型转换的正确性，如果执行了一个错误的类型转换，就抛出 ``ClassCastException`` 异常。
RTTI 通过查询 ``Class`` 对象获取运行时所需要的信息，但是在编译期，编译器不知道确定的类型，需要人为指定向下转型的具体类型。
因此，引出关键字 ``instanceof``，使用提问的方式，如下

.. code-block:: java

    if (x instanceof Dog)
        ((Dog)x).bark()

``Class.isInstance()`` 方法提供了一种 **动态地测试** 对象的途径。

.. code-block:: java

    objA.isInstance(objB)

如何比较类型信息
----------------

查询类型信息时，通过比较获取到的对象引用，发现：

- ``instanceof`` 或 ``isInstance()`` 考虑继承关系， ``子.instanceof(父)=true``， ``父.instanceof(子)=false``
- ``==`` 和 ``getClass()`` 不考虑继承关系，获取到的是最具体的类型信息

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

人们想要在运行时获取类的信息的另一个动机，是希望提供在跨网络的远程平台上创建和运行对象的能力。
这被称为 **远程方法调用（RMI）**，它允许一个 Java 程序对象分布到多台机器上。

- 将大的计算任务分成小的计算单元，分布到不同机器上（分布式计算）
- 将处理特定类型任务的代码分布到不同的机器上（多层的 C/S 架构）

正常情况下，如果我们要调用一个对象的方法，或者访问一个对象的字段，通常会传入对象实例：

.. code-block:: java

    // Main.java
    import com.itranswarp.learnjava.Person;

    public class Main {
        String getFullName(Person p) { // 传入 Person 实例
            return p.getFirstName() + " " + p.getLastName();
        }
    }

但是，如果不能获得 ``Person`` 类，只有一个 ``Object`` 实例，比如这样：

.. code-block:: java

    String getFullName(Object obj) {
        return ???
    }

怎么办？有童鞋会说：强制转型啊！

.. code-block:: java

    String getFullName(Object obj) {
        Person p = (Person) obj;
        return p.getFirstName() + " " + p.getLastName();
    }

强制转型的时候，你会发现一个问题：编译上面的代码，仍然需要引用 ``Person`` 类。
不然，去掉 ``import`` 语句，你看能不能编译通过？

所以，反射是为了解决在运行期，对某个实例一无所知的情况下，如何调用其方法。

反射机制指的是程序在运行时能够获取自身的信息。
在 Java 中，只要给定类的名字，那么就可以通过反射机制来获得类的所有属性和方法。

反射的作用是：

- 在运行时判断任意一个对象所属的类；
- 在运行时判断任意一个类所具有的成员变量和方法；
- 在运行时任意调用一个对象的方法；
- 在运行时构造任意一个类的对象。

``Class`` 类与 ``java.lang.reflect`` 类库一起，对反射的概念提供了支持。
Java 的 ``Class`` 类是反射机制的基础，通过 ``Class`` 类，我们可以获得关于一个类的相关信息。

``java.lang.Class`` 是一个比较特殊的类，它用于封装被装入到 JVM 中的类（包装类和接口）的信息。
当一个类或接口被装入 JVM 时，便会产生一个与之关联的 ``java.lang.Class`` 对象，
可以通过这个 ``Class`` 对象对被装入类的详细信息进行访问。

反射可以实现动态创建对象和编译，灵活性好，但是它的性能不足，总是慢于直接执行相同的操作。
因此，在实际生产中，应用并不是很多。


例子：类方法提取器
------------------

通常，你不需要直接使用反射工具。反射在 Java 中是用来支持其他特性的，例如对象序列化和 JavaBean。

查找类定义的源代码或 JDK 文档是费时的， **类方法提取器帮助我们快速地提取某个类的信息**
，使我们能够编写自动展示完整接口的简单工具。

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
                        print(p.matcher(method.toString()).replaceAll(""));
                    for(Constructor ctor : ctors)
                        print(p.matcher(ctor.toString()).replaceAll(""));
                    lines = methods.length + ctors.length;
                } else {
                    for(Method method : methods)
                        if(method.toString().indexOf(args[1]) != -1) {
                            print(p.matcher(method.toString()).replaceAll(""));
                            lines++;
                        }
                    for(Constructor ctor : ctors)
                        if(ctor.toString().indexOf(args[1]) != -1) {
                            print(p.matcher(ctor.toString()).replaceAll(""));
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

例子：动态代理
--------------

代理是基本的设计模式之一，它是为了提供额外的或不同的操作而插入的、用来代替 "实际" 对象的对象。

这些操作通常涉及与 "实际" 对象的通信，因此，代理通常充当中间人的角色。

代理可以帮你做一些事情，但是你又不知道是谁做的。

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
        private Interface proxied; // 指向真实对象
        public SimpleProxy(Interface proxied) { // 接收真实对象
            this.proxied = proxied;
        }
        public void doSomething() {
            print("SimpleProxy doSomething"); // 做了额外的事情
            proxied.doSomething(); // 真实对象要做到事情
        }
        public void somethingElse(String arg) {
            print("SimpleProxy somethingElse " + arg); // 做了额外的事情
            proxied.somethingElse(arg); // 真实对象要做到事情
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
        public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
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
    **** proxy: class $Proxy0, method: public abstract void Interface.somethingElse(java.lang.String),
    args: [Ljava.lang.Object;@42e816
        bonobo
    somethingElse bonobo
    *///:~

通过静态方法 ``Proxy.newProxyInstance()`` 可以创建动态代理，这个方法需要：

- 一个类加载器（通常从已经被加载的对象中获取其类加载器，然后传递给它）
- 一个你希望该代理实现的接口列表（不是类或抽象类）
- 一个 ``InvocationHandler`` 接口的实现

动态代理可以将所有调用重定向到调用处理器，因此通常会向调用处理器的构造器传递一个 "实际" 对象的引用，
从而使得调用处理器在执行其中介任务时，可以将请求转发。

空对象
------

用途：模拟对象与桩，桩只是返回桩数据。

.. code-block:: java

    public interface Null {}
