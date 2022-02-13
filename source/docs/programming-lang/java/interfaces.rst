======
接口
======

抽象类和抽象方法
----------------

抽象方法仅有声明，没有方法体，如 ``abstract void f();``。

包含抽象方法的类必须限定为抽象类，如 
``abstract class ClassName {}``，我们创建抽象类的目的是希望通过这个通用接口操纵一系列类。

如果从一个抽象类继承，并想创建该新类的对象，那么就必须为基类中的所有抽象方法提供方法定义。
如果不这样做（可以选择不做），那么导出类便也是抽象类，且编译器将会强制我们使用 ``abstract`` 
关键字来限定这个类。


接口定义
--------

抽象方法可以提供接口，抽象方法所属的类是 **部分抽象** 的类（因为抽象类中可以有某些方法的实现）。但是 
``interface`` 关键字可以产生一个 **完全抽象** 的类，如 ``interface ClassName {}``。

接口和类一样，也有访问权限控制，如果你想让这个接口具有全局访问性，那么用 ``public`` 
声明它，否则它只有包访问权限。在接口中声明的方法，若不加以声明，默认都是 ``public`` 
访问权限，而在接口中声明的属性，若不加以声明，默认是 ``public static final`` 的。

接口被用来建立类与类之间的 **协议**。
要让某个类遵循某个特定协议（或者一组协议），\ ``implements`` 它即可。

使用接口的核心原因是为了能够向上转型为多个基类型（以及由此带来的灵活性）。
事实上，如果知道某个事物应该成为一个基类，那么第一选择应该是使它成为一个接口。
接口是一种重要的工具，但是它们容易被滥用，恰当的原则应该是优先选择类而不是接口。

任何抽象性都应该是应真正的需求而产生的。
当必需时，你应该重构接口而不是到处添加额外级别的间接性，而这又会带来额外的复杂性。

接口和内部类为我们提供了一种将 **接口与实现分离** 的更加结构化的方法。

完全解耦
--------

当一个系统足够大时，解耦应该是一个必然会聊到的话题，而选择不同的实现方式，解耦能力也不同。
如果使用继承，则无法完全解耦，而使用接口，则可以实现完全解耦。

由于单根继承结构的局限性，在使用继承语法的实现中，若想要利用多态的特性，我们只能调用基类中的方法。
因此，基类和导出类之间是一对多的树形关系。

而在使用接口语法的实现中，摆脱了单根继承结构的局限性，赋予了 Java "多重继承" 的能力。
一个类可能实现了多个接口，那么我们调用任何一个接口中的任何一个方法，都可以动态绑定到实现类上。
因此，接口类和实现类之间是多对多的网状关系，大大扩展了解耦和扩展能力。

语言表述总是难以给人一个很直观的印象。若我们有一个符合如下继承关系的几个类：

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

        class Apply
        Apply : void process(Processor p, Object s)

.. admonition:: Apply.java
    :class: dropdown

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

.. mermaid::

    classDiagram
        Filter <|-- LowPass : extends
        Filter <|-- HighPass : extends
        Filter <|-- BandPass : extends
        Filter : String name()
        Filter : Waveform process()
        LowPass : Waveform process()
        HighPass : Waveform process()
        BandPass : Waveform process()

        class Waveform
        Waveform : long counter
        Waveform : long id
        Waveform : String toString()

.. admonition:: Filter.java
    :class: dropdown

    .. code-block:: java

        //: interfaces/filters/Waveform.java
        package interfaces.filters;

        public class Waveform {
            private static long counter;
            private final long id = counter++;
            public String toString() { return "Waveform " + id; }
        } ///:~

    .. code-block:: java

        //: interfaces/filters/Filter.java
        package interfaces.filters;

        public class Filter {
            public String name() {
                return getClass().getSimpleName();
            }
            public Waveform process(Waveform input) { return input; }
        } ///:~

    .. code-block:: java

        //: interfaces/filters/LowPass.java
        package interfaces.filters;

        public class LowPass extends Filter {
            double cutoff;
            public LowPass(double cutoff) { this.cutoff = cutoff; }
            public Waveform process(Waveform input) {
                return input; // Dummy processing
            }
        } ///:~

    .. code-block:: java

        //: interfaces/filters/HighPass.java
        package interfaces.filters;

        public class HighPass extends Filter {
            double cutoff;
            public HighPass(double cutoff) { this.cutoff = cutoff; }
            public Waveform process(Waveform input) { return input; }
        } ///:~

    .. code-block:: java

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

``Filter`` 与 ``Processor`` 具有相同的接口元素 ``process()``，但是因为 ``Filter`` 并非继承自 
``Processor``，因此在调用 ``Apply.process()`` 时，并不会触发 ``Filter`` 类的 ``process()`` 方法。
这主要是因为 ``Apply.process()`` 和 ``Processor.process()`` 
之间的 **耦合过紧**，于是将其应用于 ``Filter`` 时，\ **复用被禁止** 了。

但是，如果 ``Processor`` 是一个接口（之前是一个普通的类），这些限制就会变得松动，就可以实现复用了。

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

        class Apply
        Apply : void process(Processor p, Object s)

.. admonition:: 接口方式实现
    :class: dropdown

    .. code-block:: java

        //: interfaces/interfaceprocessor/Processor.java
        package interfaces.interfaceprocessor;

        public interface Processor {
            String name();
            Object process(Object input);
        } ///:~

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

    高亮除的代码实现了 **适配器模式**。
    适配器模式的出现是因为无法修改旧接口，而且旧接口无法与满足新业务的接口需求。
    引进适配器后，在旧接口的基础上稍作修改，满足新业务。
        
    在适配器方式中，\ ``FilterAdapter`` 的构造器接受你已经拥有的接口 
    ``Filter``，然后生成具有你所需要的 ``Processor`` 接口的对象。

按照之前的需求，我们还是想要用 ``Apply.process()`` 能够同时处理 ``Processor.process()`` 和 
``Filter.process()``。修改后的代码结构，既可以让 ``Processor`` 应用于 ``StringProcessor`` 
也可以应用于 ``FilterAdapter``，而后者，是继承无法办到的。这实现了 ``Processor.process()`` 与 
``StringProcessor.process()`` 的解耦。

从这个解决方案可以看出，\ **没有什么是加一层是不能解决的**。
``Apply.process()`` 方法接受 ``Processor`` 类型的对象，并不接受 ``Filter`` 类型的对象，那么我们将 
``Processor`` 作为接口，\ ``FilterAdapter`` 也来实现这个接口，然后由 ``FilterAdapter`` 接受 
``Filter`` 类型的对象，问题就解决了。

再举一个关于解耦的例子。
``Scanner`` 类的构造器接受一个 ``Readable`` 接口。
``Readable`` 是专门为 ``Scanner`` 类设计的接口。
``Scanner`` 不必将参数限定为某个特定类，只要某个类实现了 ``Readable`` 接口就可以作为 
``Scanner`` 的参数，这就很好地体现了可扩展性和完全解耦。

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
        public int read(CharBuffer cb) {        // 实现 Readable 接口需要重写 read() 方法
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


嵌套接口
--------

接口可以嵌套在类或其他接口中。需要注意的是，当实现某个接口时，\ **不需要实现** 
嵌套在其内部的任何接口，而且 ``private`` 接口不能在定义它的类之外被实现。

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

工厂模式是利用工厂批量生产对象的方式。理论上，通过这种方式，我们的代码将完全与接口的实现分离。
这就使得我们可以透明地将某个实现替换为另一个实现。
另外一种更优雅的方式创建工厂就是 :ref:`使用匿名内部类 <factory-mode-v2>`。
创建这种额外的间接性一个常见的原因是想要创建框架。

为了更深刻地理解工厂模式，我们还是用一段代码来理解一下。

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
