=======
复用类
=======

组合语法
--------

组合就是在新的类中 new 出现有类的对象。由于新的类由现有的类的对象组成，所以这种方法称为组合。

使用组合时，只需要将对象引用放入新类中即可。

初始化引用
~~~~~~~~~~

编译器为了减少负担，并不是简单地为每一个引用都创建默认对象。但是，在下面四种情况下，编译器会初始化引用：

1. 在定义对象的地方。
2. 在类的构造器中。
3. 在使用这个对象之前（这种方式称为惰性初始化）
4. 使用实例初始化。

这四种情况的代码示例如下所示：

.. code-block:: java
    :emphasize-lines: 15, 23, 24, 28, 29, 31

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
        private String // Initializing at point of definition:
            s1 = "Happy",
            s2 = "Happy",
            s3, s4;
        private Soap castille;
        private int i;
        private float toy;
        public Bath() {
            print("Inside Bath()");
            s3 = "Joy";
            toy = 3.14f;
            castille = new Soap();
        }	
        // Instance initialization:
        { i = 47; }
        public String toString() {
            if(s4 == null) // Delayed initialization:
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

按照现有类的类型来创建新类，在新类中可以保持旧类的某些属性和方法，而且添加新代码，这种方式叫做继承。

.. note:: Java 中所有的类都从隐式地从标准根类 Object 继承。

.. tip:: 
    
    在每个类中都创建一个 main() 方法可以使每个类的 **单元测试** 变得简单易行，而且，测试完成后，无需删除 main() ，可以保留待下次测试。如下所示：

    在使用单元测试时，当编译完成后，直接运行 ``java 类名`` 即可运行某个类。使用 :ref:`内部类语法 <class-in-interface>` 会更加方便。
    
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

初始化基类
~~~~~~~~~~

由于在调用子类构造器时，父类构造器已经完成了初始化，所以，即使在子类中没有看到 super 调用父类构造器，隐式地也是已经调用了的（这由编译器生成）。这对于后面理解类的初始化顺序很重要。

而且，由于 Object 类时所有类的共同父类，所以，每个类的调用链上都会经过多级 super(super(...)) 调用，直到调用到 Object 的构造器为止。参考 :ref:`初始化及类的加载 <load-class>`

上面两段话讲的是类的发现过程（从子类到父类），而构建过程正好是一个相反的过程（从父类到子类）。如下代码展示了一个从父类到子类的构建过程：

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

代理
----

代理既不是组合，也不是继承。属于第三世界。

比如我们有一个飞船控制器类（类的声明如下），但是，我们又不想把所有的接口都暴露给另一个类，这时候，继承就不能用了，因为继承会得到所有的接口。

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

那么使用代理可以在不向外界暴露飞船控制器的接口的同时（声明为 private），又能给外界提供类似的接口。如下所示：

.. code-block:: java
    :emphasize-lines: 5, 11, 14, 17, 20, 23, 26, 29

    //: reusing/SpaceShipDelegation.java

    public class SpaceShipDelegation {
        private String name;
        private SpaceShipControls controls = new SpaceShipControls();
        public SpaceShipDelegation(String name) {
            this.name = name;
        }
        // Delegated methods:
        public void back(int velocity) {
            controls.back(velocity);
        }
        public void down(int velocity) {
            controls.down(velocity);
        }
        public void forward(int velocity) {
            controls.forward(velocity);
        }
        public void left(int velocity) {
            controls.left(velocity);
        }
        public void right(int velocity) {
            controls.right(velocity);
        }
        public void turboBoost() {
            controls.turboBoost();
        }
        public void up(int velocity) {
            controls.up(velocity);
        }
        public static void main(String[] args) {
            SpaceShipDelegation protector =
                new SpaceShipDelegation("NSEA Protector");
            protector.forward(100);
        }
    } ///:~

结合使用组合和继承
------------------

确保正确清理
~~~~~~~~~~~~

Java 中没有 C++ 中析构函数的概念。

如果你想清理某些东西，需要显式地编写 finally 子句，将清理动作放在 finally 子句中，以防止异常的出现。格式为：

.. code-block:: java

    try {
        // 保护区代码
    } finally {
        // 不管保护区发生什么，这段代码一定会执行
    }

向上转型
--------

由导出类转型为基类，在继承图上是向上移动的，因此称为向上转型。

向上转型是安全的，因为调用父类方法时，不会超出子类方法集的边界，但是会丢失方法。

向下转型是不安全的，因为有可能调用子类对象的方法时，已经超出了父类方法集的边界。（泛型解决了这个问题）
