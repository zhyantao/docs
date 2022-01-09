=============
访问权限控制
=============

访问权限控制常被称为是 **具体实现的隐藏** 。

包：库单元
-----------

访问权限从大到小依次为： ``public`` 、 ``protected`` 、 包访问权限 、 ``private`` 。

访问权限用来向客户端程序员指定哪些是可用的，哪些是不可用的。

Java 的标准工具库放在了 ``java.util`` 名字空间下。

- 类库是一组类文件，每个类文件都有一个 ``public`` 类。
- 每个 Java 源代码文件通常被称为一个编译单元（或转译单元）。
- 每个编译单元只能有一个 ``public`` 类。
- 每个编译单元中的其他非 ``public`` 类用于给 ``public`` 类提供支持。

.. note:: 

    - **构件（Component）** 是指一个对象（接口规范、或二进制代码），它被用于复用，接口被明确定义。
    - 操作集合、过程、函数即使可以复用也不能称为一个构件。
    - 开发者可以通过组装已有的构件来开发新的应用系统，从而达到软件复用的目的。
    - 如果希望构件从属于同一个群组，可以使用 ``package`` 关键字。
    - ``package`` 语句必须位于除注释之外的第一行。
    - 是否可以理解为一个构件完成一个小功能呢？

Java 代码组织方式
~~~~~~~~~~~~~~~~~~

- 在 ``.java`` 文件中的每个类都会有一个 ``.class`` 输出文件，该输出文件的名称与 ``.java`` 文件中的每个类的名称相同。
- Java 可运行程序是一组可以打包并压缩为一个 Java 文档文件（JAR，使用 Java 的 jar 文档生成器）的 ``.class`` 文件。
- Java 解释器负责查找、装载、解释 Java 可运行程序。

.. note:: 

    Java 解释器的运行过程

    - 环境变量 ``CLASSPATH`` （在操作系统中可以设置）显式地声明 Java 解释器的搜索 ``.class`` 文件的根路径。
    - Java 解释器将包的名称的句点转换为反斜杠，并与根路径进行合并，得到完整的搜索路径。
    - 当 ``CLASSPATH`` 中有一项是 ``.`` 的时候，编译器就会查找当前目录（好像默认情况下也会访问）。
    
    特殊情况

    - 对于 Jar 包，需要在 ``CLASSPATH`` **直接指明** 完整路径。
    - 比如： ``C:\\flavors\\grape.jar``

Java 访问权限修饰词
--------------------

public: 接口访问权限
~~~~~~~~~~~~~~~~~~~~~

接口访问权限对每个人都是可用的。

包访问权限
~~~~~~~~~~

- 没有任何关键字（默认访问权限）。
- 包访问权限在同一个编译单元中（即一个文件）。
- 一个编译单元只能隶属于同一个包。
- 处于同一个编译单元中的所有类彼此之间都是自由访问的。

.. note:: 
    
    - 具有包访问权限的类的对象，可以由包内的任何其他类来创建，但是在包外是不行的。
    - 相同目录下的所有不具有明确的 ``package`` 声明的文件，都被视作该目录下默认包的一部分。


protected: 继承访问权限
~~~~~~~~~~~~~~~~~~~~~~~~

从 ``protected`` 从属的类继承的类，可以访问 ``protected`` 方法。

private: 你无法访问
~~~~~~~~~~~~~~~~~~~~

在多线程场景下 ``private`` 关键字很重要。

接口和实现
-----------

“封装”通过合并特征和行为来创建新的数据类型。封装成功的表现是 **一个同时带有特征和行为的数据类型** 。

“实现隐藏”通过将细节“私有化”把接口和实现分离开来。

类的访问权限
-------------

对于一个类来讲，是不能有 ``private`` 和 ``protected`` 的。

类访问权限只能有两个：包访问权限或 ``public`` 。

如果你不希望任何人使用这个类创建对象的话，将构造器声明为 ``private`` 即可。但是该类的静态方法可以使用。如下代码所示：

.. code-block:: java
    :emphasize-lines: 6,14
    :linenos:

    //: access/Lunch.java
    // Demonstrates class access specifiers. Make a class
    // effectively private with private constructors:

    class Soup1 {
        private Soup1() {}
        // (1) Allow creation via static method:
        public static Soup1 makeSoup() {
            return new Soup1();
        }
    }

    class Soup2 {
        private Soup2() {}
        // (2) Create a static object and return a reference
        // upon request.(The "Singleton" pattern):
        private static Soup2 ps1 = new Soup2();
        public static Soup2 access() {
            return ps1;
        }
        public void f() {}
    }

    // Only one public class allowed per file:
    public class Lunch {
        void testPrivate() {
            // Can't do this! Private constructor:
            //! Soup1 soup = new Soup1();
        }
        void testStatic() {
            Soup1 soup = Soup1.makeSoup();
        }
        void testSingleton() {
            Soup2.access().f();
        }
    } ///:~

.. note:: 上面代码 Soup2 实现了单例模式。
