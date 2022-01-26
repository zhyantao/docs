====
数组
====

容器和泛型对数组产生了极大的冲击，并且现在的容器在除了性能之外的各个方面都碾压数组。
通常，即使当你可以让泛型与数组以某种方式一起工作时，在编译器你最终也会得到"不受检查"的警告信息。

针对大多数场景，用的更多的是容器，而不是数组。除非你对性能有更高的要求。

关于数组的基本使用，在 :ref:`init-arrays` 一节中介绍了。


数组为什么特殊
--------------

在 Java 中，数组是一种效率最高的存储和随机访问对象引用序列的方式。数组就是一个简单的线性序列，这使得元素访问非常迅速。
但是，为这种速度所付出的代价是数组对象的大小被固定，并且在其生命周期中不可改变。

在泛型之前，其他的容器类在处理对象时，都将它们视作没有任何具体类型。
也就是说，它们将这些对象都当作 Object 来处理。

数组之所以优于容器，是因为你可以创建一个数组去持有某种具体类型，而容器不能。

容器不能持有某种类型，但是有了泛型的支持，容器就可以指定并检查它们所持有对象的类型，并且有了自动包装机制，容器看起来还能够持有基本类型。

.. code-block:: java

    //: arrays/ContainerComparison.java
    import java.util.*;
    import static net.mindview.util.Print.*;

    class BerylliumSphere {
        private static long counter;
        private final long id = counter++;
        public String toString() { return "Sphere " + id; }
    }

    public class ContainerComparison {
        public static void main(String[] args) {
            BerylliumSphere[] spheres = new BerylliumSphere[10];
            for(int i = 0; i < 5; i++)
                spheres[i] = new BerylliumSphere();
            print(Arrays.toString(spheres));
            print(spheres[4]);

            List<BerylliumSphere> sphereList =
                new ArrayList<BerylliumSphere>();
            for(int i = 0; i < 5; i++)
                sphereList.add(new BerylliumSphere());
            print(sphereList);
            print(sphereList.get(4));

            int[] integers = { 0, 1, 2, 3, 4, 5 };
            print(Arrays.toString(integers));
            print(integers[4]);

            List<Integer> intList = new ArrayList<Integer>(
                Arrays.asList(0, 1, 2, 3, 4, 5));
            intList.add(97);
            print(intList);
            print(intList.get(4));
        }
    } /* Output:
    [Sphere 0, Sphere 1, Sphere 2, Sphere 3, Sphere 4, null, null, null, null, null]
    Sphere 4
    [Sphere 5, Sphere 6, Sphere 7, Sphere 8, Sphere 9]
    Sphere 9
    [0, 1, 2, 3, 4, 5]
    4
    [0, 1, 2, 3, 4, 5, 97]
    4
    *///:~


数组是第一级对象
----------------

无论使用哪种类型的数组，数组标识符其实只是一个引用，指向堆中的一个真实对象，这个（数组）对象用以保存指向其他对象的引用。

对象数组和基本类型数组在使用上几乎是相同的，唯一的区别就是对象数组保存的是引用。


返回一个数组
------------

C/C++ 不能返回一个数组，只能返回指向数组的指针。这使得控制数组的生命周期变得困难，而且容易内存泄漏。

Java 可以直接返回一个数组（对象），使用完成后，垃圾回收器会清理。


多维数组
--------

创建基本类型的多维数组，可以使用花括号将每个向量分隔开。且每个向量的维度可以不相等。

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
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [51, 52, 53, 54, 55, 56, 57, 58, 59, 60], [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]]
    *///:~

也可以使用 new 来创建数组。


数组与泛型
-----------

通常，数组与泛型不能很好地结合。你不能实例化具有参数化类型的数组：

.. code-block:: java

    Peel<Banana>[] peels = new Peel<Banana>[10]; // Illegal

擦除会移除参数类型信息，而数组必须知道它们所持有的确切类型，以强制保证类型安全。

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
            Integer[] ints2 =
                new ClassParameter<Integer>().f(ints);
            Double[] doubles2 =
                new ClassParameter<Double>().f(doubles);
            ints2 = MethodParameter.f(ints);
            doubles2 = MethodParameter.f(doubles);
        }
    } ///:~

.. note:: 

    使用参数化方法比使用参数化类更加方便，因为你不必为每中不同的类型都使用一个参数去实例化这个类。

一般而言，泛型在类或方法的边界处很有效，而在类或方法的内部，擦除通常会使泛型变得不适用。例如，你不能创建泛型数组：

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

擦除成为障碍，因为移除类型信息后，不能创建类型未知的数组。但是，你可以创建 Object 数组，然后将其转型。


创建测试数据
------------


Arrays 实用功能
----------------

复制数组： ``System.arraycopy()`` 。

数组的比较： ``Arrays.equals()`` 。

数组元素的比较，有两种方式：

1. 实现 ``java.lang.Comparable`` 接口。
2. 自建 ``Comparator`` 接口，并提供 ``compare()`` 和 ``equals()`` 方法声明。

数组排序，分情况讨论：

- 基本类型 ``Arrays.sort()`` 可以排序。
- 自定义类型需要实现 ``java.lang.Comparable`` 接口。

在已排序的数组中查找： ``Arrays.binarySearch()`` 。
