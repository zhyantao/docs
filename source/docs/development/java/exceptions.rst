====
异常
====

发现错误的理想时机是在编译阶段。错误恢复机制是代码健壮性的最强有力的方式。

开发异常的初衷是为了方便程序员处理错误。

异常处理的一个重要原则是“只有在你知道如何处理的情况下才捕获异常”。

异常处理的一个重要目标就是把错误处理的代码同错误发生的地点相分离。

基本异常
---------

异常情形    
    阻止当前方法或作用域继续执行。

抛出异常    
    从当前环境跳出，并且把异常对象的引用 ``throw`` 给上一级环境，上一级环境是指外层作用域。故可以用抛出异常的方式从当前的作用域退出。
    
    抛出异常后，会发生：

    - 首先，同 Java 中其他对象的创建一样，使用 ``new`` 在堆上创建异常对象。
    - 然后，当前的执行路径被终止，并且从当前环境中弹出对异常对象的引用。
    - 异常处理机制接管程序，并寻找异常处理程序来继续执行程序。

异常处理程序    
    将程序从错误状态中恢复，以使程序能要么换一种方式运行，要么继续运行下去。

异常参数
~~~~~~~~~

标准异常类都有两个构造器，一个默认构造器，另一个是接受字符串作为参数，以便能够把相关信息放入异常对象的构造器。

能够抛出任意类型的 ``Throwable`` 对象是异常类型的根类。

错误信息可以保存在异常对象内部或者用异常类的名称来暗示。通常，异常对象中仅有的信息就是异常类型，除此之外，不包含任何有意义的内容。

捕获异常
---------

监控区域（guarded region）
    一段可能产生异常的代码，并且后面跟着处理这些异常的代码。

try 块
~~~~~~~

如果在方法内部抛出了异常，这个方法将在抛出异常的过程中结束。要是不希望此方法就此结束， **可以** 在方法内设置 ``catch`` 块来捕获异常。

异常处理程序
~~~~~~~~~~~~

抛出的异常必须在某处得到处理。这个“地点”就是异常处理程序，而且针对每个要捕获的异常，得准备相应的处理程序，即准备多个 ``catch`` 块。

``catch`` 只会捕获匹配的异常，这与 ``switch`` 语句中的 ``case`` 不同， ``case`` 如果不加 ``break`` 会继续执行匹配之后的 ``case`` 。

注意，异常处理理论上有两种基本模型：

- 终止模型：错误发生后，无法重新回到错误地点继续执行代码。
- 恢复模型：可以在 ``while`` 循环中放置 ``try`` 块，不断地进行尝试，直到结果满意。

Java 采取的是终止模型。

创建自定义异常
--------------

创建自定义异常，必须从已有的异常类继承，最好是选择意思相近的异常类继承（不容易找）。建立新的异常类型最简单的方法就是让编译器为你产生默认构造器。

.. code-block:: java
    :emphasize-lines: 4, 7, 9

    //: exceptions/InheritingExceptions.java
    // Creating your own exceptions.

    class SimpleException extends Exception {}

    public class InheritingExceptions {
        public void f() throws SimpleException {
            System.out.println("Throw SimpleException from f()");
            throw new SimpleException();
        }
        public static void main(String[] args) {
            InheritingExceptions sed = new InheritingExceptions();
            try {
                sed.f();
            } catch(SimpleException e) {
                System.out.println("Caught it!");
                e.printStackTrace(System.out);
            }
        }
    } /* Output:
    Throw SimpleException from f()
    Caught it!
    SimpleException
            at InheritingExceptions.f(InheritingExceptions.java:9)
            at InheritingExceptions.main(InheritingExceptions.java:14)
    *///:~

对异常来说，最重要的部分就是类名。通常，把错误信息输出到 ``System.err`` 比输出到 ``System.out`` 要好，因为这样更容易被用户注意到。

也可以为自定义类创建带参数的构造器，让其可以在创建异常对象时输出一些信息。

``e.printStackTrace()`` 可以打印“从方法调用处直到异常抛出处”的方法调用序列。

异常与记录日志
~~~~~~~~~~~~~~

使用 ``java.util.logging`` 记录日志。

.. code-block:: java

    //: exceptions/LoggingExceptions2.java
    // Logging caught exceptions.
    import java.util.logging.*;
    import java.io.*;

    public class LoggingExceptions2 {
        private static Logger logger = Logger.getLogger("LoggingExceptions2");
        static void logException(Exception e) {
            StringWriter trace = new StringWriter();
            e.printStackTrace(new PrintWriter(trace));
            logger.severe(trace.toString());
        }
        public static void main(String[] args) {
            try {
                throw new NullPointerException();
            } catch(NullPointerException e) {
                logException(e);
            }
        }
    } /* Output: (90% match)
    Aug 30, 2005 4:07:54 PM LoggingExceptions2 logException
    SEVERE: java.lang.NullPointerException
                    at LoggingExceptions2.main(LoggingExceptions2.java:16)
    *///:~

异常说明
---------

异常说明使用 ``throws`` 后加一个所有潜在异常类型的列表。 **它属于方法声明的一部分** 。告诉了客户端程序员某个方法可能会抛出的异常类型，然后客户端程序员就可以进行相应处理了。

.. code-block:: java

    void f() throws TooBig, TooSmall, DivZero { //...

代码必须与异常说明保持一致。如果方法里的代码产生了异常却没有进行处理，编译器会发现这个问题并提醒你：要么处理这个异常，要么就在异常说明中表明此方法将产生异常。

也可以声明方法将抛出异常，实际上并不抛出。这样做的好处是，为异常先占个位子，以后抛出这种异常就不用修改已有的代码了。在定义抽象基类和接口时，这种能力很重要，这样派生类或接口实现就能够抛出这种预先声明的异常了。

在编译时被强制检查的异常叫做 **被检查的异常** 。

当不知道该如何处理这个异常时，但是也不想把它“吞”了，或者打印一些无用的信息，可以直接把“被检查的异常”包装进 ``RuntimeException`` 里面：

.. code-block:: java

    try {
        // to do something useful
    } catch (IDontKnowWhatToDoWithThisCheckedException e) {
        throw new RuntimeException(e);
    }

捕获所有异常
------------

直接捕获基类 ``Exception`` 。

.. code-block:: java

    catch(Exception e) {
        System.out.println("Caught an exception");
    }

栈轨迹
~~~~~~

``printStackTrace()`` 方法所提供的信息可以通过 ``getStackTrace()`` 方法来直接访问，这个方法将返回一个由栈轨迹中的元素所构成的数组，其中每个元素都表示栈中的一帧。元素 0 是栈顶元素，并且是调用序列中的最后一个方法调用。

.. code-block:: java

    //: exceptions/WhoCalled.java
    // Programmatic access to stack trace information.

    public class WhoCalled {
        static void f() {
            // Generate an exception to fill in the stack trace
            try {
                throw new Exception();
            } catch (Exception e) {
                for(StackTraceElement ste : e.getStackTrace())
                    System.out.println(ste.getMethodName());
            }
        }
        static void g() { f(); }
        static void h() { g(); }
        public static void main(String[] args) {
            f();
            System.out.println("--------------------------------");
            g();
            System.out.println("--------------------------------");
            h();
        }
    } /* Output:
    f
    main
    --------------------------------
    f
    g
    main
    --------------------------------
    f
    g
    h
    main
    *///:~

异常链
~~~~~~

如果想要在捕获一个异常后抛出另一个异常，并且希望把原始异常的信息保存下来，这被称为异常链。可以使用 ``initCause()`` 方法把异常链上不同类型的异常串起来，便于找到异常最初发生的位置。

.. code-block:: java

    //: exceptions/DynamicFields.java
    // A Class that dynamically adds fields to itself.
    // Demonstrates exception chaining.
    import static net.mindview.util.Print.*;

    class DynamicFieldsException extends Exception {}

    public class DynamicFields {
        private Object[][] fields;
        public DynamicFields(int initialSize) {
            fields = new Object[initialSize][2];
            for(int i = 0; i < initialSize; i++)
                fields[i] = new Object[] { null, null };
        }
        public String toString() {
            StringBuilder result = new StringBuilder();
            for(Object[] obj : fields) {
                result.append(obj[0]);
                result.append(": ");
                result.append(obj[1]);
                result.append("\n");
            }
            return result.toString();
        }
        private int hasField(String id) {
            for(int i = 0; i < fields.length; i++)
                if(id.equals(fields[i][0]))
                    return i;
            return -1;
        }
        private int
        getFieldNumber(String id) throws NoSuchFieldException {
            int fieldNum = hasField(id);
            if(fieldNum == -1)
                throw new NoSuchFieldException();
            return fieldNum;
        }
        private int makeField(String id) {
            for(int i = 0; i < fields.length; i++)
                if(fields[i][0] == null) {
                    fields[i][0] = id;
                    return i;
                }
            // No empty fields. Add one:
            Object[][] tmp = new Object[fields.length + 1][2];
            for(int i = 0; i < fields.length; i++)
                tmp[i] = fields[i];
            for(int i = fields.length; i < tmp.length; i++)
                tmp[i] = new Object[] { null, null };
            fields = tmp;
            // Recursive call with expanded fields:
            return makeField(id);
        }
        public Object
        getField(String id) throws NoSuchFieldException {
            return fields[getFieldNumber(id)][1];
        }
        public Object setField(String id, Object value)
        throws DynamicFieldsException {
            if(value == null) {
                // Most exceptions don't have a "cause" constructor.
                // In these cases you must use initCause(),
                // available in all Throwable subclasses.
                DynamicFieldsException dfe =
                    new DynamicFieldsException();
                dfe.initCause(new NullPointerException());
                throw dfe;
            }
            int fieldNumber = hasField(id);
            if(fieldNumber == -1)
                fieldNumber = makeField(id);
            Object result = null;
            try {
                result = getField(id); // Get old value
            } catch(NoSuchFieldException e) {
                // Use constructor that takes "cause":
                throw new RuntimeException(e);
            }
            fields[fieldNumber][1] = value;
            return result;
        }
        public static void main(String[] args) {
            DynamicFields df = new DynamicFields(3);
            print(df);
            try {
                df.setField("d", "A value for d");
                df.setField("number", 47);
                df.setField("number2", 48);
                print(df);
                df.setField("d", "A new value for d");
                df.setField("number3", 11);
                print("df: " + df);
                print("df.getField(\"d\") : " + df.getField("d"));
                Object field = df.setField("d", null); // Exception
            } catch(NoSuchFieldException e) {
                e.printStackTrace(System.out);
            } catch(DynamicFieldsException e) {
                e.printStackTrace(System.out);
            }
        }
    } /* Output:
    null: null
    null: null
    null: null

    d: A value for d
    number: 47
    number2: 48

    df: d: A new value for d
    number: 47
    number2: 48
    number3: 11

    df.getField("d") : A new value for d
    DynamicFieldsException
                    at DynamicFields.setField(DynamicFields.java:64)
                    at DynamicFields.main(DynamicFields.java:94)
    Caused by: java.lang.NullPointerException
                    at DynamicFields.setField(DynamicFields.java:66)
                    ... 1 more
    *///:~


Java 标准异常
-------------

``Throwable`` 对象可分为两种类型：

- ``Error`` ：表示编译时和系统错误
- ``Exception`` ：表示可以被抛出的基本类型

特例：RuntimeException
~~~~~~~~~~~~~~~~~~~~~~~

也被称为“不受检查异常”。这种异常属于错误，将被自动捕获，不用你亲自动手了。

.. note:: 

    只能在代码中忽略 ``RuntimeException`` （及其子类）类型的异常，其他类型异常的处理都是由编译器强制实施的。

使用 finally 进行清理
----------------------

无论 ``try`` 块中的异常是否抛出， ``finally`` 子句中的程序一定会被执行，而 ``catch`` 块中的程序可能不会执行。

.. code-block:: java

    //: exceptions/FinallyWorks.java
    // The finally clause is always executed.

    class ThreeException extends Exception {}

    public class FinallyWorks {
        static int count = 0;
        public static void main(String[] args) {
            while(true) {
                try {
                    // Post-increment is zero first time:
                    if(count++ == 0)
                        throw new ThreeException();
                    System.out.println("No exception");
                } catch(ThreeException e) {
                    System.out.println("ThreeException");
                } finally {
                    System.out.println("In finally clause");
                    if(count == 2) break; // out of "while"
                }
            }
        }
    } /* Output:
    ThreeException
    In finally clause
    No exception
    In finally clause
    *///:~

.. note:: 

    Java 异常不允许我们回到异常抛出的地点，但是当我们把 ``try`` 块放在循环里，就可以回去了。还可以加入一个 ``static`` 类型的计数器或别的装置，使循环在放弃以前能尝试一定的次数，增强程序的健壮性。

finally 用来做什么
~~~~~~~~~~~~~~~~~~~

清理内存之外的资源。

- 已经打开的文件或网络连接
- 在屏幕上画的图形

因为 ``finally`` 子句总是会执行，所以在一个方法中，可以从多个点返回，并且可以保证重要的清理工作仍旧会执行。比如下面的程序将会从两个点返回：

.. code-block:: java

    //: exceptions/MultipleReturns.java
    import static net.mindview.util.Print.*;

    public class MultipleReturns {
        public static void f(int i) {
            print("Initialization that requires cleanup");
            try {
                print("Point 1");
                if(i == 1) return;
                print("Point 2");
                if(i == 2) return;
                print("Point 3");
                if(i == 3) return;
                print("End");
                return;
            } finally {
                print("Performing cleanup");
            }
        }
        public static void main(String[] args) {
            for(int i = 1; i <= 4; i++)
                f(i);
        }
    } /* Output:
    Initialization that requires cleanup
    Point 1
    Performing cleanup
    Initialization that requires cleanup
    Point 1
    Point 2
    Performing cleanup
    Initialization that requires cleanup
    Point 1
    Point 2
    Point 3
    Performing cleanup
    Initialization that requires cleanup
    Point 1
    Point 2
    Point 3
    End
    Performing cleanup
    *///:~

缺憾：异常丢失
~~~~~~~~~~~~~~

.. code-block:: java

    //: exceptions/LostMessage.java
    // How an exception can be lost.

    class VeryImportantException extends Exception {
        public String toString() {
            return "A very important exception!";
        }
    }

    class HoHumException extends Exception {
        public String toString() {
            return "A trivial exception";
        }
    }

    public class LostMessage {
        void f() throws VeryImportantException {
            throw new VeryImportantException();
        }
        void dispose() throws HoHumException {
            throw new HoHumException();
        }
        public static void main(String[] args) {
            try {
                LostMessage lm = new LostMessage();
                try {
                    lm.f();
                }catch(VeryImportantException v){
                    System.out.println(v);
                }    finally {
                    lm.dispose();
                }
            } catch(HoHumException e) {
                System.out.println(e);
            } 
        }
    } /* Output:
    A trivial exception
    *///:~

上面代码中 ``VeryImportantException`` 被丢失了。

异常的限制
----------

当覆盖方法时，只能抛出在基类方法的异常说明里列出的那些异常。

这个限制很有用，因为这意味着，当基类使用的代码应用到其派生类对象的时候，一样能工作，异常也不例外。

.. uml::

    @startuml
    class Exception
    class BaseballException
    class Foul
    class Strike
    class StormException
    class RainedOut
    abstract Inning
    interface Storm
    class StormyInning
    Inning <|-- StormyInning
    Storm <|.. StormyInning
    Exception <|-- BaseballException
    Exception <|-- StormException
    StormException <|-- RainedOut
    BaseballException <|-- Foul
    Foul <|-- PopFoul
    BaseballException <|-- Strike
    @enduml

.. code-block:: java

    //: exceptions/StormyInning.java
    // Overridden methods may throw only the exceptions
    // specified in their base-class versions, or exceptions
    // derived from the base-class exceptions.

    class BaseballException extends Exception {}
    class Foul extends BaseballException {}
    class Strike extends BaseballException {}

    abstract class Inning {
        public Inning() throws BaseballException {}
        public void event() throws BaseballException {
            // Doesn't actually have to throw anything
        }
        public abstract void atBat() throws Strike, Foul;
        public void walk() {} // Throws no checked exceptions
    }

    class StormException extends Exception {}
    class RainedOut extends StormException {}
    class PopFoul extends Foul {}

    interface Storm {
        public void event() throws RainedOut;
        public void rainHard() throws RainedOut;
    }

    public class StormyInning extends Inning implements Storm {
        // OK to add new exceptions for constructors, but you
        // must deal with the base constructor exceptions:
        public StormyInning()
            throws RainedOut, BaseballException {}
        public StormyInning(String s)
            throws Foul, BaseballException {}
        // Regular methods must conform to base class:
    //! void walk() throws PopFoul {} //Compile error
        // Interface CANNOT add exceptions to existing
        // methods from the base class:
    //! public void event() throws RainedOut {}
        // If the method doesn't already exist in the
        // base class, the exception is OK:
        public void rainHard() throws RainedOut {}
        // You can choose to not throw any exceptions,
        // even if the base version does:
        public void event() {}
        // Overridden methods can throw inherited exceptions:
        public void atBat() throws PopFoul {}
        public static void main(String[] args) {
            try {
                StormyInning si = new StormyInning();
                si.atBat();
            } catch(PopFoul e) {
                System.out.println("Pop foul");
            } catch(RainedOut e) {
                System.out.println("Rained out");
            } catch(BaseballException e) {
                System.out.println("Generic baseball exception");
            }
            // Strike not thrown in derived version.
            try {
                // What happens if you upcast?
                Inning i = new StormyInning();
                i.atBat();
                // You must catch the exceptions from the
                // base-class version of the method:
            } catch(Strike e) {
                System.out.println("Strike");
            } catch(Foul e) {
                System.out.println("Foul");
            } catch(RainedOut e) {
                System.out.println("Rained out");
            } catch(BaseballException e) {
                System.out.println("Generic baseball exception");
            }
        }
    } ///:~

异常匹配
--------

抛出异常的时候，异常处理系统会按照代码的书写顺序找出“最近”的处理程序。

查找的时候，并不要求抛出的异常同处理程序所声明的异常完全匹配。派生类的对象也可以匹配其基类的处理程序。
