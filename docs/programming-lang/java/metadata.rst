======
元知识
======

学习编程语言，总会有一些共性的东西，基本上所有的编程语言都会很相似甚至会相同。
给这一章起名 "元知识" 是想抽取共性的部分，然后撮合成本文。
因此，如果你学习过其他高级语言，比如 C++，即使这一小节你不阅读，也应该知道的差不多。

.. _java-datatpyes:

数据类型
--------

Java 不支持无符号类型，所有的数值都是有符号的。

.. csv-table::
    :header: "基本类型", "大小", "最小值", "最大值", "包装器类型", "默认值"

    "``boolean``", "--", "--", "--", "``Boolean``", "``false``"
    "``char``", "16-bit", ":math:`0`", ":math:`2^{16}-1`", "``Character``", "'\u0000'(``null``)"
    "``byte``", "8-bit", ":math:`-128`", ":math:`+127`", "``Byte``", "(``byte``)0"
    "``short``", "16-bit", ":math:`-2^{15}`", ":math:`+2^{15}-1`", "``Short``", "(``short``)0"
    "``int``", "32-bit", ":math:`-2^{31}`", ":math:`+2^{31}-1`", "``Integer``", "0"
    "``long``", "64-bit", ":math:`-2^{63}`", ":math:`+2^{63}-1`", "``Long``", "0L"
    "``float``", "32-bit", "IEEE754", "IEEE754", "``Float``", "0.0f"
    "``double``", "64-bit", "IEEE754", "IEEE754", "``Double``", "0.0d"
    "``void``", "--", "--", "--", "Void", "--"
    "``BigInteger``", "--", "--", "--", "--", "--"
    "``BigDecimal``", "--", "--", "--", "--", "--"
    "引用", "--", "--", "--", "--", "``null``"

以上就是基本类型的数据了，我们也可以通过使用 **直接常量表示法**，让编译器可以准确地知道要生成什么类型的数据。
直接常量就是在数值的基础上加上 **前缀** 或 **后缀**。
在 C、C++、Java 中，\ **二进制数** 没有直接的常量表示方法，可以使用 ``Integer`` 或 ``Long``
类的静态方法 ``toBinaryString()`` 来获得。

.. csv-table::
    :header: "前缀", "含义", "后缀", "含义"
    :widths: 10, 10, 10, 20

    "``0``", "八进制", "``F``", "``float`` 类型"
    "``0x``", "十六进制", "``D``", "``double`` 类型（小数的默认类型）"
    "", "", "``L``", "长整形数据"


除了直接常量表示法，还有 **指数表示法**，用 ``e`` 来代表 10 的幂次，比如 :math:`47e47 = 4.7 \times 10^{48}`
在代码中，可以直接给变量赋值为指数形式，比如 ``a = 47e47;``

指针指向一块内存，它的内容是所指内存的地址；而引用则是某块内存的别名 [1]_。

- 指针可以在运行时改变其所指向的值，引用一旦和某个对象绑定就不再改变；
- 从内存上看，指针会分配内存区域，而引用不会，它仅仅是一个别名；
- 在参数传递时，引⽤用会做类型检查，而指针不会；
- 引用不能为空，指针可以为空。

在 C++ 中，一个指针的大小可能是几个字节（跟机器的位数有关系），这个大小可以通过 ``sizeof()`` 来测量。
Java 不需要 ``sizeof()``，因为所有数据类型在所有机器中的大小都是相同的，这是Java 天然可移植带来的优势。

Java 不会自动将 ``int`` 数值转换成布尔值，因此如果 ``a`` 是一个数值，那么 ``if(a)`` 是不对的，而
``if(a != 0)`` 是可以的，而 ``if(a)`` 这种行为在 C++ 中是会允许的。
如果我们想要手动进行类型转换，可以使用类似 ``(int)value`` 的语法将其他类型的数据转换为整形数据。
需要注意的是，除了 ``boolean`` 以外，其他基本类型之间都可以互相转换。


运算符和优先级
--------------

以 C 语言中的运算符和优先级为例：

.. csv-table::
    :header: "运算符及优先级", "结合性"

    ":math:`\text{()   []   ->   .}`",   "从左到右"
    ":math:`\text{!   ~   ++   --   +   -   *   (type)   sizeof}`",   "从右到左"
    ":math:`\text{*   /   %}`",   "从左到右"
    ":math:`\text{+   -}`",   "从左到右"
    ":math:`\text{<<   >>}`",   "从左到右"
    ":math:`\text{<   <=   >   >=}`",   "从左到右"
    ":math:`\text{==   !   =}`",   "从左到右"
    ":math:`\text{&}`",   "从左到右"
    ":math:`\text{^}`",   "从左到右"
    ":math:`\text{|}`",   "从左到右"
    ":math:`\text{&&}`",   "从左到右"
    ":math:`\text{||}`",   "从左到右"
    ":math:`\text{?:}`",   "从左到右"
    ":math:`\text{=   +=   -=   *=   /=   %=   &=   ^=   |=   <<=   >>=}`",   "从右到左"
    ":math:`\text{,}`",   "从右到左"

.. note::

    一元运算符的 :math:`\text{+ - & *}` 的优先级比二元运算符 :math:`\text{+ - & *}` 的优先级高。

以上是的常见的运算符，但是，在 Java 中有几点需要注意：

当编译器观察到一个 ``String`` 后面紧跟一个 ``+``，而这个 ``+`` 的后面又紧跟一个非 ``String``
类型的元素时，就会尝试将这个非 ``String`` 类型的元素转换为 ``String``，对于类来说，会自动调用
``toString()`` 方法。
如果在应该使用 ``String`` 值的地方使用了布尔值，布尔值会自动转换为适当的文本形式，即自动转换为
``True`` 和 ``False``\ （``enum`` 类可以达到同样的目标）。

在为对象赋值时，真正操作的是对象的引用。实际上就是将对象的引用从一个地方复制到了另一个地方。
最典型的场景就是当对象作为函数的参数传递时。

使用比较运算符时，基本类型直接使用 ``==`` 或 ``!=`` 即可，判断浮点数是否为 0 是非常严格的，只要比
0 大一点点，它仍然是非零的。而比较对象时，实际上比较的是对象的引用。
比较对象内容是否相等，需要使用 ``equals()`` 方法，但是当你创建自己的类时，需要重写 ``equals()``
方法，否则，无法直接比较内容是否相等。如下代码所示：

.. code-block:: java
    :emphasize-lines: 7, 8

    //: operators/Equivalence.java

    public class Equivalence {
        public static void main(String[] args) {
            Integer n1 = new Integer(47);
            Integer n2 = new Integer(47);
            System.out.println(n1 == n2);
            System.out.println(n1.equals(n2));
        }
    } /* Output:
    false
    true
    *///:~

逻辑操作符在参与运算时，存在短路现象。

移位操作符只可用来处理整数类型：

- 左移操作：在低位补 0
- 有符号的右移操作：若符号为正，则在高位补 0
- 有符号的右移操作：若符号为负，则在高位补 1
- 无符号的右移操作：无论正负，在高位补 0

对 ``char``、\ ``byte``、\ ``short`` 类型的数值进行移位处理时，移位之前，编译器会将其自动转换为
``int`` 类型。并且得到的结果也是 ``int`` 类型。如下所示：

.. code-block:: java
    :emphasize-lines: 15, 19, 25
    :linenos:

    //: operators/URShift.java
    // Test of unsigned right shift.
    import static net.mindview.util.Print.*;

    public class URShift {
        public static void main(String[] args) {
            int i = -1;
            print("int: " + Integer.toBinaryString(i));
            i >>>= 10;
            print("int: " + Integer.toBinaryString(i));
            long l = -1;
            print("long: " + Long.toBinaryString(l));
            l >>>= 10;
            print("long: " + Long.toBinaryString(l));
            short s = -1;
            print("Short: " + Integer.toBinaryString(s));
            s >>>= 10;
            print("Short: " + Integer.toBinaryString(s));
            byte b = -1;
            print("byte: " + Integer.toBinaryString(b));
            b >>>= 10;
            print("byte: " + Integer.toBinaryString(b));
            b = -1;
            print("byte: " + Integer.toBinaryString(b));
            print("byte: " + Integer.toBinaryString(b>>>10));
        }
    } /* Output:
    int: 11111111111111111111111111111111
    int: 1111111111111111111111
    long: 1111111111111111111111111111111111111111111111111111111111111111
    long: 111111111111111111111111111111111111111111111111111111
    Short: 11111111111111111111111111111111
    Short: 11111111111111111111111111111111
    byte: 11111111111111111111111111111111
    byte: 11111111111111111111111111111111
    byte: 11111111111111111111111111111111
    byte: 1111111111111111111111
    *///:~

上面代码中的 ``int`` 和 ``long`` 类型的数据表现比较正常，一个 32 位，一个 64 位，右移后，减少了 10
位。``short`` 和 ``byte`` 类型由于在右移操作处理前和处理后的结果都会自动转换为 ``int``
类型，所以看起来都是 32 位的，并没有发生什么变化，但这并 **不是我们预期** 想要的结果。
注意到第 25 行代码，没有把结果赋值给 ``b``，而是直接打印出来，所以其结果是正确的。

Java 中 **唯一用到** 逗号操作符的地方就是 ``for`` 循环的控制表达式了。
可以在 ``for`` 循环的 initializaiton 和 step 中书写多个表达式，然后用逗号分隔开。

.. code-block:: java

    for (initializaiton; Boolean-expression; step) {
        statements;
    }


foreach
-------

``foreach`` 可以用于任何 ``Iterable`` 对象，因此可以用于数组和容器这种已经实现了 ``Iterable``
接口的对象。

不必创建 ``int`` 变量去对由访问项构成的序列进行计数，\ ``foreach`` 将自动产生每一项。

.. code-block:: java

    //: control/ForEachInt.java
    import static net.mindview.util.Range.*;
    import static net.mindview.util.Print.*;

    public class ForEachInt {
        public static void main(String[] args) {
            for(int i : range(10)) // 0..9
                printnb(i + " ");
            print();
            for(int i : range(5, 10)) // 5..9
                printnb(i + " ");
            print();
            for(int i : range(5, 20, 3)) // 5..20 step 3
                printnb(i + " ");
            print();
        }
    } /* Output:
    0 1 2 3 4 5 6 7 8 9
    5 6 7 8 9
    5 8 11 14 17
    *///:~


switch
-------

``switch`` 根据 ``integral-selector``\ （整数选择因子）产生的整数值，与 ``case``
中的情况进行比较，如果符合，执行相应的 ``statement``。
若 ``case`` 全都不匹配，就执行 ``default`` 语句。

.. code-block:: java

    switch(integral-selector) {
        case integral-value1: statement; break;
        case integral-value2: statement; break;
        // ...
        default: statement;
    }

.. rubric:: 参考资料

.. [1] 传指针和传指针引用的区别/指针和引用的区别（本质） [`webpage <https://www.cnblogs.com/x_wukong/p/5712345.html>`__]
