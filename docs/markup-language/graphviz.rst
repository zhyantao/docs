.. _graphviz:

========
Graphviz
========

基本介绍
--------

`Graphviz <https://graphviz.org/>`__\ （Graph Visualization Software）是一个由 AT&T 实验室启动的
`开源 <https://gitlab.com/graphviz/graphviz>`_ 工具包，用于绘制 DOT 语言脚本描述的图形。
Graphviz 由一种被称为 DOT 语言的图形描述语言与一组可以生成和/或处理 DOT 文件的工具组成：

dot
    一个用来将生成的图形转换成多种输出格式的命令行工具。其输出格式包括 PostScript，PDF，SVG，PNG，含注解的文本等等。
neato
    用于 sprint model 的生成。
twopi
    用于放射状图形的生成
circo
    用于圆形图形的生成。
fdp
    另一个用于生成无向图的工具。
dotty
    一个用于可视化与修改图形的图形用户界面程序。
lefty
    一个可编程的控件，它可以显示DOT图形，并允许用户用鼠标在图上执行操作。Lefty 可以作为 MVC 模型的使用图形的 GUI 程序中的视图部分。


语法格式
--------

下表是 DOT 语言的抽象语法定义。红色字体为关键字，加粗字体表示字面值常量，中括号括起来的项可有可无。
逻辑或表示多选一。阅读下表时，从第一行开始阅读，下一行的语法依赖于上一行或上几行的语法。
加粗字体和小括号括起来项中的某一项一定会出现在代码中。

.. csv-table::
    :header: "Type", "Syntax"
    :widths: 20, 50

    "``graph``", "[ ``strict`` ] (``graph`` \| ``digraph``) [ ID ] **{** stmt_list **}**"
    "stmt_list", "[ stmt [ **;** ] stmt_list ]"
    "stmt", "node_stmt \| edge_stmt \| attr_stmt \| ID **=** ID \| ``subgraph``"
    "attr_stmt", "(``graph`` \| ``node`` \| ``edge``) attr_list"
    "attr_list", "**[** [ a_list ] **]** [ attr_list ]"
    "a_list", "ID **=** ID [ (**;** \| **,**) ] [ a_list ]"
    "edge_stmt", "(node_id \| ``subgraph``) edgeRHS [ attr_list ]"
    "edgeRHS", "edgeop (node_id \| ``subgraph``) [ edgeRHS ]"
    "node_stmt", "node_id [ attr_list ]"
    "node_id", "ID [ port ]"
    "port", "**:** ID [ **:** compass_pt ] \| **:** compass_pt"
    "``subgraph``", "[ ``subgraph`` [ ID ] ] **{** stmt_list **}**"
    "compass_pt", "(n \| ne \| e \| se \| s \| sw \| w \| nw \| c \| _)"

解释一下， ``node`` 和 ``edge`` 是图形的两个主要构成元素。``graph`` 和 ``digraph`` 为函数返回值，分别代表无向图和有向图。
``ID`` 表示函数名，可有可无。大括号 ``{}`` 括起来的是函数体。函数体里面正常书写表达式 ``stmt_list``。
表达式结束的分号 ``;`` 可有可无，有分号可以帮助我们阅读代码。有向边用 ``->`` 表示，无向边用 ``--`` 表示。
注释用 ``/* */`` 或 ``//`` 表示。下图是一个简单的有向图的书写方式。

.. code-block:: text

    .. graphviz::

        // 有向图
        digraph foo {
            a -> b;
            b -> a;
        }

.. graphviz::

    // 有向图
    digraph foo {
        a -> b;
        b -> a;
    }

其他资源
--------

`PDF Manual <https://kdocs.cn/l/ckMpf2Su6Kv4>`_ 是工具使用说明，为我们提供了：

- 驱动和引擎说明；
- 应该如何自定义输出文件的格式；
- 定义图、节点、边的样式的语法格式；
- 图、节点、边的样式属性说明；
- 命令行参数说明。

`GraphViz Pocket Reference <https://graphs.grevian.org/example>`_ 为我们提供了部分使用实例。
