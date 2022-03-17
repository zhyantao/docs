====
数组
====


数组和容器
----------

在 Java 中，数组是一种 **效率最高** 的存储和随机访问对象引用序列的方式。
数组就是一个简单的线性序列，这使得元素访问非常迅速。
但是，为这种速度所付出的代价是数组对象的大小被固定，并且在其生命周期中不可改变。

在泛型之前，其他的容器类在处理对象时，都将它们视作没有任何具体类型，也就是说，它们将这些对象都当作 
``Object`` 来处理。
有了泛型之后，容器就可以指定并检查它们所持有对象的类型，并且有了自动包装机制，容器还能够持有基本类型。

容器和泛型对数组产生了极大的冲击，并且现在的容器在除了性能之外的各个方面都碾压数组。
通常，即使当你可以让泛型与数组以某种方式一起工作时，在编译器你最终也会得到 "不受检查" 的警告信息。

针对大多数场景，用的更多的是容器，而不是数组，除非你对性能有更高的要求。


数组初始化
-----------

创建基本类型的 **一维数组**，很简单。如下所示：

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

如果你创建的是 **非基本类型的数组**，那么你就创建了一个引用数组（存放引用的数组）。

如果数组中存储的是对象的引用，那么我们就称之为对象数组。
对象数组和基本类型数组在使用上几乎是相同的，唯一的区别就是对象数组保存的是对象的引用。

无论使用哪种类型的数组，数组标识符其实只是一个引用，表示堆中的一个真实对象的别名（\ 
**这部分有争议，需要修改**）。这个真实对象中保存了指向其他对象的引用。

C/C++ 无法返回整个数组，只能返回指向数组的指针，但这使数组的生命周期难以控制，容易内存泄漏。
而 Java 可以直接返回一个数组对象（也是一个引用），使用完成后垃圾回收器会自动清理。

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
            Integer[] a = new Integer[rand.nextInt(20)];    // a 是一个引用
            print("length of a = " + a.length);
            for(int i = 0; i < a.length; i++)
                a[i] = rand.nextInt(500);       // 自动包装，指的是基本类型自动转为包装类
            print(Arrays.toString(a));
        }
    } /* Output: (Sample)
    length of a = 18
    [55, 193, 361, 461, 429, 368, 200, 22, 207, 288, 128, 51, 89, 309, 278, 498, 361, 20]
    *///:~

创建基本类型的 **多维数组**，可以使用花括号将每个向量分隔开（每个向量的维度可以不相等）。

.. code-block:: java

    //: arrays/AutoboxingArrays.java
    import java.util.*;

    public class AutoboxingArrays {
        public static void main(String[] args) {
            Integer[][] a = { // Autoboxing:
                { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 },
                { 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 },
                { 51, 52, 53, 54, 55, 56, 57, 58, 59, 60 },
                { 71, 72, 73, 74, 75, 76, 77, 78, 79, 80 },
            };
            System.out.println(Arrays.deepToString(a));
        }
    } /* Output:
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 30], 
    [51, 52, 53, 54, 55, 56, 57, 58, 59, 60], 
    [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]]
    *///:~


.. _variable-argument-list:

可变参数列表
-------------

可变参数列表其实是一个数组，因此，可以用 ``foreach`` 来进行遍历，见如下代码。

.. code-block:: java
    :emphasize-lines: 5,6,19
    :linenos:

    //: initialization/NewVarArgs.java
    // Using array syntax to create variable argument lists.

    public class NewVarArgs {
        // static void printArray(Object[] args) {  // 老语法，main 函数就在使用
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

除此之外，可变参数列表支持自动包装机制（自动包装指的是基本类型自动转为包装类）。

但是，可变参数列表使重载变得更复杂了。
如果给定 ``f()``，编译器不知道该调用 ``f(Character... args)`` 还是 ``f(Integer... args)``。
这个问题可以通过添加非可变参数来解决 ``f(float i, Character... args)``。


数组的判空方法
--------------

一维数组： ``array.length == 0``

二维数组： ``array.length == 0 || array[0].length == 0``


数组复制和排序
--------------

复制数组： ``System.arraycopy()``。

数组的比较： ``Arrays.equals()``。

数组元素的比较，有两种方式：

1. 实现 ``java.lang.Comparable`` 接口。
2. 自建 ``Comparator`` 接口，并提供 ``compare()`` 和 ``equals()`` 方法声明。

数组排序，分情况讨论：

- 基本类型 ``Arrays.sort()`` 可以排序。
- 自定义类型需要实现 ``java.lang.Comparable`` 接口。

在已排序的数组中查找： ``Arrays.binarySearch()``。


数组与泛型
----------

通常，数组与泛型不能很好地结合，取而代之的是容器和泛型的结合。
如果你非要结合数组和泛型，也不是不可以，但不推荐使用，故本小节仅作为了解知识即可。

不能实例化具有参数化类型的数组。
因为编译器会进行 :ref:`erase-typeinfo`，而数组又必须知道它所持有的确切类型，以强制保证类型安全。
因此下述代码并不合法。

.. code-block:: java

    Peel<Banana>[] peels = new Peel<Banana>[10]; // Illegal



但是，你可以参数化数组本身的类型：

.. code-block:: java

    //: arrays/ParameterizedArrayType.java

    class ClassParameter<T> {
        public T[] f(T[] arg) { return arg; }
    }

    class MethodParameter {
        public static <T> T[] f(T[] arg) { return arg; }
    }

    public class ParameterizedArrayType {
        public static void main(String[] args) {
            Integer[] ints = { 1, 2, 3, 4, 5 };
            Double[] doubles = { 1.1, 2.2, 3.3, 4.4, 5.5 };
            Integer[] ints2 = new ClassParameter<Integer>().f(ints); // 参数化类须人为指定参数类型
            Double[] doubles2 = new ClassParameter<Double>().f(doubles);
            ints2 = MethodParameter.f(ints);            // 参数化方法会自动识别实参类型
            doubles2 = MethodParameter.f(doubles);
        }
    } ///:~

阅读上述代码可知，使用参数化方法比使用参数化类更加方便。

由于擦除的存在，我们将不能创建泛型数组。因为移除类型信息后，不能创建类型未知的数组。
但是，你可以创建 ``Object`` 数组，然后将其转型。

.. code-block:: java

    //: arrays/ArrayOfGenericType.java
    // Arrays of generic types won't compile.

    public class ArrayOfGenericType<T> {
        T[] array; // OK
        @SuppressWarnings("unchecked")
        public ArrayOfGenericType(int size) {
            //! array = new T[size]; // Illegal, unknown type
            array = (T[])new Object[size]; // "unchecked" Warning
        }
        // Illegal:
        //! public <U> U[] makeArray() { return new U[10]; }
    } ///:~

一般而言，泛型在类或方法的边界处很有效，而在类或方法的内部，擦除通常会使泛型变得不适用。
