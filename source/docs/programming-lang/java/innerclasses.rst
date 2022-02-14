=======
内部类
=======

创建内部类
----------

当你在内部类中需要生成对外部类对象的引用时，可以使用 ``OuterClassName.this``，\ 
这样产生的引用自动具有正确的类型。

.. code-block:: java
    :emphasize-lines: 8

    //: innerclasses/DotThis.java
    // Qualifying access to the outer-class object.

    public class DotThis {
        void f() { System.out.println("DotThis.f()"); }
        public class Inner {
            public DotThis outer() {
                return DotThis.this;
                // A plain "this" would be Inner's "this"
            }
        }
        public Inner inner() { return new Inner(); }
        public static void main(String[] args) {
            DotThis dt = new DotThis();
            DotThis.Inner dti = dt.inner();
            dti.outer().f();
        }
    } /* Output:
    DotThis.f()
    *///:~

当你想要创建内部类对象时，必须首先创建外部类对象，获得外部类对象的引用，然后使用 ``.new`` 
语法创建内部类对象。

.. code-block:: java
    :emphasize-lines: 7, 8

    //: innerclasses/DotNew.java
    // Creating an inner class directly using the .new syntax.

    public class DotNew {
        public class Inner {}
        public static void main(String[] args) {
            DotNew dn = new DotNew();
            DotNew.Inner dni = dn.new Inner();
        }
    } ///:~

在拥有外部类之前是不可能创建内部类对象的，也就是说，无法直接创建内部类对象。
因为内部类对象会暗暗地连接到创建它的外部类对象上。
但是如果你创建的是静态内部类，那么不需要对外部类对象的引用，而直接创建内部类对象了。

内部类是延时加载的，也就是说只会在第一次使用时加载。
不使用就不加载，所以可以很好的实现 **单例模式** [1]_。
也就是说，在没有创建内部类对象的情况下，内部类不会自动初始化（调用构造函数），但在编译期会生成 
``OuterClassName$InnerClassName.class`` 文件。

.. code-block:: java
    :emphasize-lines: 32, 33

    //: innerclasses/Parcel2.java
    // Returning a reference to an inner class.

    public class Parcel2 {
        class Contents {
            private int i = 11;
            public int value() { return i; }
        }
        class Destination {
            private String label;
            Destination(String whereTo) {
                label = whereTo;
            }
            String readLabel() { return label; }
        }
        public Destination to(String s) {
            return new Destination(s);
        }
        public Contents contents() {
            return new Contents();
        }
        public void ship(String dest) {
            Contents c = contents();
            Destination d = to(dest);
            System.out.println(d.readLabel());
        }
        public static void main(String[] args) {
            Parcel2 p = new Parcel2();
            p.ship("Tasmania");
            Parcel2 q = new Parcel2();
            // Defining references to inner classes:
            Parcel2.Contents c = q.contents();          // 初始化内部类对象
            Parcel2.Destination d = q.to("Borneo");
        }
    } /* Output:
    Tasmania
    *///:~

内部类对象可以访问外部类对象的所有成员，而不需要任何特殊条件。
内部类之所以具有这种特殊的访问权限，是因为当某个外部类的对象创建一个内部类对象时，\ 
此内部类对象必定会秘密地捕获一个指向那个外部类对象的引用。
然后，在你访问此外部类的成员时，就是用那个引用来选择外部类的成员。
这种引用关系的传递由编译器完成，程序员一般不用操心。


内部类与隐藏实现
----------------

内部类可以向上转型为基类，也可以向上转型为接口。
又因为内部类会天然持有外部类对象的引用，当内部类声明为 ``private`` 时，可以只得到指向基类或接口的引用。
这样，接口的实现能够完全不可见，并且不可用，所以能够很方便地隐藏实现细节。

举个例子来支持上面的表述：

.. uml::

    @startuml
    Contents <|.. PContents
    Destination <|.. PDestination
    Parcel4 +-- PContents
    Parcel4 +-- PDestination

    class PDestination {
        -String label
        +readLabel()
    }

    class PContents {
        -int i
        +int value()
    }

    class Parcel4 {
        +Destination destination
        +Contents contents
    }

    interface Destination {
        +String readLabel()
    }

    interface Contents {
        +int Value()
    }
    @enduml

.. code-block:: java

    //: innerclasses/Destination.java
    public interface Destination {
        String readLabel();
    } ///:~

    //: innerclasses/Contents.java
    public interface Contents {
        int value();
    } ///:~

    //: innerclasses/TestParcel.java

    class Parcel4 {
        private class PContents implements Contents {
            private int i = 11;
            public int value() { return i; }
        }
        protected class PDestination implements Destination {
            private String label;
            private PDestination(String whereTo) {
                label = whereTo;
            }
            public String readLabel() { return label; }
        }
        public Destination destination(String s) {
            return new PDestination(s);
        }
        public Contents contents() {
            return new PContents();
        }
    }

    public class TestParcel {
        public static void main(String[] args) {
            Parcel4 p = new Parcel4();
            Contents c = p.contents();
            Destination d = p.destination("Tasmania");
            // Illegal -- can't access private class:
            //! Parcel4.PContents pc = p.new PContents();
        }
    } ///:~


除了在类的内部声明内部类，我们同样可以 **在方法和作用域内的内部类**，这么做有两个理由：
1）如前所示，你实现了某类型的接口，于是可以创建并返回对其的引用。
2）你要解决一个复杂的问题，向创建一个类来辅助你的解决方案，但是又不希望这个类是公共可用的。


.. _factory-mode-v2:

匿名内部类
----------

匿名内部类就是在类的一个方法中，直接 ``return`` 一个实例对象。以前创建对象使用 
``new ClassName()``，但是在返回匿名对象时，在小括号后紧跟大括号，在大括号中声明类的属性以及行为。

.. code-block:: java

    //: innerclasses/Parcel10.java
    // Using "instance initialization" to perform
    // construction on an anonymous inner class.

    public class Parcel10 {
        public Destination destination(final String dest, final float price) {
            return new Destination() {
                private int cost;
                // Instance initialization for each object:
                {
                    cost = Math.round(price);
                    if(cost > 100)
                        System.out.println("Over budget!");
                }
                private String label = dest;
                public String readLabel() { return label; }
            };
        }	
        public static void main(String[] args) {
            Parcel10 p = new Parcel10();
            Destination d = p.destination("Tasmania", 101.395F);
        }
    } /* Output:
    Over budget!
    *///:~

匿名内部类既可以扩展类，也可以实现接口，但是不能两者兼备。而且，如果是实现接口，也只能实现一个接口。

如果定义一个匿名内部类，并且希望它使用一个在其外部定义的对象，那么编译器会要求其参数引用是 ``final`` 的。

之前实现过一次工厂模式（\ :ref:`factory-mode-v1`）。不同的是，现在 ``Implementation1`` 和
``Implementation2`` 的构造器都可以是 ``private`` 的，并且没有任何必要去创建作为工厂的具名类
``ServiceFactory``。另外，你经常只需要单一的工厂对象，因此在本例中它被创建为 ``Service``
实现中的一个 ``static`` 域。

.. code-block:: java

    //: innerclasses/Factories.java
    import static net.mindview.util.Print.*;

    interface Service {
        void method1();
        void method2();
    }

    interface ServiceFactory {
        Service getService();
    }	

    class Implementation1 implements Service {
        private Implementation1() {}
        public void method1() {print("Implementation1 method1");}
        public void method2() {print("Implementation1 method2");}
        public static ServiceFactory factory =
            new ServiceFactory() {
                public Service getService() {
                    return new Implementation1();
                }
            };
    }	

    class Implementation2 implements Service {
        private Implementation2() {}
        public void method1() {print("Implementation2 method1");}
        public void method2() {print("Implementation2 method2");}
        public static ServiceFactory factory =
            new ServiceFactory() {
                public Service getService() {
                    return new Implementation2();
                }
            };
    }	

    public class Factories {
        public static void serviceConsumer(ServiceFactory fact) {
            Service s = fact.getService();
            s.method1();
            s.method2();
        }
        public static void main(String[] args) {
            serviceConsumer(Implementation1.factory);
            // Implementations are completely interchangeable:
            serviceConsumer(Implementation2.factory);
        }
    } /* Output:
    Implementation1 method1
    Implementation1 method2
    Implementation2 method1
    Implementation2 method2
    *///:~


.. _nested-class:

嵌套类
------

我们给 ``static`` 内部类起一个别名，称为嵌套类。
如果不需要内部类对象与其外部类对象之间有联系，那么可以将内部类声明为 ``static``。
一个内部类被嵌套多少层并不重要，重要的是，它能够透明地访问所有它所嵌入的外部类的所有成员。

普通的内部类对象隐式地保存了一个引用，指向创建它的外部类对象。然而，当内部类是 ``static`` 
时，不需要其外部类的对象，而且，需要注意的是，不能从嵌套类的对象中访问非静态的外部类对象。
因此，普通的内部类不能有 ``static`` 属性和方法，也不能包含嵌套类，而嵌套类可以包含这些 
``static`` 属性、方法或类。

.. code-block:: java

    //: innerclasses/Parcel11.java
    // Nested classes (static inner classes).

    public class Parcel11 {
        private static class ParcelContents implements Contents {
            private int i = 11;
            public int value() { return i; }
        }
        protected static class ParcelDestination implements Destination {
            private String label;
            private ParcelDestination(String whereTo) {
                label = whereTo;
            }
            public String readLabel() { return label; }	
            // Nested classes can contain other static elements:
            public static void f() {}
            static int x = 10;
            static class AnotherLevel {
                public static void f() {}
                static int x = 10;
            }
        }
        public static Destination destination(String s) {
            return new ParcelDestination(s);
        }
        public static Contents contents() {
            return new ParcelContents();
        }
        public static void main(String[] args) {
            Contents c = contents();
            Destination d = destination("Tasmania");
        }
    } ///:~

正常情况下，在接口内不能有任何实现，但是嵌套类却可以作为接口的一部分，在嵌套类中实现外部类的接口。

因为在接口中的内部类，若不加以声明，默认都是 ``public static`` 的，故嵌套类是 
``static`` 只是将嵌套类置于接口的命名空间内，这并不违反 :ref:`interface-definition`。

.. code-block:: java

    //: innerclasses/ClassInInterface.java
    // {main: ClassInInterface$Test}

    public interface ClassInInterface {                 // 接口类
        void howdy();
        class Test implements ClassInInterface {        // 接口内的实现类
            public void howdy() {
                System.out.println("Howdy!");
            }
            public static void main(String[] args) {    // main() 测试
                new Test().howdy();
            }
        }
    } /* Output:
    Howdy!
    *///:~

在 :ref:`inheritance-syntax` 小节的小技巧中，我们提到，可以在每个类中都写一个 ``main()`` 
方法，用来测试这个类。这样做有一个缺点，那就是必须带着哪些已编译过的额外代码。
如果这对你是个麻烦，那就可以在嵌套类中编写测试代码，发布代码时，只需要将内部类的 
``.class`` 文件删除即可。

.. code-block:: java

    //: innerclasses/TestBed.java
    // Putting test code in a nested class.
    // {main: TestBed$Tester}

    public class TestBed {                              // 外部类
        public void f() { 
            System.out.println("f()"); 
        }
        public static class Tester {                    // 嵌套类
            public static void main(String[] args) {    // main() 测试
                TestBed t = new TestBed();
                t.f();
            }
        }
    } /* Output:
    f()
    *///:~


为什么需要内部类
----------------

1）多重继承的实现，既可以使用接口，也可以使用内部类。（如何理解？）


闭包与回调
~~~~~~~~~~

闭包（closure）是一个可调用的对象，它记录了一些信息，这些信息来自于创建它的作用域。
通过定义，可以看出内部类是一个闭包，因为它不仅包含外部类对象的信息，还自动地拥有一个指向外部类对象的引用。

回调（callback）通过指针实现对另一个对象的引用，进而可以操作对象中的函数。
通过回调，对象能够携带一些信息，这些信息允许它在稍后的某个时刻调用初始对象。
内部类比指针更灵活，更安全。
回调的价值在于它的灵活性，可以在运行时动态地决定需要调用什么方法。

下面的代码中，内部类 Closure 实现了 Incrementable，以提供一个返回 Callee2 的 
"钩子"（hook）——而且是一个安全的钩子。
无论谁获得此 Incrementable 引用，都只能调用 increment()，除此之外没有其他功能（不想指针那样，允许你做很多事情）。

.. uml::

    @startuml

    Incrementable <|.. Callee1
    MyIncrement <|-- Callee2
    Callee2 +-- Closure
    Incrementable <|.. Closure

    interface Incrementable {
        void increment()
    }
    class Callee1 {
        void increment()
    }
    class MyIncrement {
        void increment()
        void f(MyIncrement mi)
    }
    class Callee2 {
        void increment()
        Incrementable getCallbackReference()
    }
    class Caller {
        -Incrementable callbackReference
        Caller(Incrementable cbh) { callbackReference = cbh; }
        void go() { callbackReference.increment(); }
    }

    class Closure {
        void increment()
    }

    @enduml

.. code-block:: java

    //: innerclasses/Callbacks.java
    // Using inner classes for callbacks
    package innerclasses;
    import static net.mindview.util.Print.*;

    interface Incrementable {
        void increment();
    }

    // Very simple to just implement the interface:
    class Callee1 implements Incrementable {
        private int i = 0;
        public void increment() {
            i++;
            print(i);
        }
    }	

    class MyIncrement {
        public void increment() { print("Other operation"); }
        static void f(MyIncrement mi) { mi.increment(); }
    }	

    // If your class must implement increment() in
    // some other way, you must use an inner class:
    class Callee2 extends MyIncrement {
        private int i = 0;
        public void increment() {
            super.increment();
            i++;
            print(i);
        }
        private class Closure implements Incrementable {
            public void increment() {
                // Specify outer-class method, otherwise
                // you'd get an infinite recursion:
                Callee2.this.increment();
            }
        }
        Incrementable getCallbackReference() {
            return new Closure();
        }
    }	

    class Caller {
        private Incrementable callbackReference;
        Caller(Incrementable cbh) { callbackReference = cbh; }
        void go() { callbackReference.increment(); }
    }

    public class Callbacks {
        public static void main(String[] args) {
            Callee1 c1 = new Callee1();
            Callee2 c2 = new Callee2();
            MyIncrement.f(c2);
            Caller caller1 = new Caller(c1);
            Caller caller2 = new Caller(c2.getCallbackReference());
            caller1.go();
            caller1.go();
            caller2.go();
            caller2.go();
        }	
    } /* Output:
    Other operation
    1
    1
    2
    Other operation
    2
    Other operation
    3
    *///:~

内部类与控制框架
~~~~~~~~~~~~~~~~

应用程序框架（application framework）就是被设计用来解决某类特定问题的一个类或一组类。要运用某个应用程序框架，通常是继承一个类或多个类，并覆盖某些方法。

Java Swing 库就是一个控制框架，它解决了 GUI 的问题，并大量使用了内部类。

控制框架的精髓在于：使变化的事物和不变的事物相互分离。

内部类的继承
------------

因为内部类的构造器必须连接到指向其外部类对象的引用，因此，在继承类中，必须在构造器中显式地指明初始化语句。

.. code-block:: java
    :emphasize-lines: 11

    //: innerclasses/InheritInner.java
    // Inheriting an inner class.

    class WithInner {
        class Inner {}
    }

    public class InheritInner extends WithInner.Inner {
        //! InheritInner() {} // Won't compile
        InheritInner(WithInner wi) {
            wi.super();
        }
        public static void main(String[] args) {
            WithInner wi = new WithInner();
            InheritInner ii = new InheritInner(wi);
        }
    } ///:~


局部内部类
----------

在方法体内创建内部类叫局部内部类。局部内部类不能有访问说明符。

使用局部内部类而不使用匿名内部类理由：我们需要一个可以命名的构造器，或者需要重载内部类的构造器，而匿名内部类只能用于实例初始化。

内部类标识符
------------

内部类经过编译后会生成 ``OuterClassName$InnerClassName.class`` 文件，多级嵌套，就用多个 ``$`` 
符号分隔开。如果是匿名内部类，编译器会简单地生成一个数字作为标识，比如 ``OuterClassName$1.class``。

.. rubric:: 参考资料

.. [1] 内部类的加载时机 https://blog.csdn.net/brouth/article/details/51656603
