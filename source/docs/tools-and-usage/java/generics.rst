=====
泛型
=====

一般的类和方法，只能使用具体的类型：要么是基本类型，要么是自定以类型。

泛型实现了参数化类型的概念，使代码可以应用于多种类型。在你创建参数化类型的一个实例时，
编译器会为你负责转型操作，并且确保类型的正确性。

泛型的主要目的之一就是用来指定容器要持有什么类型的对象。

简单泛型
--------

泛型出现的最大一个原因就是容器类。

.. code-block:: java

    //: generics/Holder3.java

    class Automobile {}

    public class Holder3<T> {
        private T a;
        public Holder3(T a) { this.a = a; }
        public void set(T a) { this.a = a; }
        public T get() { return a; }
        public static void main(String[] args) {
            Holder3<Automobile> h3 =
                new Holder3<Automobile>(new Automobile());
            Automobile a = h3.get(); // No cast needed
            // h3.set("Not an Automobile"); // Error
            // h3.set(1); // Error
        }
    } ///:~

一个元组类库
~~~~~~~~~~~~

想一次方法调用就能返回多个对象，但是 return 语句只允许返回单个对象。
因此解决办法就是创建一个对象，用它来持有想要返回的多个对象。

这个概念称为元组，它将一组对象直接打包存储与其中的一个单一对象。
这个容器对象允许读取其中的元素，但是不允许向其中存放新的对象。

通常，元组可以具有任意长度，同时，元组中的对象可以是任意不同的类型。

我们希望能够为每一个对象指明其类型，并且从容器中读取出来时，能够得到正确的类型。
要处理不同长度的问题，我们需要创建多个不同的元组。

下面的程序是一个 2 维元组，可以持有两个对象。

.. code-block:: java

    //: net/mindview/util/TwoTuple.java
    package net.mindview.util;

    public class TwoTuple<A,B> {
        public final A first;
        public final B second;
        public TwoTuple(A a, B b) { first = a; second = b; }
        public String toString() {
            return "(" + first + ", " + second + ")";
        }
    } ///:~

我们可以使用继承机制实现更长的元组。

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

为了 **使用元组** ，你只需要定义一个长度合适的元组，将其作为方法的返回值，然后再 return 语句中创建该元组，并返回即可。

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

泛型可以应用于接口。例如生成器，这是一种专门负责创建对象的类。实际上这是工厂方法设计模式的一种应用。

不过，当使用生成器创建新对象时，它不需要任何参数，而工厂方法一般需要参数。也就是说，生成器无需额外的信息就知道如何创建新对象。

一般而言，一个生成器只定义一个方法，该方法用以产生新对象。在这里，就是用 next() 方法。

.. code-block:: java

    //: net/mindview/util/Generator.java
    // A generic interface.
    package net.mindview.util;
    public interface Generator<T> { T next(); } ///:~

比如我们可以实现 Generator 类，用以生成 Fibonacci 数列。

.. code-block:: java
    :emphasize-lines: 7

    //: generics/Fibonacci.java
    // Generate a Fibonacci sequence.
    import net.mindview.util.*;

    public class Fibonacci implements Generator<Integer> {
        private int count = 0;
        public Integer next() { return fib(count++); }
        private int fib(int n) {
            if(n < 2) return 1;
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

虽然，在 Fibonacci 类使用的都是 int 类型，但是其类型参数却是 Integer 。

这个例子引出了 Java 泛型的一个局限性：基本类型无法作为类型参数。

不过，Java SE5 具备自动打包和拆包的功能，可以很方便地在基本类型和其相应的包装器类型之间进行转换。

泛型方法
--------

泛型可以应用于方法。

.. hint:: 

    如果使用泛型方法可以取代整个类泛型化，那么就应该只使用泛型方法。

定义泛型方法，只需将泛型参数列表置于返回值之前。

.. code-block:: java

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

.. note:: 

    当使用泛型类时，必须在创建对象的时候指定类型参数的值，而使用泛型方法的时候，通常不必指明参数类型，因为编译器会为我们找出具体的类型。
    这称为类型参数推断（type argument inference）。因此， **我们可以像调用普通方法一样调用 f() ，就好像 f() 被无限次地重载过。**
    甚至，它可以接受 GenericMethods 作为其参数类型。

    类型推断只对赋值操作有效，其他时候并不起作用。如果你将一个泛型方法调用的结果作为参数，传递给另一个方法，这时编译器不会执行推断。
    在这种情况下，编译器认为，调用泛型方法后，其返回值被赋给一个 Object 类型的变量。比较下面两个程序段。

程序段一：赋值，可以推断

.. code-block:: java

    //: generics/SimplerPets.java
    import typeinfo.pets.*;
    import java.util.*;
    import net.mindview.util.*;

    public class SimplerPets {
        public static void main(String[] args) {
            Map<Person, List<? extends Pet>> petPeople = New.map();
            // Rest of the code is the same...
        }
    } ///:~

程序段二：作为参数，不能推断

.. code-block:: java

    //: generics/LimitsOfInference.java
    import typeinfo.pets.*;
    import java.util.*;

    public class LimitsOfInference {
        static void f(Map<Person, List<? extends Pet>> petPeople) {}
        public static void main(String[] args) {
            // f(New.map()); // Does not compile
        }
    } ///:~

可变参数与泛型方法
~~~~~~~~~~~~~~~~~~

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

擦除的神秘之处
--------------

可以声明 ``ArrayList.class`` 但是不能声明 ``ArrayList<Integer>.class`` 就是因为擦除。

擦除会移除参数类型信息。 ``List<String>`` 与 ``List<Integer>`` 在运行时事实上是相同的类型，即 ``List`` 。

泛型类型只有在静态类型检查期间才出现，在此之后，程序中的所有泛型类型都将被擦除，替换为它们的非泛型上界。
例如， ``List<T extends HasF>`` 中的 ``T`` 擦除到了 ``HasF``
就好像在类的声明中用 ``HasF`` 替换了 ``T`` 一样，其中 ``HasF`` 就是上界。
而 ``List<T>`` 中的 ``T`` 因未指定边界，将被擦除为 ``Object`` 。

擦除的核心动机就是，它使得泛化的客户端可以用非泛化的类库来使用，反之亦然，这经常被称为“迁移兼容性”。
通过允许非泛型代码与泛型代码共存，擦除使得非泛型代码向着泛型迁移成为可能。

擦除的补偿
----------

擦除直观上的理解就是发生了向上转型，它丢失了泛型代码中执行某些操作的能力。
任何在运行时需要知道确切类型信息的操作都将无法工作。

下面的代码段无法进行编译：

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

边界
----
通配符
-------
问题
----
自限定的类型
------------
动态类型安全
------------
异常
----
混型
----
潜在类型机制
------------
对缺乏潜在类型机制的补偿
------------------------
将函数对象用作策略
------------------
