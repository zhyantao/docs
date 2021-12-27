=====
多态
=====

多态的作用是消除类型之间的耦合关系。

多态方法调用允许一种类型表现出与其他相似类型之间的区别，只要它们都是从同一个基类导出而来的。

多态 = 动态绑定 = 后期绑定 = 运行时绑定。

忘记对象类型
------------

不管导出类的存在，编写的代码只是与基类打交道（因为有向上转型，所以这个想法是可行的），这是多态允许的。

.. _dynamic-binding:

动态绑定
--------

当我们用多态来编写代码时，编译器实际上无法知道当前对象正在调用的是基类的哪个导出类的对象的方法。但是，这个问题可以使用绑定来解决。

方法调用绑定
~~~~~~~~~~~~~

将一个方法调用同一个方法主体关联起来称为绑定。

- 若在程序执行前进行绑定（如果有的话，由编译器和连接程序实现），叫做前期绑定。（这是面向过程语言的绑定方式）
- 若在程序运行时根据对象的类型进行绑定，叫做后期绑定。（这是面向对象语言的绑定方式）

Java 中除了 static 方法和 final 方法（private 方法属于 final 方法）之外，其他所有方法都是后期绑定。

后期绑定实际上是在对象中安置某种“类型信息”来实现的。

产生正确的行为
~~~~~~~~~~~~~~

编写只与基类打交道的代码，并且这些代码对所有的导出类都可以正确运行。

下面例子中，RandomShapeGenerator 是一种“工厂”（factory），在我们每次调用 next() 方法时，它可以为随机选择的 Shape 对象产生一个引用。

公共接口
^^^^^^^^

.. code-block:: java

    //: polymorphism/shape/Shape.java
    package polymorphism.shape;

    public class Shape {
        public void draw() {}
        public void erase() {}
    } ///:~

各种形状
^^^^^^^^

.. code-block:: java

    //: polymorphism/shape/Circle.java
    package polymorphism.shape;
    import static net.mindview.util.Print.*;

    public class Circle extends Shape {
        public void draw() { print("Circle.draw()"); }
        public void erase() { print("Circle.erase()"); }
    } ///:~

    //: polymorphism/shape/Square.java
    package polymorphism.shape;
    import static net.mindview.util.Print.*;

    public class Square extends Shape {
        public void draw() { print("Square.draw()"); }
        public void erase() { print("Square.erase()"); }
    } ///:~

    //: polymorphism/shape/Triangle.java
    package polymorphism.shape;
    import static net.mindview.util.Print.*;

    public class Triangle extends Shape {
        public void draw() { print("Triangle.draw()"); }
        public void erase() { print("Triangle.erase()"); }
    } ///:~

随机形状生成器
^^^^^^^^^^^^^^

.. code-block:: java

    //: polymorphism/shape/RandomShapeGenerator.java
    // A "factory" that randomly creates shapes.
    package polymorphism.shape;
    import java.util.*;

    public class RandomShapeGenerator {
        private Random rand = new Random(47);
        public Shape next() {
            switch(rand.nextInt(3)) {
                default:
                case 0: return new Circle();
                case 1: return new Square();
                case 2: return new Triangle();
            }
        }
    } ///:~

主函数
^^^^^^

.. code-block:: java
    :emphasize-lines: 6

    //: polymorphism/Shapes.java
    // Polymorphism in Java.
    import polymorphism.shape.*;

    public class Shapes {
        private static RandomShapeGenerator gen = new RandomShapeGenerator();
        public static void main(String[] args) {
            Shape[] s = new Shape[9];
            // Fill up the array with shapes:
            for(int i = 0; i < s.length; i++)
                s[i] = gen.next();
            // Make polymorphic method calls:
            for(Shape shp : s)
                shp.draw();
        }
    } /* Output:
    Triangle.draw()
    Triangle.draw()
    Square.draw()
    Triangle.draw()
    Square.draw()
    Triangle.draw()
    Square.draw()
    Triangle.draw()
    Circle.draw()
    *///:~

.. note:: 
    
    Shape 基类给其所有的导出类建立了一个公共接口。

    向上转型是在 return 语句里发生的。
    
    每个 return 语句取得一个指向某个 Circle、Square 或 Triangle 的引用，并将其以 Shape 类型从 next() 方法中发送出去。


可扩展性
~~~~~~~~

.. mermaid::

    classDiagram
        Instrument <|-- Wind : extends
        Instrument <|-- Percussion : extends
        Instrument <|-- Stringed : extends
        Wind <|-- Woodwind : extends
        Wind <|-- Brass : extends
        Instrument : void play()
        Instrument : String what()
        Instrument : void adjust()
        Wind : void play()
        Wind : String what()
        Wind : void adjust()
        Percussion : void play()
        Percussion : String what()
        Percussion : void adjust()
        Stringed : void play()
        Stringed : String what()
        Stringed : void adjust()
        Woodwind : void play()
        Woodwind : String what()
        Brass : void play()
        Brass : void adjust()


由于有多态机制，我们可以 **根据自己的需求对系统添加任意多的新类型** ，而不需要更改 ``tune()`` 方法。在一个设计良好的 OOP 程序中，大多数或者所有方法 **都会遵循** ``tune()`` 的模型，而且 **只与基类接口通信** 。这样的程序是 **可扩展** 的，因为可以从通用的基类继承出新的数据类型，从而新添一些功能。那些操纵基类接口的方法 **不需要任何改动就可以应用于新类** 。

事实上，不需要改动 ``tune()`` 方法，所有的新类都能与原有类一起正确运行。即使 ``tune()`` 方法是单独存放在某个文件中，并且在 Instrument 接口中添加了其他的新方法， ``tune()`` 也 **不需要再编译就能正确运行** 。

.. code-block:: java
    :emphasize-lines: 44, 50

    //: polymorphism/music3/Music3.java
    // An extensible program.
    package polymorphism.music3;
    import polymorphism.music.Note;
    import static net.mindview.util.Print.*;

    class Instrument {
        void play(Note n) { print("Instrument.play() " + n); }
        String what() { return "Instrument"; }
        void adjust() { print("Adjusting Instrument"); }
    }

    class Wind extends Instrument {
        void play(Note n) { print("Wind.play() " + n); }
        String what() { return "Wind"; }
        void adjust() { print("Adjusting Wind"); }
    }	

    class Percussion extends Instrument {
        void play(Note n) { print("Percussion.play() " + n); }
        String what() { return "Percussion"; }
        void adjust() { print("Adjusting Percussion"); }
    }

    class Stringed extends Instrument {
        void play(Note n) { print("Stringed.play() " + n); }
        String what() { return "Stringed"; }
        void adjust() { print("Adjusting Stringed"); }
    }

    class Brass extends Wind {
        void play(Note n) { print("Brass.play() " + n); }
        void adjust() { print("Adjusting Brass"); }
    }

    class Woodwind extends Wind {
        void play(Note n) { print("Woodwind.play() " + n); }
        String what() { return "Woodwind"; }
    }	

    public class Music3 {
        // Doesn't care about type, so new types
        // added to the system still work right:
        public static void tune(Instrument i) {
            // ...
            i.play(Note.MIDDLE_C);
        }
        public static void tuneAll(Instrument[] e) {
            for(Instrument i : e)
                tune(i);
        }	
        public static void main(String[] args) {
            // Upcasting during addition to the array:
            Instrument[] orchestra = {
                new Wind(),
                new Percussion(),
                new Stringed(),
                new Brass(),
                new Woodwind()
            };
            tuneAll(orchestra);
        }
    } /* Output:
    Wind.play() MIDDLE_C
    Percussion.play() MIDDLE_C
    Stringed.play() MIDDLE_C
    Brass.play() MIDDLE_C
    Woodwind.play() MIDDLE_C
    *///:~

构造器和多态
------------

构造器不具有多态性（实际上它们是 static 方法，只不过该 static 声明是隐式的）

构造器的调用顺序
~~~~~~~~~~~~~~~~

基类的构造器总是在导出类的构造过程中被调用，而且按照继承层次逐渐向上链接，以使每个基类的构造器都能得到调用。

继承与清理
~~~~~~~~~~

通过组合和继承方法来创建新类时，永远不必担心对象的清理问题，子对象通常都会留给垃圾回收器进行处理。

如果确实遇到清理的问题，那么必须为新类创建 ``dispose()`` 方法（这个方法名可以自定义）。如果需要进行一些特殊的清理动作，就必须在导出类中覆盖 ``dispose()`` 方法。

.. code-block:: java
    :emphasize-lines: 36-37, 47-49, 61-63, 73-75, 80

    //: polymorphism/Frog.java
    // Cleanup and inheritance.
    package polymorphism;
    import static net.mindview.util.Print.*;

    class Characteristic {
        private String s;
        Characteristic(String s) {
            this.s = s;
            print("Creating Characteristic " + s);
        }
        protected void dispose() {
            print("disposing Characteristic " + s);
        }
    }

    class Description {
        private String s;
        Description(String s) {
            this.s = s;
            print("Creating Description " + s);
        }
        protected void dispose() {
            print("disposing Description " + s);
        }
    }

    class LivingCreature {
        private Characteristic p = new Characteristic("is alive");
        private Description t = new Description("Basic Living Creature");
        LivingCreature() {
            print("LivingCreature()");
        }
        protected void dispose() {
            print("LivingCreature dispose");
            t.dispose();
            p.dispose();
        }
    }

    class Animal extends LivingCreature {
        private Characteristic p = new Characteristic("has heart");
        private Description t = new Description("Animal not Vegetable");
        Animal() { print("Animal()"); }
        protected void dispose() {
            print("Animal dispose");
            t.dispose();
            p.dispose();
            super.dispose();
        }
    }

    class Amphibian extends Animal {
        private Characteristic p = new Characteristic("can live in water");
        private Description t = new Description("Both water and land");
        Amphibian() {
            print("Amphibian()");
        }
        protected void dispose() {
            print("Amphibian dispose");
            t.dispose();
            p.dispose();
            super.dispose();
        }
    }

    public class Frog extends Amphibian {
        private Characteristic p = new Characteristic("Croaks");
        private Description t = new Description("Eats Bugs");
        public Frog() { print("Frog()"); }
        protected void dispose() {
            print("Frog dispose");
            t.dispose();
            p.dispose();
            super.dispose();
        }
        public static void main(String[] args) {
            Frog frog = new Frog();
            print("Bye!");
            frog.dispose();
        }
    } /* Output:
    Creating Characteristic is alive
    Creating Description Basic Living Creature
    LivingCreature()
    Creating Characteristic has heart
    Creating Description Animal not Vegetable
    Animal()
    Creating Characteristic can live in water
    Creating Description Both water and land
    Amphibian()
    Creating Characteristic Croaks
    Creating Description Eats Bugs
    Frog()
    Bye!
    Frog dispose
    disposing Description Eats Bugs
    disposing Characteristic Croaks
    Amphibian dispose
    disposing Description Both water and land
    disposing Characteristic can live in water
    Animal dispose
    disposing Description Animal not Vegetable
    disposing Characteristic has heart
    LivingCreature dispose
    disposing Description Basic Living Creature
    disposing Characteristic is alive
    *///:~

.. note:: 

    当覆盖被继承类的 ``dispose()`` 方法时，务必记住调用基类的 ``dispose()`` 方法，否则，基类的清理动作就不会发生。应该首先对导出类进行清理，然后才是基类。

    如果这些成员对象存在于其他一个或多个对象时，不能直接简单使用 ``dispose()`` 方法，需要使用 **引用计数(** ``static int counter`` **)** 来跟踪仍旧访问着共享对象的数量。

构造器内部的多态方法的行为
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip:: 从概念上讲，构造器的工作实际上是创建对象。

因为构造器调用的层次结构的存在（子类构造器调用父类构造器），会出现一个两难的问题。

如果在构造器的内部 **调用** *正在构造的对象* 的某个动态绑定方法，会发生什么呢？

.. note:: 

    在一般的方法内部，动态绑定的调用是在运行时才决定的，因为对象无法知道它是属于 **方法所在的那个类** 还是 **那个类的导出类** 。

如果要调用构造器内部的一个动态绑定方法，就要用到那个方法的被覆盖后的定义。然而，这个调用的效果可能相当难以预料，因为被覆盖的方法在对象被完全构造之前就会被调用。这里讲的原理有些抽象，看一下下面的代码：

.. code-block:: java
    :emphasize-lines: 10, 32
    :linenos:

    //: polymorphism/PolyConstructors.java
    // Constructors and polymorphism
    // don't produce what you might expect.
    import static net.mindview.util.Print.*;

    class Glyph {
        void draw() { print("Glyph.draw()"); }
        Glyph() {
            print("Glyph() before draw()");
            draw();
            print("Glyph() after draw()");
        }
    }	

    class RoundGlyph extends Glyph {
        private int radius = 1;
        RoundGlyph(int r) {
            radius = r;
            print("RoundGlyph.RoundGlyph(), radius = " + radius);
        }
        void draw() {
            print("RoundGlyph.draw(), radius = " + radius);
        }
    }	

    public class PolyConstructors {
        public static void main(String[] args) {
            new RoundGlyph(5);
        }
    } /* Output:
    Glyph() before draw()
    RoundGlyph.draw(), radius = 0
    Glyph() after draw()
    RoundGlyph.RoundGlyph(), radius = 5
    *///:~

注意到，第 32 行的输出，有两个让我们感到意外的地方：

- ``Glyph.draw()`` 并没有在 Glyph 类中得到调用，而是调用的其导出类的 ``draw()`` 方法。
- ``radius`` 并不是初始值 1，而是 0。

这是因为 :ref:`上一节 <load-class>` 讲的初始化顺序并不十分完整，下面做完整叙述：

1. 在其他任何事物发生之前，将分配给对象的存储空间初始化为二进制的 0。
2. :ref:`如前所述 <load-class>` 那样调用基类构造器。此时，调用被覆盖后的 ``draw()`` 方法（要在调用 RoundGlyph 构造器之前调用），由于步骤 1 的缘故，我们此时会发现 ``radius`` 的值为 0。
3. 按照声明的顺序调用成员的初始化方法。
4. 调用导出类的构造器主体。

协变返回类型
------------

协变返回类型表示在导出类中被覆盖的方法可以返回基类方法的返回类型的某种导出类型。

.. mermaid::

    classDiagram
        Grain <|-- Wheat : extends
        Mill <|-- WheatMill : extends
        Grain : String toString()
        Wheat : String toString()
        Mill : Grain process()
        WheatMill : Wheat process()

.. code-block:: java
    :emphasize-lines: 22, 25

    //: polymorphism/CovariantReturn.java

    class Grain {
        public String toString() { return "Grain"; }
    }

    class Wheat extends Grain {
        public String toString() { return "Wheat"; }
    }

    class Mill {
        Grain process() { return new Grain(); }
    }

    class WheatMill extends Mill {
        Wheat process() { return new Wheat(); }
    }

    public class CovariantReturn {
        public static void main(String[] args) {
            Mill m = new Mill();
            Grain g = m.process();
            System.out.println(g);
            m = new WheatMill();
            g = m.process();
            System.out.println(g);
        }
    } /* Output:
    Grain
    Wheat
    *///:~


用继承进行设计
--------------

向下转型与运行时类型识别
~~~~~~~~~~~~~~~~~~~~~~~~

在使用多态的过程中，会发生向上转型。但是向上转型会丢掉一些方法，想要重新获得这些丢掉的方法，需要显式地指明导出类的类型，这称为向下转型。
