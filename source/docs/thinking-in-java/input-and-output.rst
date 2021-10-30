==============
Java I/O 系统
==============

File 类
--------

``File`` 类实际上叫做 ``FilePath`` 类更合适，它返回的是一个路径。

``File`` 既可以代表一个特定文件的名称，也可以代表一个目录下的一组文件的名称。
如果是一组文件，可以对这个集合调用 ``list()`` 方法，它将返回一个字符数组。

目录列表器
~~~~~~~~~~

编译运行下面的文件：

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

输入和输出
----------

流，代表任何有能力产出数据的数据源对象或者是有能力接收数据的接收端对象。“流”屏蔽了实际的 I/O 设备中处理数据的细节。

任何自 ``InputStream`` 或 ``Reader`` 派生来的类都有 ``read()`` 方法，用于读取单个字节或字节数组。

任何自 ``OutputStream`` 或 ``Writer`` 派生而来的类都有 ``write()`` 方法，用于写单个字节或字节数组。

但是我们通常不会用到这些方法，它们之所以存在是因为别的类可以使用它们，以便提供更有用的接口。
因此我们很少使用单一的类来创建流对象，而是通过叠加多个对象来提供所期望的功能（这是装饰器设计模式）。

InputStream 可以接收的数据源包括：

- 字节数组： ``ByteArrayInputStream``
- String 对象： ``StringBufferInputStream``
- 文件： ``FileInputStream``
- 管道： ``PipedInputStream``
- 一种由其他种类的流组成的序列，以便我们可以将它们收集合并到一个流内： ``SequenceInputStream``
- 其他数据源，如 Internet 连接等
- ``FileInputStream``

OutputStream 可以接收的数据源包括：

- 字节数组： ``ByteArrayInputStream``
- 文件： ``FileInputStream``
- 管道： ``PipedInputStream``
- ``FileInputStream``

添加属性和有用的接口
--------------------



Reader 和 Writer
-----------------
自我独立的类：RandomAccessFile
------------------------------
I/O 流的典型使用方式
--------------------
文件读写的实用工具
------------------
标准 I/O
---------
进程控制
--------
新 I/O
-------
压缩
----
对象序列化
----------
XML
---
Preferences
------------
