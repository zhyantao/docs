=============
访问权限控制
=============

访问权限用来向客户端程序员指定哪些是可用的，哪些是不可用的。

访问权限从大到小依次为： ``public``、\ ``protected``、\ ``包访问权限``、 ``private``。

包：库单元
-----------

包是一个文件夹。我们用 ``package`` 关键字来声明该文件夹所在的位置，然后配合 Windows 下的 
``CLASSPATH`` 环境变量就能准确定位一个文件了。

.. note:: 

    Java 解释器的运行过程：

    - 环境变量 ``CLASSPATH`` （在操作系统中可以设置）显式地声明 Java 解释器的搜索 ``.class`` 文件的根路径。
    - Java 解释器将包的名称的句点转换为反斜杠，并与根路径进行合并，得到完整的搜索路径。
    - 当 ``CLASSPATH`` 中有一项是 ``.`` 的时候，编译器就会查找当前目录（好像默认情况下也会访问）。
    
    特殊情况：

    - 对于 Jar 包，需要在 ``CLASSPATH`` **直接指明** 完整路径。
    - 比如： ``C:\\flavors\\grape.jar``

包访问权限没有任何关键字（默认访问权限）。
具备包访问权限指的是在同一个包（文件夹）下的变量可以相互访问的，如示例代码所示。
包的存在是为了隔离名称空间，比如 Java 的标准工具库放在了 ``java.util`` 名字空间下。

.. code-block:: java

    //: src/File1.java

    class File1 {
        int data = 10;
    }

.. code-block:: java

    //: src/File2.java
    public class File2 {
        public static void main(String[] args) {
            File1 f1 = new File1();
            System.out.println(f1.data);
        }
    }/* Output:
    10
    *///:~


类库是一个比包更大的概念，它是指多个文件夹的集合，通常我们可见的类库文件也就是 ``.jar`` 或 
``.war`` 文件。

有了类库的概念，那么我们更深一步地讨论一个更大的概念：\ **构件 —— 类库的组合**。

构件概念的提出主要基于软件重用的思想。
虽然对象也是一种可重用的软件实体，但是用对象实现需求需要两部分的代码：1）编写业务逻辑代码，2）\ 
编写服务支持代码，如安全服务、事务服务等。第 1 步比较简单，但是第 2 步则需要编写和中间件或服务\ 
器接口交互的代码，涉及大量的底层实现，代码量大，移植性、重用性也比较差 [1]_。

构件技术通过分离服务支持的逻辑，将对服务的需求实现为描述性文件，代码量小，移植性和重用性高。
开发者可以通过组装已有的构件来开发新的应用系统，从而达到软件复用的目的。
如果希望构件从属于同一个群组，可以使用 ``package`` 关键字。

JavaBean 是 Java 中的术语，行业内通常称为 Java 豆，在计算机领域代表 Java 构件 [2]_。
JavaBean 可分为两种：一种是有用户界面的 JavaBean；还有一种是没有用户界面，主要负责处理事务\ 
（如数据运算，操纵数据库）的 JavaBean。JSP 通常访问的是后一种 JavaBean。

最初，JavaBean 的目的是为了让用户可以使用JavaBean将功能、处理、值、数据库访问和其他任何可以用 
Java 代码创造的对象进行打包，并且其他的开发者可以通过内部的 JSP 页面、Servlet、其他 JavaBean、\ 
applet 程序或者应用来使用这些对象。用户可以认为 JavaBean 
提供了一种随时随地的复制和粘贴的功能，而不用关心任何改变。
特别是用与帮助厂家开发在综合开发环境（IDE）下使用的 Java 软件部件。
这些包括如 Grid 控件，用户可以将该部件拖放到开发环境中。
从此，JavaBean 就可以扩展为一个 Java Web 应用的标准部件，并且 JavaBean 
部件框架已经扩展为企业版的 Bean（EJB） [2]_。


类的访问权限
-------------

对于一个类来讲，是不能用 ``private`` 或 ``protected`` 来修饰的，但可以是 ``public`` 或包访问权限。

如果你不希望除本类之外的任何其他类使用本类创建对象的话，将构造器声明为 ``private`` 
即可，但是该类的静态方法仍然可以使用。
其实，这也是 **单例模式** 的一种设计思路，\ ``static`` 数据只能存储一份，且对象只能由本类创建。

.. code-block:: java
    :emphasize-lines: 6,14

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


.. rubric:: 参考资料

.. [1] 窦蕾 袁臻 刘冬梅. 基于构件的中间件技术J2EE[J]. 计算机科学, 2004, 31(6): 13-16.
.. [2] Java Bean [`webpage <https://www.cnblogs.com/wzooey/p/3687557.html>`__]
