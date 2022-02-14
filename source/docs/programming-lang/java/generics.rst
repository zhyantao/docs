=====
泛型
=====

背景知识
---------

泛型（generics）是 JDK 5 中引入的一个新特性，允许在定义类和接口的时候使用类型参数。

正常情况下，我们经常会给方法传递参数，那么能不能给类或接口传递参数呢？因此，诞生了泛型。

泛型的诞生，很大一部分应用都是用在容器上了。

我们知道，一个 List 容器可以放入不同类型的元素，如果没有泛型，那么当我们想要存放 String 元素时，
就需要定义一个可以接受 String 的 List 接口，后面想放 Interger 时，又要定义另一个接口。

而泛型的出现，最大的好处就是可以提高代码的复用性。
我们使用 JDK 为我们提供的泛型接口，可以方便地存放各种不同类型的元素到容器中，而不用自己实现。

使用泛型的好处就是在编译的时候能够检查类型安全，并且所有的强制转换都是自动和隐式的。


通配符
------

通配符是文本值中代替未知字符的特殊字符，可方便使用类似但不相同的数据查找多个项目。

在计算机软件技术中，通配符可用于代替单个或多个字符。

通常地，星号 ``*`` 匹配 0 个或以上的字符，问号 ``?`` 匹配 1 个字符。

在 Java 泛型中，常用的通配符和含义如下（没有星号）：

- ``E`` ：Element，在集合中使用，因为集合中存放的是元素
- ``T`` ：Type，Java 类
- ``K`` ：Key，键
- ``V`` ：Value，值
- ``N`` ：Number，数值类型
- ``?`` ：表示不确定的 Java 类型

**限定通配符** 对类型进⾏限制， 泛型中有两种限定通配符：（尖括号部分只是代表一个具体类型）

- 上界通配符，格式为： ``<? extends T>`` 是指泛型中的类必须为当前类的子类或当前类；
- 下界通配符，格式为： ``<? super T>`` 是指泛型中的类必须为当前类或者其父类。

泛型类型必须⽤限定内的类型来进⾏初始化，否则会导致编译错误。

在使用泛型时，存取元素时用 ``super``，获取元素时，用 ``extends``。 

频繁往外读取内容的，适合用上界 ``Extends``。经常往里插入的，适合用下界 ``Super``。

**⾮限定通配符** 表⽰可以⽤任意泛型类型来替代，类型为 ``<T>``。


简单泛型
--------

在这个案例中，我们用 ``Holder3`` 持有 ``Automobile`` 对象。代码实现如下：

.. code-block:: java

    //: generics/Holder3.java

    class Automobile {}

    public class Holder3<T> {
        private T a;
        
        public Holder3(T a) { 
            this.a = a; 
        }
        
        public void set(T a) { 
            this.a = a; 
        }
        
        public T get() { 
            return a; 
        }
        
        public static void main(String[] args) {
            Holder3<Automobile> h3 = new Holder3<Automobile>(new Automobile());
            Automobile a = h3.get(); // No cast needed
            // h3.set("Not an Automobile"); // Error
            // h3.set(1); // Error
        }
    } ///:~

使用了泛型之后，我们得到了一个类型安全的容器，在取出容器的内容时，编译器自动为我们完成了转型。
因为我们给容器说，只能接收 ``Automobile`` 类型的对象，因此，在传入 ``String`` 和 ``Interger`` 
对象时都报错了。

使用泛型的容器除了能够接收单一类型的对象外，也可以设计为能够接收多个类型的对象，比如下面代码所示：

.. code-block:: java

    //: net/mindview/util/TwoTuple.java
    package net.mindview.util;

    public class TwoTuple<A,B> {
        public final A first;
        public final B second;
        
        public TwoTuple(A a, B b) { 
            first = a; 
            second = b; 
        }
        
        public String toString() {
            return "(" + first + ", " + second + ")";
        }
    } ///:~


这种成对的对象，我们可以称之为 **元组**。往容器中塞对象时，需要一次一个元组。

上面的代码段是一次塞两个对象，而且我们可以使用继承机制实现更长的元组。

.. code-block:: java

    //: net/mindview/util/ThreeTuple.java
    package net.mindview.util;

    public class ThreeTuple<A,B,C> extends TwoTuple<A,B> {
        public final C third;

        public ThreeTuple(A a, B b, C c) {
            super(a, b);
            third = c;
        }
        
        public String toString() {
            return "(" + first + ", " + second + ", " + third +")";
        }
    } ///:~

为了 **使用元组**，你只需要定义一个长度合适的元组，将其作为方法的返回值，然后再 ``return`` 
语句中创建该元组，并返回即可。

.. code-block:: java

    //: generics/TupleTest.java
    import net.mindview.util.*;

    public class TupleTest {
        static TwoTuple<String,Integer> f() {
            // Autoboxing converts the int to Integer:
            return new TwoTuple<String,Integer>("hi", 47);
        }
        
        public static void main(String[] args) {
            TwoTuple<String,Integer> ttsi = f();
            System.out.println(ttsi);
            // ttsi.first = "there"; // Compile error: final
        }
    } /* Output:
    (hi, 47)
    *///:~


泛型接口
--------

将泛型应用于接口，我们希望实现该接口的类，能够返回给我们满足一些符合我们预期的类型信息。

作为案例，我们希望创建一个生成器，它可以给我们生成（返回）Fibonacci 数列中的下一个值。

一般而言，一个生成器只定义一个方法，该方法用以产生新对象。在这里，就是用 ``next()`` 方法。

.. code-block:: java

    //: net/mindview/util/Generator.java
    // A generic interface.
    package net.mindview.util;
    
    public interface Generator<T> { 
        T next(); 
    } ///:~

比如我们可以实现 ``Generator`` 类，用以生成 Fibonacci 数列。

.. code-block:: java
    :emphasize-lines: 8

    //: generics/Fibonacci.java
    // Generate a Fibonacci sequence.
    import net.mindview.util.*;

    public class Fibonacci implements Generator<Integer> {
        private int count = 0;
        
        public Integer next() { 
            return fib(count++); 
        }
        
        private int fib(int n) {
            if(n < 2) 
                return 1;
            return fib(n-2) + fib(n-1);
        }

        public static void main(String[] args) {
            Fibonacci gen = new Fibonacci();
            for(int i = 0; i < 18; i++)
                System.out.print(gen.next() + " ");
        }
    } /* Output:
    1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584
    *///:~

虽然，在 Fibonacci 类使用的都是 ``int`` 类型，但是其类型参数却是 ``Integer``。

这个例子引出了 Java **泛型的一个局限性：基本类型无法作为类型参数**。

不过，Java SE5 具备自动打包和拆包的功能，可以很方便地在基本类型和其相应的包装器类型之间进行转换。


泛型方法
--------

.. hint:: 

    如果使用泛型方法可以取代整个类泛型化，那么就应该只使用泛型方法。

定义泛型方法，只需将泛型参数列表置于返回值之前。

.. code-block:: java
    :emphasize-lines: 4

    //: generics/GenericMethods.java

    public class GenericMethods {
        public <T> void f(T x) {
            System.out.println(x.getClass().getName());
        }
        public static void main(String[] args) {
            GenericMethods gm = new GenericMethods();
            gm.f("");
            gm.f(1);
            gm.f(1.0);
            gm.f(1.0F);
            gm.f('c');
            gm.f(gm);
        }
    } /* Output:
    java.lang.String
    java.lang.Integer
    java.lang.Double
    java.lang.Float
    java.lang.Character
    GenericMethods
    *///:~

**可变参数与泛型方法：**

.. code-block:: java

    //: generics/GenericVarargs.java
    import java.util.*;

    public class GenericVarargs {
        public static <T> List<T> makeList(T... args) {
            List<T> result = new ArrayList<T>();
            for(T item : args)
                result.add(item);
            return result;
        }
        public static void main(String[] args) {
            List<String> ls = makeList("A");
            System.out.println(ls);
            ls = makeList("A", "B", "C");
            System.out.println(ls);
            ls = makeList("ABCDEFFHIJKLMNOPQRSTUVWXYZ".split(""));
            System.out.println(ls);
        }
    } /* Output:
    [A]
    [A, B, C]
    [, A, B, C, D, E, F, F, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z]
    *///:~

当使用泛型类时，必须在创建对象的时候指定类型参数的值，而使用泛型方法的时候，通常不必指明参数类型。
因为编译器会为我们找出具体的类型。这称为 **类型参数推断（type argument inference）**。

因此， **我们可以像调用普通方法一样调用 f()，就好像 f() 被无限次地重载过。** 甚至，它可以接受 
``GenericMethods`` 作为其参数类型。

**类型推断只对赋值操作有效，其他时候并不起作用。**
如果你将一个泛型方法调用的结果作为参数，传递给另一个方法，这时编译器不会执行推断。
在这种情况下，编译器认为，调用泛型方法后，其返回值被赋给一个 ``Object`` 类型的变量。
比较下面两个程序段：

程序段一：等号赋值，可以推断

.. code-block:: java

    //: generics/SimplerPets.java
    import typeinfo.pets.*;
    import java.util.*;
    import net.mindview.util.*;

    public class SimplerPets {
        public static void main(String[] args) {
            Map<Person, List<? extends Pet>> petPeople = New.map(); // 等号赋值给一个泛型容器
            // Rest of the code is the same...
        }
    } ///:~

程序段二：参数引用传递，不能推断

.. code-block:: java

    //: generics/LimitsOfInference.java
    import typeinfo.pets.*;
    import java.util.*;

    public class LimitsOfInference {
        static void f(Map<Person, List<? extends Pet>> petPeople) {}
        public static void main(String[] args) {
            // f(New.map()); // Does not compile  // 函数返回值作为参数赋值给泛型容器
        }
    } ///:~


.. _erase-typeinfo:

类型擦除
--------

类型擦除指的是通过类型参数合并，将泛型类型实例关联到同一份字节码上。
编译器只为泛型类型生成一份字节码，并将其实例关联到这份字节码上。
具象化一些就是，我们可以声明 ``ArrayList.class`` 但是不能声明 ``ArrayList<Integer>.class`` 
就是因为擦除。擦除会移除参数类型信息。 ``List<String>`` 与 ``List<Integer>`` 
在运行时事实上是相同的类型，即 ``List``。

类型擦除的关键在于从泛型类型中清除类型参数的相关信息，并且再必要的时候添加类型检查和类型转换的方法。

类型擦除可以简单的理解为将泛型 Java 代码转换为普通 Java 代码，只不过编译器更直接点，将泛型 Java 
代码直接转换成普通 Java 字节码。

以 ``List<T extends HasF>`` 为例，类型擦除的主要过程如下：

1. 将所有的泛型参数用其最左边界（最顶级的父类型）类型替换。这是说，泛型参数 ``<T extends HasF>``
   经过擦除后，变成了 ``HasF``。若 ``<T>`` 未指定边界，将被擦除为 ``Object``。
2. 移除所有的类型参数。经过这一步变换， ``List<T extends HasF>`` 就变成了额 ``List``。


擦除带来的问题
--------------

丢失类型信息
~~~~~~~~~~~~

擦除最直接的影响就是丢失了一些类型信息。

**擦除直观上的理解就是发生了向上转型**，它丢失了泛型代码中执行某些操作的能力。
任何在运行时需要知道确切类型信息的操作都将无法工作。比如，下面的代码段无法进行编译：

.. code-block:: cpp

    //: generics/Erased.java
    // {CompileTimeError} (Won't compile)

    public class Erased<T> {
        private final int SIZE = 100;
        
        public static void f(Object arg) {
            if(arg instanceof T) {}           // Error
            T var = new T();                  // Error
            T[] array = new T[SIZE];          // Error
            T[] array = (T)new Object[SIZE];  // Unchecked warning
        }
    } ///:~


泛型与重载
~~~~~~~~~~~

当类型擦除遇到重载时，也会遇到一些问题，如下代码，它将无法通过编译：

.. code-block:: java

    import java.util.List;

    public class TypeErasue {
        public static void method(List<String> list) {
            System.out.println("invoke method(List<String> list)");
        }
        public static void method(List<Integer> list) {
            System.out.println("invoke method(List<Integer> list)");
        }
    }

因为前面讲过， ``List<Integer>`` 和 ``List<String>`` 编译后都被擦除了，变成了一样的原生类型 ``List``。
擦除动作导致这两个方法的特征签名变得一模一样。


泛型与 catch
~~~~~~~~~~~~~

如果我们自定义了一个泛型异常类 ``GenericException``，那么不要尝试用多个 ``catch`` 取匹配不同的异常类型。
例如你想要分别捕获 ``GenericException`` 、 ``GenericException``，这也是有问题的。


泛型内包含静态变量
~~~~~~~~~~~~~~~~~~

先阅读一下下面的代码段，你认为结果是多少？

.. code-block:: cpp

    class MyStatic<T> {
        public static int var = 0; // 泛型内的静态变量
    }

    public class TypeErasue {
        public static void main(String[] args) {
            MyStatic<Integer> myStatic1 = new MyStatic<Integer>();
            myStatic1.var = 1;
            MyStatic<String> myStatic2 = new MyStatic<String>();
            myStatic2.var = 2;
            System.out.println(myStatic1.var);
        }
    }

答案是 2。经过类型擦除，所有的泛型类实例都关联到同一份字节码上，因此，\ **泛型类的所有静态变量是共享的**\。


List 和 List<Object>
----------------------

**区别一：**

原始类型 ``List`` 和带参数类型 ``List<Object>`` 之间的主要区别是：
在编译时编译器不会对原始类型进行类型安全检查，却会对带参数的类型进行检查。

通过使用 ``Object`` 作为类型，可以告知编译器该方法可以接受任何类型的对象，比如 ``String`` 或 ``Integer``。

**区别二：**

你可以把任何带参数的类型传递给原始类型 ``List``，但却不能把 ``List<String>`` 传递给接受 ``List<Object>`` 
的方法，因为会产生编译错误。


List<?> 和 List<Object>
-------------------------

``List<?>`` 是一个未知类型的 ``List``，而 ``List<Object>`` 其实是任意类型的 ``List``。你可以把 ``List<String>``，\ 
``List<Integer>`` 赋值给 ``List<?>``，却不能把 ``List<String>`` 赋值给 ``List<Object>``。