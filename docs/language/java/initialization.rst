==========
初始化对象
==========

.. _load-class:

初始化及类的加载
-----------------

每个类的编译代码都存在于它自己的独立的 ``.class`` 文件中，该文件只有在需要使用程序代码时才会被加载。

一般来说，"类的代码在初次使用时才加载"。这通常发生于创建类的第一个对象时，但是当访问 ``static`` 域
**或** ``static`` 方法时，也会发生加载。

先阅读一下代码，有一个直观的感受：

.. code-block:: java

    //: reusing/Beetle.java
    // The full process of initialization.
    import static net.mindview.util.Print.*;

    class Insect {
        private int i = 9;
        protected int j;
        Insect() {
            print("i = " + i + ", j = " + j);                                   // 4
            j = 39;
        }
        private static int x1 = printInit("static Insect.x1 initialized");      // 1
        static int printInit(String s) {
            print(s);                                                           // 1, 2, 5
            return 47;
        }
    }

    public class Beetle extends Insect {
        private int k = printInit("Beetle.k initialized");                      // 5
        public Beetle() {
            print("k = " + k);                                                  // 6
            print("j = " + j);                                                  // 7
        }
        private static int x2 = printInit("static Beetle.x2 initialized");      // 2
        public static void main(String[] args) {
            print("Beetle constructor");                                        // 3
            Beetle b = new Beetle();
        }
    } /* Output:
    static Insect.x1 initialized
    static Beetle.x2 initialized
    Beetle constructor
    i = 9, j = 0
    Beetle.k initialized
    k = 47
    j = 39
    *///:~

下面介绍一下一般的类的实例化流程：

1. 基类构造总是先于导出类。按照继承关系，首先对基类进行加载，向上回溯，直到触及 ``Object``。
2. 按照从基类到导出类的顺序，对所有的 ``static`` 属性赋予人为设定的值（初始化顺序很重要，因为导出类
   ``static`` 可能依赖于基类的 ``static``，注意，\ ``main`` 方法也是 ``static`` 的，因此 ``main``
   也会在这一步执行）。
3. 通过将内存设为二进制 0，一举完成对代码中出现的所有非 ``static`` 数据 :ref:`设置默认值 <java-datatpyes>`。
4. 按照从基类到导出类的顺序，首先对所有的\ **非** ``static`` 属性赋予人为设定的值，然后执行构造器函数。
5. 执行完构造器，对象的初始化就算完成了。

.. note::

    注意，不管是 ``static`` 函数还是普通函数，都不会包含在实例化过程中，只有调用的时候才会执行。


this 关键字
------------

``this`` 关键字指代当前对象的引用，因此，我们经常使用 ``this`` 关键字传递自身引用。
使用 ``this`` 调用方法，表示调用当前对象的方法或属性\
（因为可能类的属性和方法内部的属性可能同名，这时候可以用 ``this`` 关键字来区分）。\
``return this`` 表示返回当前对象的引用。

.. code-block:: java
    :emphasize-lines: 18
    :linenos:

    //: initialization/PassingThis.java

    class Person {
        public void eat(Apple apple) {
            Apple peeled = apple.getPeeled(); // 给苹果削皮
            System.out.println("Yummy");
        }
    }

    class Peeler {  // 削皮刀
        static Apple peel(Apple apple) {
            // ... remove peel
            return apple; // Peeled
        }
    }

    class Apple {   // 苹果
        Apple getPeeled() { return Peeler.peel(this); }
    }

    public class PassingThis {
        public static void main(String[] args) {
            new Person().eat(new Apple());
        }
    } /* Output:
    Yummy
    *///:~

上面代码高亮处表示 ``Apple`` 类用于生成剥皮后的苹果。

使用 ``this`` 关键字，可以在构造器中调用构造器，因为生命周期，不能在非构造器函数中调用构造器。

.. code-block:: java
    :emphasize-lines: 17,19,23
    :linenos:

    //: initialization/Flower.java
    // Calling constructors with "this"
    import static net.mindview.util.Print.*;

    public class Flower {
        int petalCount = 0;
        String s = "initial value";
        Flower(int petals) {
            petalCount = petals;
            print("Constructor w/ int arg only, petalCount= " + petalCount);
        }
        Flower(String ss) {
            print("Constructor w/ String arg only, s = " + ss);
            s = ss;
        }
        Flower(String s, int petals) {
            this(petals);
    //!     this(s); // Can't call two!
            this.s = s; // Another use of "this"
            print("String & int args");
        }
        Flower() {
            this("hi", 47);
            print("default constructor (no args)");
        }
        void printPetalCount() {
    //!     this(11); // Not inside non-constructor!
            print("petalCount = " + petalCount + " s = "+ s);
        }
        public static void main(String[] args) {
            Flower x = new Flower();
            x.printPetalCount();
        }
    } /* Output:
    Constructor w/ int arg only, petalCount= 47
    String & int args
    default constructor (no args)
    petalCount = 47 s = hi
    *///:~

.. note::

    1. 使用 ``this(String[] args)`` 调用构造器时，只能调用一个。
    2. 构造器调用必须位于方法的最开始。

与 ``this(String[] args)`` 类似，使用 ``super(String[] args)`` 调用父类对象的某个构造器。

static 关键字
--------------

``static`` 关键字的适用场景：

1. 想为某特定域只分配一份存储空间，而不去考虑究竟要创建多少对象，甚至根本就不创建对象。
2. 希望某个方法不与包含它的类的任何对象关联在一起，即通过类名调用方法。

.. note::

    1. ``static`` 方法内部不能调用非静态方法，是因为生命周期。
    2. ``static`` 方法没有 ``this`` 方法，也是因为生命周期，\ ``static`` 方法先于对象创建。
    3. ``static`` 方法其实是 Java 中的全局方法。


final 关键字
------------

``final`` 可以用于修饰属性、方法和类，发生的效果是一致的，表示 "这是无法改变的"，细微之处略有差别。

被 ``final`` 声明的属性无法被修改。因此常用 ``final`` 用来修饰编译时常量。
编译时常量可以在编译期直接带入计算式参与计算，减轻了运行时的负担。
对于基本数据类型，\ ``final`` 使数值恒定不变。
对于引用类型，\ ``final`` 使引用恒定不变，即一旦引用被初始化，无法再指向其他对象。
参数列表中使用 ``final`` 时，表示无法更改参数引用的指向。
按照惯例，既是 ``static`` 又是 ``final`` 的域（即编译器常量）用 **大写字母**
表示，使用下划线分隔各个单词。

.. note::

    - 一个既是 ``static`` 又是 ``final`` 的域只占据一段不能改变的存储空间。
    - 定义为 ``public`` 强调可以用于包之外。
    - 定义为 ``static`` 强调只有一份。
    - 定义为 ``final`` 强调是一个常量。

被 ``final`` 声明的方法无法重写。
所有的 ``private`` 方法都 **隐式地** 指定为 ``final``\，因为无法改变。
一个方法一旦被 ``final`` 声明，将不会发生动态绑定行为。

被 ``final`` 声明的类无法被继承。


finalize() 方法
----------------

不是 ``new`` 出来的对象，会获得一块特殊的内存，垃圾回收器不会回收，需要使用 ``finalize()`` 方法来释放。

当某个对象处于某种状态时（例如文件处于打开状态），如果直接使用 ``finalize()``
清理该对象占用的内存空间，可能会发生异常。因此 ``finalize()`` 可以用来发现异常。
如下代码所示：

.. code-block:: java
    :emphasize-lines: 13,29
    :linenos:

    //: initialization/TerminationCondition.java
    // Using finalize() to detect an object that
    // hasn't been properly cleaned up.

    class Book {
        boolean checkedOut = false;
        Book(boolean checkOut) {            // 设置 "图书已出库" 标志位
            checkedOut = checkOut;
        }
        void checkIn() {                    // 将 "图书入库"
            checkedOut = false;
        }
        protected void finalize() {
            if(checkedOut)                  // 检查 "图书是否已出库"
                System.out.println("Error: checked out");
            // 正常情况下，清理完导出类后，也应该对基类进行清理：
            // super.finalize(); // Call the base-class version
        }
    }

    public class TerminationCondition {
        public static void main(String[] args) {
            Book novel = new Book(true);    // 设置 "图书已出库"，清理库存
            // Proper cleanup:
            novel.checkIn();                // 设置 "图书入库"
            // Drop the reference, forget to clean up:
            new Book(true);                 // 设置 "图书出库"
            // Force garbage collection & finalization:
            System.gc();                    // 调用 finalize() 后发现没有库存，报错
        }
    } /* Output:
    Error: checked out
    *///:~

那么如何保证 ``finalize()`` 代码一定会被执行呢？Java 中没有 C++ 中析构函数的概念。
如果你想清理某些东西，需要显式地编写 ``finally`` 子句，将清理动作放在 ``finally``
子句中，以防止异常的出现。

.. code-block:: java

    try {
        // 保护区代码
    } finally {
        // 不管保护区发生什么，这段代码一定会执行
    }
