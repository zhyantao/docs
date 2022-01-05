=============
一切都是对象
=============

用引用操纵对象
--------------


必须由你创建所有对象
--------------------

存储到什么地方
~~~~~~~~~~~~~~~

寄存器：位于处理器内部，最快，但是数量有限。

堆栈：位于 RAM 中，通过堆栈指针分配和释放空间，创建时知道生命周期。

堆：位于 RAM 中，通用内存池，用于存储 Java 对象，不知道对象的生命周期。

常量存储：位于程序代码内部，安全，且永远不会被改变。

非 RAM 对象：完全存活于程序之外，可以不受程序的控制，程序没有运行时也可以存在，如流对象 [1]_ 和持久化对象 [2]_ 。

.. rubric:: 注

.. [1] 流对象：对象转化为字节流，通常发送给另一台机器。
.. [2] 持久化对象：对象存放于磁盘上，JDBC 和 Hibernate 提供轻量级持久化支持。

数据类型
~~~~~~~~~~~~

基本数据类型
^^^^^^^^^^^^^

.. csv-table:: 基本数据类型
    :header: "基本类型", "大小", "最小值", "最大值", "包装器类型", "默认值"

    "boolean", "--", "--", "--", "Boolean", "false"
    "char", "16-bit", "Unicode :math:`0`", "Unicode :math:`2^{16}-1`", "Character", "'\u0000'(null)"
    "byte", "8-bit", ":math:`-128`", ":math:`+127`", "Byte", "(byte)0"
    "short", "16-bit", ":math:`-2^{15}`", ":math:`+2^{15}-1`", "Short", "(short)0"
    "int", "32-bit", ":math:`-2^{31}`", ":math:`+2^{31}-1`", "Integer", "0"
    "long", "64-bit", ":math:`-2^{63}`", ":math:`+2^{63}-1`", "Long", "0L"
    "float", "32-bit", "IEEE754", "IEEE754", "Float", "0.0f"
    "double", "64-bit", "IEEE754", "IEEE754", "Double", "0.0d"
    "void", "--", "--", "--", "Void", ""

高精度数字
^^^^^^^^^^^

- ``BigInteger``
- ``BigDecimal``

永远不需要销毁对象
-------------------

作用域
~~~~~~~

以花括号为边界

.. code-block:: java

    {
        int x = 12;
        // Only x is avaliable
        {
            int q = 96;
            // Both x & q avaliable
        }
        // Only x is avaliable
        // q is "out of scope"
    }

对象的作用域
~~~~~~~~~~~~~

对象的生命周期并不受花括号限制，可以存活于作用域之外。

.. code-block:: java

    {
        String s = new String("a string");
    } // End of scope

在花括号结束时，变量 s 就消失了，但是 s 指向的 String 对象仍然占据内存空间。String 对象只要你需要，就会一直存在， **直到没有指向该对象的引用时（可能是有一个计数器来记录有多少个指向该对象的引用）** ，由垃圾回收器回收。

创建新的数据类型：类
--------------------

字段和方法
~~~~~~~~~~

- 字段：或称数据成员
- 方法：或称成员函数

方法、参数和返回值
------------------

调用方法的行为通常被称为 ``发送消息给对象`` 。

参数列表
~~~~~~~~

基本数据类型之间进行 ``值传递`` ，对象作为参数实际上是 ``引用传递`` 。

有时候，我们不确定需要传递的参数的个数，那么可以参考 :ref:`可变参数列表的使用方法 <variable-argument-list>` 。

构建一个 Java 程序
-------------------

运用其他构件
~~~~~~~~~~~~

- 反转域名后，句点就用来代表子目录的划分
- 配置 ``CLASSPATH`` 以显式声明搜索路径
- 使用 ``import`` 关键字导入一个包，也就是一个类库（在其他语言中，一个库不仅包含类，还可能包含方法和数据，但 Java 中所有的代码都必须写在类里）
- 搜索类库的完整路径为 ``%CLASSPATH%\{import后面的路径}`` 

你的第一个 Java 程序
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    public class HelloDate {
        public static void main(String[] args) {
            System.out.println("Hello, it's: ");
            System.out.println(new Date());
        }
    }

注释和嵌入式文档
-----------------

注释文档 javadoc
~~~~~~~~~~~~~~~~~

只能为 public 和 protected 成员进行文档注释

语法
^^^^^

- 注释文档以 ``/**`` 开始，以 ``*/`` 结束
- 独立文档标签以 ``@`` 开头
- 行内文档标签也是以 ``@`` 开头，但要括在花括号内

一些标签示例
^^^^^^^^^^^^

- ``@see`` 引用其他类，查看更多
- ``{@link package.class#member label}`` 类似于 ``@see``，位于行内，label 为超链接文本
- ``{@docRoot}`` 产生到文档根目录的相对路径，用于文档树页面的显式超链接
- ``{@inheritDoc}`` 从当前类的最直接基类中继承相关文档到当前文档的注释中
- ``@version version-infomation`` 使用 ``javadoc -version`` 提取出 HTML 文档中的版本信息
- ``@author author-infomation`` 使用 ``javadoc -author`` 提取出 HTML 文档中的作者信息
- ``@since`` 指定程序代码最早使用的 JDK 版本
- ``@param parameter-name description`` 
- ``@return description`` 
- ``@throws fully-qualified-class-name description`` 
- ``@deprecated`` 指出一些旧特性已由新特性取代，建议用户不要使用旧特性，因为旧特性将来可能会被删除

嵌入式 HTML
~~~~~~~~~~~

在注释中使用 HTML 标签即可

用法举例
~~~~~~~~

.. code-block:: java

    //: object/HelloDate.java
    import java.util.*;

    /** The first Thinking in Java example program.
    * Displays a string and today's date.
    * @author Bruce Eckel
    * @author www.MindView.net
    * @version 4.0
    */
    public class HelloDate {
        /** Entry point to class & application.
        * @param args array of string arguments
        * @throws exceptions No exceptions thrown
        */
        public static void main(String[] args) {
            System.out.println("Hello, it's: ");
            System.out.println(new Date());
        }
    } /* Output: (55% match)
    Hello, it's:
    Wed Oct 05 14:39:36 MDT 2005
    *///:~


编码风格：驼峰式
-----------------

- methodName
- ClassName
