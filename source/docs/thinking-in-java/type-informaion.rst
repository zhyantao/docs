=========
类型信息
=========

Java 在运行时识别对象和类的信息，主要有两种方式：

- RTTI（Runtime Type Identification）：运行时类型识别
- 反射：允许在运行时发现和使用类的信息

为什么需要 RTTI
----------------

面向对象的基本目的：让代码只操纵对基类的引用。这样，如果要添加一个新类来扩展程序，就不会影响到原来的代码。

.. uml::

    @startuml

    class Shape
    class Circle
    class Square
    class Triangle

    Shape <|-- Circle
    Shape <|-- Square
    Shape <|-- Triangle

    @enduml

比如，当把元素放入数组 ``List<Shape>`` 中时，会丢失 ``Shape`` 类型信息，向上转型为 ``Object`` 。
当从数组 ``List<Shape>`` 中取出元素时，容器 ``List`` 会自动将结果转型回 ``Shape`` 。
这是 RTTI 最基本的使用形式，因为在 Java 中，所有的类型转换都是在运行时进行正确性检查的。

但是，这个例子 RTTI 转型并不彻底， ``Object`` 被转型为 ``Shape`` ，并没有转型为 ``Circle`` 、 ``Square`` 或者 ``Triangle`` 。
这是因为目前我们只知道这个 ``List<Shape>`` 保存的都是 ``Shape`` 。这是由 **容器** 和 **泛型** 来保证这种机制的。

接下来是由 **多态** 进行动态绑定，将 ``Shape`` 转型为 ``Circle`` 、 ``Square`` 或者 ``Triangle`` 。

Class 对象
-----------

类型信息在运行时是如何表示的？

- 加载。每编写并编译了一个新类，类加载器查找字节码，并从字节码中创建一个 Class 对象。
  
  - 每个类都有一个 Class 对象，被保存在同名 ``.class`` 文件中。
  - Java 使用 Class 对象来创建所有普通类的对象（执行 RTTI），Class 对象包含了与类有关的信息。
  - 一旦某个类的 Class 对象被载入内存，它就被用来创建这个类的所有对象。

- 链接。验证类中的字节码，为静态域分配存储空间，并且若必须的话，将解析这个类创建的对其他类的所有引用。
- 初始化。如果该类具有超类，则对其初始化，执行静态初始化器和静态初始化块。

.. code-block:: java

    //: typeinfo/SweetShop.java
    // Examination of the way the class loader works.
    import static net.mindview.util.Print.*;

    class Candy {
        static { print("Loading Candy"); }
    }

    class Gum {
        static { print("Loading Gum"); }
    }

    class Cookie {
        static { print("Loading Cookie"); }
    }

    public class SweetShop {
        public static void main(String[] args) {	
            print("inside main");
            new Candy();
            print("After creating Candy");
            try {
                Class.forName("Gum");
            } catch(ClassNotFoundException e) {
                print("Couldn't find Gum");
            }
            print("After Class.forName(\"Gum\")");
            new Cookie();
            print("After creating Cookie");
        }
    } /* Output:
    inside main
    Loading Candy
    After creating Candy
    Loading Gum
    After Class.forName("Gum")
    Loading Cookie
    After creating Cookie
    *///:~

Class 对象常用的方法：

- ``Class.forName()`` 查找相应类的对象的 Class 对象引用
- ``Class.getClass()`` 获取 Class 对象的引用
- ``Class.getInterfaces()`` 获取感兴趣的对象所包含的接口
- ``Class.getSuperclass()`` 查找基类

普通对象 object 的常用方法：

- ``object.getSimpleName()`` 产生不包含包名的类名
- ``object.getCanonicalName()`` 产生全限定的类名

.. note:: 

    Java 虚拟机使用类加载器生成 Class 对象（首先检查是否已经生成，若未生成，就根据类名查找 ``.class`` 文件）。
    
    类加载器子系统实际上包含一条类加载器链，但是只有一个原生类加载器，它是 JVM 实现的一部分。
    原生加载器加载的是可信类，包括从本地盘加载的 Java API 类（若从网络中加载类需要手动挂接）。
    
    所有的类都是在对其第一次使用时，动态加载到 JVM 中的。当程序创建第一个对类的静态成员的引用时，就会加载这个类。
    因此，当用 ``new`` 创建对象时，就是在创建类的构造器的引用，这说明构造器就是 ``static`` 的。

    但是，Java 程序在它开始运行之前，并未完全加载，其余各个部分是在需要时才加载的。

类字面常量
~~~~~~~~~~

使用类字面常量生成对 Class 对象的引用：

.. code-block:: java

    FancyToy.class

这样做比用 ``forName()`` 更简单、更安全。

类字面常量可以用于：

- 普通类
- 接口
- 数组
- 基本数据类型
- 基本数据类型的包装器类

.. note:: 

    使用 ``.class`` 创建对 Class 对象的引用时，不会自动初始化该 Class 对象，而使用 ``forName()`` 会初始化对象。

泛化的 Class 引用
~~~~~~~~~~~~~~~~~

Class 引用总是指向某个 Class 对象，它可以创建类的对象，并包含可作用于这些对象的所有方法代码。
它还包含该类的静态成员，因此，Class 引用表示的就是它所指向的对象的确切类型，而该对象便是 Class 类的一个对象。

普通的类的引用可以被重新赋值为指向任何其他的 Class 对象，这是不安全的。
可以使用泛型语法对 Class 引用所指向的 Class 对象的类型进行限定。为了放宽这种限定，可以使用通配符，比如 ``Class<?>`` 。
向 Class 引用添加泛型语法的原因仅仅是为了提供编译期类型检查。

.. code-block:: java
    :emphasize-lines: 6

    //: typeinfo/GenericClassReferences.java

    public class GenericClassReferences {
        public static void main(String[] args) {
            Class intClass = int.class;
            Class<Integer> genericIntClass = int.class;
            genericIntClass = Integer.class; // Same thing
            intClass = double.class;
            // genericIntClass = double.class; // Illegal
        }
    } ///:~

类型转换前先做检查
------------------

比如上面说的 Shape 在向下转型时，编译器不知道转型为什么形式，就需要人为地显示指定。

RTTI 类型识别有三种方式：

- 传统的类型转换
- 查询 Class 对象
- 使用关键字 instanceof

使用类字面常量
~~~~~~~~~~~~~~~
动态的 instanceof
~~~~~~~~~~~~~~~~~~
递归计数
~~~~~~~~
注册工厂
--------
instanceof 与 Class 的等价性
----------------------------
反射：运行时的类信息
---------------------
类方法提取器
~~~~~~~~~~~~
动态代理
--------
空对象
------
模拟对象与桩
~~~~~~~~~~~~
接口与类型信息
--------------
