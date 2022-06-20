====
容器
====

通常，程序总是根据运行时才知道的某些条件去创建新对象。
编程时，你可以将任意数量的对象放置到容器中，并且不需要担心容器应该设置为多大。

容器经常和泛型搭配使用。
使用泛型时，容器知道它保存的是什么类型，在调用容器中对象中的方法时，会替你执行转型。
另外，你可以将某个类型的子类保存到容器中。

Java 容器分为 Collection 和 Map 两大类，其下又有很多子类。

Colleciton
-----------

``Colleciton`` 是描述所有序列容器的共性的根接口，实现 ``Colleciton`` 就要提供 ``iterator()`` 方法。
所有的 ``Collection`` 都可以使用 ``foreach`` 语法，而且所有实现了 ``iterator()`` 方法的类都可以用于
``foreach`` 语法。

.. margin::
    
    - 实线为继承（extends）
    - 虚线为实现（implements）

.. uml::

    @startuml

    interface Collection
    interface List
    interface Set
    interface Queue
    abstract AbstractList
    class AbstracSequentialtList
    abstract AbstractSet
    abstract SortedSet
    interface Iterator
    interface ListIterator

    Iterator <|-- ListIterator

    Collection <|-- List
    Collection <|-- Set
    Collection <|-- Queue
    Collection <|.. AbstractCollection
    
    AbstractCollection <|-- AbstractList
    List <|.. AbstractList
    AbstractCollection <|-- AbstractSet

    AbstractList <|-- ArrayList
    AbstractList <|-- Vector
    AbstractList <|-- AbstracSequentialtList

    AbstracSequentialtList <|-- LinkedList

    Vector <|-- Stack

    Set <|-- AbstractSet
    Set <|-- SortedSet
    SortedSet <|.. TreeSet
    AbstractSet <|.. HashSet
    AbstractSet <|.. TreeSet
    HashSet <|-- LinkedHashSet

    Queue <|.. LinkedList
    Queue <|.. PriorityQueue

    @enduml


.. uml::

    package java.util <<Folder>> {
        class Collections
        class Arrays
    }

List 和 Set
~~~~~~~~~~~~~

``List`` 和 ``Set`` 都继承了 ``Colleciton`` 接口。都是用来存储一组同一类型的元素的。

不同的是， ``List`` 中的元素有序、可重复，而 ``Set`` 中的元素无序、不可重复。

``Set`` 中最常被使用的是测试归属性（询问某个对象是否在 ``Set`` 中），使用 ``contains()``
方法就可以。因此 ``HashSet`` 是最常用的实现方式。

``Set`` 具有与 ``Collection`` 完全一样的接口，因此没有任何额外的功能，实际上 ``Set`` 就是
``Collection``，只是行为不同（这是继承与多态思想的典型应用）。

``TreeSet`` 将元素存储在红黑树数据结构中，而 ``HashSet`` 使用的是散列函数。

ArrayList、LinkedList 和 Vector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``List`` 主要有 ``ArrayList`` 、 ``LinkedList`` 与 ``Vector`` 几种实现。
它们的使用方式也很相似，主要区别在于因为实现方式的不同，所以对不同的操作具有不同的效率。

``ArrayList`` 是一个可改变大小的数组。当更多的元素加入到 ``ArrayList`` 中时，其大小将会动态地增长。
内部的元素可以直接通过 get 与 set 方法进行访问，因为 ``ArrayList`` 本质上就是 一个数组。

``LinkedList`` 是一个双链表，在添加和删除元素时具有比 ``ArrayList`` 更好的性能。
但在 ``get`` 与 ``set`` 方面弱于 ``ArrayList``。
当然，这些对比都是指数据量很大或者操作很频繁的情况下的对比，如果数据和运算量很小，那么对比将失去意义。

``Vector`` 和 ``ArrayList`` 类似，但属于强同步类。
如果你的程序本身是线程安全的（没有在多个线程之间共享同一个集合/对象）那么使用 ``ArrayList``
是更好的选择。

``Vector`` 和 ``ArrayList`` 在更多元素添加进来时会请求更大的空间。
``Vector`` 每次请求其大小的双倍空间，而 ``ArrayList`` 每次对 ``size`` 增长 50%。

而 ``LinkedList`` 还实现了 ``Queue`` 接口，该接口比 ``List`` 提供了更多的方法，包括 ``offer()``，
``peek()``， ``poll()`` 等。

注意：默认情况下 ``ArrayList`` 的初始容量非常小，所以如果可以预估数据量的话，
分配一个较大的初始值属于最佳实践。这样可以减少调整大小的开销。

HashSet 和 TreeSet
~~~~~~~~~~~~~~~~~~~

``TreeSet`` 是二叉树实现的， ``TreeSet`` 中的数据是自动排好序的，不允许放入 ``null`` 值。

``HashSet`` 是哈希表实现的， ``HashSet`` 中的数据是无序的，可以放入 ``null``，但只能放入一个 ``null``，
两者中的值都不能重复，就如数据库中唯一约束。

在 ``HashSet`` 中，基本的操作都是由 ``HashMap`` 底层实现的，因为 ``HashSet`` 底层是用 ``HashMap`` 存储数据的。
当向 ``HashSet`` 中添加元素的时候，首先计算元素的 ``hashcode`` 值，
然后通过扰动计算和按位与的方式计算出这个元素的存储位置，如果这个位置位空，就将元素添加进去；
如果不为空，则用 ``equals`` 方法比较元素是否相等，相等就不添加，否则找一个空位添加。

``TreeSet`` 的底层是 ``TreeMap`` 的 ``keySet()``，而 ``TreeMap`` 是基于红黑树实现的，红黑树是一种平衡二叉查找树，
它能保证任何一个节点的左右子树的高度差不会超过较矮的那棵的一倍。

``TreeMap`` 是按 ``key`` 排序的，元素在插入 ``TreeSet`` 时 ``compareTo()`` 方法要被调用，所以
``TreeSet`` 中的元素要实现 ``Comparable`` 接口。 ``TreeSet`` 作为一种 ``Set``，它不允许出 现重复元素。
``TreeSet`` 是用 ``compareTo()`` 来判断重复元素的。


Map
----

``Map`` 是一组成对的 "键值对" 对象，允许用一个对象查找另一个对象，也叫 "映射表"、"关联数组" 或 "字典"。

- ``HashMap``，使用了最快的查找技术，没有明显的顺序。
- ``TreeMap``，按照比较结果升序保存键。
- ``LinkedHashMap``，按照插入顺序保存键，同时保留了 ``HashMap`` 的查询速度。

``Map`` 类为 ``Colleciton`` 类的底层实现提供了支持，比如 ``HashSet`` 基于 ``HashMap`` 实现，
``TreeSet`` 基于 ``TreeMap`` 实现。

.. margin::
    
    - 实线为继承（extends）
    - 虚线为实现（implements）

.. uml::

    @startuml

    interface Map
    abstract AbstractMap
    interface SortedMap

    Map <|-- AbstractMap
    Map <|-- SortedMap

    AbstractMap <|.. HashMap
    AbstractMap <|.. TreeMap
    AbstractMap <|.. IdentityHashMap
    AbstractMap <|.. WeakHashMap
    AbstractMap <|.. HashTable
    SortedMap <|.. TreeMap
    HashMap <|-- LinkedHashMap

    @enduml


容器的初始化
------------

.. code-block:: java

    //: holding/AddingGroups.java
    // Adding groups of elements to Collection objects.
    import java.util.*;

    public class AddingGroups {
        public static void main(String[] args) {
            Collection<Integer> collection = new ArrayList<Integer>(Arrays.asList(1, 2, 3, 4, 5));
            Integer[] moreInts = { 6, 7, 8, 9, 10 };
            collection.addAll(Arrays.asList(moreInts));

            // Runs significantly faster, but you can't construct a Collection this way:
            Collections.addAll(collection, 11, 12, 13, 14, 15);
            Collections.addAll(collection, moreInts);

            // Produces a list "backed by" an array:
            List<Integer> list = Arrays.asList(16, 17, 18, 19, 20);
            list.set(1, 99); // OK -- modify an element
            // list.add(21); // Runtime error because the underlying array cannot be resized.
        }
    } ///:~

``java.util.Collection`` 是一个集合接口。它提供了对集合对象进行基本操作的通用接口方法。
``Collection`` 接口在 Java 类库中有很多具体的实现。
``Collection`` 接口的意义是为各种具体的集合提供了最大化的统一操作方式。

``java.util.Collections`` 是一个包装类。它包含有各种有关集合操作的静态多态方法。
此类 **不能实例化**，就像一 **个工具类**，服务于 Java 的 Collection 框架。

``java.lang.Array`` 是 Java 中 **最基本的一个存储结构**。提供了动态创建和访问 Java **数组** 的方法。
其中的元素的类型必须相同。效率高，但容量固定且无法动态改变。
它无法判断其中实际存有多少元素， ``length`` 只是告诉我们 array 的容量。

``java.util.Arrays`` 静态类专门用来操作 array，提供搜索、排序、复制等静态方法。

- ``equals()`` ：比较两个 array 是否相等。array 拥有相同元素个数，且所有对应元素两两相等。
- ``sort()`` ：用来对 array 进行排序。
- ``binarySearch()`` ：在排好序的 array 中寻找元素。
- ``asList()`` ：传入一个参数 array，将其转化为 ``List``

``Colleciton.addAll()`` 比 ``Collections.allAll()`` 运行更快，但不如 ``Collections.addAll()``
和 ``Arrays.asList()`` 灵活。 ``Colleciton.allAll()`` 只能接受另一个 ``Collection`` 对象作为参数。

容器的打印
----------

打印容器可以使用数组工具类 ``Arrays.toString()`` 方法，它默认打印出容器中的内容。

.. code-block:: java

    //: holding/PrintingContainers.java
    // Containers print themselves automatically.
    import java.util.*;
    import static net.mindview.util.Print.*;

    public class PrintingContainers {
        static Collection fill(Collection<String> collection) {
            collection.add("rat");
            collection.add("cat");
            collection.add("dog");
            collection.add("dog");
            return collection;
        }
        static Map fill(Map<String,String> map) {
            map.put("rat", "Fuzzy");
            map.put("cat", "Rags");
            map.put("dog", "Bosco");
            map.put("dog", "Spot");
            return map;
        }
        public static void main(String[] args) {
            print(fill(new ArrayList<String>()));
            print(fill(new LinkedList<String>()));
            print(fill(new HashSet<String>()));
            print(fill(new TreeSet<String>()));
            print(fill(new LinkedHashSet<String>()));
            print(fill(new HashMap<String,String>()));
            print(fill(new TreeMap<String,String>()));
            print(fill(new LinkedHashMap<String,String>()));
        }
    } /* Output:
    [rat, cat, dog, dog]
    [rat, cat, dog, dog]
    [dog, cat, rat]
    [cat, dog, rat]
    [rat, cat, dog]
    {dog=Spot, cat=Rags, rat=Fuzzy}
    {cat=Rags, dog=Spot, rat=Fuzzy}
    {rat=Fuzzy, cat=Rags, dog=Spot}
    *///:~

容器的遍历
----------

遍历容器，我们通常用迭代器，它是一个对象。

要使用迭代器，首先用 ``容器名.iterator()`` 方法生成一个迭代器对象。迭代器对象有几个方法：

- ``hasNext()`` 判断是否有下一个元素；
- ``next()`` 获取下一个元素；
- ``remove()`` 删除当前指向的元素。

.. code-block:: java

    //: holding/SimpleIteration.java
    import typeinfo.pets.*;
    import java.util.*;

    public class SimpleIteration {
        public static void main(String[] args) {
            List<Pet> pets = Pets.arrayList(12);
            Iterator<Pet> it = pets.iterator();
            while(it.hasNext()) {
                Pet p = it.next();
                System.out.print(p.id() + ":" + p + " ");
            }
            System.out.println();
            // A simpler approach, when possible:
            for(Pet p : pets)
                System.out.print(p.id() + ":" + p + " ");
            System.out.println();
            // An Iterator can also remove elements:
            it = pets.iterator();
            for(int i = 0; i < 6; i++) {
                it.next();
                it.remove();
            }
            System.out.println(pets);
        }
    } /* Output:
    0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx 8:Cymric 9:Rat 10:EgyptianMau 11:Hamster
    0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx 8:Cymric 9:Rat 10:EgyptianMau 11:Hamster
    [Pug, Manx, Cymric, Rat, EgyptianMau, Hamster]
    *///:~

``ListIterator`` 是一个更加强大的 ``Iterator`` 的子类型，它只能用于各种 ``List`` 类的访问。

``Iterator`` 只能向前移动，但是 ``ListIterator`` 可以双向移动，并且可以使用 ``set()``
方法替换它指向的元素， ``listIterator(n)`` 方法可以返回索引为 n 的元素。

常用方法
--------

.. list-table::
    :header-rows: 1

    * - 
      - 增
      - 删
      - 查
      - 改
      - 判空
      - 判等
      - 大小
      - 截取
      - 拼接
    * - int[]
      - 
      - 
      - arr[i]
      - arr[i]=23
      - arr == null || arr.length == 0
      - 
      - arr.length
      - Arrays.copyOfRange(arr, 2, 6)
      - 
    * - String
      - sb.append(), sb.insert()
      - sb.deleteCharAt(), sb.delete(i,j)
      - str.ChatAt()
      - str.setCharAt()
      - str == null || str.isEmpty()
      - str.equals(str2)
      - str.length()
      - str.substring(i), str.substring(i, j)
      - str.concat("abc")
    * - ArrayList
      - list.add()
      - list.remove()
      - list.get()
      - list.set(1, 100)
      - list.isEmpty()
      - 
      - list.size()
      - 
      - 
    * - LinkedList
      - list.add(), list.addFirst()
      - list.remove(), list.removeLast()
      - list.get()
      - 
      - list.isEmpty()
      - 
      - list.size()
      - 
      - 
    * - HashMap
      - map.put()
      - map.remove()
      - map.get(), map.getOrSetDefault(), map.containsKey()
      - map.keySet()
      - 
      - 
      - 
      - 
      - 
    * - HashSet
      - set.add()
      - set.remove()
      - set.contains()
      - 
      - 
      - 
      - 
      - 
      - 
    * - Queue
      - queue.offer()
      - queue.poll()
      - queue.peek()
      - 
      - queue.isEmpty()
      - 
      - queue.size()
      - 
      - 
    * - Deque
      - deque.offer(), deque.offerFirst(), deque.offerLast()
      - deque.poll(), deque.pollFirst(), deque.pollLast()
      - 
      - 
      - deque.isEmpty()
      - 
      - deque.size()
      - 
      - 
    * - Stack
      - stack.push()
      - stack.pop()
      - stack.peek()
      - 
      - stack.isEmpty()
      - 
      - stack.size()
      - 
      - 
