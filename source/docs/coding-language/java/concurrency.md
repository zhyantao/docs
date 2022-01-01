# 并发

## 走进并行世界

### 你必须知道的几个概念

- 同步（Synchronous）和异步（Asynchronous）[^java_multithread]
- 并发（Concurrency）和并行（Parallelism）
- 临界区：一种公共资源或共享数据，可被多个线程使用
- 阻塞（Blocking）和非阻塞（Non-Blocking）
- 死锁（Deadlock）、饥饿（Starvation）和活锁（Livelock）

[^java_multithread]: 葛一鸣, 郭超. 实战Java高并发程序设计\[M\]. 电子工业出版社, 2015.

### 并发级别

- 阻塞（Blocking）
- 无饥饿（Starvation-Free）：解决公平问题。
- 无障碍（Obstruction-Free）：都可以进入临界区，出现问题回滚。
- 无锁（Lock-Free）：都进入临界区，且有一个在有限步可以得到执行。
- 无等待（Wait-Free）：都进入临界区，都可以在有限步得到执行。

### 两个重要定律

- Amdahl 定律：加速比的计算公式和理论上限。
- Gustafson 定律：同上，以不同的角度分析问题。

### Java 内存模型（JMM）

- 原子性（Atomicity）：多个线程不会互相干扰。
- 可见性（Visibility）：一个线程修改了值之后，其他线程能否立马看到结果。
- 有序性（Ordering）：编译器可能对代码重新排序，导致多线程运算结果出错。

``````{admonition} 一个不符合原子性的例子
:class: dropdown

```{code-block} java
/**
 * 测试原子性，确保运行环境为 32 位虚拟机
 * 64 位机器不会出现问题
 */

public class MultiThreadLong {
    public static long t = 0;
    
    public static class ChangeT implements Runnable {
        private long to;
        
        public ChangeT(long to) {
            this.to = to;
        }
        
        @Override
        public void run() {
            while(true) {
                MultiThreadLong.t = to;
                Thread.yield();
            }
        }
    }

    public static class ReadT implements Runnable {
        @Override
        public void run() {
            while(true) {
                long tmp = MultiThreadLong.t;

                if (tmp != 111L && tmp != -999L && tmp != 333L && tmp != -444L) {
                    System.out.println(tmp);
                }
                
                Thread.yield();
            }
        }
    }

    public static void main(String[] args) {
        new Thread(new ChangeT(111L)).start();
        new Thread(new ChangeT(-999L)).start();
        new Thread(new ChangeT(333L)).start();
        new Thread(new ChangeT(-444L)).start();
        new Thread(new ReadT()).start();
    }
}
```
``````

### 不能指令重排的指令

- 一个线程内语义的串行性
- `volatile` 写先于读，保证可见性
- 解锁先于加锁
- 线程的 `start()` 先于它的每个动作
- 线程操作先于 `Thread.join()`
- `interrupt()` 先于中断后的代码
- 构造函数先于 `finalize()`

## Java 并行程序基础

### 有关线程你必须知道的事

- 进程是线程的容器，线程是最基本的执行单元。
- 线程间的切换和调度的成本远远小于进程。

线程的几种基本状态，在 Thread 中的 State 枚举中定义了：

```{code-block} java
public enum State {
    NEW,            // 创建态：操作系统为新进程分配资源，创建 PCB
    RUNNABLE,       // 就绪态或运行态：等待 CPU 分配时间片
    BLOCKING,       // 阻塞态：因 synchronized 阻塞，等待解锁
    WAITING,        // 等待态：等待唤醒继续执行
    TIMED_WAITING,  // 超时等待态：等待唤醒或时间片到继续执行
    TERMINATED;     // 终止态：操作系统回收资源，撤销 PCB
}
```

```{figure} ../../../_static/images/java-thread.jpg

Java 线程状态图
```

### 初识线程：线程的基本操作

#### 新建线程

方法一：通过继承 `Thread` 类，重写 `run()` 方法。

```{code-block} java
public class NewThead {
    public static void main(String[] args) {
        Thread t1 = new Thread() {
            @Override
            public void run() {
                System.out.println("hello world");
            }
        };
        t1.start();
    }
}
```

方法二：通过实现 `Rannable` 接口。

```{code-block} java
public class NewThread2 implements Runnable {
    @Override
    public void run() {
        System.out.println("hello world");
    }
    public static void main(String[] args) {
        Thread t1 = new Thread(new NewThread2());
        t1.start();
    }
}
```

#### 终止线程

应当尽量避免使用 `stop()` 方法，它会强制线程终止，释放所有的锁，进而导致一些不一致性问题。

```{code-block} java
public class StopThread {
    public static User u = new User();
    
    public static class User {
        private int id;
        private String name;

        public int getId() {
            return this.id;
        }

        public String getName() {
            return this.name;
        }

        public void setId(int id) {
            this.id = id;
        }

        public void setName(String name) {
            this.name = name;
        }

        public User() {
            id = 0;
            name = "0";
        }

        @Override
        public String toString() {
            return "User [id=" + id + ", name=" + name + "]";
        }
    }

    public static class ChangeObjectThread extends Thread {
        @Override
        public void run() {
            while(true) {
                synchronized(u) {
                    int v = (int)(System.currentTimeMillis()/1000);
                    u.setId(v);
                    // Oh, do sth. else
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    u.setName(String.valueOf(v));
                }
                Thread.yield(); // 谦让出 CPU 的使用权，下次循环的时候再次竞争
            }
        }
    }

    public static class ReadObjcetThread extends Thread {
        @Override
        public void run() {
            while(true) {
                synchronized(u) {
                    if (u.getId() != Integer.parseInt(u.getName())) {
                        System.err.println(u.toString());
                    }
                }
                Thread.yield();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        new ReadObjcetThread().start();
        while(true) {
            Thread t = new ChangeObjectThread();
            t.start();
            Thread.sleep(150);
            t.stop(); // 不安全，运行时打印结果所示
        }
    }
}
```

更为稳妥的方式是，在需要终止的线程代码中，人工设置中断标志位，让其正常结束，而不是强制终止。

```{code-block} java
public class StopThread2 {
    public static User u = new User();
    
    public static class User {
        private int id;
        private String name;

        public int getId() {
            return this.id;
        }

        public String getName() {
            return this.name;
        }

        public void setId(int id) {
            this.id = id;
        }

        public void setName(String name) {
            this.name = name;
        }

        public User() {
            id = 0;
            name = "0";
        }

        @Override
        public String toString() {
            return "User [id=" + id + ", name=" + name + "]";
        }
    }

    public static class ChangeObjectThread extends Thread {
        // 设置标志位，以安全的方式终止线程
        volatile boolean stopme = false;
        
        public void stopMe() {
            stopme = true;
        }

        @Override
        public void run() {
            while(true) {
                // 检查标志位，是否应该停止
                if (stopme) {
                    System.out.println("Exit by stopMe()");
                    break;
                }

                synchronized(u) {
                    int v = (int)(System.currentTimeMillis()/1000);
                    u.setId(v);
                    // Oh, do sth. else
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    u.setName(String.valueOf(v));
                }
                Thread.yield();
            }
        }
    }

    public static class ReadObjcetThread extends Thread {
        @Override
        public void run() {
            while(true) {
                synchronized(u) {
                    if (u.getId() != Integer.parseInt(u.getName())) {
                        System.err.println(u.toString());
                    }
                }
                Thread.yield();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        new ReadObjcetThread().start();
        while(true) {
            // Thread t = new ChangeObjectThread(); // 多态不能通过编译检查，因为只能调用父类有的方法
            ChangeObjectThread t = new ChangeObjectThread();
            t.start();
            Thread.sleep(150);
            t.stopMe(); // 通过设置标志位安全地停止
        }
    }
    
}
```

#### 线程中断

JDK 对上述过程提供了更好的封装，以便我们可以直接拿来使用。

```{code-block} java
public void Thread.interrupt();             // 中断线程（这句话只是设置中断标志位，并不会让一个线程终止）
public boolean Thread.isInterrupted();      // 判断线程是否别中断
public static boolean Thread.interrupted(); // 判断是否被中断，并清除当前中断状态
```

没有根据中断标志做出响应，程序并不会停止。

```{code-block} java
public class InterruptThread {
    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread() {
            @Override
            public void run() {
                while(true) {
                    Thread.yield();
                }
            }
        };
        t1.start();
        Thread.sleep(2000);
        t1.interrupt(); // 只是设置了中断标志位，实际上程序并没有停止。
    }
}
```

下面的代码段对中断标志位进行了判断，然后终止了线程。

```{code-block} java
public class InterruptThread2{
    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread() {
            @Override
            public void run() {
                while(true) {
                    if (Thread.currentThread().isInterrupted()) {
                        break;
                    }

                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        System.out.println("在睡眠时被中断了，会清除中断标志位");
                        // 重新设置中断标志位
                        Thread.currentThread().interrupt();
                    }

                    Thread.yield();
                }
            }
        };

        t1.start();
        Thread.sleep(2000);
        t1.interrupt();
    }
    
}
```

#### 等待（wait）和通知（notify）

`wait()` 和 `notify()` 是由 `Object` 类产生的，所以，任何对象都可以调用。

我们可以把对象想象成临界资源，在某个线程内对临界资源调用 `wait()` 方法，表示等一会儿再才能进入临界区。在临界资源上调用 `notify()` 方法，它会在候选队列中随机选一个候选人，进入临界区。

`wait()` 和 `notify()` 必须在 `synchronized` 函数中才能使用。`synchronized` 函数包含的区域就是临界区。

```{code-block} java
public class NotifyThread {
    final static Object object = new Object(); // wait 和 notify 方法可以用于所有对象

    public static class T1 extends Thread {
        @Override
        public void run() {
            synchronized(object) {
                System.out.println(System.currentTimeMillis() + ": T1 启动了");

                try {
                    System.out.println(System.currentTimeMillis() + ": T1 等待某人唤醒");
                    object.wait(); // wait 释放 object 的锁了。
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                System.out.println(System.currentTimeMillis() + ": T1 被唤醒了，结束了");
            }
        }
    }

    public static class T2 extends Thread {
        @Override
        public void run() {
            synchronized(object) {
                System.out.println(System.currentTimeMillis() + ": T2 启动了，打算从队列中唤醒某个线程");

                object.notify(); // wait 和 notify 必须放在 synchronized 语句中才能生效
    
                System.out.println(System.currentTimeMillis() + ": T2 还要睡两秒，还没放弃锁");
    
                try {
                    Thread.sleep(2000); // sleep 不会放弃锁
                } catch (InterruptedException e) {
                    // e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) {
        Thread t1 = new T1();
        Thread t2 = new T2();
        t1.start();
        t2.start();
    }
}
```

#### 挂起（suspend）和继续执行（resume）线程

`suspend()` 和 `resume()` 是一个快要废弃的方法了，它们不安全，将会导致数据不一致性问题，如下代码所示。

```{code-block} java
public class BadSuspend {
    public static Object u = new Object();

    static ChangeObjectThread t1 = new ChangeObjectThread("t1");
    static ChangeObjectThread t2 = new ChangeObjectThread("t2");

    public static class ChangeObjectThread extends Thread {
        public ChangeObjectThread(String name) {
            super.setName(name);
        }

        @Override
        public void run() {
            synchronized(u) {
                System.out.println("in " + getName());
                Thread.currentThread().suspend(); // 挂起，但是不释放锁
            }
            System.out.println("线程" + getName() + "结束了");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        t1.start(); // t1 进入临界区，并挂起
        Thread.sleep(100); // main 线程睡眠 100 ms
        t2.start(); // t2 申请进入临界区，但是 t1 在临界区，无法进入
        t1.resume(); // t1 继续执行
        t2.resume(); // 实际上 t2 并没有解锁成功，因为 resume 先于 suspend 执行了
        t1.join(); // main 线程等待 t1 结束，实际上它正常结束了
        t2.join(); // main 线程等待 t2 结束，但是 t2 没有解锁成功，陷入了死锁
    }
}
```

如果非要使用，那么可以参考设置标志位的方式修改上面的代码。

```{code-block} java
public class GoodSuspend {
    public static Object u = new Object();

    public static class ChangeObjectThread extends Thread {
        // 通过设置标志位，让线程正常终止
        volatile boolean suspendme = false;

        public void suspendMe() {
            suspendme = true;
        }

        public void resumeMe() {
            suspendme = false;
            synchronized(this) {
                notify();
            }
        }

        @Override
        public void run() {
            while(true) {
                synchronized(this) {
                    while(suspendme) {
                        try {
                            wait();
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }

                synchronized(u) { // 两个线程竞争 u 的使用权
                    try {
                        System.out.println("in ChangeObjectThread");
                        Thread.sleep(500);
                    } catch (InterruptedException e) {

                    }
                }

                Thread.yield();
            }
        }
    }

    public static class ReadObjectThread extends Thread {
        @Override
        public void run() {
            while(true) {
                synchronized(u) { // 两个线程竞争 u 的使用权
                    try {
                        System.out.println("in ReadObjectThread");
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        
                    }
                }

                Thread.yield();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ChangeObjectThread t1 = new ChangeObjectThread();
        ReadObjectThread t2 = new ReadObjectThread();

        t1.start();
        t2.start();

        Thread.sleep(1000);

        System.out.println("t1 挂起 4 秒，下面 4 秒只有 t2 在执行");
        t1.suspendMe();
        Thread.sleep(4000);

        System.out.println("继续执行 t1 两个线程争抢 CPU 资源");
        t1.resumeMe();
    }
}
```

#### 等待线程结束（join）和谦让（yield）

`t1.join()` 是等待线程 `t1` 结束。

```{code-block} java
public class JoinThread {
    public volatile static int i = 0;

    public static class AddThread extends Thread {
        @Override
        public void run() {
            for (i = 0; i < 10000000; i++);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        AddThread t1 = new AddThread();
        t1.start();
        t1.join(); // main 线程等待 t1 线程执行完毕
        System.out.println(i); // 因此结果总是 10000000
    }
}
```

谦让（`yield`）是指让出 CPU 的使用权，前面很多代码段都有用到。

### volatile 和 Java 内存模型（JMM）

### 分门别类的管理：线程组

### 驻守后台：守护线程（Daemon）

### 先干重要的事：线程优先级

### 线程安全的概念与 synchronized

### 程序中的幽灵：隐蔽的错误

#### 无提示的错误案例

#### 并发下的 ArrayList

#### 并发下诡异的 HashMap

#### 初学者常见问题：错误的加锁

## JDK 并发包

### 多线程的团队协作：同步控制

#### synchronized 的功能扩展：重入锁

#### 重入锁的好搭档：Condition 条件

#### 允许多个线程同时访问：信号量（Semaphore）

#### ReadWriteLock 读写锁

#### 倒计时器：CountDownLatch

#### 循环栅栏：CyclicBarrier

#### 线程阻塞工具类：LockSupport

### 线程复用：线程池

#### 什么是线程池

#### 不要重复发明轮子：JDK 对线程池的支持

#### 线程池的内部实现

#### 超负载了怎么办：拒绝策略

#### 自定义线程创建：ThreadFactory

#### 我的应用我做主：扩展线程池

#### 合理的选择：优化线程池中的线程数量

#### 堆栈去哪里了：在线程池中寻找堆栈

#### 分而治之：Fork/Join 框架

### 不要重复发明轮子：JDK 的并发容器

#### 超好用的工具类：并发集合简介

#### 线程安全的 HashMap

#### 有关 List 的线程安全

#### 高效读写的队列：深度剖析 ConcurrentLinkedQueue

#### 不变模式下的 CopyOnWriteArrayList

#### 数据共享通道：BlockingQueue

#### 随机数据结构：跳表（SkipList）
