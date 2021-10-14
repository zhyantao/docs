==============
持有对象：容器
==============

通常，程序总是根据运行时才知道的某些条件去创建新对象。编程时，你可以将任意数量的对象放置到容器中，并且不需要担心容器应该设置为多大。

.. uml::

    @startuml

    interface Collection
    interface List
    interface Set
    interface Queue
    interface Iterator
    interface ListIterator
    interface Map
    class HashMap
    class TreeMap
    class LinkedHashMap
    class ArrayList
    class LinkedList
    class HashSet
    class PriorityQueue
    class TreeMap
    class LinkedHashSet

    Iterator <|-- ListIterator

    Collection <|-- List
    Collection <|-- Set
    Collection <|-- Queue

    List <|.. ArrayList
    List <|.. LinkedList
    
    Set <|.. HashSet
    Set <|.. TreeSet
    HashSet <|-- LinkedHashSet

    Queue <|.. LinkedList
    Queue <|.. PriorityQueue

    Map <|.. HashMap
    Map <|.. TreeMap
    HashMap <|-- LinkedHashMap

    @enduml

泛型和类型安全的容器
--------------------

使用泛型时，容器知道它保存的是什么类型，在调用容器中对象中的方法时，会替你执行转型。另外，你可以将某个类型的子类保存到容器中。

基本概念
--------

Collection
    一个独立元素的序列，这些元素都服从一条或多条规则。 ``Colleciton`` 是描述所有序列容器的共性的根接口，实现 ``Colleciton`` 就要提供 ``iterator()`` 方法。
    所有的 ``Collection`` 都可以使用 ``foreach`` 语法，而且所有实现了 ``iterator()`` 方法的类都可以用于 ``foreach`` 语法。

Map
    - 一组成对的“键值对”对象，允许用一个对象查找另一个对象，也叫“映射表”、“关联数组”或“字典”。
    - ``HashMap`` ，使用了最快的查找技术，没有明显的顺序。
    - ``TreeMap`` ，按照比较结果升序保存键。
    - ``LinkedHashMap`` ，按照插入顺序保存键，同时保留了 ``HashMap`` 的查询速度。

List
    - ``ArrayList`` ，按照插入顺序保存元素。
    - ``LinkedList`` ，按照插入顺序保存元素。

Set
    - ``HashSet`` ，使用了最快的查找技术。
    - ``TreeSet`` ，按照比较结果升序保存对象。
    - ``LinkedHashSet`` ，按照插入顺序保存对象。

添加一组元素
------------

``Collection`` 的构造器可以接受另一个 ``Collection`` ，用它来将自身初始化。

``Colleciton.addAll()`` 比 ``Collections.allAll()`` 运行更快。

``Colleciton.allAll()`` 只能接受另一个 ``Collection`` 对象作为参数。不如 ``Collections.addAll()`` 和 ``Arrays.asList()`` 灵活。

``Map`` 只能用另一个 ``Map`` 初始化。

.. code-block:: java

    //: holding/AddingGroups.java
    // Adding groups of elements to Collection objects.
    import java.util.*;

    public class AddingGroups {
        public static void main(String[] args) {
            Collection<Integer> collection =
                new ArrayList<Integer>(Arrays.asList(1, 2, 3, 4, 5));
            Integer[] moreInts = { 6, 7, 8, 9, 10 };
            collection.addAll(Arrays.asList(moreInts));
            // Runs significantly faster, but you can't
            // construct a Collection this way:
            Collections.addAll(collection, 11, 12, 13, 14, 15);
            Collections.addAll(collection, moreInts);
            // Produces a list "backed by" an array:
            List<Integer> list = Arrays.asList(16, 17, 18, 19, 20);
            list.set(1, 99); // OK -- modify an element
            // list.add(21); // Runtime error because the
                             // underlying array cannot be resized.
        }
    } ///:~

容器的打印
----------

你必须使用 ``Arrays.toString()`` 来产生数组的可打印表示，但是打印容器无需任何帮助。容器会默认打印出容器中的内容。

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

List
-----

这里填充常用的函数和返回值。注意它们的参数和返回值。

迭代器
-------

迭代器是一个对象，它的工作是遍历并选择序列中的对象，而客户端程序员不必知道或关心该序列底层的结构。

使用方法：

1. ``iterator()`` 要求容器返回一个 ``Iterator`` 。 ``Iterator`` 将准备好返回序列的第一个元素。
2. 使用 ``next()`` 获得序列中的下一个元素。
3. 使用 ``hasNext()`` 检查序列中是否还有元素。
4. 使用 ``remove()`` 将迭代器新近返回的元素删除。

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

ListIterator
~~~~~~~~~~~~~

``ListIterator`` 是一个更加强大的 ``Iterator`` 的子类型，它只能用于各种 ``List`` 类的访问。

``Iterator`` 只能向前移动，但是 ``ListIterator`` 可以双向移动，并且可以使用 ``set()`` 方法替换它访问过的最后一个元素， ``listIterator(n)`` 方法可以返回索引为 n 的元素。

LinkedList
-----------

使用方法参考 `Java API Specification <https://docs.oracle.com/en/java/javase/11/docs/api/index.html>`_

``LinkedList`` 可以用于栈、队列或双端队列。

Stack
------

使用方法参考 `Java API Specification <https://docs.oracle.com/en/java/javase/11/docs/api/index.html>`_

可以直接将 ``LinkedList`` 用作栈，如下所示。但是如果你只需要栈的行为，这里使用继承就不合适了，因为这样会产生具有 ``LinkedList`` 的其他所有方法的类。

.. code-block:: java

    //: net/mindview/util/Stack.java
    // Making a stack from a LinkedList.
    package net.mindview.util;
    import java.util.LinkedList;

    public class Stack<T> {
        private LinkedList<T> storage = new LinkedList<T>();
        public void push(T v) { storage.addFirst(v); }
        public T peek() { return storage.getFirst(); }
        public T pop() { return storage.removeFirst(); }
        public boolean empty() { return storage.isEmpty(); }
        public String toString() { return storage.toString(); }
    } ///:~

.. note:: 

    泛型 ``<T>`` 告诉编译器这将是一个参数化类型，而其中的类型参数，即在类被使用时将会被实际类型替换。

Set
----

``Set`` 中最常被使用的是测试归属性（询问某个对象是否在 ``Set`` 中），使用 ``contains()`` 方法就可以。因此 ``HashSet`` 是最常用的实现方式。

``Set`` 具有与 ``Collection`` 完全一样的接口，因此没有任何额外的功能，实际上 ``Set`` 就是 ``Collection`` ，只是行为不同（这是继承与多态思想的典型应用）。

``TreeSet`` 将元素存储在红黑树数据结构中，而 ``HashSet`` 使用的是散列函数。

Map
----

使用方法参考 `Java API Specification <https://docs.oracle.com/en/java/javase/11/docs/api/index.html>`_

这是一种映射关系的实现，可以将一种对象映射为另一种对象。比如一个人可以拥有多个宠物，如下代码实现：

.. code-block:: java
    :emphasize-lines: 8, 9

    //: holding/MapOfList.java
    package holding;
    import typeinfo.pets.*;
    import java.util.*;
    import static net.mindview.util.Print.*;

    public class MapOfList {
        public static Map<Person, List<? extends Pet>>
            petPeople = new HashMap<Person, List<? extends Pet>>();
        static {
            petPeople.put(new Person("Dawn"),
                Arrays.asList(new Cymric("Molly"),new Mutt("Spot")));
            petPeople.put(new Person("Kate"),
                Arrays.asList(new Cat("Shackleton"),
                    new Cat("Elsie May"), new Dog("Margrett")));
            petPeople.put(new Person("Marilyn"),
                Arrays.asList(
                    new Pug("Louie aka Louis Snorkelstein Dupree"),
                    new Cat("Stanford aka Stinky el Negro"),
                    new Cat("Pinkola")));	
            petPeople.put(new Person("Luke"),
                Arrays.asList(new Rat("Fuzzy"), new Rat("Fizzy")));
            petPeople.put(new Person("Isaac"),
                Arrays.asList(new Rat("Freckly")));
        }
        public static void main(String[] args) {
            print("People: " + petPeople.keySet());
            print("Pets: " + petPeople.values());
            for(Person person : petPeople.keySet()) {
                print(person + " has:");
                for(Pet pet : petPeople.get(person))
                    print("        " + pet);
            }
        }
    } /* Output:	
    People: [Person Luke, Person Marilyn, Person Isaac, Person Dawn, Person Kate]
    Pets: [[Rat Fuzzy, Rat Fizzy], [Pug Louie aka Louis Snorkelstein Dupree, Cat Stanford aka Stinky el Negro, Cat Pinkola], [Rat Freckly], [Cymric Molly, Mutt Spot], [Cat Shackleton, Cat Elsie May, Dog Margrett]]
    Person Luke has:
            Rat Fuzzy
            Rat Fizzy
    Person Marilyn has:
            Pug Louie aka Louis Snorkelstein Dupree
            Cat Stanford aka Stinky el Negro
            Cat Pinkola
    Person Isaac has:
            Rat Freckly
    Person Dawn has:
            Cymric Molly
            Mutt Spot
    Person Kate has:
            Cat Shackleton
            Cat Elsie May
            Dog Margrett
    *///:~


Queue
------

使用方法参考 `Java API Specification <https://docs.oracle.com/en/java/javase/11/docs/api/index.html>`_

队列常被当作一种可靠的将对象从程序的某个区域传输到另一个区域的途径。队列在并发编程中特别重要。

PriorityQueue
~~~~~~~~~~~~~~

使用方法参考 `Java API Specification <https://docs.oracle.com/en/java/javase/11/docs/api/index.html>`_

优先级队列声明下一个弹出元素是最需要的元素（具有最高的优先级）。当你在 ``PriorityQueue`` 上调用 ``offer()``
方法来插入一个对象时，这个对象会在队列中被排序。默认的排序将使用对象在队列中的自然顺序，但是你可以提供自己的
``Comparator`` 来修改这个顺序。

.. code-block:: java

    //: holding/PriorityQueueDemo.java
    import java.util.*;

    public class PriorityQueueDemo {
        public static void main(String[] args) {
            PriorityQueue<Integer> priorityQueue = new PriorityQueue<Integer>();
            Random rand = new Random(47);
            for(int i = 0; i < 10; i++)
                priorityQueue.offer(rand.nextInt(i + 10));
            QueueDemo.printQ(priorityQueue);
            List<Integer> ints = Arrays.asList(25, 22, 20, 18, 14, 9, 3, 1, 1, 2, 3, 9, 14, 18, 21, 23, 25);
            priorityQueue = new PriorityQueue<Integer>(ints);
            QueueDemo.printQ(priorityQueue);
            
            priorityQueue = new PriorityQueue<Integer>(ints.size(), Collections.reverseOrder());
            priorityQueue.addAll(ints);
            QueueDemo.printQ(priorityQueue);

            String fact = "EDUCATION SHOULD ESCHEW OBFUSCATION";
            List<String> strings = Arrays.asList(fact.split(""));
            PriorityQueue<String> stringPQ = new PriorityQueue<String>(strings);
            QueueDemo.printQ(stringPQ);
            
            stringPQ = new PriorityQueue<String>(strings.size(), Collections.reverseOrder());
            stringPQ.addAll(strings);
            QueueDemo.printQ(stringPQ);

            Set<Character> charSet = new HashSet<Character>();
            for(char c : fact.toCharArray())
                charSet.add(c); // Autoboxing
            PriorityQueue<Character> characterPQ = new PriorityQueue<Character>(charSet);
            QueueDemo.printQ(characterPQ);
        }
    } /* Output:
    0 1 1 1 1 1 3 5 8 14
    1 1 2 3 3 9 9 14 14 18 18 20 21 22 23 25 25
    25 25 23 22 21 20 18 18 14 14 9 9 3 3 2 1 1
                A A B C C C D D E E E F H H I I L N N O O O O S S S T T U U U W
    W U U U T T S S S O O O O N N L I I H H F E E E D D C C C B A A
        A B C D E F H I L N O S T U W
    *///:~

.. note:: 

    上述例子中， ``Iteger`` 、 ``String`` 和 ``Character`` 可以与 ``PriorityQueue`` 一起工作，因为这些类已经内建了自然排序。所以没有提供 ``Comparator`` 。

foreach 与迭代器
~~~~~~~~~~~~~~~~

不存在从数组到 ``Iterator`` 的自动转换，你必须手动执行这种转换。

.. code-block:: java

    //: holding/ArrayIsNotIterable.java
    import java.util.*;

    public class ArrayIsNotIterable {
        static <T> void test(Iterable<T> ib) {
            for(T t : ib)
                System.out.print(t + " ");
        }
        public static void main(String[] args) {
            test(Arrays.asList(1, 2, 3));
            String[] strings = { "A", "B", "C" };
            // An array works in foreach, but it's not Iterable:
            //! test(strings);
            // You must explicitly convert it to an Iterable:
            test(Arrays.asList(strings));
        }
    } /* Output:
    1 2 3 A B C
    *///:~

适配器方法惯用法
~~~~~~~~~~~~~~~~

如果现有一个 ``Iterable`` 类，你想要添加一种或多种在 ``foreach`` 语句中使用这个类的方法，应该怎么做呢？例如，假设你希望可以选择以向前或向后的方向迭代一个单词列表。如果直接继承这个类，并覆盖 ``iterator()`` 方法，你只能替换现有的方法，而不能实现选择。

一种解决方案是适配器方法，当你有一个接口并需要另一个接口时，编写适配器就可以解决问题。

.. code-block:: java

    //: holding/AdapterMethodIdiom.java
    // The "Adapter Method" idiom allows you to use foreach
    // with additional kinds of Iterables.
    import java.util.*;

    class ReversibleArrayList<T> extends ArrayList<T> {
        public ReversibleArrayList(Collection<T> c) { super(c); }
        public Iterable<T> reversed() {
            return new Iterable<T>() {
                public Iterator<T> iterator() {
                    return new Iterator<T>() {
                        int current = size() - 1;
                        public boolean hasNext() { return current > -1; }
                        public T next() { return get(current--); }
                        public void remove() { // Not implemented
                            throw new UnsupportedOperationException();
                        }
                    };
                }
            };
        }
    }	

    public class AdapterMethodIdiom {
        public static void main(String[] args) {
            ReversibleArrayList<String> ral =
                new ReversibleArrayList<String>(
                    Arrays.asList("To be or not to be".split(" ")));
            // Grabs the ordinary iterator via iterator():
            for(String s : ral)
                System.out.print(s + " ");
            System.out.println();
            // Hand it the Iterable of your choice
            for(String s : ral.reversed())
                System.out.print(s + " ");
        }
    } /* Output:
    To be or not to be
    be to not or be To
    *///:~
