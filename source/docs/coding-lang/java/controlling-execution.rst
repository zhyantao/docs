============
控制执行流程
============

true 和 false
--------------

Java **不允许** 我们将一个数字作为布尔值使用（这在 C 和 C++ 中是允许的）

比如 ``if(a)`` 是不对的，而 ``if(a != 0)`` 是可以的。即需要用条件表达式将其转化为布尔值。

迭代
-----

do-while
~~~~~~~~~~

while 和 do-while **唯一的区别** 就是 do-while 中的语句至少会执行一次，即便第一次就被计算为 false 。

在实际应用中，while 比 do-while 更常用。

for
~~~~

.. code-block:: java

    for (initializaiton; Boolean-expression; step) {
        statements;
    }

执行顺序为：

1. initializaiton
2. Boolean-expression 如果为真，执行 3，否则执行 5
3. statements
4. step 回到 2
5. 结束

逗号操作符
~~~~~~~~~~~

Java 中 **唯一用到** 逗号操作符的地方就是 for 循环的控制表达式了。

可以在 for 循环的 initializaiton 和 step 中书写多个表达式，然后用逗号分隔开。

foreach 语法
-------------

用于数组和容器。不必创建 int 变量去对由访问项构成的序列进行计数，foreach 将自动产生每一项。

foreach 可以用于任何 Iterable 对象。

.. code-block:: java

    //: control/ForEachInt.java
    import static net.mindview.util.Range.*;
    import static net.mindview.util.Print.*;

    public class ForEachInt {
        public static void main(String[] args) {
            for(int i : range(10)) // 0..9
                printnb(i + " ");
            print();
            for(int i : range(5, 10)) // 5..9
                printnb(i + " ");
            print();
            for(int i : range(5, 20, 3)) // 5..20 step 3
                printnb(i + " ");
            print();
        }
    } /* Output:
    0 1 2 3 4 5 6 7 8 9
    5 6 7 8 9
    5 8 11 14 17
    *///:~

return
-------

void 方法的结尾有一个隐式的 return。因此在方法中并非总是必须有一个 return 语句。

臭名昭著的 goto
----------------

Java 不支持 goto 语句。

switch
-------

switch 根据 integral-selector（整数选择因子）产生的整数值，与 case 中的情况进行比较，如果符合，执行相应的 statement。case 全都不匹配，就执行 default 语句。

.. code-block:: java

    switch(integral-selector) {
        case integral-value1: statement; break;
        case integral-value2: statement; break;
        // ...
        default: statement;
    }
