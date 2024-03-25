==========
概率论基础
==========

分布函数与概率分布
------------------

.. note::

    `Cheat Sheet of Probability <https://kdocs.cn/l/cpypzti6jqvK>`_

:math:`E(X^2)=E^2(X)+D(X)` 和 :math:`E(\overline{X}^2)=E^2(\overline{X})+D(\overline{X})` 这两个公式对所有公式都满足吗？

在 `数理统计公式大全 <https://kdocs.cn/l/cq4IXMIWKAG0>`_ 中，多次出现符号 :math:`\lambda`，其实 :math:`\lambda=\dfrac{1}{\bar{X}}`

概念区分

- 密度：
- 概率密度：
- 概率分布：
- 概率：
- 概率密度函数图像的纵坐标代表的是概率，总面积求和等于 1。

如何查表（认识符号的含义）角标为概率值。角标有三种叫法，1）信任系数 2）置信度 3）置信水平。置信水平是指某个范围包含参数
:math:`\theta` 真值的可信程度。 :math:`P(\underline{\theta} \leq \theta \leq \overline{\theta}) \geq 1 - \alpha`。
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


- `Probability Cheatsheet v2.0 <https://kdocs.cn/l/cuUQ21Xer5d0>`_
