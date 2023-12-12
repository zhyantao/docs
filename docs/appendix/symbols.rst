.. _symbols:

======
符号表
======

数学是符号的艺术，能够认识和理解符号背后的含义，才能步入数学的殿堂。更多 :math:`LaTeX` 符号参考：

- :ref:`LaTeX 入门 <latex-basic>`
- `一份不太简短的 LaTeX 2ε 介绍 <https://www.kdocs.cn/p/136412211457>`_ 4.9 小节
- `常用数学符号和公式排版 <https://www.latexlive.com/help#d11>`_
- `在线 LaTeX 公式编辑器 <https://www.latexlive.com>`_ （可导出为图片）

.. hint::

    函数 :math:`f(x;\theta)` 中的分号用来分隔自变量和参数。

    概率 :math:`p(\theta | \phi^*)` 中的竖线用来分隔自变量和参数。

    表达式 :math:`\alpha = \arg \min\limits_{\omega \in W} d(\beta, \omega), \ \forall \omega \in W`
    的意思：当函数取最小值时，将 :math:`\omega` 的值赋给 :math:`\alpha`。

    表达式 :math:`\alpha = \min\limits_{\omega \in W} d(\beta, \omega), \ \forall \omega \in W`
    的意思：当函数取最小值时，将这个最小值赋给 :math:`\alpha`。

.. _symbol-definition:

通用符号
--------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 20, 20, 40

    ":math:`x`", "标量", "``x``", "小写意大利体， :math:`LaTeX` 默认字体"
    ":math:`\tilde{x}`", "变量的取值", "``\tilde{x}``", "字母上有波浪号，表示 :math:`x` 取的特定值"
    ":math:`\mathbf{x}`", "向量", "``\mathbf{x}``", "小写粗体，高中时写作 :math:`\vec{x}` "
    ":math:`\mathbf{X}`", "矩阵(或多维)", "``\mathbf{X}``", "大写粗体"
    ":math:`\mathrm{d}`", "求导数", "``\mathrm{d}``", "直立的 :math:`\mathrm{d}` "
    ":math:`\partial`", "求偏导", "``\partial``", "求导符号 :math:`\mathrm{d}` 的变体"
    ":math:`\nabla_\theta`", "对 :math:`\theta` 求梯度", "``\nabla_\theta``", "向量微分算子"

.. _probability-statistics-symbols:

概率和统计
----------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 30, 20, 20

    ":math:`X`", "观测变量（也叫随机变量）", "``X``", "大写意大利体"
    ":math:`x`", "观测值", "``x``", "小写意大利体"
    ":math:`p(x)`", "观测变量取观测值时的概率", "``p(x)``", "小写意大利体"
    ":math:`\mathcal{X}`", "观测变量的取值空间", "``\mathcal{X}``", "大写花体"
    ":math:`\mathcal{N}(\cdot)`", "正态分布", "``\mathcal{N}(\cdot)``", "大写花体"
    ":math:`\mathbb{E}`", "数学期望", "``\mathbb{E}``", "黑板体"


矩阵分析
--------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 20, 20, 20

    ":math:`\mathscr{F}`", "函数空间", "``\mathscr{F}``", "大写花体"
    ":math:`\mathbb{R}`", "实数域", "``\mathbb{R}``", "黑板体"
    ":math:`\mathbb{C}`", "复数域", "``\mathbb{C}``", "黑板体"
    ":math:`\mathbb{Q}`", "有理数域", "``\mathbb{Q}``", "黑板体"

.. _set-theory:

集合论
-------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 10, 25, 20, 50

    ":math:`\subset`", "真包含（真子集）", "``\subset``", "高中课本记作 :math:`\subsetneqq`，也有书记作 :math:`\subsetneq`"
    ":math:`\subseteq`", "包含（子集）", "``\subseteq``", "高中课本记作 :math:`\subset`，因此有歧义， `注意约定 <https://zh.wikipedia.org/wiki/%E5%AD%90%E9%9B%86>`_"
    ":math:`\in`", "属于", "``\in``", ":math:`a \in A`"
    ":math:`\notin`", "不属于", "``\notin``", ":math:`a \notin A`"

.. _Meta-FSL-symbols:

机器学习
--------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 40, 30, 20

    ":math:`M_{meta}`", "元学习模型", "``M_{meta}``", "大写"
    ":math:`M_{fine-tune}`", "数学模型（小样本模型）", "``M_{fine-tune}``", "大写"
    ":math:`\mathscr{D}_{meta-train}`", "用于训练 :math:`M_{meta}` 的数据集", "``\mathscr{D}_{meta-train}``", "大写花体"
    ":math:`\mathscr{D}_{meta-test}`", "用于训练和测试 :math:`M_{fine-tune}` 的数据集", "``\mathscr{D}_{meta-test}``", "大写花体"
    ":math:`\mathcal{D}_{train}`", "支持集（Support Set）", "``\mathcal{D}_{train}``", "大写花体"
    ":math:`\mathcal{D}_{test}`", "查询集（Query Set）", "``\mathcal{D}_{test}``", "大写花体"
    ":math:`\mathcal{T}` aka task", ":math:`\mathcal{D}` 的一行，即神经网络输入", "``\mathcal{T}``", "大写花体"
    ":math:`C_1 \sim C_{10}`", ":math:`\mathcal{D}_{meta-train}` 中的 10 个类别", "``C_1 \sim C_{10}``", "大写"
    ":math:`P_1 \sim P_{5}`", ":math:`\mathcal{D}_{meta-test}` 中的 5 个类别", "``P_1 \sim P_{5}``", "大写"
    ":math:`\mathcal{L}`", "损失函数", "``\mathcal{L}``", "大写花体"

数据库
-------
.. csv-table::
    :header: "符号","含义",":math:`\LaTeX` 语法", "备注"
    :widths: 10, 15, 30, 10

    ":math:`\Pi`\ ","投影","``\Pi``",""
    ":math:`\sigma`\ ","选择","``\sigma``",""
    ":math:`\rho`\ ","重命名","``\rho``",""
    ":math:`\mathcal{G}`\ ","聚合函数","``\mathcal{G}``",""
    ":math:`\cap`\ ","交","``\cap``",""
    ":math:`\cup`\ ","补","``\cup``",""
    ":math:`\bowtie`\ ","自然连接","``\bowtie``",""
    ":math:`\mathop{\bowtie}\limits_{A \theta B}^{}`\ ","内连接","``\mathop{\bowtie}\limits_{A \theta B}^{}``",""
    "⟕","左外连接","--",""
    "⟖","右外连接","--",""
    "⟗","全外连接","--",""
    ":math:`\times`\ ","笛卡尔乘积","``\times``",""
    ":math:`\div`\ ","除","``\div``",""
    ":math:`\leftarrow`\ ","赋值","``\leftarrow``",""
    ":math:`\land` or :math:`\vee`\ ","条件并列","``\land`` or ``\vee``",""
    ":math:`\neg`\ ","非","``\neg``",""
    ":math:`\exists`\ ","存在","``\exists``",""
    ":math:`\forall`\ ","对所有","``\forall``",""
    ":math:`\gt\ge\lt\le\ne`\ ","比较","``\gt\ge\lt\le\ne``",""
    ":math:`\overset{F}{\rightarrow}`","函数依赖","``\overset{F}{\rightarrow}``",""
