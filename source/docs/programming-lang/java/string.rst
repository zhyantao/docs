=======
字符串
=======

不可变 String
-------------

``String`` 对象是不可变的（只读的）。 ``String`` 类中每一个看起来会修改 ``String`` 值的方法，实际上都是创建了一个全新的 ``String`` 对象，以包含修改后的字符串内容。

把 ``String`` 对象作为方法的参数时，都会复制一份引用。

重载 “+” 与 StringBuilder
--------------------------

用于 ``String`` 的 “+” 和 “+=” 是 Java 中仅有的两个重载过的操作符，而 Java 并不允许程序员重载任何操作符。

“+” 可以用来拼接字符串。

创建字符串时，显式地声明 ``StringBuilder`` 相比于让编译器自动调用 ``StringBuilder`` 的方法 ``append()`` 将会更加高效。 

因为编译器自动调用 ``StringBuilder.append()`` 方法时，可能会多次构建对象并分配缓存，而显式地声明后，可以只生成一个 ``StringBuilder`` 对象。

因此，当你为一个类编写 ``toString()`` 方法时，如果字符串比较简单，那就可以信赖编译器。但是，如果你要在 ``toString()`` 方法中使用循环，那最好自己创建一个 ``StringBuilder`` 对象。

.. code-block:: java

    //: strings/WhitherStringBuilder.java

    public class WhitherStringBuilder {
        public String implicit(String[] fields) {
            String result = "";
            for(int i = 0; i < fields.length; i++)
                result += fields[i];
            return result;
        }
        public String explicit(String[] fields) {
            StringBuilder result = new StringBuilder();
            for(int i = 0; i < fields.length; i++)
                result.append(fields[i]);
            return result.toString();
        }
    } ///:~

.. note:: 

    可以使用 ``javap -c WhitherStringBuilder`` 来进行反编译，查看编译后的代码。

无意识的递归
------------

Java 中的每个类都是继承自 ``Object`` ，标准容器类也不例外。因此每个容器类都有 ``toString()`` 方法，并且覆写了该方法，使得它生成的 ``String`` 对象能够表达容器自身，以及容器所包含的对象。

例如 ``ArrayList.toString()`` 会 **遍历** ``ArrayList`` 中包含的所有对象，调用每个元素上的 ``toString()`` 方法。

如果你希望 ``toString()`` 方法打印出对象的内存地址。
不可以使用 ``this.toString()`` ，因为在打印语句中会强制 ``InfiniteRecursion`` 对象转型为 ``String`` 但是有没有提供实现。
但是，可以使用 ``InfiniteRecursion`` 的父类 ``Object`` 中的 ``toString()`` 方法，
因此正确的做法时使用 ``super.toString()`` 方法来打印对象的内存地址。

.. code-block:: java

    //: strings/InfiniteRecursion.java
    // Accidental recursion.
    // {RunByHand}
    import java.util.*;

    public class InfiniteRecursion {
        public String toString() {
            return " InfiniteRecursion address: " + super.toString() + "\n";
        }
        public static void main(String[] args) {
            List<InfiniteRecursion> v =
                new ArrayList<InfiniteRecursion>();
            for(int i = 0; i < 10; i++)
                v.add(new InfiniteRecursion());
            System.out.println(v);
        }
    } ///:~

String 上的操作
----------------

.. csv-table::
    :header: "方法", "参数，重载版本", "作用"
    :widths: 15,40,40

    "构造方法", "默认版本， ``String`` ， ``StringBuilder`` ， ``StringBuffer`` ， ``char`` 数组， ``byte`` 数组", "创建 ``String`` 对象"
    "``length()``", "", "``String`` 中字符的个数"
    "``charAt()``", "``int`` 索引", "获取 ``String`` 中索引位置上的 ``char`` "
    "``getChars()``，``getBytes()``", "待复制部分的开始和结束索引，复制的目标数组，目标数组的开始索引", "复制 ``char`` 或 ``byte`` 到一个目标数组中"
    "``toCharArray()``", "", "生成一个 ``char[]`` ，包含 ``String`` 中的所有字符"
    "``equals()``，``equalsIgnoreCase()``", "与之进行比较的 ``String`` ", "比较两个 ``String`` 的内容是否相同。如果相同，结果为 ``true`` "
    "``compareTo()``，``compareToIgnoreCase()``", "与之进行比较的 ``String`` ", "按词典顺序比较 ``String`` 的内容，比较结果为负数、零或正数。注意，大小写不等价"
    "``contains()``", "要搜索的 ``CharSequence`` ", "如果该 ``String`` 对象包含参数的内容，则返回 ``true`` "
    "``contentEquals()``", "与之进行比较的 ``CharSequence`` 或 ``StringBuffer``", "如果该 ``String`` 对象与参数的内容完全一致，则返回 ``true`` "
    "``isEmpty()``", "", "返回 ``boolean`` 结果，以表明 ``String`` 对象的长度是否为0"
    "``regionMatches()``", "该 ``String`` 的索引偏移量，另一个 ``String`` 及其索引偏移量，要比较的长度。重载版本增加了“忽略大小写”功能", "返回 ``boolean`` 结果，以表明所比较区域是否相等"
    "``startsWith()``", "可能的起始 ``String`` 。重载版本在参数中增加了偏移量", "返回 ``boolean`` 结果，以表明该 ``String`` 是否以传入参数开始"
    "``endsWith()``", "该 ``String`` 可能的后缀 ``String`` ", "返回 ``boolean`` 结果，以表明此参数是否是该字符串的后缀"
    "``indexOf()``，``lastIndexOf()``", "重载版本包括： ``char`` ， ``char`` 与起始索引， ``String`` ， ``String`` 与起始索引", "如果该 ``String`` 并不包含此参数，就返回-1；否则返回此参数在 ``String`` 中的起始索引。 ``lastIndexOf()`` 是从后往前搜索"
    "``matches()``", "一个正则表达式", "返回 ``boolean`` 结果，以表明该 ``String`` 和给出的正则表达式是否匹配"
    "``split()``", "一个正则表达式。可选参数为需要拆分的最大数量", "按照正则表达式拆分 ``String`` ，返回一个结果数组"
    "``join()`` （Java8引入的）", "分隔符，待拼字符序列。用分隔符将字符序列拼接成一个新的 ``String`` ", "用分隔符拼接字符片段，产生一个新的 ``String`` "
    "``substring()`` （即 ``subSequence()`` ）", "重载版本：起始索引；起始索引+终止索引", "返回一个新的 ``String`` 对象，以包含参数指定的子串"
    "``concat()``", "要连接的 ``String`` ", "返回一个新的 ``String`` 对象，内容为原始 ``String`` 连接上参数 ``String`` "
    "``replace()``", "要替换的字符，用来进行替换的新字符。也可以用一个 ``CharSequence`` 替换另一个 ``CharSequence`` ", "返回替换字符后的新 ``String`` 对象。如果没有替换发生，则返回原始的 ``String`` 对象"
    "``replaceFirst()``", "要替换的正则表达式，用来进行替换的 ``String`` ", "返回替换首个目标字符串后的 ``String`` 对象"
    "``replaceAll()``", "要替换的正则表达式，用来进行替换的 ``String`` ", "返回替换所有目标字符串后的 ``String`` 对象"
    "``toLowerCase()``，``toUpperCase()``", "", "将字符的大小写改变后，返回一个新的 ``String`` 对象。如果没有任何改变，则返回原始的 ``String`` 对象"
    "``trim()``", "", "将 ``String`` 两端的空白符删除后，返回一个新的 ``String`` 对象。如果没有任何改变，则返回原始的 ``String`` 对象"
    "``valueOf()``（``static``）", "重载版本：``Object``；``char[]``；``char[]``，偏移量，与字符个数； ``boolean`` ； ``char`` ；``int``；``long``；``float``；``double``", "返回一个表示参数内容的 ``String`` "
    "``intern()``", "", "为每个唯一的字符序列生成一个且仅生成一个 ``String`` 引用"
    "``format()``", "要格式化的字符串，要替换到格式化字符串的参数", "返回格式化结果 ``String``"

格式化输出
-----------

printf()
~~~~~~~~~~

.. code-block:: java

    printf("Row 1: [%d, %f]\n", x, y);

System.out.format()
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    System.out.format("Row 1: [%d, %f]\n", x, y);

Formatter 类
~~~~~~~~~~~~~~

利用 ``Formatter`` 类时，需要指定想要将结果输出到哪里。

.. code-block:: java

    //: strings/Turtle.java
    import java.io.*;
    import java.util.*;

    public class Turtle {
        private String name;
        private Formatter f;
        public Turtle(String name, Formatter f) {
            this.name = name;
            this.f = f;
        }
        public void move(int x, int y) {
            f.format("%s The Turtle is at (%d,%d)\n", name, x, y);
        }
        public static void main(String[] args) {
            PrintStream outAlias = System.out;
            Turtle tommy = new Turtle("Tommy",
                new Formatter(System.out));
            Turtle terry = new Turtle("Terry",
                new Formatter(outAlias));
            tommy.move(0,0);
            terry.move(4,8);
            tommy.move(3,4);
            terry.move(2,5);
            tommy.move(3,3);
            terry.move(3,3);
        }
    } /* Output:
    Tommy The Turtle is at (0,0)
    Terry The Turtle is at (4,8)
    Tommy The Turtle is at (3,4)
    Terry The Turtle is at (2,5)
    Tommy The Turtle is at (3,3)
    Terry The Turtle is at (3,3)
    *///:~

格式化说明符
~~~~~~~~~~~~

.. code-block:: text

    %[argument_index$][flags][width][.precision]conversion

``width`` 控制一个域的 **最小尺寸** ，默认右对齐，可以使用 ``flag`` “-” 来进行左对齐。

``.precision`` 缺省时，默认保留 6 位（只能用于浮点数）。

``conversion`` 可选项如下

.. csv-table::
    :header: "格式控制符", "含义"

    "d", "整数型（十进制）"
    "c", "Unicode 字符"
    "b", "Boolean 值"
    "s", "String"
    "f", "浮点数（十进制）"
    "e", "浮点数（科学计数）"
    "x", "整数（十六进制）"
    "h", "散列码（十六进制）"
    "\%", "字符 “%”"

String.format()
~~~~~~~~~~~~~~~~~

用于生成格式化的 ``String`` 对象。

.. code-block:: java

    String.format("I'm %s, and %d years old", name, age);

正则表达式
-----------

用于匹配字符串。我们要学习的是，应该如何将一个字符串转化为更通用的规则。

一些常用的符号
~~~~~~~~~~~~~~~

一次匹配一个的字符
^^^^^^^^^^^^^^^^^^

.. csv-table::
    :header: "表达式", "含义"
    :widths: 30, 70

    "``.``", "任意字符"
    "``[abc]``", "（在...之内）包含 ``a`` 、 ``b`` 或 ``c`` 的任何字符（和 ``a|b|c`` 作用相同）"
    "``[a-zA-Z]``", "（在...之内）从 ``a`` 到 ``z`` 、 ``A`` 到 ``Z`` 的任何一个字符"
    "``[^abc]``", "（除...之外）除 ``a`` 、 ``b`` 、 ``c`` 之外的任何一个字符"
    "``[abc[hij]]``", "（并） ``a`` 、 ``b`` 、 ``c`` 、 ``h`` 、 ``i`` 、 ``j`` 中的任意字符"
    "``[a-z&&[hij]]``", "（交） ``h`` 、 ``i`` 或 ``j`` 中的某一个字符"
    "``\s``", "空白符（空格、tab、换行、换页、回车）"
    "``\S``", "非空白符（ ``[^\s]`` ）"
    "``\d``", "数字（ ``[0-9]`` ）"
    "``\D``", "非数字（ ``[^0-9]`` ）"
    "``\w``", "词字符（ ``[a-zA-Z_0-9]`` ）"
    "``\W``", "非词字符（ ``[^\w]`` ）"
    "``\t``", "制表符Tab"
    "``\n``", "换行符"
    "``\r``", "回车"
    "``\\``", "反斜杠"

一次匹配多个字符
^^^^^^^^^^^^^^^^

.. csv-table::
    :header: "贪婪型","勉强型","占有型","如何匹配"
    :widths: 20,20,20,40

    "``X?``","``X??``","``X?+``","一个或零个 ``X``"
    "``X*``","``X*?``","``X*+``","零个或多个 ``X``"
    "``X+``","``X+?``","``X++``","一个或多个 ``X``"
    "``X{n}``","``X{n}?``","``X{n}+``","恰好 ``n`` 次 ``X``"
    "``X{n,}``","``X{n,}?``","``X{n,}+``","至少 ``n`` 次 ``X``"
    "``X{n,m}``","``X{n,m}?``","``X{n,m}+``","``X`` 至少 ``n`` 次，但不超过 ``m`` 次"

确定字符出现的位置
^^^^^^^^^^^^^^^^^^

.. csv-table::
    :header: "表达式", "含义"
    :widths: 30, 70

    "``^``", "一行的开始"
    "``$``", "一行的结束"
    "``\b``", "词的边界"
    "``\B``", "非词的边界"
    "``\G``", "前一个匹配的结束"

Pattern 和 Matcher
~~~~~~~~~~~~~~~~~~~~

导入 ``java.util.regex`` 包中的 ``Pattern`` 类。

工作流程：

- 导入 ``java.util.regex.Pattern`` 和 ``java.util.regex.Matcher``
- 使用 ``static Pattern.compile()`` 编译正则表达式，生成 ``Pattern`` 对象
- 使用 ``Pattern`` 对象的 ``matcher()`` 方法生成 ``Matcher`` 对象
- 使用 ``Matcher`` 对象的 ``find()`` 方法匹配字符串
- 使用 Matcher 对象的 group() 方法取出字符串

.. code-block:: java

    //: strings/TestRegularExpression.java
    // Allows you to easily try out regular expressions.
    // {Args: abcabcabcdefabc "abc+" "(abc)+" "(abc){2,}" }
    import java.util.regex.*;
    import static net.mindview.util.Print.*;

    public class TestRegularExpression {
        public static void main(String[] args) {
            if(args.length < 2) {
                print("Usage:\njava TestRegularExpression " +
                    "characterSequence regularExpression+");
                System.exit(0);
            }
            print("Input: \"" + args[0] + "\"");
            for(String arg : args) {
                print("Regular expression: \"" + arg + "\"");
                Pattern p = Pattern.compile(arg);
                Matcher m = p.matcher(args[0]);
                while(m.find()) {
                    print("Match \"" + m.group() + "\" at positions " +
                        m.start() + "-" + (m.end() - 1));
                }
            }
        }
    } /* Output:
    Input: "abcabcabcdefabc"
    Regular expression: "abcabcabcdefabc"
    Match "abcabcabcdefabc" at positions 0-14
    Regular expression: "abc+"
    Match "abc" at positions 0-2
    Match "abc" at positions 3-5
    Match "abc" at positions 6-8
    Match "abc" at positions 12-14
    Regular expression: "(abc)+"
    Match "abcabcabc" at positions 0-8
    Match "abc" at positions 12-14
    Regular expression: "(abc){2,}"
    Match "abcabcabc" at positions 0-8
    *///:~

``Pattern`` 对象提供了 ``split()`` 方法，它从匹配了 ``regex`` 的地方分割输入字符串，返回分割后的子字符串数组。

**组（Groups）** 是用括号划分的正则表达式，可以根据组的编号来引用某个组。

- 组号为 0 表示为整个表达式
- 组号为 1 表示被第一对括号括起来的组，以此类推

.. code-block:: text

    A(B(C))D

因此，组 0 是 ABCD，组 1 是 BC，组 2 是 C。

``public int groupCount()`` 返回该匹配器的模式中的分组数目，但不包括第 0 组。

``public String group(int i)`` 返回 **前一次** 匹配操作的组号，如果匹配成功，但是指定的组没有匹配输入字符串的任何部分，则返回 ``null`` 。

.. code-block:: java

    //: strings/Groups.java
    import java.util.regex.*;
    import static net.mindview.util.Print.*;

    public class Groups {
        static public final String POEM =
            "Twas brillig, and the slithy toves\n" +
            "Did gyre and gimble in the wabe.\n" +
            "All mimsy were the borogoves,\n" +
            "And the mome raths outgrabe.\n\n" +
            "Beware the Jabberwock, my son,\n" +
            "The jaws that bite, the claws that catch.\n" +
            "Beware the Jubjub bird, and shun\n" +
            "The frumious Bandersnatch.";
        public static void main(String[] args) {
            Matcher m =
                Pattern.compile("(?m)(\\S+)\\s+((\\S+)\\s+(\\S+))$")
                    .matcher(POEM);
            while(m.find()) {
                for(int j = 0; j <= m.groupCount(); j++)
                    printnb("[" + m.group(j) + "]");
                print();
            }
        }
    } /* Output:
    [the slithy toves][the][slithy toves][slithy][toves]
    [in the wabe.][in][the wabe.][the][wabe.]
    [were the borogoves,][were][the borogoves,][the][borogoves,]
    [mome raths outgrabe.][mome][raths outgrabe.][raths][outgrabe.]
    [Jabberwock, my son,][Jabberwock,][my son,][my][son,]
    [claws that catch.][claws][that catch.][that][catch.]
    [bird, and shun][bird,][and shun][and][shun]
    [The frumious Bandersnatch.][The][frumious Bandersnatch.][frumious][Bandersnatch.]
    *///:~

.. note:: 

    ``find()`` 可以在输入的任意位置定位正则表达式，而 ``lookingAt()`` 和 ``matches()`` 只有在正则表达式与输入的最开始处就开始匹配时才会成功。

    ``matches()`` 只有在整个输入都匹配正则表达式时才会成功，而 ``lookingAt()`` 只要输入的第一部分匹配就会成功。

    ``group()`` 方法只返回已匹配的部分。

Pattern 标记
^^^^^^^^^^^^^

.. csv-table::
    :header: "编译标记","效果"
    :widths: 30, 70

    "``Pattern.CANON_EQ``","当且仅当两个字符的完全规范分解相匹配时，才认为它们是匹配的。例如，如果我们指定这个标记，表达式 ``\u003F`` 就会匹配字符串 ``?`` 。默认情况下，匹配不考虑规范的等价性"
    "``Pattern.CASE_INSENSITIVE(?i)``","默认情况下，大小写不敏感的匹配假定只有US-ASCII字符集中的字符才能进行。这个标记允许模式匹配不考虑大小写（大写或小写）。通过指定 ``UNICODE_CASE`` 标记及结合此标记。基于Unicode的大小写不敏感的匹配就可以开启了"
    "``Pattern.COMMENTS(?x)``","在这种模式下，空格符将被忽略掉，并且以 ``#`` 开始直到行末的注释也会被忽略掉。通过嵌入的标记表达式也可以开启Unix的行模式"
    "``Pattern.DOTALL(?s)``","在dotall模式下，表达式 ``.`` 匹配所有字符，包括行终止符。默认情况下， ``.`` 不会匹配行终止符"
    "``Pattern.MULTILINE(?m)``","在多行模式下，表达式 ``^`` 和 ``$`` 分别匹配一行的开始和结束。 ``^`` 还匹配输入字符串的开始，而 ``$`` 还匹配输入字符串的结尾。默认情况下，这些表达式仅匹配输入的完整字符串的开始和结束"
    "``Pattern.UNICODE_CASE(?u)``","当指定这个标记，并且开启 ``CASE_INSENSITIVE`` 时，大小写不敏感的匹配将按照与Unicode标准相一致的方式进行。默认情况下，大小写不敏感的匹配假定只能在US-ASCII字符集中的字符才能进行"
    "``Pattern.UNIX_LINES(?d)``","在这种模式下，在 ``.`` 、 ``^`` 和 ``$`` 的行为中，只识别行终止符 ``\n``"

替换操作
~~~~~~~~~

- ``replaceFirst(String replacement)`` 用 ``replacement`` 替换掉第一个匹配成功的部分
- ``replaceAll(String replacement)`` 用 ``replacement`` 替换掉所有匹配成功的部分
- ``appendReplacement(StringBuffer sbuf, String replacement)`` 执行渐进式的替换

.. code-block:: java

    //: strings/TheReplacements.java
    import java.util.regex.*;
    import net.mindview.util.*;
    import static net.mindview.util.Print.*;

    /*! Here's a block of text to use as input to
        the regular expression matcher. Note that we'll
        first extract the block of text by looking for
        the special delimiters, then process the
        extracted block. !*/

    public class TheReplacements {
        public static void main(String[] args) throws Exception {
            String s = TextFile.read("TheReplacements.java");
            // Match the specially commented block of text above:
            Matcher mInput =
                Pattern.compile("/\\*!(.*)!\\*/", Pattern.DOTALL)
                    .matcher(s);
            if(mInput.find())
                s = mInput.group(1); // Captured by parentheses
            // Replace two or more spaces with a single space:
            s = s.replaceAll(" {2,}", " ");
            // Replace one or more spaces at the beginning of each
            // line with no spaces. Must enable MULTILINE mode:
            s = s.replaceAll("(?m)^ +", "");
            print(s);
            s = s.replaceFirst("[aeiou]", "(VOWEL1)");
            StringBuffer sbuf = new StringBuffer();
            Pattern p = Pattern.compile("[aeiou]");
            Matcher m = p.matcher(s);
            // Process the find information as you
            // perform the replacements:
            while(m.find())
                m.appendReplacement(sbuf, m.group().toUpperCase());
            // Put in the remainder of the text:
            m.appendTail(sbuf);
            print(sbuf);
        }
    } /* Output:
    Here's a block of text to use as input to
    the regular expression matcher. Note that we'll
    first extract the block of text by looking for
    the special delimiters, then process the
    extracted block.
    H(VOWEL1)rE's A blOck Of tExt tO UsE As InpUt tO
    thE rEgUlAr ExprEssIOn mAtchEr. NOtE thAt wE'll
    fIrst ExtrAct thE blOck Of tExt by lOOkIng fOr
    thE spEcIAl dElImItErs, thEn prOcEss thE
    ExtrActEd blOck.
    *///:~

reset()
~~~~~~~~~

使用 ``reset()`` 可以将现有的 ``Matcher`` 对象应用于一个新的字符序列。

.. code-block:: java

    //: strings/Resetting.java
    import java.util.regex.*;

    public class Resetting {
        public static void main(String[] args) throws Exception {
            Matcher m = Pattern.compile("[frb][aiu][gx]")
                .matcher("fix the rug with bags");
            while(m.find())
                System.out.print(m.group() + " ");
            System.out.println();
            m.reset("fix the rig with rags");
            while(m.find())
                System.out.print(m.group() + " ");
        }
    } /* Output:
    fix rug bag
    fix rig rag
    *///:~

正则表达式与 Java I/O
~~~~~~~~~~~~~~~~~~~~~~

应用正则表达式在一个文件中进行搜索匹配操作。

.. code-block:: java

    //: strings/JGrep.java
    // A very simple version of the "grep" program.
    // {Args: JGrep.java "\\b[Ssct]\\w+"}
    import java.util.regex.*;
    import net.mindview.util.*;

    public class JGrep {
        public static void main(String[] args) throws Exception {
            if(args.length < 2) {
                System.out.println("Usage: java JGrep file regex");
                System.exit(0);
            }
            Pattern p = Pattern.compile(args[1]);
            // Iterate through the lines of the input file:
            int index = 0;
            Matcher m = p.matcher("");
            for(String line : new TextFile(args[0])) {
                m.reset(line);
                while(m.find())
                    System.out.println(index++ + ": " +
                        m.group() + ": " + m.start());
            }
        }
    } /* Output: (Sample)
    0: strings: 4
    1: simple: 10
    2: the: 28
    3: Ssct: 26
    4: class: 7
    5: static: 9
    6: String: 26
    7: throws: 41
    8: System: 6
    9: System: 6
    10: compile: 24
    11: through: 15
    12: the: 23
    13: the: 36
    14: String: 8
    15: System: 8
    16: start: 31
    *///:~

.. error:: 并没有按照作者说的产生输出。

扫描输入
---------

工作流程：

- 使用 ``StringReader`` 将 ``String`` 转化为可读的流对象
- 用这个流对象来构造 ``BufferReader`` 对象
- 使用 ``BufferReader`` 对象的 ``readLine()`` 方法读取一行文本（ ``readLine()`` 方法将一行输入转为 ``String`` 对象）
- 使用 ``Integer`` 、 ``Double`` 等类的各种解析方法来解析数据

.. code-block:: java

    //: strings/SimpleRead.java
    import java.io.*;

    public class SimpleRead {
        public static BufferedReader input = new BufferedReader(
            new StringReader("Sir Robin of Camelot\n22 1.61803"));
        public static void main(String[] args) {
            try {
                System.out.println("What is your name?");
                String name = input.readLine();
                System.out.println(name);
                System.out.println("How old are you? What is your favorite double?");
                System.out.println("(input: <age> <double>)");
                String numbers = input.readLine();
                System.out.println(numbers);
                String[] numArray = numbers.split(" ");
                int age = Integer.parseInt(numArray[0]);
                double favorite = Double.parseDouble(numArray[1]);
                System.out.format("Hi %s.\n", name);
                System.out.format("In 5 years you will be %d.\n",
                    age + 5);
                System.out.format("My favorite double is %f.",
                    favorite / 2);
            } catch(IOException e) {
                System.err.println("I/O exception");
            }
        }
    } /* Output:
    What is your name?
    Sir Robin of Camelot
    How old are you? What is your favorite double?
    (input: <age> <double>)
    22 1.61803
    Hi Sir Robin of Camelot.
    In 5 years you will be 27.
    My favorite double is 0.809015.
    *///:~

Java SE5 新增了 ``Scanner`` 类，它可以大大减轻扫描输入的工作负担。

.. code-block:: java

    //: strings/BetterRead.java
    import java.util.*;

    public class BetterRead {
        public static void main(String[] args) {
            Scanner stdin = new Scanner(SimpleRead.input);
            System.out.println("What is your name?");
            String name = stdin.nextLine();
            System.out.println(name);
            System.out.println(
                "How old are you? What is your favorite double?");
            System.out.println("(input: <age> <double>)");
            int age = stdin.nextInt();
            double favorite = stdin.nextDouble();
            System.out.println(age);
            System.out.println(favorite);
            System.out.format("Hi %s.\n", name);
            System.out.format("In 5 years you will be %d.\n",
                age + 5);
            System.out.format("My favorite double is %f.",
                favorite / 2);
        }
    } /* Output:
    What is your name?
    Sir Robin of Camelot
    How old are you? What is your favorite double?
    (input: <age> <double>)
    22
    1.61803
    Hi Sir Robin of Camelot.
    In 5 years you will be 27.
    My favorite double is 0.809015.
    *///:~

``Scanner`` 的构造器可以接收任意类型的输入对象，包括：

-  ``File``
-  ``InputStream``
-  ``String``
-  ``Readable`` 实现类（上一个例子中的 ``BufferedReader`` 也归于这一类）

有了 ``Scanner`` ，所有的输入、分词、以及解析的操作都隐藏在不同类型的 ``next`` 方法中。

普通的 ``next()`` 方法返回下一个 ``String`` 。

所有的基本类型（除 ``char`` 之外）都有对应的 ``next`` 方法，包括 ``BigDecimal`` 和 ``BigInteger`` 。

所有的 ``next`` 方法，只有在找到一个完整的分词之后才会返回。

``Scanner`` 还有相应的 ``hasNext`` 方法，用以判断下一个输入分词是否是所需的类型，如果是则返回 ``true`` 。

``Scanner`` 没有用 ``try`` 区块捕获 ``IOException`` ，因为， ``Scanner`` 在输入结束时会自动抛出 ``IOException`` ，所以 ``Scanner`` 会把 ``IOException`` 吞掉。不过，通过 ``ioException()`` 方法，你可以找到最近发生的异常，因此，你可以在必要时检查它。

Scanner 定界符
~~~~~~~~~~~~~~~

默认情况下， ``Scanner`` 根据空白字符对输入进行分词，但是你可以用正则表达式指定自己所需的定界符。

.. code-block:: java

    //: strings/ScannerDelimiter.java
    import java.util.*;

    public class ScannerDelimiter {
        public static void main(String[] args) {
            Scanner scanner = new Scanner("12, 42, 78, 99, 42");
            scanner.useDelimiter("\\s*,\\s*");
            while(scanner.hasNextInt())
                System.out.println(scanner.nextInt());
        }
    } /* Output:
    12
    42
    78
    99
    42
    *///:~

用正则表达式扫描
~~~~~~~~~~~~~~~~

当 ``next()`` 方法配合指定的正则表达式使用时，将找到下一个匹配该模式的输入部分，调用 ``match()`` 方法就可以获得匹配结果。

.. note:: 

    这种配合，仅仅针对下一个输入分词进行匹配，如果你的正则表达式中含有定界符，那永远不可能匹配成功。
