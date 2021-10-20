======
符号表
======

.. note:: 

    其他 :math:`LaTeX` 符号参考 `一份不太简短的 LaTeX 2ε 介绍 <https://www.kdocs.cn/p/136412211457>`_ 4.9 小节。
    数学符号所代表的数学含义参考 `Wikipedia <https://en.wikipedia.org/wiki/List_of_mathematical_symbols_by_subject>`_ 。

.. tip:: 

    数学是符号的艺术，能够认识和理解符号背后的含义，才能步入数学的殿堂。

.. _symbol-definition:

通用符号
--------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 20, 30, 40

    ":math:`x`", "标量", "``:math:`x```", "小写意大利体， :math:`LaTeX` 默认字体"
    ":math:`\mathbf{x}`", "向量", "``:math:`\mathbf{x}```", "小写粗体，高中时写作 :math:`\vec{x}` "
    ":math:`\mathbf{X}`", "矩阵(或多维)", "``:math:`\mathbf{X}```", "大写粗体"
    ":math:`\mathrm{d}`", "求导数", "``:math:`\mathrm{d}```", "直立的 :math:`\mathrm{d}` "
    ":math:`\partial`", "求偏导", "``:math:`\partial```", "求导符号 :math:`\mathrm{d}` 的变体"
    ":math:`\nabla`", "求梯度", "``:math:`\nabla```", "向量微分算子"

.. note::

    :math:`f(x;\theta)` 中的分号用来分开自变量和参数。

元学习和小样本学习
------------------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 40, 40, 15

    ":math:`M_{meta}`", "元学习模型", "``:math:`M_{meta}```", "大写粗体"
    ":math:`M_{fine-tune}`", "数学模型（小样本模型）", "``:math:`M_{fine-tune}```", "大写粗体"
    ":math:`\mathcal{D}_{meta-train}`", "用于训练 :math:`M_{meta}` 的数据集", "``:math:`\mathcal{D}_{meta-train}```", "大写花体"
    ":math:`\mathcal{D}_{meta-test}`", "用于训练和测试 :math:`M_{fine-tune}` 的数据集", "``:math:`\mathcal{D}_{meta-test}```", "大写花体"
    ":math:`\mathcal{T}`", ":math:`\mathcal{D}` 的一行，即神经网络输入", "``:math:`\mathcal{T}```", "大写花体"
    ":math:`C_1 \sim C_{10}`", ":math:`\mathcal{D}_{meta-train}` 中的 10 个类别", "``:math:`C_1 \sim C_{10}```", "大写粗体"
    ":math:`P_1 \sim P_{5}`", ":math:`\mathcal{D}_{meta-test}` 中的 5 个类别", "``:math:`P_1 \sim P_{5}```", "大写粗体"
    ":math:`\mathcal{L}`", "损失函数", "``:math:`\mathcal{L}```", "大写花体"


概率和统计
----------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 20, 30, 40

    ":math:`X`", "随机变量", "``:math:`X```", "大写意大利体"
    ":math:`\mathcal{N}(\cdot)`", "正态分布", "``\mathcal{N}(\cdot)```", "大写花体"

矩阵分析
--------

.. csv-table::
    :header: "符号", "含义", ":math:`\LaTeX` 语法", "备注"
    :widths: 15, 20, 30, 40

    ":math:`\mathscr{F}`", "函数空间", "``:math:`\mathscr{F}```", "大写花体"
    ":math:`\mathbb{R}`", "实数域", "``:math:`\mathbb{R}```", "黑板体"
    ":math:`\mathbb{C}`", "复数域", "``:math:`\mathbb{C}```", "黑板体"
    ":math:`\mathbb{Q}`", "有理数域", "``:math:`\mathbb{Q}```", "黑板体"
