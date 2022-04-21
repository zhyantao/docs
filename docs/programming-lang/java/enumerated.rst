====
枚举
====

基本使用
---------

.. code-block:: java

    //: initialization/Spiciness.java

    public enum Spiciness {
        NOT, MILD, MEDIUM, HOT, FLAMING
    } ///:~

按照惯例，枚举类型的成员通常用大写字母，多个单词之间用下划线隔开。

.. code-block:: java
    :emphasize-lines: 4,9,21
    :linenos:

    //: initialization/Burrito.java

    public class Burrito {
        Spiciness degree;
        public Burrito(Spiciness degree) { this.degree = degree;}
        public void describe() {
            System.out.print("This burrito is ");
            switch(degree) {
                case NOT:    System.out.println("not spicy at all.");
                            break;
                case MILD:
                case MEDIUM: System.out.println("a little hot.");
                            break;
                case HOT:
                case FLAMING:
                default:     System.out.println("maybe too hot.");
            }
        }
        public static void main(String[] args) {
            Burrito
                plain = new Burrito(Spiciness.NOT),
                greenChile = new Burrito(Spiciness.MEDIUM),
                jalapeno = new Burrito(Spiciness.HOT);
            plain.describe();
            greenChile.describe();
            jalapeno.describe();
        }
    } /* Output:
    This burrito is not spicy at all.
    This burrito is a little hot.
    This burrito is maybe too hot.
    *///:~

``enum`` 和 ``class`` 一样，只是一个关键字。
像 ``class`` 被 ``Class`` 类维护一样， ``enum`` 被 ``Enum`` 类维护。

枚举类除了不能继承之外，和普通类的使用方式是一致的，它也可在类里面定义自己的方法，也可以实现接口。

不能继承是因为 ``Enum`` 这个类是 ``final`` 的。

背景知识
--------

在 Java 语言中还没有引入枚举类型之前，表示枚举类型的常用模式是声明一组具 ``int`` 常量。
之前我们通常利用 ``public final static`` 方法定义的代码如下，分别用 1 表示春天，2 表示夏天，3
表示秋天，4 表示冬天。

.. code-block:: java

    public class Season {
        public static final int SPRING = 1;
        public static final int SUMMER = 2;
        public static final int AUTUMN = 3;
        public static final int WINTER = 4;
    }

这种方法称作 ``int`` 枚举模式。可这种模式有什么问题呢，通常我们写出来的代码都会考虑它的安全性、易用性和可读性。

**首先我们来考虑一下它的类型安全性**，当然这种模式不是类型安全的。

比如说，我们设计一个函数，要求传入春夏秋冬的某个值。但是使用 ``int`` 类型，我们无法保证传入的值为合法。

代码如下所示：

程序 ``getChineseSeason(Season.SPRING)`` 是我们预期的使用方法。
可 ``getChineseSeason(5)`` 显然就不是了，而且编译很通过，在运行时会出现什么情况，我们就不得而知了。
这显然就不符合 Java 程序的类型安全。

**接下来我们来考虑一下这种模式的可读性**。使用枚举的大多数场合，我都需要方便得到枚举类型的字符串表达式。
如果将 ``int`` 枚举常量打印出来，我们所见到的就是一组数字，这是没什么太大的用处。

我们可能会想到使用 ``String`` 常量代替 ``int`` 常量。
虽然它为这些常量提供了可打印的字符串，但是它会导致性能问题，因为它依赖于字符串的比较操作，所以这种模式也是我们不期望的。

从类型安全性和程序可读性两方面考虑， ``int`` 和 ``String`` 枚举模式的缺点就显露出来了。

幸运的是，从 Java 1.5 发行版本开始，就提出了另一种可以替代的解决方案，可以避免 ``int`` 和
``String`` 枚举模式的缺点，并提供了许多额外的好处。
那就是枚举类型。接下来的章节将介绍枚举类型的定义、特征、应用场景和优缺点。

枚举类的常用方法
----------------

``Enum`` 类提供了一些有用的函数，我们可以加以利用，在 ``enum`` 实例上调用以下方法：

- ``values()`` 返回 ``enum`` 实例对应的数组。实际上 ``Enum`` 类并没有这个函数，是编译器为我们添加的。
- ``ordinal()`` 返回元素的下标；
- ``equals()`` 、  ``==`` 他们作用完全相同， ``equals`` 方法默认实现就是通过 ``==`` 来比较的；
- ``compareTo()`` 方法比较的是 ``Enum`` 的 ``ordinal`` 顺序大小；
- ``name()`` 返回 ``enum`` 实例声明时的名字，效果与 ``toString()`` 方法相同；
- ``getDeclaringClass()`` 返回 ``enum`` 实例所属的 ``enum`` 类。

.. code-block:: java

    //: enumerated/EnumClass.java
    // Capabilities of the Enum class
    import static net.mindview.util.Print.*;

    enum Shrubbery { GROUND, CRAWLING, HANGING }

    public class EnumClass {
        public static void main(String[] args) {
            for(Shrubbery s : Shrubbery.values()) {
                print(s + " ordinal: " + s.ordinal());
                printnb(s.compareTo(Shrubbery.CRAWLING) + " ");
                printnb(s.equals(Shrubbery.CRAWLING) + " ");
                print(s == Shrubbery.CRAWLING);
                print(s.getDeclaringClass());
                print(s.name());
                print("----------------------");
            }
            // Produce an enum value from a string name:
            for(String s : "HANGING CRAWLING GROUND".split(" ")) {
                Shrubbery shrub = Enum.valueOf(Shrubbery.class, s);
                print(shrub);
            }
        }
    } /* Output:
    GROUND ordinal: 0
    -1 false false
    class Shrubbery
    GROUND
    ----------------------
    CRAWLING ordinal: 1
    0 true true
    class Shrubbery
    CRAWLING
    ----------------------
    HANGING ordinal: 2
    1 false false
    class Shrubbery
    HANGING
    ----------------------
    HANGING
    CRAWLING
    GROUND
    *///:~

枚举和单例
----------

单例模式是 23 种设计模式中最为常用的设计模式，但是它并没有想象的那么简单。

因为单例模式要考虑很多问题，比如线程安全问题、序列化对单例的破坏等。

单例模式一般有七种写法，最好的是哪一种呢？在 StackOverflow 的回答中，最高赞的是用枚举实现的。

这七种实现方案中，各种方式都比较复杂，是因为要考虑线程安全问题。

举例来说，使用 "双重校验锁" 实现单例：

.. code-block:: java

    public class Singleton {
        private volatile static Singleton singleton;
        private Singleton () {}
        public static Singleton getSingleton() {
            if (singleton == null) {
                synchronized (Singleton.class) {
                    singleton = new Singleton();
                }
            }
        }
        return singleton;
    }

然后，对比一下枚举实现，就会发现简单很多：

.. code-block:: java

    public enum Singleton {
        INSTANCE;
        public void whateverMethod() {}
    }

上面的双重锁校验的代码之所以很臃肿，是因为大部分代码都是在保证线程安全。

为了在保证线程安全和锁粒度之间做权衡，代码难免会写的复杂些。
但是，这段代码还是有问题的，因为他无法解决反序列化会破坏单例的问题。

枚举可解决线程安全问题。枚举其实在 "底层" 做了线程安全方面的保证的，只不过不用我们自己手写罢了。

枚举对我们定义的那些枚举值都用了 ``static`` 来修饰。如下：

.. code-block:: java

    public final class T extends Enum {
        // 省略部分内容
        public static final T SPRING;
        public static final T SUMMER;
        public static final T AUTUMN;
        public static final T WINTER;
        private static final T ENUM$VALUES[];

        static {
            SPRING = new T("SPRING", 0);
            SUMMER = new T("SUMMER", 1);
            AUTUMN = new T("AUTUMN", 2);
            WINTER = new T("WINTER", 3);
            ENUM$VALUES = new T([] {
                SPRING, SUMMER, AUTUMN, WINTER;
            });
        }

**首先考虑一下枚举实现的类型安全问题，**
了解 JVM 的类加载机制的朋友应该对这部分比较清楚。 ``static`` 类型的属性会在类被加载之后被初始化。
当一个 Java 类第一次被真正使用到的时候静态资源被初始化、Java 类的加载和初始化过程都是线程安全的。

因为虚拟机在加载枚举的类的时候，会使用 ``ClassLoader`` 的 ``loadClass`` 方法，而这个方法使用同步代码块保证了线程安全。

所以，创建一个 ``enum`` 类型是线程安全的。

也就是说，我们定义的一个枚举，在第一次被真正用到的时候，会被虚拟机加载并初始化，而这个初始化过程是线程安全的。

而我们知道，解决单例的并发问题，主要解决的就是初始化过程中的线程安全问题。

所以，由于枚举的以上特性，枚举实现的单例是天生线程安全的。

**然后再考虑一下序列化和反序列化是否会破坏单例。**

在序列化的时候 Java 仅仅是将枚举对象的 ``name`` 属性输出到结果中，反序列化的时候则是通过 ``java.lang.Enum`` 的
``valueOf`` 方法来根据名字查找枚举对象。同时，编译器是不允许任何对这种序列化机制的定制的，因此禁用了
``writeObject`` 、 ``readObject`` 、 ``readObjectNoData`` 、 ``writeReplace`` 和 ``readResolve`` 等方法。

普通的 Java 类的反序列化过程中，会通过反射调用类的默认构造函数来初始化对象。
所以，即使单例中构造函数是私有的，也会被反射给破坏掉。由于反序列化后的对象是重新 ``new`` 出来的，所以这就破坏了单例。

但是，枚举的反序列化并不是通过反射实现的。所以，就不会发生由于反序列化导致的单例破坏问题。
