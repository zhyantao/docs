============
初始化与清理
============

构造器重载和方法重载
--------------------

.. code-block:: java
    :emphasize-lines: 8,12,17,20
    :linenos:

    //: initialization/Overloading.java
    // Demonstration of both constructor
    // and ordinary method overloading.
    import static net.mindview.util.Print.*;

    class Tree {
        int height;
        Tree() {
            print("Planting a seedling");
            height = 0;
        }
        Tree(int initialHeight) {
            height = initialHeight;
            print("Creating new Tree that is " +
                height + " feet tall");
        }	
        void info() {
            print("Tree is " + height + " feet tall");
        }
        void info(String s) {
            print(s + ": Tree is " + height + " feet tall");
        }
    }

    public class Overloading {
        public static void main(String[] args) {
            for(int i = 0; i < 5; i++) {
                Tree t = new Tree(i);
                t.info();
                t.info("overloaded method");
            }
            // Overloaded constructor:
            new Tree();
        }	
    } /* Output:
    Creating new Tree that is 0 feet tall
    Tree is 0 feet tall
    overloaded method: Tree is 0 feet tall
    Creating new Tree that is 1 feet tall
    Tree is 1 feet tall
    overloaded method: Tree is 1 feet tall
    Creating new Tree that is 2 feet tall
    Tree is 2 feet tall
    overloaded method: Tree is 2 feet tall
    Creating new Tree that is 3 feet tall
    Tree is 3 feet tall
    overloaded method: Tree is 3 feet tall
    Creating new Tree that is 4 feet tall
    Tree is 4 feet tall
    overloaded method: Tree is 4 feet tall
    Planting a seedling
    *///:~

this 关键字
------------

使用 this 关键字传递自身引用。

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
    

.. note:: 

    1. this 关键字指代当前对象的引用，使用 this 调用方法，表示调用当前对象的方法或属性。（因为可能类的属性和方法内部的属性可能同名，这时候可以用 this 关键字来区分）
    2. return this 表示返回当前对象的引用。
    3. 上面代码第 18 行，由 Apple 类生成的苹果对象将自身传递给了外部操作 Peeler.peel()。Peeler 剥完皮后又把苹果返回了。
    
在构造器中调用构造器。

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

.. tip:: 

    与 ``this(String[] args)`` 类似，使用 ``super(String[] args)`` 调用父类对象的某个构造器。

static 关键字
--------------

1. static 方法内部不能调用非静态方法。
2. static 方法没有 this 方法。
3. static 方法其实时 Java 中的全局方法。
4. 想为某特定域只分配一份存储空间，而不去考虑究竟要创建多少对象，甚至根本就不创建对象。
5. 希望某个方法不与包含它的类的任何对象关联在一起。即通过类名调用方法。

final关键字
-----------

final 是指“这是无法改变的”。

final 数据
~~~~~~~~~~

声明 final 数据时，通常针对：

1. 一个永不改变的 **编译时常量** 。
2. 一个在运行时被初始化的值，而你不希望它被改变。

编译时常量可以在编译期直接带入计算式参与计算，减轻了运行时的负担。

- 对于基本数据类型，final 使数值恒定不变。
- 对于引用类型，final 使引用恒定不变，即一旦引用被初始化，无法再指向其他对象。
- 参数列表中使用 final 时，表示无法更改参数引用的指向。

.. note:: 
    
    - 一个既是 static 又是 final 的域只占据一段不能改变的存储空间
    - 定义为 public 强调可以用于包之外
    - 定义为 static 强调只有一份
    - 定义为 final 强调是一个常量

.. tip:: 
    
    按照惯例，既是 static 又是 final 的域（即编译器常量）用大写表示，使用下划线分隔各个单词。

final 方法
~~~~~~~~~~~

- 使用 final 方法可以锁定方法，使继承类无法重写该方法。
- 类中所有的 **private 方法** 都隐式地指定为 final，因为无法改变。
- “关闭”动态绑定。 :ref:`参考 <dynamic-binding>`

final 类
~~~~~~~~

将某个类声明为 final 表示该类将无法被继承。

finalize() 方法
----------------

1. 不是 new 出来的对象，垃圾回收器不会回收。
2. 不是 new 出来的对象，会获得一块特殊的内存，需要使用 finalize() 方法来释放。
3. 当某个对象处于某种状态时（例如文件处于打开状态），如果直接使用 finalize() 清理该对象占用的内存空间，可能会发生异常。因此 finalize() 可以用来发现异常。如下代码所示：

.. code-block:: java
    :emphasize-lines: 13,29
    :linenos:

    //: initialization/TerminationCondition.java
    // Using finalize() to detect an object that
    // hasn't been properly cleaned up.

    class Book {
        boolean checkedOut = false;
        Book(boolean checkOut) {  // true为图书出库
            checkedOut = checkOut;
        }
        void checkIn() {  // 图书出库后，需要做状态检查和设置
            checkedOut = false;
        }
        protected void finalize() {
            if(checkedOut)  // 图书出库后，如果没有做检查和设置，会抛出异常
                System.out.println("Error: checked out");
            // Normally, you'll also do this:
            // super.finalize(); // Call the base-class version
        }
    }

    public class TerminationCondition {
        public static void main(String[] args) {
            Book novel = new Book(true);  // 图书出库
            // Proper cleanup:
            novel.checkIn();
            // Drop the reference, forget to clean up:
            new Book(true);
            // Force garbage collection & finalization:
            System.gc();
        }
    } /* Output:
    Error: checked out
    *///:~


构造器的初始化
--------------

1. 静态变量会先于非静态变量初始化。
2. 即使没有显式地使用 static 关键字，构造器实际上也是静态方法。
3. 不论类中的属性成员分布于方法成员之前还是之后，属性成员都会先于类中的任何方法成员，进行初始化。如下代码所示：

.. code-block:: java
    :emphasize-lines: 12,18,20
    :linenos:

    //: initialization/OrderOfInitialization.java
    // Demonstrates initialization order.
    import static net.mindview.util.Print.*;

    // When the constructor is called to create a
    // Window object, you'll see a message:
    class Window {
        Window(int marker) { print("Window(" + marker + ")"); }
    }

    class House {
        Window w1 = new Window(1); // Before constructor
        House() {
            // Show that we're in the constructor:
            print("House()");
            w3 = new Window(33); // Reinitialize w3
        }
        Window w2 = new Window(2); // After constructor
        void f() { print("f()"); }
        Window w3 = new Window(3); // At end
    }

    public class OrderOfInitialization {
        public static void main(String[] args) {
            House h = new House();
            h.f(); // Shows that construction is done
        }
    } /* Output:
    Window(1)
    Window(2)
    Window(3)
    House()
    Window(33)
    f()
    *///:~

.. _init-arrays:

数组初始化
-----------

.. code-block:: java
    :emphasize-lines: 6-8
    :linenos:

    //: initialization/ArraysOfPrimitives.java
    import static net.mindview.util.Print.*;

    public class ArraysOfPrimitives {
    public static void main(String[] args) {
        int[] a1 = { 1, 2, 3, 4, 5 };
        int[] a2;
        a2 = a1;
        for(int i = 0; i < a2.length; i++)
            a2[i] = a2[i] + 1;
        for(int i = 0; i < a1.length; i++)
            print("a1[" + i + "] = " + a1[i]);
    }
    } /* Output:
    a1[0] = 2
    a1[1] = 3
    a1[2] = 4
    a1[3] = 5
    a1[4] = 6
    *///:~


.. note:: 如果你创建的是非基本类型的数组，那么你就创建了一个引用数组。如下所示：

.. code-block:: java
    :emphasize-lines: 9
    :linenos:

    //: initialization/ArrayClassObj.java
    // Creating an array of nonprimitive objects.
    import java.util.*;
    import static net.mindview.util.Print.*;

    public class ArrayClassObj {
        public static void main(String[] args) {
            Random rand = new Random(47);
            Integer[] a = new Integer[rand.nextInt(20)];
            print("length of a = " + a.length);
            for(int i = 0; i < a.length; i++)
                a[i] = rand.nextInt(500); // Autoboxing
            print(Arrays.toString(a));
        }
    } /* Output: (Sample)
    length of a = 18
    [55, 193, 361, 461, 429, 368, 200, 22, 207, 288, 128, 51, 89, 309, 278, 498, 361, 20]
    *///:~

.. _variable-argument-list:

可变参数列表
-------------

.. code-block:: java
    :emphasize-lines: 5,6,19
    :linenos:

    //: initialization/NewVarArgs.java
    // Using array syntax to create variable argument lists.

    public class NewVarArgs {
        // static void printArray(Object[] args) {  // 老语法
        static void printArray(Object... args) {    // 新语法
            for(Object obj : args)
                System.out.print(obj + " ");
            System.out.println();
        }
        public static void main(String[] args) {
            // Can take individual elements:
            printArray(new Integer(47), new Float(3.14), new Double(11.11));
            printArray(47, 3.14F, 11.11);
            printArray("one", "two", "three");
            printArray(new A(), new A(), new A());
            // Or an array:
            printArray((Object[])new Integer[]{ 1, 2, 3, 4 });
            printArray(); // Empty list is OK
        }
    } /* Output: (75% match)
    47 3.14 11.11
    47 3.14 11.11
    one two three
    A@1bab50a A@c3c749 A@150bd4d
    1 2 3 4
    *///:~

.. note:: 
    
    1. 可变参数列表其实是一个数组。这就是为什么可以用 foreach 来进行迭代的原因。
    2. 可变参数列表支持自动包装机制。
    3. 可变参数列表使重载变得更复杂了。比如现在有方法 f(Character... args), f(Integer... args)。当调用 f() 时，编译器不知道该调用两者中的哪一个了。这时可以通过加一个非可变参数来解决：f(float i, Character... args)。

枚举类型
---------

.. code-block:: java

    //: initialization/Spiciness.java

    public enum Spiciness {
        NOT, MILD, MEDIUM, HOT, FLAMING
    } ///:~

.. note:: 

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


