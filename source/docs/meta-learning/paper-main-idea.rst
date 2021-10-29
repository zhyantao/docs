============
论文主要思路
============

.. note:: 

    现在各种各样的 Meta Learning 研究，大多都是 HyperNetwork、MAML、条件神经网络这三种方法。要么改改网络结构，要么结合一下这三种的方法。

HyperNetwork
-------------

HyperNetwork 主要用来生成参数 :footcite:p:`zoph2016neural` 。它使用 :math:`\mathcal{D}_{train}` 来训练 HyperNetwork 得到
:math:`h(\mathcal{D}_{train};\varphi)` ，这里的 :math:`\varphi` 就是网络的超参数，HyperNetwork 也就是 Meta Network 了。
我们可以使用 :math:`\varphi` 来进一步训练小样本神经网络 :math:`f(x_{test};\theta)` 得到参数 :math:`\theta` 。

基于记忆 Memory 的方法
----------------------

把上次的标签作为下一次的输入 :footcite:p:`santoro2016meta`  :footcite:p:`munkhdalai2017meta` 。

基于预测梯度的方法
-------------------

目的是加快网络的更新速度 :footcite:p:`andrychowicz2016learning` 。
将经验风险最小化损失的梯度，同样传导到 meta learner 上，更新其参数；通常 inner loop（Learner）更新N步，outer loop（Meta Learner）更新一步。

利用 Attention 注意力机制方法
-----------------------------

利用以往的任务训练一个 Attention 模型，从而面对新任务时，能够直接关注最重要的部分 :footcite:p:`vinyals2016matching` 。

借鉴 LSTM 的方法更新网络参数
-----------------------------

LSTM 的内部更新机制非常类似于梯度下降的更新。借用 LSTM 的网络结构，输入当前网络的参数，直接输出新的更新参数 :footcite:p:`ravi2017optimization` 。

面向 RL 的 Meta Learning 方法
-----------------------------

增加一些外部信息，如 reward、action 来实现增强学习的自主学习能力 :footcite:p:`wang2016learning`  :footcite:p:`duan2016rl` 。

MAML 基于梯度的做法
-------------------

通过训练一个好的 base model，将 model 同时应用到监督学习和 RL。作者想训练一个通用的模型，既可以用于监督学习，也可以用于增强学习 :footcite:p:`finn2017model` 。

1. 采集 task，得到 :math:`\mathcal{D}_{train}` 和 :math:`\mathcal{D}_{test}`
2. 使用 :math:`\mathcal{D}_{train}` 训练少数几步，得到新参数
3. 利用新参数训练 :math:`\mathcal{D}_{test}` ，用梯度下降更新参数

缺点：为什么用两次梯度下降？容易引起梯度爆炸和导致训练变慢，无法应用到大网络比如 ResNet 。

条件神经网络
------------

利用 WaveNet 方法，充分利用历史数据。这是一个思路简单，效果极好的 **SOTA** :footcite:p:`mishra2017meta` 。缺点：总是拖着条件。

参考文献
--------

.. footbibliography::
