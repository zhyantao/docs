====
并发
====

Web 是最常见的 Java 应用系统之一，而基本的 Web 类库 —— Servlet —— 具有天生的多线程性。
因为 Web 服务器经常包含多个处理器，而并发是充分利用这些处理器的理想方式。

尽管 Swing 和 SWT 类库都有针对线程安全的机制，但是不理解并发，就很难了解如何正确地使用它们。

学习并发就像学习一门新的编程语言。用并发解决的问题大体可分为两种：速度、设计可管理性。


基本的线程机制
--------------

定义任务
~~~~~~~~

线程可以驱动任务， ``Runnable`` 接口提供描述任务的方式。
要想定义任务，只需实现 ``Runnable`` 接口并编写 ``run()`` 方法，使得该任务可以执行你的命令。

例如， ``LiftOff`` 任务将显示发射之前的倒计时：

.. code-block:: java

    //: concurrency/LiftOff.java
    // Demonstration of the Runnable interface.

    public class LiftOff implements Runnable {
        protected int countDown = 10; // Default
        private static int taskCount = 0;
        private final int id = taskCount++;
        public LiftOff() {}
        public LiftOff(int countDown) {
            this.countDown = countDown;
        }
        public String status() {
            return "#" + id + "(" +
                (countDown > 0 ? countDown : "Liftoff!") + "), ";
        }
        public void run() {
            while(countDown-- > 0) {
                System.out.print(status());
                Thread.yield();
            }
        }
    } ///:~

注意，标识符 ``id`` 可以用来区分任务的多个实例，它是 ``final`` 的。

通常， ``run()`` 方法会写成无限循环的形式，这就意味着，除非有某个条件使得 ``run()`` 终止，否则它将永远运行下去。

静态方法， ``Thread.yield()`` 调用的是线程调度器，可以将 CPU 从一个线程转移给另一个线程。

下面的代码是用 ``main()`` 方法所在的线程驱动 ``LiftOff`` 对象，实际上，任何线程都可以启动另一个线程。

.. code-block:: java

    //: concurrency/MainThread.java

    public class MainThread {
        public static void main(String[] args) {
            LiftOff launch = new LiftOff();
            launch.run();
        }
    } /* Output:
    #0(9), #0(8), #0(7), #0(6), #0(5), #0(4), #0(3), #0(2), #0(1), #0(Liftoff!),
    *///:~


Thread 类
~~~~~~~~~~

用 ``Thread`` 驱动 ``LiftOff`` 对象。 Thread 只需要一个 ``Runnable`` 对象。

.. code-block:: java

    //: concurrency/BasicThreads.java
    // The most basic use of the Thread class.

    public class BasicThreads {
        public static void main(String[] args) {
            Thread t = new Thread(new LiftOff());
            t.start();
            System.out.println("Waiting for LiftOff");
        }
    } /* Output: (90% match)
    Waiting for LiftOff
    #0(9), #0(8), #0(7), #0(6), #0(5), #0(4), #0(3), #0(2), #0(1), #0(Liftoff!),
    *///:~

你可以同时启动多个线程。

.. code-block:: java

    //: concurrency/MoreBasicThreads.java
    // Adding more threads.

    public class MoreBasicThreads {
        public static void main(String[] args) {
            for(int i = 0; i < 5; i++)
                new Thread(new LiftOff()).start();
            System.out.println("Waiting for LiftOff");
        }
    } /* Output: (Sample)
    Waiting for LiftOff
    #0(9), #1(9), #2(9), #3(9), #4(9), #0(8), #1(8), #2(8), 
    #3(8), #4(8), #0(7), #1(7), #2(7), #3(7), #4(7), #0(6), 
    #1(6), #2(6), #3(6), #4(6), #0(5), #1(5), #2(5), #3(5), 
    #4(5), #0(4), #1(4), #2(4), #3(4), #4(4), #0(3), #1(3), 
    #2(3), #3(3), #4(3), #0(2), #1(2), #2(2), #3(2), #4(2), 
    #0(1), #1(1), #2(1), #3(1), #4(1), #0(Liftoff!), 
    #1(Liftoff!), #2(Liftoff!), #3(Liftoff!), #4(Liftoff!),
    *///:~

如果你的机器上有多个处理器，线程调度器将会在这些处理器之间默默地分发线程。

使用 Executor
~~~~~~~~~~~~~~

执行器（ ``Executor`` ）将为你管理 ``Thread`` 对象。

- ``LiftOff`` 直到如何执行任务
- ``ExecutorService`` 直到如何构建恰当的上下文来执行 ``Runnable`` 对象

.. code-block:: java

    //: concurrency/CachedThreadPool.java
    import java.util.concurrent.*;

    public class CachedThreadPool {
        public static void main(String[] args) {
            ExecutorService exec = Executors.newCachedThreadPool();
            for(int i = 0; i < 5; i++)
                exec.execute(new LiftOff());
            exec.shutdown();
        }
    } /* Output: (Sample)
    #0(9), #0(8), #1(9), #2(9), #3(9), #4(9), #0(7), #1(8), 
    #2(8), #3(8), #4(8), #0(6), #1(7), #2(7), #3(7), #4(7), 
    #0(5), #1(6), #2(6), #3(6), #4(6), #0(4), #1(5), #2(5), 
    #3(5), #4(5), #0(3), #1(4), #2(4), #3(4), #4(4), #0(2), 
    #1(3), #2(3), #3(3), #4(3), #0(1), #1(2), #2(2), #3(2), 
    #4(2), #0(Liftoff!), #1(1), #2(1), #3(1), #4(1), 
    #1(Liftoff!), #2(Liftoff!), #3(Liftoff!), #4(Liftoff!),
    *///:~

注意，可以直接将 ``CachedThreadPool`` 替换为不同类型的 ``Executor`` ，比如 ``FixedThreadPool`` 。

- ``CachedThreadPool`` 通常会创建与所需数量相同的线程
- ``FixedThreadPool`` 可以一次性预先执行代价高昂的线程分配
- ``SingleThreadPool`` 像是线程数量为 1 的 ``FixedThreadPool``

``SingleThreadPool`` 将线程按照顺序执行了，如下所示。在这种方式下，你不需要在共享资源上处理同步。

.. code-block:: java

    //: concurrency/SingleThreadExecutor.java
    import java.util.concurrent.*;

    public class SingleThreadExecutor {
        public static void main(String[] args) {
            ExecutorService exec =
                Executors.newSingleThreadExecutor();
            for(int i = 0; i < 5; i++)
                exec.execute(new LiftOff());
            exec.shutdown();
        }
    } /* Output:
    #0(9), #0(8), #0(7), #0(6), #0(5), #0(4), #0(3), #0(2), 
    #0(1), #0(Liftoff!), #1(9), #1(8), #1(7), #1(6), #1(5), 
    #1(4), #1(3), #1(2), #1(1), #1(Liftoff!), #2(9), #2(8), 
    #2(7), #2(6), #2(5), #2(4), #2(3), #2(2), #2(1), 
    #2(Liftoff!), #3(9), #3(8), #3(7), #3(6), #3(5), #3(4), 
    #3(3), #3(2), #3(1), #3(Liftoff!), #4(9), #4(8), #4(7), 
    #4(6), #4(5), #4(4), #4(3), #4(2), #4(1), #4(Liftoff!),
    *///:~

从任务中返回值
~~~~~~~~~~~~~~

``Runnable`` 是执行工作的独立任务，但是它不返回任何值。如果你希望任务完成时能够返回一个值，那么可以实现 ``Callable`` 接口，而不是 ``Runnable`` 接口。

``Callable`` 是一种具有类型参数的泛型，他的类型参数表示的是从方法 ``call()`` 中返回的值，并且必须使用 ``ExecutorService.submit()`` 方法调用它。

.. code-block:: java

    //: concurrency/CallableDemo.java
    import java.util.concurrent.*;
    import java.util.*;

    class TaskWithResult implements Callable<String> {
        private int id;
        public TaskWithResult(int id) {
            this.id = id;
        }
        public String call() {
            return "result of TaskWithResult " + id;
        }
    }

    public class CallableDemo {
        public static void main(String[] args) {
            ExecutorService exec = Executors.newCachedThreadPool();
            ArrayList<Future<String>> results =
                new ArrayList<Future<String>>();
            for(int i = 0; i < 10; i++)
                results.add(exec.submit(new TaskWithResult(i)));
            for(Future<String> fs : results)
                try {
                    // get() blocks until completion:
                    System.out.println(fs.get());
                } catch(InterruptedException e) {
                    System.out.println(e);
                    return;
                } catch(ExecutionException e) {
                    System.out.println(e);
                } finally {
                    exec.shutdown();
                }
        }
    } /* Output:
    result of TaskWithResult 0
    result of TaskWithResult 1
    result of TaskWithResult 2
    result of TaskWithResult 3
    result of TaskWithResult 4
    result of TaskWithResult 5
    result of TaskWithResult 6
    result of TaskWithResult 7
    result of TaskWithResult 8
    result of TaskWithResult 9
    *///:~

``submit()`` 方法会产生 ``Future`` 对象，他用 ``Callable`` 返回结果的特定类型进行了参数化。
你可以用 ``isDone()`` 方法来检查 ``Future`` 是否已经完成。
当任务完成时，它具有一个结果，你可以调用 ``get()`` 方法来获取该结果。

你也可以不用 ``isDone()`` 来检查，直接使用 ``get()`` ，这种情况下 ``get()`` 将阻塞，直到结果准备就绪。


线程优先级
~~~~~~~~~~

用 ``getPriority()`` 来读取现有线程的优先级，用 ``setPriority()`` 来修改优先级。

.. code-block:: java

    //: concurrency/SimplePriorities.java
    // Shows the use of thread priorities.
    import java.util.concurrent.*;

    public class SimplePriorities implements Runnable {
        private int countDown = 5;
        private volatile double d; // No optimization
        private int priority;
        public SimplePriorities(int priority) {
            this.priority = priority;
        }
        public String toString() {
            return Thread.currentThread() + ": " + countDown;
        }
        public void run() {
            Thread.currentThread().setPriority(priority);
            while(true) {
                // An expensive, interruptable operation:
                for(int i = 1; i < 100000; i++) {
                    d += (Math.PI + Math.E) / (double)i;
                    if(i % 1000 == 0)
                        Thread.yield();
                }
                System.out.println(this);
                if(--countDown == 0) return;
            }
        }
        public static void main(String[] args) {
            ExecutorService exec = Executors.newCachedThreadPool();
            for(int i = 0; i < 5; i++)
                exec.execute(
                    new SimplePriorities(Thread.MIN_PRIORITY));
            exec.execute(
                    new SimplePriorities(Thread.MAX_PRIORITY));
            exec.shutdown();
        }
    } /* Output: (70% match)
    Thread[pool-1-thread-4,1,main]: 5
    Thread[pool-1-thread-6,10,main]: 5
    Thread[pool-1-thread-3,1,main]: 5
    Thread[pool-1-thread-5,1,main]: 5
    Thread[pool-1-thread-1,1,main]: 5
    Thread[pool-1-thread-2,1,main]: 5
    Thread[pool-1-thread-2,1,main]: 4
    Thread[pool-1-thread-5,1,main]: 4
    Thread[pool-1-thread-4,1,main]: 4
    Thread[pool-1-thread-6,10,main]: 4
    Thread[pool-1-thread-1,1,main]: 4
    Thread[pool-1-thread-5,1,main]: 3
    Thread[pool-1-thread-3,1,main]: 4
    Thread[pool-1-thread-4,1,main]: 3
    Thread[pool-1-thread-2,1,main]: 3
    Thread[pool-1-thread-5,1,main]: 2
    Thread[pool-1-thread-1,1,main]: 3
    Thread[pool-1-thread-6,10,main]: 3
    Thread[pool-1-thread-4,1,main]: 2
    Thread[pool-1-thread-3,1,main]: 3
    Thread[pool-1-thread-2,1,main]: 2
    Thread[pool-1-thread-5,1,main]: 1
    Thread[pool-1-thread-4,1,main]: 1
    Thread[pool-1-thread-3,1,main]: 2
    Thread[pool-1-thread-6,10,main]: 2
    Thread[pool-1-thread-1,1,main]: 2
    Thread[pool-1-thread-2,1,main]: 1
    Thread[pool-1-thread-3,1,main]: 1
    Thread[pool-1-thread-6,10,main]: 1
    Thread[pool-1-thread-1,1,main]: 1
    *///:~

- 最后一个线程的优先级最高，其余所有线程的优先级被设为最低；
- 优先级在 ``run()`` 开头设置；
- ``Thread.currentThread()`` 获取驱动该任务的 ``Thread`` 对象的引用。 

后台线程
~~~~~~~~

后台（daemon）线程是指程序运行的时候在后台提供一种通用服务的线程，并且，这种线程并不属于程序中不可或缺的部分。
因此，当所有的非后台线程结束时，程序也就终止了，同时也会杀死进程中的所有后台线程。
反过来说，只要有任何非后台线程在运行，程序就不会终止。

比如，执行的 ``main()`` 就是一个非后台线程。

.. code-block:: java

    //: concurrency/SimpleDaemons.java
    // Daemon threads don't prevent the program from ending.
    import java.util.concurrent.*;
    import static net.mindview.util.Print.*;

    public class SimpleDaemons implements Runnable {
        public void run() {
            try {
                while(true) {
                    TimeUnit.MILLISECONDS.sleep(100);
                    print(Thread.currentThread() + " " + this);
                }
            } catch(InterruptedException e) {
                print("sleep() interrupted");
            }
        }
        public static void main(String[] args) throws Exception {
            for(int i = 0; i < 10; i++) {
                Thread daemon = new Thread(new SimpleDaemons());
                daemon.setDaemon(true); // Must call before start()
                daemon.start();
            }
            print("All daemons started");
            TimeUnit.MILLISECONDS.sleep(175);
        }
    } /* Output: (Sample)
    All daemons started
    Thread[Thread-7,5,main] SimpleDaemons@9fa7c29
    Thread[Thread-2,5,main] SimpleDaemons@10ab6798
    Thread[Thread-0,5,main] SimpleDaemons@781aca96
    Thread[Thread-9,5,main] SimpleDaemons@5c20fdea
    Thread[Thread-5,5,main] SimpleDaemons@7bb27ed2
    Thread[Thread-3,5,main] SimpleDaemons@28f008cd
    Thread[Thread-4,5,main] SimpleDaemons@77552fff
    Thread[Thread-8,5,main] SimpleDaemons@564426af
    Thread[Thread-6,5,main] SimpleDaemons@29448f89
    Thread[Thread-1,5,main] SimpleDaemons@31bf17b1
    *///:~

注意，必须在线程启动之前调用 ``setDaemon()`` 方法，才能把它设置为后台线程。

若注释掉 ``main()`` 中最后一行 ``sleep()`` 就看不到后台线程的打印结果了。
因为 ``main()`` 是唯一的非后台线程，这么快就执行完了，后台线程也就不用等待了。

加入一个线程
~~~~~~~~~~~~

一个线程可以在其他线程上调用 ``join()`` 方法，效果是等待一段时间直到第二个线程结束才继续执行。

如果某个线程在另一个线程 ``t`` 上调用 ``t.join()`` ，此线程将被挂起，直到目标线程 ``t`` 结束（即 ``t.isAlive()`` 返回假）才恢复。

也可以在调用 ``join()`` 时带上一个超时参数，这样如果目标线程在这段时间内没有结束， ``join()`` 方法总能返回。

对 ``join()`` 方法的调用可以被中断，做法是在调用线程上调用 ``interrupt()`` 方法，这时需要用到 ``try-catch`` 子句。

.. code-block:: java

    //: concurrency/Joining.java
    // Understanding join().
    import static net.mindview.util.Print.*;

    class Sleeper extends Thread {
        private int duration;
        public Sleeper(String name, int sleepTime) {
            super(name);
            duration = sleepTime;
            start();
        }
        public void run() {
            try {
                sleep(duration);
            } catch(InterruptedException e) {
                print(getName() + " was interrupted. " +
                    "isInterrupted(): " + isInterrupted());
                return;
            }
            print(getName() + " has awakened");
        }
    }

    class Joiner extends Thread {
        private Sleeper sleeper;
        public Joiner(String name, Sleeper sleeper) {
            super(name);
            this.sleeper = sleeper;
            start();
        }
        public void run() {
        try {
                sleeper.join();
            } catch(InterruptedException e) {
                print("Interrupted");
            }
            print(getName() + " join completed");
        }
    }

    public class Joining {
        public static void main(String[] args) {
            Sleeper
                sleepy = new Sleeper("Sleepy", 1500),
                grumpy = new Sleeper("Grumpy", 1500);
            Joiner
                dopey = new Joiner("Dopey", sleepy),
                doc = new Joiner("Doc", grumpy);
            grumpy.interrupt();
        }
    } /* Output:
    Grumpy was interrupted. isInterrupted(): false
    Doc join completed
    Sleepy has awakened
    Dopey join completed
    *///:~

``doc`` 比 ``dopey`` 执行的快，是因为如果 ``Sleeper`` 被中断， ``Joiner`` 将和 ``Sleeper`` 一同结束。

第二种情况是，如果 ``Sleeper`` 正常结束， ``Joiner`` 也将和 ``Sleeper`` 一同结束。


线程组
~~~~~~

线程组是一次不成功的尝试。 *said by Joshua Bloch*


捕获异常
~~~~~~~~

一旦异常逃出任务 ``run()`` 方法，它就会向外传播到控制台，除非你用特殊的步骤捕获这种错误的异常。

.. admonition:: ExceptionThread.java
    :class: dropdown
        
    .. code-block:: java

        //: concurrency/ExceptionThread.java
        // {ThrowsException}
        import java.util.concurrent.*;

        public class ExceptionThread implements Runnable {
            public void run() {
                throw new RuntimeException();
            }
            public static void main(String[] args) {
                ExecutorService exec = Executors.newCachedThreadPool();
                exec.execute(new ExceptionThread());
            }
        } ///:~

``Thread.UncaughtExceptionHandler`` 允许你在每个 ``Thread`` 对象上都附着一个异常处理器。
``Thread.UncaughtExceptionHandler.uncaughtException()`` 会在线程因未捕获的异常而临近死亡时被调用。

为了使用它，我们创建了一个新类型的 ``ThreadFactory`` ，它将每个新创建的 ``Thread`` 对象附着一个 ``Thread.UncaughtExceptionHandler`` 。

.. admonition:: CaptureUncaughtException.java
    :class: dropdown
            
    .. code-block:: java

        //: concurrency/CaptureUncaughtException.java
        import java.util.concurrent.*;

        class ExceptionThread2 implements Runnable {
            public void run() {
                Thread t = Thread.currentThread();
                System.out.println("run() by " + t);
                System.out.println(
                    "eh = " + t.getUncaughtExceptionHandler());
                throw new RuntimeException();
            }
        }

        class MyUncaughtExceptionHandler implements
        Thread.UncaughtExceptionHandler {
            public void uncaughtException(Thread t, Throwable e) {
                System.out.println("caught " + e);
            }
        }

        class HandlerThreadFactory implements ThreadFactory {
            public Thread newThread(Runnable r) {
                System.out.println(this + " creating new Thread");
                Thread t = new Thread(r);
                System.out.println("created " + t);
                t.setUncaughtExceptionHandler(
                    new MyUncaughtExceptionHandler());
                System.out.println(
                    "eh = " + t.getUncaughtExceptionHandler());
                return t;
            }
        }

        public class CaptureUncaughtException {
            public static void main(String[] args) {
                ExecutorService exec = Executors.newCachedThreadPool(
                    new HandlerThreadFactory());
                exec.execute(new ExceptionThread2());
            }
        } /* Output: (90% match)
        HandlerThreadFactory@de6ced creating new Thread
        created Thread[Thread-0,5,main]
        eh = MyUncaughtExceptionHandler@1fb8ee3
        run() by Thread[Thread-0,5,main]
        eh = MyUncaughtExceptionHandler@1fb8ee3
        caught java.lang.RuntimeException
        *///:~

在线程中捕获的异常，不能跨线程传播回 ``main()`` 。

.. code-block:: java

    //: concurrency/NaiveExceptionHandling.java
    // {ThrowsException}
    import java.util.concurrent.*;

    public class NaiveExceptionHandling {
        public static void main(String[] args) {
            try {
                ExecutorService exec =
                    Executors.newCachedThreadPool();
                exec.execute(new ExceptionThread());
            } catch(RuntimeException ue) {
                // This statement will NOT execute!
                System.out.println("Exception has been handled!");
            }
        }
    } ///:~


共享受限资源
------------
终结任务
--------
线程之间的协作
--------------
死锁
----
新类库中的构件
--------------
仿真
----
性能调优
--------
活动对象
--------
