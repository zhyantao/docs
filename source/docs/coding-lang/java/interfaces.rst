======
接口
======

接口和内部类为我们提供了一种将接口与实现分离的更加结构化的方法。

使用接口的原因：

- 核心原因：为了能够向上转型为多个基类型（以及由此带来的灵活性）
- 防止客户端程序员创建该类的对象（与抽象基类的目的相同）

事实上，如果知道某个事物应该成为一个基类，那么第一选择应该是使它成为一个接口。

任何抽象性都应该是应真正的需求而产生的。当必需时，你应该重构接口而不是到处添加额外级别的间接性，并由此带来的额外的复杂性。

恰当的原则应该是优先选择类而不是接口。从类开始，如果接口的必需性变得非常明确，那么就进行重构。

.. note:: 接口是一种重要的工具，但是它们容易被滥用。

抽象类和抽象方法
----------------

使用抽象类是希望：

- 创建具有某些未实现方法的类
- 建立通用接口

我们创建抽象类是希望通过这个通用接口操纵一系列类。

抽象方法仅有声明，没有方法体，如 ``abstract void f();`` 。包含抽象方法的类必须限定为抽象类，如 ``abstract class ClassName {}`` 。

如果从一个抽象类继承，并想创建该新类的对象，那么就必须为基类中的所有抽象方法提供方法定义。如果不这样做（可以选择不做），那么导出类便也是抽象类，且编译器将会强制我们使用 ``abstract`` 关键字来限定这个类。

接口
----

抽象方法可以提供接口，抽象方法所属的类是 **部分抽象** 的类（因为抽象类中可以有某些方法的实现）。但是 ``interface`` 关键字可以产生一个 **完全抽象** 的类，如 ``interface ClassName {}`` 。

接口被用来建立类与类之间的 **协议** 。

要让某个类遵循某个特定接口（或者一组接口），需要使用 ``implements`` 关键字。

.. note:: 

    - 可以在 ``interface`` 前添加 ``public`` 关键字，如果不添加 ``public`` 关键字，则只有包访问权限。
    - 接口中的方法隐式地是 ``public`` 的。
    - 接口中的属性隐式地是 ``static`` 和 ``final`` 的（也可以不包含属性字段）。

完全解耦
--------

使用方法操作继承而来的对象时，我们只能操作父类或子类，而无法操作在继承结构之外的类。接口让我们在编写代码时可以脱离这种由于继承结构带来的束缚。语言的描述有些抽象，我们通过下例来进一步理解：

使用继承无法完全解耦
~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    classDiagram
        Processor <|-- Upcase : extends
        Processor <|-- Downcase : extends
        Processor <|-- Splitter : extends
        Processor : String name()
        Processor : Object process()
        Upcase : String process()
        Downcase : String process()
        Splitter : String process()

        class Waveform
        Waveform : long counter
        Waveform : long id
        Waveform : String toString()

        Filter <|-- LowPass : extends
        Filter <|-- HighPass : extends
        Filter <|-- BandPass : extends
        Filter : String name()
        Filter : Waveform process()
        LowPass : Waveform process()
        HighPass : Waveform process()
        BandPass : Waveform process()

        class Apply
        Apply : void process(Processor p, Object s)

**代码段一**

.. code-block:: java
    :emphasize-lines: 33

    //: interfaces/classprocessor/Apply.java
    package interfaces.classprocessor;
    import java.util.*;
    import static net.mindview.util.Print.*;

    class Processor {
        public String name() {
            return getClass().getSimpleName();
        }
        Object process(Object input) { return input; }
    }	

    class Upcase extends Processor {
        String process(Object input) { // Covariant return
            return ((String)input).toUpperCase();
        }
    }

    class Downcase extends Processor {
        String process(Object input) {
            return ((String)input).toLowerCase();
        }
    }

    class Splitter extends Processor {
        String process(Object input) {
            // The split() argument divides a String into pieces:
            return Arrays.toString(((String)input).split(" "));
        }
    }	

    public class Apply {
        public static void process(Processor p, Object s) {
            print("Using Processor " + p.name());
            print(p.process(s));
        }
        public static String s =
            "Disagreement with beliefs is by definition incorrect";
        public static void main(String[] args) {
            process(new Upcase(), s);
            process(new Downcase(), s);
            process(new Splitter(), s);
        }
    } /* Output:
    Using Processor Upcase
    DISAGREEMENT WITH BELIEFS IS BY DEFINITION INCORRECT
    Using Processor Downcase
    disagreement with beliefs is by definition incorrect
    Using Processor Splitter
    [Disagreement, with, beliefs, is, by, definition, incorrect]
    *///:~

**代码段二**

.. code-block:: java

    //: interfaces/filters/Waveform.java
    package interfaces.filters;

    public class Waveform {
        private static long counter;
        private final long id = counter++;
        public String toString() { return "Waveform " + id; }
    } ///:~

    //: interfaces/filters/Filter.java
    package interfaces.filters;

    public class Filter {
        public String name() {
            return getClass().getSimpleName();
        }
        public Waveform process(Waveform input) { return input; }
    } ///:~

    //: interfaces/filters/LowPass.java
    package interfaces.filters;

    public class LowPass extends Filter {
        double cutoff;
        public LowPass(double cutoff) { this.cutoff = cutoff; }
        public Waveform process(Waveform input) {
            return input; // Dummy processing
        }
    } ///:~

    //: interfaces/filters/HighPass.java
    package interfaces.filters;

    public class HighPass extends Filter {
        double cutoff;
        public HighPass(double cutoff) { this.cutoff = cutoff; }
        public Waveform process(Waveform input) { return input; }
    } ///:~

    //: interfaces/filters/BandPass.java
    package interfaces.filters;

    public class BandPass extends Filter {
        double lowCutoff, highCutoff;
        public BandPass(double lowCut, double highCut) {
            lowCutoff = lowCut;
            highCutoff = highCut;
        }
        public Waveform process(Waveform input) { return input; }
    } ///:~

``Filter`` 与 ``Processor`` 具有相同的接口元素 ``process()`` ，但是因为 ``Filter`` 并非继承自 ``Processor`` ，因此不能将 ``Filter`` 用于 ``Apply.process()`` 方法，即便这样做可以正常运行。这里主要是因为 ``Apply.process()`` 方法和 ``Processor`` 之间的 **耦合过紧** ，于是将其应用于 ``Filter`` 时，复用被禁止了。

但是，如果 ``Processor`` 是一个接口（之前是一个普通的类），这些限制就会变得松动，就可以实现复用了。

使用接口实现完全解耦
~~~~~~~~~~~~~~~~~~~~

.. mermaid::

    classDiagram
        class Processor
        Processor <|-- StringProcessor : implements
        Processor <|-- FilterAdapter : implements
        <<interface>> Processor
        <<abstract>> StringProcessor
        Processor : Object process(Processor p, Object s)
        FilterAdapter : Waveform process()
        
        class StringProcessor
        <<abstract>> StringProcessor
        StringProcessor : abstract String process()
        StringProcessor <|-- Upcase : extends
        StringProcessor <|-- Downcase : extends
        StringProcessor <|-- Splitter : extends
        Upcase : String  process()
        Downcase : String  process()
        Splitter : String  process()

修改后的代码结构，既可以让 ``Processor`` 应用于 ``StringProcessor`` 也可以应用于 ``FilterAdapter`` ，而后者，是继承无法办到的。这实现了 ``Processor.process()`` 与 ``StringProcessor.process()`` 的解耦。具体实现代码如下：

**代码段三**

.. code-block:: java

    //: interfaces/interfaceprocessor/Processor.java
    package interfaces.interfaceprocessor;

    public interface Processor {
        String name();
        Object process(Object input);
    } ///:~

**代码段四**

.. code-block:: java

    //: interfaces/interfaceprocessor/Apply.java
    package interfaces.interfaceprocessor;
    import static net.mindview.util.Print.*;

    public class Apply {
        public static void process(Processor p, Object s) {
            print("Using Processor " + p.name());
            print(p.process(s));
        }
    } ///:~

**代码段五**

.. code-block:: java

    //: interfaces/interfaceprocessor/StringProcessor.java
    package interfaces.interfaceprocessor;
    import java.util.*;

    public abstract class StringProcessor implements Processor{
        public String name() {
            return getClass().getSimpleName();
        }
        public abstract String process(Object input);
        public static String s =
            "If she weighs the same as a duck, she's made of wood";
        public static void main(String[] args) {
            Apply.process(new Upcase(), s);
            Apply.process(new Downcase(), s);
            Apply.process(new Splitter(), s);
        }
    }	

    class Upcase extends StringProcessor {
        public String process(Object input) { // Covariant return
            return ((String)input).toUpperCase();
        }
    }

    class Downcase extends StringProcessor {
        public String process(Object input) {
            return ((String)input).toLowerCase();
        }
    }

    class Splitter extends StringProcessor {
        public String process(Object input) {
            return Arrays.toString(((String)input).split(" "));
        }	
    } /* Output:
    Using Processor Upcase
    IF SHE WEIGHS THE SAME AS A DUCK, SHE'S MADE OF WOOD
    Using Processor Downcase
    if she weighs the same as a duck, she's made of wood
    Using Processor Splitter
    [If, she, weighs, the, same, as, a, duck,, she's, made, of, wood]
    *///:~

**代码段六**

.. code-block:: java
    :emphasize-lines: 7, 12

    //: interfaces/interfaceprocessor/FilterProcessor.java
    package interfaces.interfaceprocessor;
    import interfaces.filters.*;

    class FilterAdapter implements Processor {
        Filter filter;
        public FilterAdapter(Filter filter) {
            this.filter = filter;
        }
        public String name() { return filter.name(); }
        public Waveform process(Object input) {
            return filter.process((Waveform)input);
        }
    }	

    public class FilterProcessor {
        public static void main(String[] args) {
            Waveform w = new Waveform();
            Apply.process(new FilterAdapter(new LowPass(1.0)), w);
            Apply.process(new FilterAdapter(new HighPass(2.0)), w);
            Apply.process(
                new FilterAdapter(new BandPass(3.0, 4.0)), w);
        }
    } /* Output:
    Using Processor LowPass
    Waveform 0
    Using Processor HighPass
    Waveform 0
    Using Processor BandPass
    Waveform 0
    *///:~

代码段六实现了 **适配器模式** ，适配器模式的出现是因为无法修改旧接口，而且旧接口无法与满足新业务的接口需求，这时候需要使用适配器来在旧接口的基础上稍作修改，满足新业务。
        
在适配器方式中， ``FilterAdapter`` 的构造器接受你已经拥有的接口 ``Filter`` ，然后生成具有你所需要的 ``Processor`` 接口的对象。

Java 中的多重继承
-----------------

Java 中的多重继承由接口实现。组合多个类的接口的行为被称为多重继承。

一个类在只能继承一个类的同时可以继承多个接口，并可以向上转型为每个接口，因为每个接口都是一个独立类型。具体类必须放在最前面，后面跟着的是接口。

通过继承来扩展接口
------------------

接口可以继承接口。

组合接口时的名字冲突
~~~~~~~~~~~~~~~~~~~~

尽量避免。

适配接口
--------

在下例中， ``Scanner`` 类的构造器接受一个 ``Readable`` 接口。 ``Readable`` 是专门为 ``Scanner`` 类设计的接口。 ``Scanner`` 不必将参数限定为某个特定类，只要某个类实现了 ``Readable`` 接口就可以作为 ``Scanner`` 的参数，这就很好地体现了可扩展性和完全解耦。

.. code-block:: java
    :emphasize-lines: 6, 13, 25

    //: interfaces/RandomWords.java
    // Implementing an interface to conform to a method.
    import java.nio.*;
    import java.util.*;

    public class RandomWords implements Readable {
        private static Random rand = new Random(47);
        private static final char[] capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".toCharArray();
        private static final char[] lowers = "abcdefghijklmnopqrstuvwxyz".toCharArray();
        private static final char[] vowels = "aeiou".toCharArray();
        private int count;
        public RandomWords(int count) { this.count = count; }	
        public int read(CharBuffer cb) {
            if(count-- == 0)
                return -1; // Indicates end of input
            cb.append(capitals[rand.nextInt(capitals.length)]);
            for(int i = 0; i < 4; i++) {
                cb.append(vowels[rand.nextInt(vowels.length)]);
                cb.append(lowers[rand.nextInt(lowers.length)]);
            }
            cb.append(" ");
            return 10; // Number of characters appended
        }
        public static void main(String[] args) {
            Scanner s = new Scanner(new RandomWords(10));
            while(s.hasNext())
                System.out.println(s.next());
        }
    } /* Output:
    Yazeruyac
    Fowenucor
    Goeazimom
    Raeuuacio
    Nuoadesiw
    Hageaikux
    Ruqicibui
    Numasetih
    Kuuuuozog
    Waqizeyoy
    *///:~

.. note:: 

    实现 ``Readable`` 接口需要重写 ``read()`` 方法。

接口中的域
----------

接口中的域默认是 ``static final`` 和 ``public`` 的，可以很方便地用来创建常量组（Java SE5 之前与 ``enum`` 有相同效果）。他们的值被存储在该接口的静态存储区内。

.. note:: 有了 enum 类型，使用接口来群组常量就没多大作用了。

.. code-block:: java

    //: interfaces/Months.java
    // Using interfaces to create groups of constants.
    package interfaces;

    public interface Months {
        int
            JANUARY = 1, FEBRUARY = 2, MARCH = 3,
            APRIL = 4, MAY = 5, JUNE = 6, JULY = 7,
            AUGUST = 8, SEPTEMBER = 9, OCTOBER = 10,
            NOVEMBER = 11, DECEMBER = 12;
    } ///:~

嵌套接口
--------

接口可以嵌套在类或其他接口中。需要注意的是，当实现某个接口时，不需要实现嵌套在其内部的任何接口，而且， ``private`` 接口不能在定义它的类之外被实现。

.. code-block:: java

    //: interfaces/nesting/NestingInterfaces.java
    package interfaces.nesting;

    class A {
        interface B {
            void f();
        }
        public class BImp implements B {
            public void f() {}
        }
        private class BImp2 implements B {
            public void f() {}
        }
        public interface C {
            void f();
        }
        class CImp implements C {
            public void f() {}
        }	
        private class CImp2 implements C {
            public void f() {}
        }
        private interface D {
            void f();
        }
        private class DImp implements D {
            public void f() {}
        }
        public class DImp2 implements D {
            public void f() {}
        }
        public D getD() { return new DImp2(); }
        private D dRef;
        public void receiveD(D d) {
            dRef = d;
            dRef.f();
        }
    }	

    interface E {
        interface G {
            void f();
        }
        // Redundant "public":
        public interface H {
            void f();
        }
        void g();
        // Cannot be private within an interface:
        //! private interface I {}
    }	

    public class NestingInterfaces {
        public class BImp implements A.B {
            public void f() {}
        }
        class CImp implements A.C {
            public void f() {}
        }
        // Cannot implement a private interface except
        // within that interface's defining class:
        //! class DImp implements A.D {
        //!    public void f() {}
        //! }
        class EImp implements E {
            public void g() {}
        }
        class EGImp implements E.G {
            public void f() {}
        }
        class EImp2 implements E {
            public void g() {}
            class EG implements E.G {
                public void f() {}
            }
        }	
        public static void main(String[] args) {
            A a = new A();
            // Can't access A.D:
            //! A.D ad = a.getD();
            // Doesn't return anything but A.D:
            //! A.DImp2 di2 = a.getD();
            // Cannot access a member of the interface:
            //! a.getD().f();
            // Only another A can do anything with getD():
            A a2 = new A();
            a2.receiveD(a.getD());
        }
    } ///:~

.. _factory-mode-v1:

接口与工厂模式
--------------

.. mermaid::

    classDiagram
        class Service
        class ServiceFactory
        <<interface>> Service
        <<interface>> ServiceFactory
        Service <|-- Implementation1 : implements
        Service <|-- Implementation2 : implements
        ServiceFactory <|-- Implementation1Factory : implements
        ServiceFactory <|-- Implementation2Factory : implements
        Service : method1()
        Service : method2()
        ServiceFactory : getService()
        Implementation1Factory : getService()
        Implementation2Factory : getService()
        Implementation1 : method1()
        Implementation1 : method2()
        Implementation2 : method1()
        Implementation2 : method2()


接口是实现多重继承的途径，而生成遵循某个接口的对象的典型方式就是 **工厂方法** 设计模式。

与直接调用构造器不同，我们在接口的 **某个实现** 上 **调用创建方法** ，在 **工厂对象** 上 **生成接口的某个实现的对象** 。

理论上，通过这种方式，我们的代码将完全 **与接口的实现分离** ，这就使得我们可以透明地将某个实现 **替换** 为另一个实现。

.. note:: 

    创建这种额外的间接性一个常见的原因是想要创建框架。另外一种更优雅的方式创建工厂就是 :ref:`使用匿名内部类 <factory-mode-v2>` 。

.. code-block:: java
    :emphasize-lines: 15, 16, 21, 27, 28, 33

    //: interfaces/Factories.java
    import static net.mindview.util.Print.*;

    interface Service {
        void method1();
        void method2();
    }

    interface ServiceFactory {
        Service getService();
    }

    class Implementation1 implements Service {
        Implementation1() {} // Package access
        public void method1() {print("Implementation1 method1");}
        public void method2() {print("Implementation1 method2");}
    }	

    class Implementation1Factory implements ServiceFactory {
        public Service getService() {
            return new Implementation1();
        }
    }

    class Implementation2 implements Service {
        Implementation2() {} // Package access
        public void method1() {print("Implementation2 method1");}
        public void method2() {print("Implementation2 method2");}
    }

    class Implementation2Factory implements ServiceFactory {
        public Service getService() {
            return new Implementation2();
        }
    }	

    public class Factories {
        public static void serviceConsumer(ServiceFactory fact) {
            Service s = fact.getService();
            s.method1();
            s.method2();
        }
        public static void main(String[] args) {
            serviceConsumer(new Implementation1Factory());
            // Implementations are completely interchangeable:
            serviceConsumer(new Implementation2Factory());
        }
    } /* Output:
    Implementation1 method1
    Implementation1 method2
    Implementation2 method1
    Implementation2 method2
    *///:~

.. warning:: 

    优先使用类而不是接口。如果你的设计中需要某个接口，你必须了解它。否则，不到迫不得已，不要将其放到你的设计中。
