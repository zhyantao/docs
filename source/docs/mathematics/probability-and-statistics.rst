================
概率论与数理统计
================

分布函数与概率分布
------------------

.. note:: 

    `Cheat Sheet of Probability <https://kdocs.cn/l/cpypzti6jqvK>`_

:math:`E(X^2)=E^2(X)+D(X)` 和 :math:`E(\overline{X}^2)=E^2(\overline{X})+D(\overline{X})` 这两个公式对所有公式都满足吗？

在 `数理统计公式大全 <https://kdocs.cn/l/cq4IXMIWKAG0>`_ 中，多次出现符号 :math:`\lambda` ，其实 :math:`\lambda=\dfrac{1}{\bar{X}}`

概念区分

- 密度：
- 概率密度：
- 概率分布：
- 概率：
- 概率密度函数图像的纵坐标代表的是概率，总面积求和等于 1 。

如何查表（认识符号的含义）角标为概率值。角标有三种叫法，1）信任系数 2）置信度 3）置信水平。置信水平是指某个范围包含参数
:math:`\theta` 真值的可信程度。 :math:`P(\underline{\theta} \leq \theta \leq \overline{\theta}) \geq 1 - \alpha` 。
置信区间并不唯一，因此区间长度也不唯一。

i.i.d. 独立同分布

有一些分布的性质这里并没有写全。可以上网搜索。

一些函数：

- :math:`\theta` 的先验分布： :math:`\pi(\theta)`
- 条件密度函数： :math:`P(x_1, x_2, \dots, x_n | \theta)`
- :math:`x_1, x_2, \dots, x_n` 和参数 :math:`\theta` 的联合密度函数： :math:`P(x_1, x_2, \dots, x_n, \theta) = P(x_1, x_2, \dots, x_n | \theta) \pi(\theta)`
- 参数 :math:`\theta` 的后验密度函数或后验分布： :math:`\pi(\theta | x_1, x_2, \dots, x_n)=\dfrac{P(x_1, x_2, \dots, x_n, \theta)}{P(x_1, x_2, \dots, x_n)} = \dfrac{P(x_1, x_2, \dots, x_n | \theta) \pi(\theta)}{\int P(x_1, x_2, \dots, x_n | \theta) \pi(\theta)\mathrm{d}\theta}`
- 边际分布或 :math:`x_1, x_2, \dots, x_n` 的无条件分布： :math:`P(x_1, x_2, \dots, x_n) = \int P(x_1, x_2, \dots, x_n | \theta) \pi(\theta)\mathrm{d}\theta`

离散型
~~~~~~

- 两点分布
- 二项分布
- 泊松分布
- 几何分布
- 超几何分布

连续型
~~~~~~~

- 均匀分布
- 指数分布
- 正态分布
- 标准正态分布

多维
~~~~~

贝叶斯估计
~~~~~~~~~~

贝叶斯估计是执果索因，在已知结果 :math:`A` 发生的情况下，求 :math:`B_i` 发生的概率。也就是说，探究是哪个原因导致了 :math:`A` 的发生。

:math:`P(B_i|A) = \dfrac{P(AB_i)}{P(A)}=\dfrac{P(B_i)P(A|B_i)}{\displaystyle\sum_{j=1}^nP(B_j)P(A|B_j)}`

:math:`AB_i` 同时发生的概率为已知过程 :math:`B_i` 发生的情况下，结果 :math:`A` 发生的概率与过程 :math:`B_i` 发生的概率的乘积。

:math:`P(A|B_i)=P(A|B_i)P(B_i)`

例如：结果为晚点、不晚点，原因为乘飞机、乘动车、乘非机动车。则可以设

- A：晚点
- B1：乘飞机
- B2：乘动车
- B3：乘非机动车

考虑：

1. 如果求一个结果发生的概率，而且知道这个结果有不同的原因，考虑全概率公式。
2. 已知结果发生，求某个原因发生的概率，考虑贝叶斯公式。

数理统计基础
------------

.. note:: 

    `Cheat Sheet of Statistics <https://kdocs.cn/l/cdcIGVv2EHj9>`_

三种分布
~~~~~~~~~

- :math:`\mathcal{X}^2` 分布
- t 分布
- F 分布

:math:`\mathcal{X}^2` 分布的图像和 F 分布的图像很相似。

t 分布和正态分布的图像很相似。

参数估计
--------

- 矩估计
- 最大似然估计
- 区间估计
- 估计评价

显著性水平 :math:`\alpha` + 置信水平 = 1

假设检验
--------

一般是做双边检验。

做单边检验时，不等号容易写反，这个疑问可以 Google "One-Tailed and Two-Tailed Hypothesis Tests"

分布检验
--------

前提条件： 

- 总体分布已知 
- 非参数假设检验问题

:math:`\mathcal{X}^2` 拟合优度检验 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 分布中不含未知参数的 :math:`\mathcal{X}^2` 检验法

  - 总体为离散分布时的 :math:`\mathcal{X}^2` 检验法
  - 总体为连续分布时的 :math:`\mathcal{X}^2` 检验法

- 分布中含未知参数的 :math:`\mathcal{X}^2` 检验法

列联表独立性检验 
~~~~~~~~~~~~~~~~
正态性检验
~~~~~~~~~~

- W 检验
- D 检验

方差分析
--------

方差分析是检验两个或多个总体均值之间是否存在差异的方法。

方差分析的目的是将试验误差所引起的结果差异与试验条件的改变（即各因子不同水平的变化）所引起的结果差异区分开，
以便能够抓住问题的实质，此外，还要将试验结果的主要因子和次要因子区分开来，以便集中力量研究几个主要因子。

单因素方差分析
~~~~~~~~~~~~~~~

实质是检验若干个具有相同方差的正态总体的均值是否相等的一种统计方法。

无交互作用的双因素无重复试验方差分析
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
有交互作用的双因素方差分析
~~~~~~~~~~~~~~~~~~~~~~~~~~

回归分析
---------

正交试验设计
------------

正交试验设计方法是一种研究多因子试验问题的重要数学方法。主要使用正交表这一工具来进行整体设计、综合比较、统计分析。


其他资源
--------

- `数理统计手抄，带示例，挺好的 <https://kdocs.cn/l/cnz6IbIdC1p1>`_
- `可以作为上面的补充材料，更全面 <https://kdocs.cn/l/ce7Qrzy5O9zK>`_
- `带有详细解释的小抄表 <https://kdocs.cn/l/cuUQ21Xer5d0>`_
- `制作精良的总结，有时间一定要读一下 <https://kdocs.cn/l/cdeLJEPc9zWG>`_
