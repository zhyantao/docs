=====
多态
=====

多态 = 动态绑定 = 后期绑定 = 运行时绑定。

利用多态机制，我们可以将 **相似类型之间的区别** 表现出来，只要它们都是从同一个基类导出而来的。
使用多态的目的是消除类型之间的耦合关系。


.. _dynamic-binding:

动态绑定
--------

当我们用多态来编写代码时，在编译期，编译器无法知道当前对象正在调用基类的哪个导出类的对象的方法。
只有到了运行期，通过动态绑定，该问题得以解决，具体的运行细节，在 :ref:`第一章 <ploy-dyna-bind>` 
做了比较多的相关描述。

Java 中除了 ``static`` 方法和 ``final`` 方法（\ ``private`` 方法属于 ``final`` 方法）之外，其他所有方法都是后期绑定。

后期绑定实际上是在对象中安置某种 "类型信息" 来实现的。

利用多态的特性，我们可以编写只与基类打交道的代码，并且这些代码对所有的导出类都可以正确运行。

阅读几段代码，体会一下动态绑定的效果。

.. code-block:: java

    //: polymorphism/shape/Shape.java
    package polymorphism.shape;

    public class Shape {
        public void draw() {}
        public void erase() {}
    } ///:~

.. code-block:: java

    //: polymorphism/shape/Circle.java
    package polymorphism.shape;
    import static net.mindview.util.Print.*;

    public class Circle extends Shape {
        public void draw() { print("Circle.draw()"); }
        public void erase() { print("Circle.erase()"); }
    } ///:~

.. code-block:: java

    //: polymorphism/shape/Square.java
    package polymorphism.shape;
    import static net.mindview.util.Print.*;

    public class Square extends Shape {
        public void draw() { print("Square.draw()"); }
        public void erase() { print("Square.erase()"); }
    } ///:~

.. code-block:: java

    //: polymorphism/shape/Triangle.java
    package polymorphism.shape;
    import static net.mindview.util.Print.*;

    public class Triangle extends Shape {
        public void draw() { print("Triangle.draw()"); }
        public void erase() { print("Triangle.erase()"); }
    } ///:~

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

.. code-block:: java
    :emphasize-lines: 11

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

上面的例子中，\ ``RandomShapeGenerator`` 是一个 "工厂"，用于生产 ``Shape`` 对象。

由于代码过于简单，也许你会忽略多态现象的发生，因此，我将发生多态的代码所在的行高亮了。

由于有多态机制，我们可以 **根据自己的需求对系统添加任意多的新类型**\ ，而不需要更改 ``next()`` 
方法。在一个设计良好的 OOP 程序中，大多数或者所有方法 **都会遵循** ``next()`` 的模型，而且 
**只与基类接口通信**\ 。这样的程序是 **可扩展** 
的，因为可以从通用的基类继承出新的数据类型，从而新添一些功能。那些操纵基类接口的方法 
**不需要任何改动就可以应用于新类**\ 。

事实上，不需要改动 ``next()`` 方法，所有的新类都能与原有类一起正确运行。即使 ``next()`` 
方法是单独存放在某个文件中，并且在 ``Shape`` 接口中添加了其他的新方法，\ ``next()`` 也 
**不需要再编译就能正确运行** 。


构造器和多态
------------

构造器 **不具有** 多态性（实际上它们是 ``static`` 方法，只不过该 ``static`` 声明是隐式的）。

基类的构造器 **总是** 在导出类的构造过程中被调用，而且 **按照继承层次** 逐渐向上链接，以使 
**每个基类的构造器都能得到调用**。

通过组合和继承方法来创建新类时，永远不必担心对象的 **清理** 问题，子对象通常都会留给垃圾回收器进行处理。

如果确实遇到清理的问题，那么必须为新类创建 ``dispose()`` 
方法（这个方法名可以自定义）。如果需要进行一些特殊的清理动作，就必须在导出类中覆盖 ``dispose()`` 
方法，示例代码如下。

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

当覆盖被继承类的 ``dispose()`` 方法时，务必记住调用基类的 ``dispose()`` 
方法，否则，基类的清理动作就不会发生。应该首先对导出类进行清理，然后才是基类。

如果这些成员对象存在于其他一个或多个对象时，不能直接简单使用 ``dispose()`` 
方法，需要使用 **引用计数(** ``static int counter`` **)** 来跟踪仍旧访问着共享对象的数量。

.. note:: 
    
    在一般的方法内部，动态绑定的调用是在运行时才决定的，因为对象无法知道它是属于 **方法所在的那个类** 
    还是 **那个类的导出类**\ 。由于动态绑定的存在，可能会出现难以预料的现象，具体细节参考下文描述。

如果先讲原理，可能会有些抽象且难以理解，因此，我们首先阅读一段代码，将问题澄清。

.. code-block:: java
    :emphasize-lines: 32
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

注意到，第 32 行的输出让我们感到意外：

- 基类 ``Glyph`` 中的 ``draw()`` 方法并没有绑定到基类对象上。
  因为基类的 ``draw()`` 并没有在基类中得到调用，转而调用的是导出类的 ``draw()`` 方法。
- 导出类 ``RoundGlyph`` 中的 ``radius`` 属性并没有绑定到导出类对象上。
  因为导出类的 ``radius`` 属性的初始值不是 1，而是 0（为什么是 0？参考 :ref:`load-class`）。

因为构造器调用的层次结构的存在（子类构造器调用父类构造器），会出现一个两难的问题：
如果要调用构造器内部的一个动态绑定方法，就要用到那个方法的被覆盖后的定义。
然而，这个调用的效果可能相当难以预料，因为被覆盖的方法在对象被完全构造之前就会被调用。


协变返回类型
------------

多态是一种机制，当多态机制应用到 **返回值类型** 上时，我们给它起了一个名字叫 "协变返回类型"。

协变返回类型指的是 **子类中的成员函数的** 返回值类型不必严格等同于
**父类中被重写的成员函数的** 返回值类型，而可以是更 "狭窄" 的类型。

为了便于理解，首先我们创建几个类，让其符合如下的继承关系：

.. mermaid::

    classDiagram
        Grain <|-- Wheat : extends
        Mill <|-- WheatMill : extends
        Grain : String toString()
        Wheat : String toString()
        Mill : Grain process()
        WheatMill : Wheat process()

.. code-block:: java
    :emphasize-lines: 29, 30

    //: polymorphism/CovariantReturn.java

    class Grain {
        public String toString() { 
            return "Grain"; 
        }
    }

    class Wheat extends Grain {
        public String toString() { 
            return "Wheat"; 
        }
    }

    class Mill {
        Grain process() { 
            return new Grain(); 
        }
    }

    class WheatMill extends Mill {
        Wheat process() { 
            return new Wheat(); 
        }
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

注意到，高亮代码仅仅也是用父类引用指向子类对象（并没有声明 ``Wheat`` 和 ``WheatMill`` 变量）。
在执行到方法，处理其返回值时，自动地而且正确地使用了多态机制完成了从基类到导出类的转换。
