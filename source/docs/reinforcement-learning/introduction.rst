============
强化学习介绍
============

强化学习比较难的原因就是因为它有很多专业术语。以超级玛丽为例，理解机器学习中的几个常用的术语。
注意，R 大写表示游戏还未结束，r 小写表示游戏已经结束，获得了观测值。

- state 状态
- action 
- agent
- policy :math:`\pi`
- reward R
- state transition

:math:`\pi` 是一个概率密度函数

- :math:`\pi : (s, a) \mapsto [0, 1]`
- :math:`\pi (a|s) = \mathbb{P}(A=a|S=s)`

Action-Value Function :math:`Q(s, a)`

:math:`Q_{\pi}(s_t, a_t)=\mathbb{E}[u_t|S_t=s_t, A_t=a_t]`

