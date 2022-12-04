=======
复用类
=======

组合语法
--------

组合是指在本类中实例化其他类的对象，并保存其他类的对象的引用。

初始化引用是指对引用指向的对象进行初始化，对象的 **初始化流程** 参考 :ref:`load-class`。

下面将探讨引用的 **初始化时机**。编译器为了减少负担，并不是简单地为每一个引用都创建默认对象。
只有出现下面四种情况时，编译器会初始化引用：
1）在定义对象时；
2）在类的构造器中；
3）在使用对象前，惰性初始化；
4）在使用对象时。

为了更清晰地理解这四种情况，我们阅读一段代码，对号入座。

.. code-block:: java
    :emphasize-lines: 15, 23, 24, 28, 29, 32

    //: reusing/Bath.java
    // Constructor initialization with composition.
    import static net.mindview.util.Print.*;

    class Soap {
        private String s;
        Soap() {
            print("Soap()");
            s = "Constructed";
        }
        public String toString() { return s; }
    }

    public class Bath {
        private String                          // 情况 1：在对象定义时
            s1 = "Happy",
            s2 = "Happy",
            s3, s4;
        private Soap castille;
        private int i;
        private float toy;
        public Bath() {
            print("Inside Bath()");             // 情况 2：在构造器内
            s3 = "Joy";
            toy = 3.14f;
            castille = new Soap();
        }

        { i = 47; }                             // 情况 4：在对象使用时

        public String toString() {
            if(s4 == null)                      // 情况 3：在对象使用前，惰性初始化
                s4 = "Joy";
            return
                "s1 = " + s1 + "\n" +
                "s2 = " + s2 + "\n" +
                "s3 = " + s3 + "\n" +
                "s4 = " + s4 + "\n" +
                "i = " + i + "\n" +
                "toy = " + toy + "\n" +
                "castille = " + castille;
        }
        public static void main(String[] args) {
            Bath b = new Bath();
            print(b);
        }
    } /* Output:
    Inside Bath()
    Soap()
    s1 = Happy
    s2 = Happy
    s3 = Joy
    s4 = Joy
    i = 47
    toy = 3.14
    castille = Constructed
    *///:~

.. _inheritance-syntax:

继承语法
--------

继承是指在父类的基础上添加新的功能。

Java 中所有的类都继承自 ``Object``，我们将这种现象命名为 **单根继承结构**。

在 :ref:`load-class` 一节，我们发现在调用子类构造器时，父类构造器已经完成了初始化，那么这种现象是如何发生的呢？
众所周知，程序发生的所有行为都是因为函数调用的存在，所以，即使在子类中没有看到 ``super``
调用父类构造器，隐式地也是已经调用了的（这可能由编译器生成），对于后面理解类的初始化顺序 **很重要**。

而且，由于 ``Object`` 是所有类的共同父类，所以，每个类的调用链上都会经过很多次的 ``super``
调用，直到调用到 ``Object`` 的构造器为止。

上面两段话讲的是从子类到父类的类的 **发现过程**，而 **构建过程** 正好是一个相反的过程（从父类到子类）。
如下代码展示了一个从父类到子类的 **构建过程**：

.. code-block:: java

    //: reusing/Cartoon.java
    // Constructor calls during inheritance.
    import static net.mindview.util.Print.*;

    class Art {
        Art() { print("Art constructor"); }
    }

    class Drawing extends Art {
        Drawing() { print("Drawing constructor"); }
    }

    public class Cartoon extends Drawing {
        public Cartoon() { print("Cartoon constructor"); }
        public static void main(String[] args) {
            Cartoon x = new Cartoon();
        }
    } /* Output:
    Art constructor
    Drawing constructor
    Cartoon constructor
    *///:~

.. tip::

    为了更加方便地进行 **单元测试**，我们可以在每个类中都创建一个 ``main()`` 方法。
    要运行某个单元，只需在编译完成后直接运行 ``java 类名``\ （还有另外两种实现方式
    :ref:`供参考 <nested-class>`）。测试完成后，无需删除 ``main()`` 可以保留待下次测试。
    如下所示：

    .. code-block:: java
        :emphasize-lines: 12, 28

        //: reusing/Detergent.java
        // Inheritance syntax & properties.
        import static net.mindview.util.Print.*;

        class Cleanser {
            private String s = "Cleanser";
            public void append(String a) { s += a; }
            public void dilute() { append(" dilute()"); }
            public void apply() { append(" apply()"); }
            public void scrub() { append(" scrub()"); }
            public String toString() { return s; }
            public static void main(String[] args) {
                Cleanser x = new Cleanser();
                x.dilute(); x.apply(); x.scrub();
                print(x);
            }
        }

        public class Detergent extends Cleanser {
            // Change a method:
            public void scrub() {
                append(" Detergent.scrub()");
                super.scrub(); // Call base-class version
            }
            // Add methods to the interface:
            public void foam() { append(" foam()"); }
            // Test the new class:
            public static void main(String[] args) {
                Detergent x = new Detergent();
                x.dilute();
                x.apply();
                x.scrub();
                x.foam();
                print(x);
                print("Testing base class:");
                Cleanser.main(args);
            }
        } /* Output:
        Cleanser dilute() apply() Detergent.scrub() scrub() foam()
        Testing base class:
        Cleanser dilute() apply() scrub()
        *///:~

代理语法
--------

考虑一种场景，若我们 **不想** 把某个类的所有接口都暴露给另一个类，就不能用继承了，因为继承会得到所有接口。
那么使用代理可以在不向外界暴露接口的同时（声明为 ``private``），又能给外界提供类似的接口。
代理既不是组合，也不是继承，属于第三世界。从字面意思理解，代理就是 "倒手" 的意思，起到承上启下的作用。

.. code-block:: java

    //: reusing/SpaceShipControls.java

    public class SpaceShipControls {
        void up(int velocity) {}
        void down(int velocity) {}
        void left(int velocity) {}
        void right(int velocity) {}
        void forward(int velocity) {}
        void back(int velocity) {}
        void turboBoost() {}
    } ///:~

.. code-block:: java

    //: reusing/SpaceShipDelegation.java

    public class SpaceShipDelegation {
        private String name;
        private SpaceShipControls controls = new SpaceShipControls();   // 创建受托对象
        public SpaceShipDelegation(String name) {
            this.name = name;
        }

        // 编写代理行为
        public void forward(int velocity) {
            controls.forward(velocity);
        }
        public void left(int velocity) {
            controls.left(velocity);
        }

        public static void main(String[] args) {
            SpaceShipDelegation protector =                             // 创建代理对象
                new SpaceShipDelegation("NSEA Protector");
            protector.forward(100);                                     // 让代理对象执行方法
        }
    } ///:~
