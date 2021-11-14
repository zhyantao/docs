.. highlight:: rst
.. _restructuredtext:

=========================
reStructuredText 语法入门
=========================

.. hint:: 

    文档也支持 `reST 风格的 Markdown 语法 <./tools-and-usage/MyST-syntax-cheat-sheet.html>`_ 。本文转载自
    `MegEngine <https://megengine.org.cn/doc/stable/zh/development/contribute-to-docs/restructuredtext.html>`_ （有修改），仅供学习参考。

.. _indentation-rst:

缩进（Indentation）
-------------------

.. warning::

    - 本文档使用 4 格缩进，错误的缩进将导致无法正确渲染样式。
    - 如果在 Sphinx reST 内使用代码块，其缩进要求不受影响（如 Python）。

.. _sections-rst:

章节（Sections）
----------------

.. code-block::

    ========
    一级标题
    ========

    二级标题
    --------

    三级标题
    ~~~~~~~~

    四级标题
    ^^^^^^^^

.. warning::

    - **标记符必须与文本长度一致，否则会导致 Warning （无法通过 CI）。** 
    - 你可以采用更深的嵌套级别，但在文档中应当避免出现四级甚至更深的标题。

.. panels::

  正确示范
  ^^^^^^^^
  .. code-block::

      ========
      一级标题
      ========

  ---
  错误示范
  ^^^^^^^^
  .. code-block::

      ======================
      一级标题
      ======================

.. _paragraphs-rst:

段落（Paragraphs）
------------------

段落（:duref:`参考 <paragraphs>`）是由一个或多个空白行分隔的文本块，是 reST 文档中最基本的部分。
缩进在 reST 语法中很重要（与 Python 一样），因此同一段落的所有行都必须左对齐到相同的缩进级别。

保留换行特性
~~~~~~~~~~~~

行块（:duref:`参考 <line-blocks>`）是保留换行符的一种方法：

.. code-block::

    | 第一部分，
    | 第二部分。

| 第一部分，
| 第二部分。

.. _inlnie-markup-rst:

内联标记（Inline markup）
-------------------------

.. code-block:: text

    *一个星号标记出需要用户着重阅读的内容*

*一个星号标记出需要用户着重阅读的内容*

.. code-block:: text

    **两个星号表示文本十分重要，一般用粗体显示。**

**两个星号表示文本十分重要，一般用粗体显示。**

.. code-block:: text

    `一个反引号表示一个作品的引用，且必须包含作品的标题。`

`一个反引号表示一个作品的引用，且必须包含作品的标题。`

.. code-block:: text

    ``两个反引号表示预定义格式文本``

``两个反引号表示预定义格式文本``

.. dropdown:: :fa:`eye,mr-1` 使用注意事项

    .. warning::

        标记符号与被包裹的文本内容之间不能存在空格，与外部文本之间必须存在空格。

    .. panels::

      正确示范
      ^^^^^^^^
      .. code-block:: text

          这些文本 **表示强调** 作用

      这些文本 **表示强调** 作用
      ---
      错误示范
      ^^^^^^^^
      .. code-block:: text

          这些文本 ** 表示强调** 作用
          这些文本 **表示强调 ** 作用
          这些文本**表示强调** 作用

      这些文本 ** 表示强调** 作用
      这些文本 **表示强调 ** 作用
      这些文本**表示强调** 作用

.. _list-rst:

列表（List）
------------

.. warning::

    列表语法是最容易被用错的地方，在文档中也极为常见。

定义列表
~~~~~~~~

定义列表（:duref:`参考 <definition-lists>`）在 API 文档很常见，使用方法如下：

.. code-block::

    术语 （限定在一行文本）
        术语的定义，必须使用缩进。

        支持使用多个段落。

    下一个术语
        下一个术语对应的定义。

术语 （限定在一行文本）
    术语的定义，必须使用缩进。

    支持使用多个段落。

下一个术语
    下一个术语对应的定义。

无序列表
~~~~~~~~

无序列表（:duref:`参考 <bullet-lists>`）的用法很自然。
只需要在段落开头放置横杠，然后正确地缩进：

.. panels::

    正确的示范（ **2 格缩进** ）
    ^^^^^^^^^^^^^^^^^^^^^^
    .. code-block::

        - 这是一个无序列表。
        - 它有两个元素，
          第二个元素占据两行源码，视作同一个段落。

    - 这是一个无序列表。
    - 它有两个元素，
      第二个元素占据两行源码，视作同一个段落。
    ---
    错误的示范（4 格缩进）
    ^^^^^^^^^^^^^^^^^^^^^^
    .. code-block::

        - 这是一个无序列表。
        - 它有两个元素，
             第二个元素被解析成定义列表。

    - 这是一个无序列表。
    - 它有两个元素，
         第二个元素被解析成定义列表。

有序列表
~~~~~~~~

对于有序列表，可以自己编号，也可以使用 # 来自动编号：

.. code-block::

    1. 这是一个有序列表。
    2. 它也有两个元素。

1. 这是一个有序列表。
2. 它也有两个元素。

.. code-block::

    #. 这又是一个有序列表。
    #. 但是它能够自动编号。

#. 这又是一个有序列表。
#. 但是它能够自动编号。

嵌套列表
~~~~~~~~

嵌套列表必须使用 **空白行** 和父列表项目隔开：

.. panels::

    正确示范（ **2 格缩进** ）
    ^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. code-block::

        - 这是一个列表。

          - 它嵌套了一个子列表，
          - 并且有自己的子元素。

        - 这里是父列表的后续元素。

    - 这是一个列表。

      - 它嵌套了一个子列表，
      - 并且有自己的子元素。

    - 这里是父列表的后续元素。
    ---
    错误示范
    ^^^^^^^^
    .. code-block::

        - 这并不是嵌套列表，
          - 前面三行被看作是同一个元素，
          - 其中横杠被解析成普通的文本。
        - 这是列表的第二个元素。

    - 这并不是嵌套列表，
      - 前面三行被看作是同一个元素，
      - 其中横杠被解析成普通的文本。
    - 这是列表的第二个元素。

.. _tables-rst:

表格（Tables）
--------------

网格表
~~~~~~

对于网格表（:duref:`参考 <grid-tables>`），必须手动“画”出单元格：

.. code-block::

    +------------------------+------------+----------+----------+
    | Header row, column 1   | Header 2   | Header 3 | Header 4 |
    | (header rows optional) |            |          |          |
    +========================+============+==========+==========+
    | body row 1, column 1   | column 2   | column 3 | column 4 |
    +------------------------+------------+----------+----------+
    | body row 2             | ...        | ...      |          |
    +------------------------+------------+----------+----------+

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | ...        | ...      |          |
+------------------------+------------+----------+----------+

简单表
~~~~~~

简单表（:duref:`参考 <simple-tables>`）写起来很简单，但有局限性：
它们必须包含多个行，并且第一列单元格不能包含多行。

.. code-block::

    =====  =====  =======
    A      B      A and B
    =====  =====  =======
    False  False  False
    True   False  False
    False  True   False
    True   True   True
    =====  =====  =======

=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======

CSV 表
~~~~~~

CSV 表格可以根据 CSV（逗号分隔值）数据创建表。

.. code-block::

    .. csv-table:: Frozen Delights!
        :header: "Treat", "Quantity", "Description"
        :widths: 15, 10, 30

        "Albatross", 2.99, "On a stick!"
        "Crunchy Frog", 1.49, "If we took the bones out, 
        it wouldn't becrunchy, now would it?"
        "Gannet Ripple", 1.99, "On a stick!"

.. csv-table:: Frozen Delights!
    :header: "Treat", "Quantity", "Description"
    :widths: 15, 10, 30

    "Albatross", 2.99, "On a stick!"
    "Crunchy Frog", 1.49, "If we took the bones out, 
    it wouldn't becrunchy, now would it?"
    "Gannet Ripple", 1.99, "On a stick!"

List 表
~~~~~~~

List 表可以根据两级无序列表来生成表格：

.. code-block::
    
    .. list-table:: Frozen Delights!
        :widths: 15 10 30
        :header-rows: 1

        - - Treat
          - Quantity
          - Description
        - - Albatross
          - 2.99
          - On a stick!
        - - Crunchy Frog
          - 1.49
          - If we took the bones out, it wouldn't be
             crunchy, now would it?
        - - Gannet Ripple
          - 1.99
          - On a stick!

.. list-table:: Frozen Delights!
    :widths: 15 10 30
    :header-rows: 1

    - - Treat
      - Quantity
      - Description
    - - Albatross
      - 2.99
      - On a stick!
    - - Crunchy Frog
      - 1.49
      - If we took the bones out, it wouldn't be
         crunchy, now would it?
    - - Gannet Ripple
      - 1.99
      - On a stick!

.. _hyperlinks-rst:

超链接（Hyperlinks）
--------------------

使用 ```链接文本 <https://domain.invalid>`_`` 来插入内联网页链接。

你也可以使用目标定义（:duref:`参考 <hyperlink-targets>`）的形式分离文本和链接：

.. code-block::

    这个段落包含一个 `超链接`_.

    .. _超链接: https://domain.invalid/

这个段落包含一个 `超链接`_.

.. _超链接: https://domain.invalid/

.. warning::

    - 在链接文本和 ``<`` 符号之间必须至少有一个空格。
    - 同 :ref:`inlnie-markup-rst` ，
      标记符和被包裹的文本之间不能有空格，
      而标记符和外部文本之间至少需要有一个空格。
    - 如果在同一个页面中两个 **链接文本** 相同，编译器会报 **警告** ，
      此时，可以在末尾用两个下划线 ``__`` 来解决


.. _images-rst:

图片（Images）
--------------

reST 支持图像指令，用法如下：

.. code-block::

    .. image:: gnu.png
        :height: 100px (length)
        :width: 200px (length or percentage of the current line width)
        :scale: integer percentage (the "%" symbol is optional)
        :alt: alternate text
        :align: "top", "middle", "bottom", "left", "center", or "right"
        :target: text (URI or reference name)

当在 Sphinx 中使用时，给定的文件名（在此处为 ``gnu.png`` ）必须相对于源文件。

.. image:: ../../_static/images/lenna.jpg
    :height: 200px
    :width: 200px
    :alt: Lenna, 512 times 512, Grayscale
    :align: center
    :target: http://www.lenna.org/

.. warning::

    - 文档中所使用的图片请统一放置在 ``source/_static/images`` 目录内。
      **绝对不允许** 直接将图片放在和文本文件相同的文件夹内，这样虽然方便了写作时进行引用，
      但却给整个文档的维护引入了技术债务，将形成潜在的风险。
    - 一般情况下请优先使用 `SVG <https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Adding_vector_graphics_to_the_Web>`_ 格式的矢量图，使用位图请权衡好图片体积和清晰度。
    - 尽可能使用 :ref:`Graphviz <graphviz-ext>` 或 :ref:`Mermaid <mermaid-ext>` 语法绘制示意图。
    - 图片文件名需要有相应的语义信息，不可使用完全随机生成的字符。
    - 文档中若包含 ``gif`` 或 ``svg`` 格式的图片，编译生成 PDF 时将无法通过编译。解决方法是：图片后缀用星号表示 `Ref <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#images>`__。

.. note::

    如果你想要给图片添加描述性文字，请使用 ``figure`` 代替 ``image``,
    接着使用 ``:caption: text`` 作为传入的参数，其它参数用法一致。

视频（Videos）
--------------

.. code-block:: html

    .. raw:: html

        <iframe 
            width="560" height="315" 
            src="https://www.youtube.com/embed/1eYqV_vGlJY" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>

.. raw:: html

    <iframe 
        width="560" height="315" 
        src="https://www.youtube.com/embed/1eYqV_vGlJY" 
        title="YouTube video player" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>

.. _cross-reference-rst:

交叉引用（Cross-reference）
---------------------------

使用 ``:role:`target``` 语法，就会创造一个 ``role`` 类型的指向 ``target`` 的链接。

- 最常见的使用情景是文档内部页面的相互引用（尤其是引用 API 参考内容时）。
- 显示的链接文本会和 ``target`` 一致，
  你也可以使用 ``:role:`title <target>``` 来将链接文本指定为 ``title``

.. _test-ref-label:

通过 ref 进行引用
~~~~~~~~~~~~~~~~~

为了支持对任意位置的交叉引用，使用了标准的 reST 标签（标签名称在整个文档中必须唯一）。

可以通过两种方式引用标签：

**1、** 在章节标题之前放置一个标签，引用时则可以使用 ``:ref:`label-name``` , 比如：

.. code-block::

    .. _test-ref-label:

    通过 ref 进行引用
    ~~~~~~~~~~~~~~~~~

    跳转到 :ref:`test-ref-label`

跳转到 :ref:`test-ref-label` 。这种方法将自动获取章节标题作为链接文本，且对图片和表格也一样有效。

**2、** 如果标签没有放在标题之前，则需要使用 ``:ref:`Link title <label-name>``` 来指定名称。

.. _footnotes-rst:

脚注（Footnotes）
-----------------

脚注（:duref:`参考 <footnotes>`）使用 ``[#name]_`` 来标记脚注的位置，并在 ``Footnotes`` 专栏（rubic）后显示，例如：

.. code-block::

    Lorem ipsum [1]_ dolor sit amet ... [2]_

    .. rubric:: Footnotes

    .. [1] Text of the first footnote.
    .. [2] Text of the second footnote.

Lorem ipsum [1]_ dolor sit amet ... [2]_

.. rubric:: Footnotes

.. [1] Text of the first footnote.
.. [2] Text of the second footnote.

你可以显式使用 ``[1]_`` 来编号，否则使用 ``[#]_`` 进行自动编号。

.. _citation-rst:

引用（Citation）
----------------

引用和脚注类似，但不需要进行编号，且全局可用：

.. code-block::

    Lorem ipsum [Ref]_ dolor sit amet.

    .. [Ref] Book or article reference, URL or whatever.

Lorem ipsum [Ref]_ dolor sit amet.

.. [Ref] Book or article reference, URL or whatever.

.. _math-rst:

数学公式（Math）
----------------

只需要使用类似的语法：

.. code-block::

    Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.

Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.

.. _sphinx-directives:

Sphinx 拓展指令
---------------

.. warning::

    以下语法非原生 ReStructuredText 语法，需要通过 Sphinx 进行支持。

``.. toctree::`` 
  Table of contents tree. 用于组织文档结构。

``.. note::`` 
  用于添加提示性信息，用户忽视这些信息可能出错。
  
``.. warning::``
  用于添加警告性信息，用户忽视这些信息一定出错。

``.. versionadded:: version``
  描述 API 添加版本，如果用于单个模块, 则必须放在显式文本内容顶部。

``.. versionchanged:: version``
  描述 API 变更版本，指出以何种方式（新参数）进行了更改以及可能的副作用。

``.. deprecated:: version``
  描述 API 弃用版本，简要地告知替代使用方式。

``.. seealso::``
  包括对模块文档或外部文档的引用列表，内容应该是一个 reST 定义列表，比如：
  
  .. code-block::

      .. seealso::

      Module :py:mod:`zipfile`
          Documentation of the :py:mod:`zipfile` standard module.

      `GNU tar manual, Basic Tar Format <http://link>`_
          Documentation for tar archive files, including GNU tar extensions.

  也可以使用简略写法，如下所示：

  .. code-block::
      
      .. seealso:: modules :py:mod:`zipfile`, :py:mod:`tarfile`

``.. rubric:: title``
  用于创建一个不会产生导航锚点的标题。

``.. centered::``
  创建居中文本

``.. math::``
  LaTeX 标记的数学公式，相较于 ``:math:`` 语法提供了更干净的阅读空间。

  .. code-block::

      .. math::

        (a + b)^2 = a^2 + 2ab + b^2

        (a - b)^2 = a^2 - 2ab + b^2

  .. math::

    (a + b)^2 = a^2 + 2ab + b^2

    (a - b)^2 = a^2 - 2ab + b^2

  .. warning::

      用于 Python 文档字符串中时，必须将所有反斜杠加倍，或者使用 Python 原始字符串 ``r"raw"``.

``.. highlight:: language``
  使用指定语言（Pygments 支持）的语法高亮，直到再次被定义。

``.. code-block:: [language]``
  展示代码块，如果未设置 ``language``, highlight_language 将被使用。
  
.. note::

    想要了解完整的指令和配置项，请访问 `Directives
    <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>`_ 页面。

.. _sphinx-ext:

Sphinx 插件语法
---------------

.. note::

    下面的语法通过 Sphinx Extensions 支持，同样可以用于 Python 文档字符串。

PlantUML 语法支持
~~~~~~~~~~~~~~~~~

文件已通过 `sphinxcontrib-plantuml <https://github.com/sphinx-contrib/plantuml>`_
插件支持 PlantUML 语法，语法规则参考 :ref:`plantuml` ，样例如下：

.. code-block:: 

    .. uml::

        Alice -> Bob: Hi!
        Alice <- Bob: How are you?

.. uml::

    Alice -> Bob: Hi!
    Alice <- Bob: How are you?

.. tip:: 相同条件下，优先使用 PlantUML 或 GraphViz 绘制图片，因为 Mermaid 无法在 PDF 文件上渲染。

.. _graphviz-ext:

Graphviz 语法支持
~~~~~~~~~~~~~~~~~

文档已经通过 `sphinx.ext.graphviz 
<https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`_ 插件支持
Graphviz 语法，语法规则参考 :ref:`graphviz` ，样例如下：

.. code-block:: 

    .. graphviz::

        digraph foo {
            "bar" -> "baz";
        }


.. graphviz::

    digraph foo {
        "bar" -> "baz";
    }

.. _mermaid-ext:

Mermaid 语法支持
~~~~~~~~~~~~~~~~

文档已经通过 `sphinxcontrib-mermaid 
<https://sphinxcontrib-mermaid-demo.readthedocs.io/en/latest/>`_ 插件支持
`Mermaid <https://mermaid-js.github.io/mermaid/>`_ 语法，样例如下：

.. code-block::
    
    .. mermaid::

        sequenceDiagram
            participant Alice
            participant Bob
            Alice->John: Hello John, how are you?
            loop Healthcheck
                 John->John: Fight against hypochondria
            end
            Note right of John: Rational thoughts <br/>prevail...
            John-->Alice: Great!
            John->Bob: How about you?
            Bob-->John: Jolly good!

.. mermaid::

    sequenceDiagram
        participant Alice
        participant Bob
        Alice->John: Hello John, how are you?
        loop Healthcheck
             John->John: Fight against hypochondria
        end
        Note right of John: Rational thoughts <br/>prevail...
        John-->Alice: Great!
        John->Bob: How about you?
        Bob-->John: Jolly good!

.. _toggle-ext:

Toggle 语法支持
~~~~~~~~~~~~~~~

文档已经通过 `sphinx-togglebutton 
<https://sphinx-togglebutton.readthedocs.io/en/latest/>`_ 插件支持常见 Toggle 功能，样例如下：

.. code-block::

    .. admonition:: Here's my title
        :class: dropdown, warning

        My note

.. admonition:: Here's my title
    :class: dropdown, warning
    
    My note

以上展示的为基础用法，更多用法请参考文档。

.. _pannels-ext:

Pannels 语法支持
~~~~~~~~~~~~~~~~

文档已经通过 `sphinx-panels 
<https://sphinx-panels.readthedocs.io/en/latest/>`_ 插件支持常见 Pannels 功能，样例如下：

.. code-block::

    .. panels::
        :container: container-lg pb-3
        :column: col-lg-4 col-md-4 col-sm-6 col-xs-12 p-2

        panel1
        ---
        panel2
        ---
        panel3
        ---
        :column: col-lg-12 p-2
        panel4

.. panels::
    :container: container-lg pb-3
    :column: col-lg-4 col-md-4 col-sm-6 col-xs-12 p-2

    panel1
    ---
    panel2
    ---
    panel3
    ---
    :column: col-lg-12 p-2
    panel4

以上展示的为 Grid Layout 用法，Card Layout, Image Caps 等用法请参考文档。

.. note::

    该插件也实现了 Toggle, Tabs 语法功能。

.. _tabs-ext:

Tabs 语法支持
~~~~~~~~~~~~~

文档已经通过 `sphinx-tabs 
<https://sphinx-tabs.readthedocs.io/en/latest/>`_ 插件支持常见 Tabs 功能，样例如下：

.. code-block::

    .. tabs::

        .. tab:: Apples

            Apples are green, or sometimes red.

        .. tab:: Pears

            Pears are green.

        .. tab:: Oranges

            Oranges are orange.

.. tabs::

    .. tab:: Apples

        Apples are green, or sometimes red.

    .. tab:: Pears

        Pears are green.

    .. tab:: Oranges

        Oranges are orange.

以上展示的为 Basic 用法，Nested / Group / Code Tabs 用法请参考文档。

GitHub URL 缩写
~~~~~~~~~~~~~~~

为了方面写文档时引用 GitHub 上的源代码，支持如下语法：

.. code-block:: 
    
    - :src:`source/docs/`
    - :docs:`source/conf.py`
    - :issue:`1`
    - :pull:`21`

- :src:`source/docs/`
- :docs:`source/conf.py`
- :issue:`1`
- :pull:`21`

该功能通过 `sphinx.ext.extlinks 
<https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html>`_ 插件支持。

参考文献
---------

基于 `sphinxcontrib-bibtex <https://sphinxcontrib-bibtex.readthedocs.io/en/latest/index.html>`_
插件书写参考文献。使用时首先将参考文献的引用写在 ``refs.bib`` 中，然后在正文中添加引用。

引用出现的位置分为行内引用 ``cite`` 和脚注引用 ``footcite`` ，引用格式也分为引用时给出作者署名
``t`` 和引用时不给出作者署名，只在文中注明递增[序号] ``p`` 。因此其组合一共有四种：

1. ``:cite:t:``
2. ``:cite:p:``
3. ``:footcite:t:``
4. ``:footcite:p:``

对应地，插入参考文献可以使用 ``.. bibliography::`` 或 ``.. footbibliography::`` 。

将引用写入 refs.bib 
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    @Book{1987:nelson,
        author = {Edward Nelson},
        title = {Radically Elementary Probability Theory},
        publisher = {Princeton University Press},
        year = {1987}
    }

行内引用
~~~~~~~~

.. code-block:: text

    See :cite:t:`1987:nelson` for an introduction to non-standard analysis.
    Non-standard analysis is fun :cite:p:`1987:nelson`.

    .. bibliography::

See :cite:t:`1987:nelson` for an introduction to non-standard analysis.
Non-standard analysis is fun :cite:p:`1987:nelson`.

.. bibliography::

.. warning::

    整个文档只能有一处写 ``.. bibliography::`` ，否则编译的时候会报重复引用的警告。如果只想在单个 ``rst`` 文件中写明参考文献，可以使用 ``footcite`` 来避免这种警告。

脚注引用
~~~~~~~~

.. code-block:: text

    See :footcite:t:`1987:nelson` for an introduction to non-standard analysis.
    Non-standard analysis is fun\ :footcite:p:`1987:nelson`.

    .. footbibliography::

See :footcite:t:`1987:nelson` for an introduction to non-standard analysis.
Non-standard analysis is fun\ :footcite:p:`1987:nelson`.

.. footbibliography::

.. note:: 

    使用反斜杠加空格来抑制脚注之前的空格。
