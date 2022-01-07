============
强化学习介绍
============

.. hint:: 
    
    学习强化学习需要具备的先验知识：1）知道怎么搭建神经网络，2）\ :ref:`vector-chain-rule`\ 。

术语介绍
--------

随机变量（Random Variable）和观测值（Observation）
    概率统计中通常用大小写区分随机变量和它的观测值。随机变量用大写，观测值用小写。

概率密度函数（Probability Density Function, PDF）
    它表示在某个确定的取值点附近的可能性。概率密度函数在定义域上的积分：
    连续的 :math:`\int_{\mathcal{X}} p(x)dx = 1` ，离散的 :math:`\int_{x \in \mathcal{X}} p(x)dx = 1`\ 。
    期望：连续的 :math:`\mathbb{E}[f(X)] = \int_{\mathcal{X}} p(x) f(x) dx` ，
    离散的 :math:`\mathbb{E}[f(X)] = \int_{x \in \mathcal{X}} p(x) f(x) dx`\ 。

随机变量的域（Domain）
    观测值的取值范围就是观测变量的域，用花体表示，参考\ :ref:`符号表 <probability-statistics-symbols>`\ 。

随机抽样（Random Sampling）
    这一章提到的随机抽样都是又放回的随机抽样。

智能体（Agent）
    可以理解为研究对象，比如车、人。

状态（State）
    可以理解为当前图像帧。

动作（Action）
    智能体能够表现出的行为。

决策函数（Policy Function）
    根据 State 判断智能体做出 Action 的可能性，决策函数是一个概率密度函数。

状态转移（State Transition）
    根据 Old State 和 Action 判断做出 New State 的可能性，状态转移函数是一个概率密度函数。
    
奖励和回报（Reward and Return）
    回报（Return）也叫累计奖励（Cumulative Future Reward），表示未来获得奖励的总和，记作 :math:`U_t`\ 。
    数学表达式为 :math:`U_t = R_t + R_{t+1} + \dots` 一直加到游戏结束。
    由于未来的奖励和现在的奖励通常并不一样吸引人，我们可以给未来的奖励打个折扣，叫做折扣回报，记作
    :math:`U_t = R_t + \gamma R_{t+1} + \gamma^2 R_{t+2} + \dots` 

动作价值函数（Action Value Function）
    数学表达式为 :math:`Q_\pi(s_t, a_t)=\mathbb{E}[u_t | S_t=s_t, A_t = a_t]`\ 。因为未来的状态和动作均未知，
    可以通过求期望的方式，利用积分把未来的不确定性给积掉，因此 :math:`s_{t+1}, a_{t+1}, \dots` 都被积掉了，
    剩下了 :math:`s_t, a_t`\ 。动作价值函数给动作打分，评价在该决策下，采取这些动作有多大胜算。

最优动作价值函数（Optimal Action Value Function）
    数学表达式为 :math:`Q^{*}(s_t, a_t)=\max\limits_{\pi} Q_\pi(s_t, a_t)`\ 。根据每个决策函数，比较价值函数的值，挑选出最优的价值函数的值。

状态价值函数（State Value Funciton）
    数学表达式为 :math:`V_\pi(s_t)=\mathbb{E}_A[Q_\pi(s_t, A)]`\ 。状态价值函数评价当前状态的好坏，快赢了还是快输了。
    :math:`\mathbb{E}_A[V_\pi(s_t)]` 也能用来评价 :math:`\pi` 的好坏： :math:`\pi` 越好 :math:`\mathbb{E}` 越大。

基本原理
--------

因为 :math:`\pi` 和 :math:`p` 都是概率密度函数，我们依靠这种概率模型，在所有可能的取值集合中随机抽样，可以得到强化学习的两个随机性来源：

1. 下一个动作： :math:`\mathbb{P}[A=a | S=s] = \pi(a | s)`\ 。下一个动作是根据决策函数 :math:`\pi` 随机抽样得到。
2. 下一个状态： :math:`\mathbb{P}[S'=s | S=s, A=a] = p(s' | s, a)`\ 。下一个状态是根据状态转移函数 :math:`p` 随机抽样得到。

.. note:: 

    因为下一个动作会有一个取值集合，比如上、下、左、右，决策函数的指示根据当前状态，做出每个动作的可能性。
    因为下一个状态也会有一个取值集合，比如下雨、晴天，状态转移函数指示在做出当前动作后，分别出现下雨或晴天的可能性。

强化学习的目标是学习决策函数和状态转移函数，从而可以根据这两个函数预测下一个动作和下一个状态，进而使智能体能够做出正确的决策。
因此基本上也就两种基本思路，Policy Based RL 学习 :math:`\pi` 和 Value Based RL 学习 :math:`Q^{*}`\ 。

通过不断地更新智能体的动作和环境的状态，就会得到一个 :math:`(\text{State, Action, Reward})` 轨迹（Trajectory）： 
:math:`(s_1, a_1, r_1), (s_2, a_2, r_2), ..., (s_t, a_t, r_t)`\ 。

在预测过程中通过累计奖励 :math:`U_t` 来判断决策是不是一个好决策， :math:`U_t` 越大越好。因为 :math:`R_i` 依赖于 :math:`S_i` 和 :math:`A_i` ，
:math:`U_t` 依赖于 :math:`R_t, R_{t+1}, \dots`\ ，因此 :math:`U_t` 依赖于 :math:`S_t, A_t, S_{t+1}, A_{t+1}, \dots`\ 。 

更多细节参考 `【金山文档】 深度强化学习, 王树森 <https://kdocs.cn/l/cld4jk5tHgp8>`_
