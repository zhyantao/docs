==============
Java I/O 系统
==============

作者在这一章的描述，看起来像是在教我们如何使用工具，但是本章中涉及到很多类。
如果你没有捋清楚它们之间的关系，看起来还是比较费劲。看着看着，可能就迷糊了。

因此，我们还是首先对类之间的关系做一下梳理。

.. hint:: 

    流，代表任何有能力产出数据的数据源对象或者是有能力接收数据的接收端对象。

    - InputStream 和 OutputStream 的派生类用来处理 **字节流** ；
    - Reader 和 Writer 的派生类用来处理 **字符流** 。

InputStream
------------

.. uml::

    @startuml

    abstract InputStream {
        abstract int read()
    }

    class ByteArrayInputStream
    class FileInputStream
    class FilterInputStream
    class ObjectInputStream
    class PipedInputStream
    class SequenceInputStream
    class StringBufferInputStream
    class DataInputStream
    class BufferedInputStream

    InputStream <|-- ByteArrayInputStream
    InputStream <|-- FileInputStream
    InputStream <|-- FilterInputStream
    InputStream <|-- ObjectInputStream
    PipedInputStream --|> InputStream
    SequenceInputStream --|> InputStream
    StringBufferInputStream --|> InputStream
    FilterInputStream <|-- DataInputStream
    FilterInputStream <|-- BufferedInputStream

    @enduml

OutputStream
-------------

.. uml::

    @startuml

    abstract OutputStream {
        abstract void write()
    }

    class ByteArrayOutputStream
    class FileOutputStream
    class FilterOutputStream
    class ObjectOutputStream
    class PipedOutputStream
    class DataOutputStream
    class BufferedOutputStream
    class PrintStream

    ByteArrayOutputStream --|> OutputStream
    OutputStream <|-- FileOutputStream
    OutputStream <|-- FilterOutputStream
    OutputStream <|-- ObjectOutputStream
    PipedOutputStream --|> OutputStream
    FilterOutputStream <|-- DataOutputStream
    FilterOutputStream <|-- BufferedOutputStream
    FilterOutputStream <|-- PrintStream
    
    @enduml

Reader
------

.. uml::

    @startuml

    abstract Reader {
        abstract int read()
        abstract void close()
    }

    class BufferedReader
    class CharArrayReader
    class FilterReader
    class InputStreamReader
    class PipedReader
    class StringReader
    class URLReader
    class FileReader

    Reader <|-- BufferedReader
    Reader <|-- CharArrayReader
    Reader <|-- FilterReader
    Reader <|-- InputStreamReader
    PipedReader --|> Reader
    StringReader --|> Reader
    URLReader --|> Reader
    InputStreamReader <|-- FileReader
    
    @enduml

.. hint:: InputStreamReader 可以把 InputStream 转化为 Reader

Writer
------

.. uml::

    @startuml

    abstract Writer {
        abstract int write()
        abstract void flush()
        abstract void close()
    }

    class BufferedWriter
    class CharArrayWriter
    class FilterWriter
    class OutputStreamWriter
    class PipedWriter
    class StringWriter

    Writer <|-- BufferedWriter
    Writer <|-- CharArrayWriter
    Writer <|-- FilterWriter
    Writer <|-- OutputStreamWriter
    PipedWriter --|> Writer
    StringWriter --|> Writer
    
    @enduml

.. hint:: OutputStreamWriter 可以把 OutputStream 转化为 Writer

文件读写的实用工具
------------------

目录列表器
~~~~~~~~~~

用于查看一个目录下有哪些文件，编译运行下面的代码：

- 如果不带参数，查看一个完整目录列表
- 如果带参数，可以用正则表达式来进行条件筛选。

下面代码中实现了接口的 ``accept()`` 方法。 ``DirFilter`` 这个类存在的唯一原因就是 ``accept()`` 方法，
目的是把 ``accept()`` 方法提供给 ``list()`` 使用，使 ``list()`` 可以回调 ``accept()`` ，进而以决定那些文件包含在列表中。

.. code-block:: java

    //: io/DirList.java
    // Display a directory listing using regular expressions.
    // {Args: "D.*\.java"}
    import java.util.regex.*;
    import java.io.*;
    import java.util.*;

    public class DirList {
        public static void main(String[] args) {
            File path = new File(".");
            String[] list;
            if(args.length == 0)
                list = path.list();
            else
                list = path.list(new DirFilter(args[0]));
            Arrays.sort(list, String.CASE_INSENSITIVE_ORDER);
            for(String dirItem : list)
                System.out.println(dirItem);
        }
    }

    class DirFilter implements FilenameFilter {
        private Pattern pattern;
        public DirFilter(String regex) {
            pattern = Pattern.compile(regex);
        }
        public boolean accept(File dir, String name) {
            return pattern.matcher(name).matches();
        }
    } /* Output:
    DirectoryDemo.java
    DirList.java
    DirList2.java
    DirList3.java
    *///:~

上面代码中的 ``DirFilter`` 类很适合用匿名内部类来实现，如下：

.. admonition:: DirList3.java
    :class: dropdown

    .. code-block:: java

        //: io/DirList3.java
        // Building the anonymous inner class "in-place."
        // {Args: "D.*\.java"}
        import java.util.regex.*;
        import java.io.*;
        import java.util.*;

        public class DirList3 {
            public static void main(final String[] args) {
                File path = new File(".");
                String[] list;
                if(args.length == 0)
                    list = path.list();
                else
                    list = path.list(new FilenameFilter() {
                        private Pattern pattern = Pattern.compile(args[0]);
                        public boolean accept(File dir, String name) {
                            return pattern.matcher(name).matches();
                        }
                    });
                Arrays.sort(list, String.CASE_INSENSITIVE_ORDER);
                for(String dirItem : list)
                    System.out.println(dirItem);
            }
        } /* Output:
        DirectoryDemo.java
        DirList.java
        DirList2.java
        DirList3.java
        *///:~

    .. hint:: 使用匿名内部类的方式不便于阅读，因此需要谨慎使用。

目录的检查及创建
~~~~~~~~~~~~~~~~

``File`` 对象也可以用来创建新的目录或尚不存在的完整的目录路径。

.. admonition:: MakeDirectories.java
    :class: dropdown

    .. code-block:: java

        //: io/MakeDirectories.java
        // Demonstrates the use of the File class to
        // create directories and manipulate files.
        // {Args: MakeDirectoriesTest}
        import java.io.*;

        public class MakeDirectories {
            private static void usage() {
                System.err.println(
                    "Usage:MakeDirectories path1 ...\n" +
                    "Creates each path\n" +
                    "Usage:MakeDirectories -d path1 ...\n" +
                    "Deletes each path\n" +
                    "Usage:MakeDirectories -r path1 path2\n" +
                    "Renames from path1 to path2");
                System.exit(1);
            }
            private static void fileData(File f) {
                System.out.println(
                    "Absolute path: " + f.getAbsolutePath() +
                    "\n Can read: " + f.canRead() +
                    "\n Can write: " + f.canWrite() +
                    "\n getName: " + f.getName() +
                    "\n getParent: " + f.getParent() +
                    "\n getPath: " + f.getPath() +
                    "\n length: " + f.length() +
                    "\n lastModified: " + f.lastModified());
                if(f.isFile())
                    System.out.println("It's a file");
                else if(f.isDirectory())
                    System.out.println("It's a directory");
            }
            public static void main(String[] args) {
                if(args.length < 1) usage();
                if(args[0].equals("-r")) {
                    if(args.length != 3) usage();
                    File
                        old = new File(args[1]),
                        rname = new File(args[2]);
                    old.renameTo(rname);
                    fileData(old);
                    fileData(rname);
                    return; // Exit main
                }
                int count = 0;
                boolean del = false;
                if(args[0].equals("-d")) {
                    count++;
                    del = true;
                }
                count--;
                while(++count < args.length) {
                    File f = new File(args[count]);
                    if(f.exists()) {
                        System.out.println(f + " exists");
                        if(del) {
                            System.out.println("deleting..." + f);
                            f.delete();
                        }
                    }
                    else { // Doesn't exist
                        if(!del) {
                            f.mkdirs();
                            System.out.println("created " + f);
                        }
                    }
                    fileData(f);
                }
            }
        } /* Output: (80% match)
        created MakeDirectoriesTest
        Absolute path: d:\aaa-TIJ4\code\io\MakeDirectoriesTest
        Can read: true
        Can write: true
        getName: MakeDirectoriesTest
        getParent: null
        getPath: MakeDirectoriesTest
        length: 0
        lastModified: 1101690308831
        It's a directory
        *///:~

缓冲输入文件
~~~~~~~~~~~~

为了提高速度，我们希望使用缓冲读取文件。

.. code-block:: java
    :emphasize-lines: 14

    //: io/BufferedInputFile.java
    import java.io.*;

    public class BufferedInputFile {
        // Throw exceptions to console:
        public static String
        read(String filename) throws IOException {
            // Reading input by lines:
            BufferedReader in = new BufferedReader(
                new FileReader(filename));
            String s;
            StringBuilder sb = new StringBuilder();
            while((s = in.readLine())!= null)
                sb.append(s + "\n");
            in.close();
            return sb.toString();
        }
        public static void main(String[] args)
        throws IOException {
            System.out.print(read("BufferedInputFile.java"));
        }
    } /* (Execute to see output) *///:~

注意，第 14 行必须添加换行符，因为 ``readLine()`` 已将它们删掉。

读取文件
~~~~~~~~

读取文件可以使用多种方式：

- 使用 ``StringReader`` （字符流方式）
- 使用 ``ByteArrayInputStream`` （字节流方式）

字符流方式如下：

.. code-block:: java
    :emphasize-lines: 11

    //: io/MemoryInput.java
    import java.io.*;

    public class MemoryInput {
        public static void main(String[] args)
        throws IOException {
            StringReader in = new StringReader(
                BufferedInputFile.read("MemoryInput.java"));
            int c;
            while((c = in.read()) != -1)
                System.out.print((char)c);
        }
    } /* (Execute to see output) *///:~

注意，第 11 行 ``read()`` 是以 int 形式返回下一字节，因此必须转型为 char 才能正确打印。

字节流方式如下：

.. code-block:: java
    :emphasize-lines: 12

    //: io/FormattedMemoryInput.java
    import java.io.*;

    public class FormattedMemoryInput {
        public static void main(String[] args)
        throws IOException {
            try {
                DataInputStream in = new DataInputStream(
                    new ByteArrayInputStream(
                    BufferedInputFile.read(
                        "FormattedMemoryInput.java").getBytes()));
                while(true)
                    System.out.print((char)in.readByte());
            } catch(EOFException e) {
                System.err.println("End of stream");
            }
        }
    } /* (Execute to see output) *///:~

注意，第 12 行代码，是用异常来终止循环的。因为对于 ``readByte()`` 方法来讲，任何字节的值都是合法的结果，返回值不能用来检测输入是否结束。

或者一次一个字节第读取文件：

.. code-block:: java
    :emphasize-lines: 11

    //: io/TestEOF.java
    // Testing for end of file while reading a byte at a time.
    import java.io.*;

    public class TestEOF {
        public static void main(String[] args)
        throws IOException {
            DataInputStream in = new DataInputStream(
                new BufferedInputStream(
                    new FileInputStream("TestEOF.java")));
            while(in.available() != 0)
                System.out.print((char)in.readByte());
        }
    } /* (Execute to see output) *///:~

注意，第 11 行代码，没有用异常来终止循环，而是用 ``available()`` 来检测可供提取的字符数的。

输出到文件
~~~~~~~~~~

首先，创建一个与指定文件连接的 ``FileWriter`` ，通常，我们会用 ``BufferedWriter`` 将其包装起来用以缓冲输出。
在本例中，为了提供格式化机制，它被装饰成了 ``PrintWriter`` 。按照这种方式创建的数据文件可以作为普通文本文件读取。

.. code-block:: java
    :emphasize-lines: 17

    //: io/BasicFileOutput.java
    import java.io.*;

    public class BasicFileOutput {
        static String file = "BasicFileOutput.out";
        public static void main(String[] args)
        throws IOException {
            BufferedReader in = new BufferedReader(
                new StringReader(
                    BufferedInputFile.read("BasicFileOutput.java")));
            PrintWriter out = new PrintWriter(
                new BufferedWriter(new FileWriter(file)));
            int lineCount = 1;
            String s;
            while((s = in.readLine()) != null )
                out.println(lineCount++ + ": " + s);
            out.close();
            // Show the stored file:
            System.out.println(BufferedInputFile.read(file));
        }
    } /* (Execute to see output) *///:~

我们看到要为 out 显式调用 ``close()`` 。如果我们不为所有的输出文件调用 ``close()`` ，就会发现缓冲区内容不会被刷新清空，那么它们也就不完整。

读写随机访问文件
~~~~~~~~~~~~~~~~

使用 RandomAccessFile 利用 ``seek()`` 可以在文件中到处移动，并修改文件中的某个值。在使用 RandomAccessFile 时，你必须知道文件排版，这样才能正确操作它。
RandomAccessFile 拥有读取基本类型和 UTF-8 字符串的各种具体方法。

.. code-block:: java
    :emphasize-lines: 23

    //: io/UsingRandomAccessFile.java
    import java.io.*;

    public class UsingRandomAccessFile {
        static String file = "rtest.dat";
        static void display() throws IOException {
            RandomAccessFile rf = new RandomAccessFile(file, "r");
            for(int i = 0; i < 7; i++)
                System.out.println(
                    "Value " + i + ": " + rf.readDouble());
            System.out.println(rf.readUTF());
            rf.close();
        }
        public static void main(String[] args)
        throws IOException {
            RandomAccessFile rf = new RandomAccessFile(file, "rw");
            for(int i = 0; i < 7; i++)
                rf.writeDouble(i*1.414);
            rf.writeUTF("The end of the file");
            rf.close();
            display();
            rf = new RandomAccessFile(file, "rw");
            rf.seek(5*8);
            rf.writeDouble(47.0001);
            rf.close();
            display();
        }
    } /* Output:
    Value 0: 0.0
    Value 1: 1.414
    Value 2: 2.828
    Value 3: 4.242
    Value 4: 5.656
    Value 5: 7.069999999999999
    Value 6: 8.484
    The end of the file
    Value 0: 0.0
    Value 1: 1.414
    Value 2: 2.828
    Value 3: 4.242
    Value 4: 5.656
    Value 5: 47.0001
    Value 6: 8.484
    The end of the file
    *///:~

注意，第 23 行，因为 double 总是 8 字节长，所以为了用 ``seek()`` 查找第 5 个双精度值，你只需用 5*8 来产生查找位置。

读取二进制文件
~~~~~~~~~~~~~~

.. code-block:: java

    //: net/mindview/util/BinaryFile.java
    // Utility for reading files in binary form.
    package net.mindview.util;
    import java.io.*;

    public class BinaryFile {
        public static byte[] read(File bFile) throws IOException{
            BufferedInputStream bf = new BufferedInputStream(
                new FileInputStream(bFile));
            try {
                byte[] data = new byte[bf.available()];
                bf.read(data);
                return data;
            } finally {
                bf.close();
            }
        }
        public static byte[] read(String bFile) throws IOException {
            return read(new File(bFile).getAbsoluteFile());
        }
    } ///:~

标准 I/O
---------

从标准输入中读取
~~~~~~~~~~~~~~~~

- ``System.out`` 和 ``System.err`` 已经被包装成了 PrintStream
- ``System.in`` 没有经过包装

这意味着我们可以立即使用 ``System.out`` 和 ``System.err`` 但是在读取 ``System.in`` 之前必须对其进行包装。

通常我们会用 ``readLine()`` 一次一行地读取输入，为此，我们将 ``System.in`` 包装成 ``BufferedReader`` 来使用。
这要求我们必须用 ``InputStreamReader`` 把 ``System.in`` 转换为 ``Reader`` 。

.. code-block:: java

    //: io/Echo.java
    // How to read from standard input.
    // {RunByHand}
    import java.io.*;

    public class Echo {
        public static void main(String[] args)
        throws IOException {
            BufferedReader stdin = new BufferedReader(
                new InputStreamReader(System.in));
            String s;
            while((s = stdin.readLine()) != null && s.length()!= 0)
                System.out.println(s);
            // An empty line or Ctrl-Z terminates the program
        }
    } ///:~

.. note:: 文中多次提到“包装”这个概念，最简单直接的理解就是：把一个类或对象传入外层类的构造器。

将 System.out 转换成 PrintWriter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

跟类型转换很像，在外层用对象的构造器包裹一下。

.. code-block:: java

    //: io/ChangeSystemOut.java
    // Turn System.out into a PrintWriter.
    import java.io.*;

    public class ChangeSystemOut {
        public static void main(String[] args) {
            PrintWriter out = new PrintWriter(System.out, true);
            out.println("Hello, world");
        }
    } /* Output:
    Hello, world
    *///:~

标准 I/O 重定向
~~~~~~~~~~~~~~~

.. code-block:: java
    :emphasize-lines: 14-16

    //: io/Redirecting.java
    // Demonstrates standard I/O redirection.
    import java.io.*;

    public class Redirecting {
        public static void main(String[] args)
        throws IOException {
            PrintStream console = System.out;
            BufferedInputStream in = new BufferedInputStream(
                new FileInputStream("Redirecting.java"));
            PrintStream out = new PrintStream(
                new BufferedOutputStream(
                    new FileOutputStream("test.out")));
            System.setIn(in);
            System.setOut(out);
            System.setErr(out);
            BufferedReader br = new BufferedReader(
                new InputStreamReader(System.in));
            String s;
            while((s = br.readLine()) != null)
                System.out.println(s);
            out.close(); // Remember this!
            System.setOut(console);
        }
    } ///:~

注意，程序开头处存储了对最初 ``System.out`` 对象的引用，并且在结尾处将系统输出恢复到了该对象上。

I/O 重定向操纵的是字节流，而不是字符流，因此我们使用的是 ``InputStream`` 和 ``OutputStream`` 而不是 ``Reader`` 和 ``Writer`` 。

进程控制
--------

进程控制常见的任务是：我们想在程序中执行命令行，并把结果打印出来。

要想运行一个程序，只需要向 ``OSExecute.command()`` 传递一个 command 字符串，它与以在控制台上运行该程序所键入的命令相同。

.. code-block:: java

    //: net/mindview/util/OSExecute.java
    // Run an operating system command
    // and send the output to the console.
    package net.mindview.util;
    import java.io.*;

    public class OSExecute {
        public static void command(String command) {
            boolean err = false;
            try {
                Process process =
                    new ProcessBuilder(command.split(" ")).start();
                BufferedReader results = new BufferedReader(
                    new InputStreamReader(process.getInputStream()));
                String s;
                while((s = results.readLine())!= null)
                    System.out.println(s);
                BufferedReader errors = new BufferedReader(
                    new InputStreamReader(process.getErrorStream()));
                // Report errors and return nonzero value
                // to calling process if there are problems:
                while((s = errors.readLine())!= null) {
                    System.err.println(s);
                    err = true;
                }
            } catch(Exception e) {
                // Compensate for Windows 2000, which throws an
                // exception for the default command line:
                if(!command.startsWith("CMD /C"))
                    command("CMD /C " + command);
                else
                    throw new RuntimeException(e);
            }
            if(err)
                throw new OSExecuteException("Errors executing " +
                    command);
        }
    } ///:~

下面的代码段展示如何使用上面的代码段：

.. code-block:: java

    //: io/OSExecuteDemo.java
    // Demonstrates standard I/O redirection.
    import net.mindview.util.*;

    public class OSExecuteDemo {
        public static void main(String[] args) {
            OSExecute.command("javap OSExecuteDemo");
        }
    } /* Output:
    Compiled from "OSExecuteDemo.java"
    public class OSExecuteDemo extends java.lang.Object{
            public OSExecuteDemo();
            public static void main(java.lang.String[]);
    }
    *///:~

注意，这里的异常是自定义的：

.. code-block:: java

    //: net/mindview/util/OSExecuteException.java
    package net.mindview.util;

    public class OSExecuteException extends RuntimeException {
        public OSExecuteException(String why) { super(why); }
    } ///:~

新 I/O
-------

目的在于提高速度。速度的提高来自于所使用的结构更接近于操作系统执行 I/O 的方式：通道和缓冲器。

- 唯一直接与通道交互的缓冲器是 ``ByteBuffer`` ；
- ``Reader`` 和 ``Writer`` 这种字符模式类不能用于产生通道；
- ``java.nio.channels.Channels`` 可以在通道中产生 ``Reader`` 和 ``Writer`` 。

通道是一个相当基础的东西：可以向它传送用于读写的 ``ByteBuffer`` ，并且可以锁定文件的某些区域用于独占式访问。

创建通道
~~~~~~~~

下面的代码创建了三种类型的通道：1、可写；2、可读可写；3、可读。

.. code-block:: java

    //: io/GetChannel.java
    // Getting channels from streams
    import java.nio.*;
    import java.nio.channels.*;
    import java.io.*;

    public class GetChannel {
        private static final int BSIZE = 1024;
        public static void main(String[] args) throws Exception {
            // Write a file:
            FileChannel fc =
                new FileOutputStream("data.txt").getChannel();
            fc.write(ByteBuffer.wrap("Some text ".getBytes()));
            fc.close();
            // Add to the end of the file:
            fc =
                new RandomAccessFile("data.txt", "rw").getChannel();
            fc.position(fc.size()); // Move to the end
            fc.write(ByteBuffer.wrap("Some more".getBytes()));
            fc.close();
            // Read the file:
            fc = new FileInputStream("data.txt").getChannel();
            ByteBuffer buff = ByteBuffer.allocate(BSIZE);
            fc.read(buff);
            buff.flip();
            while(buff.hasRemaining())
                System.out.print((char)buff.get());
        }
    } /* Output:
    Some text Some more
    *///:~

- ``getChannel()`` 会产生一个 ``FileChannel`` ；
- ``warp()`` 将已存在的字节数组“包装”到 ``ByteBuffer`` 中，也可以使用 ``put()`` 方法填充 ``ByteBuffer`` ；
- 对于只读访问，必须显式地使用静态的 ``allocate()`` 方法来分配 ``ByteBuffer`` ；
- 一旦调用 ``read()`` 来告知 ``FileChannel`` 向 ``ByteBuffer`` 存储字节，就必须调用缓冲器上的 ``flip()`` 。

用通道复制文件
~~~~~~~~~~~~~

.. code-block:: java

    //: io/ChannelCopy.java
    // Copying a file using channels and buffers
    // {Args: ChannelCopy.java test.txt}
    import java.nio.*;
    import java.nio.channels.*;
    import java.io.*;

    public class ChannelCopy {
        private static final int BSIZE = 1024;
        public static void main(String[] args) throws Exception {
            if(args.length != 2) {
                System.out.println("arguments: sourcefile destfile");
                System.exit(1);
            }
            FileChannel
                in = new FileInputStream(args[0]).getChannel(),
                out = new FileOutputStream(args[1]).getChannel();
            ByteBuffer buffer = ByteBuffer.allocate(BSIZE);
            while(in.read(buffer) != -1) {
                buffer.flip(); // Prepare for writing
                out.write(buffer);
                buffer.clear();    // Prepare for reading
            }
        }
    } ///:~

更理想的方式是使用方法 transferTo() 和 transferFrom() 将通道直接相连：

.. code-block:: java

    //: io/TransferTo.java
    // Using transferTo() between channels
    // {Args: TransferTo.java TransferTo.txt}
    import java.nio.channels.*;
    import java.io.*;

    public class TransferTo {
        public static void main(String[] args) throws Exception {
            if(args.length != 2) {
                System.out.println("arguments: sourcefile destfile");
                System.exit(1);
            }
            FileChannel
                in = new FileInputStream(args[0]).getChannel(),
                out = new FileOutputStream(args[1]).getChannel();
            in.transferTo(0, in.size(), out);
            // Or:
            // out.transferFrom(in, 0, in.size());
        }
    } ///:~



压缩
----
对象序列化
----------
XML
---
Preferences
------------
