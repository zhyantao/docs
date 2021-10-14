========================
深度学习中的矩阵计算规则
========================

编辑此文时，我参考了 :footcite:t:`DBLP:journals/corr/abs-1802-01528` 的论文，复习时可以在
`之前的笔记 <https://www.kdocs.cn/p/135966556760>`_ 上进行补充说明。

作者在 :footcite:p:`DBLP:journals/corr/abs-1802-01528` 中对推导过程做了介绍，以及一些结论的总结。

只有对前四章的数学基础完全理解后，才能对后续章节的应用做到了如指掌。

有时候想一想，这种计算规则，其实本质上就是约定个 shape 的事。

.. tip:: 

    - 向量或标量的一切运算规则都要基于标量运算规则，都要考虑转换到标量形式时才能进行相关计算；
    - 向量或矩阵的求导规则运用多元微分学的知识，对某个变量求导时，其他变量看作常数；
    - 学习路线：标量求导、向量求导、矩阵求导、一元微分(求导)链式法则、向量微分链式法则。

.. note:: 

    凡是书写数学相关的内容，都应当遵守 :ref:`符号定义 <symbol-definition>` 规则，这样方便后续阅读和理解，至少对于一个人来讲是如此。

    以前，我们知道含有变量的函数的求导方法 :math:`(x^2)'=2x` ，现在对如果将 :math:`x` 表示为数字 5 ，那么他的导数是什么？很明显，我们以前的先验知识告诉我们，答案是 10 。

    现在，因为在神经网络上，神经元之间的连接通常是线性关系，因此，大概率的情况下，不会出现二次方以及对数函数等其他我们在高中阶段就已经学习过的复杂函数。
    因为通常来讲，我们一般的做法是将神经元上的数字乘以与之相连接的边的权重，再加上某个偏置，即可得到输出。因此，对于单个神经元来讲，它就是线性的。
    正因为这种线性关系的存在，我们在下面的假设中，会通常假设 :math:`\mathbf{f}(\mathbf{w})=\mathbf{w}, \mathbf{g}(\mathbf{x})=\mathbf{x}`
    隐含意思就是对于神经网络的某一层来讲，影响权值和偏置的函数有两个，分别是 :math:`f_i` 和 :math:`g_i` 。他们分别作用于权重 :math:`f_i(\mathbf{w})` 和神经元 :math:`g_i(\mathbf{x})` 。
    计算得到的结果用于下一层神经元的输入，但是为什么计算结果还是记作 :math:`\mathbf{w}` 和 :math:`\mathbf{b}` 呢？这里并不是很懂，也就是说，为什么要假设 :math:`f_i(\mathbf{w})=\mathbf{w}` ？
    是因为激活函数选择了 ReLU 的缘故吗？

词汇释义
--------
    
- **binary：** 二元的
- **unary：** 一元的
- **derivatives：** 导数，或称微分
- **total derivative：** 全微分（假设变量间互相依赖）
- **partical derivative：** 偏微分（假设除 x 外都是常量）
- **with respect to：** 作用于
- **nested：** 嵌套的
- **whereas：** 但是
- **commute：** 交换(律)

.. note:: 

    关于全微分和偏微分的理解可能网络上并不一致。参考 :footcite:p:`DBLP:journals/corr/abs-1802-01528` 第 19 页，第 4 段。

.. _scalar-derivative-rules:

标量求导
--------

.. csv-table::
    :header: ":math:`f(x)`", "对 :math:`x` 求导", "Example"

    ":math:`c`", ":math:`0`", ":math:`\dfrac{\mathrm d}{\mathrm d x}99=0`"
    ":math:`cf`", ":math:`c\dfrac{\mathrm d f}{\mathrm d x}`", ":math:`\dfrac{\mathrm d}{\mathrm d x}3x=3`"
    ":math:`x^n`", ":math:`nx^{n-1}`", ":math:`\dfrac{\mathrm d}{\mathrm d x}x^3=3x^2`"
    ":math:`f+g`", ":math:`\dfrac{\mathrm d f}{\mathrm d x}+\dfrac{\mathrm d g}{\mathrm d x}`", ":math:`\dfrac{\mathrm d}{\mathrm d x}(x^2+3x)=2x+3`"
    ":math:`f-g`", ":math:`\dfrac{\mathrm d f}{\mathrm d x}-\dfrac{\mathrm d g}{\mathrm d x}`", ":math:`\dfrac{\mathrm d}{\mathrm d x}(x^2-3x)=2x-3`"
    ":math:`fg`", ":math:`f\dfrac{\mathrm d g}{\mathrm d x}+\dfrac{\mathrm d f}{\mathrm d x}g`", ":math:`\dfrac{\mathrm d}{\mathrm d x}(x^2x)=x^2+x2x=3x^2`"
    ":math:`f\big(g(x)\big)`", ":math:`\dfrac{\mathrm d f(u)}{\mathrm d u}\dfrac{\mathrm d u}{\mathrm d x}, let\ u= g(x)`", ":math:`\dfrac{\mathrm d}{\mathrm d x}\ln{x^2}=\dfrac{1}{x^2}2x=\dfrac{2}{x}`"

向量求导
--------

设 :math:`f(x, y) = 3 x^2 y` ，即 :math:`\mathbf{x} = \begin{bmatrix} x \\ y \end{bmatrix}` ， :math:`f(\mathbf{x})=3x^2y` 。

:math:`\nabla f(x, y) =\begin{bmatrix}\dfrac{\partial f(x,y)}{\partial x}, \dfrac{\partial f(x,y)}{\partial y}\end{bmatrix}=\begin{bmatrix}6yx, 3x^2\end{bmatrix}`

.. note:: 

    这里使用了分子布局（ :math:`\mathit{Numerator\ layout}` ）。
    
.. tip:: 

    设向量 :math:`\mathbf{x}` 表示一组变量 :math:`\mathbf{x} = \begin{bmatrix} \mathit{x_1} \\ \mathit{x_1} \\ \vdots \\ \mathit{x_n} \\ \end{bmatrix}` ，
    向量 :math:`\mathbf{f}` 表示一组函数 :math:`\mathbf{f} = \begin{bmatrix} \mathit{f_1} \\ \mathit{f_1} \\ \vdots \\ \mathit{f_m} \\ \end{bmatrix}` ，
    当 :math:`\mathbf{f}` 中的某个函数 :math:`\mathit{f_i}` 作用于向量 :math:`\mathbf{x}` 时，其实质是
    :math:`f_i(\mathbf{x}) = 2 \mathit{x_1}^2 + 3 \mathit{x_2} + \dots` 这种形式。

矩阵求导
--------

设 :math:`\begin{bmatrix}f(x,y)=3x^2y \\ g(x,y)=2x+y^8 \end{bmatrix}` ，则 :math:`\mathit{Jacobian\ matrix}` 为：

.. math::

    J = 
        \begin{bmatrix}
            \nabla f(x,y) \\\\
            \nabla g(x,y) 
        \end{bmatrix} = 
        \begin{bmatrix}
            \dfrac{\partial f(x,y)}{\partial x} & \dfrac{\partial f(x,y)}{\partial y} \\\\
            \dfrac{\partial g(x,y)}{\partial x} & \dfrac{\partial g(x,y)}{\partial y}
        \end{bmatrix} = 
        \begin{bmatrix}
            6yx & 3x^2 \\\\
            2 & 8y^7
        \end{bmatrix}


.. note:: 

    :math:`\mathit{Jacobian\ matrix}` 的一般形式： :math:`\mathbf{y}=\mathbf{f}(\mathbf{x})` 。

    其中， :math:`\mathbf{x}=\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}` ，
    :math:`\mathbf{y}=\begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_m \end{bmatrix}` ，
    :math:`\mathbf{f}(\mathbf{x})=\begin{bmatrix} f_1(\mathbf{x}) \\ f_2(\mathbf{x}) \\ \vdots \\ f_m(\mathbf{x}) \end{bmatrix}`
    ，将 :math:`f_i(\mathbf{x})` 展开后，可以得到标量形式 :math:`f_i(\mathbf{x}) = 2 \mathit{x_1}^2 + 3 \mathit{x_2} + \dots`
    。需要注意的是： :math:`|\mathbf{x}|=n` 但是 :math:`|\mathbf{y}|=|\mathbf{f}|=m` 。
    
    .. math::

        J = 
            \dfrac{\partial \mathbf{y}}{\partial \mathbf{x}} =
            \begin{bmatrix}
                \nabla f_1(\mathbf{x}) \\\\
                \nabla f_2(\mathbf{x}) \\\\
                \vdots \\\\
                \nabla f_m(\mathbf{x})
            \end{bmatrix} = 
            \begin{bmatrix}
                \dfrac{\partial}{\partial \mathbf{x}}f_1(\mathbf{x}) \\\\
                \dfrac{\partial}{\partial \mathbf{x}}f_2(\mathbf{x}) \\\\
                \vdots \\\\
                \dfrac{\partial}{\partial \mathbf{x}}f_m(\mathbf{x})
            \end{bmatrix} = 
            \begin{bmatrix}
                \dfrac{\partial}{\partial x_1}f_1(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_1(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_1(\mathbf{x}) \\\\
                \dfrac{\partial}{\partial x_1}f_2(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_2(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_2(\mathbf{x}) \\\\
                \vdots & \vdots & \ddots & \vdots \\\\
                \dfrac{\partial}{\partial x_1}f_m(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_m(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_m(\mathbf{x})
            \end{bmatrix}

    注意到，我们在展开 :math:`\dfrac{\partial \mathbf{y}}{\partial \mathbf{x}}` 时，是按照分子竖着展开，分母横着展开的，这种展开方式叫做分子布局（ :math:`\mathit{Numerator\ layout}` ）。其实还有另外相反的一种展开方式，叫做分母布局（ :math:`\mathit{Denominator\ layout}` ）。作者在论文中一直使用的是分子布局。

    这种展开规则 **很重要** ，这是解向量求导问题的一个 **突破点** ，学会了展开规则，向量求导就变得非常简单了，因为你可以通过目标方程目测出结果矩阵的形状，而且，结果矩阵是标量形式的。

.. tip:: 

    恒等函数（ :math:`\mathit{Identity\ function}` ） :math:`\mathbf{y}=\mathbf{f}(\mathbf{x})=\mathbf{x}` ，即 :math:`y_i = f_i(\mathbf{x})=x_i` ，在文中多次出现，是作为一个简单的 demo 来诠释概念是应该如何理解和应用的。

    这里需要注意的是在恒等函数中 :math:`|\mathbf{x}|=|\mathbf{y}|=|\mathbf{f}|=n` 。

    .. math::

        J &= 
            \dfrac{\partial \mathbf{y}}{\partial \mathbf{x}} =
            \begin{bmatrix}
            \nabla f_1(\mathbf{x}) \\\\
            \nabla f_2(\mathbf{x}) \\\\
            \vdots \\\\
            \nabla f_m(\mathbf{x})
            \end{bmatrix} = 
            \begin{bmatrix}
            \dfrac{\partial}{\partial \mathbf{x}}f_1(\mathbf{x}) \\\\
            \dfrac{\partial}{\partial \mathbf{x}}f_2(\mathbf{x}) \\\\
            \vdots \\\\
            \dfrac{\partial}{\partial \mathbf{x}}f_m(\mathbf{x})
            \end{bmatrix} \\\\
        &= \begin{bmatrix}
            \dfrac{\partial}{\partial x_1}f_1(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_1(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_1(\mathbf{x}) \\\\
            \dfrac{\partial}{\partial x_1}f_2(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_2(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_2(\mathbf{x}) \\\\
            \vdots & \vdots & \ddots & \vdots \\\\
            \dfrac{\partial}{\partial x_1}f_m(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_m(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_m(\mathbf{x})
            \end{bmatrix} \\\\
        &= \begin{bmatrix}
            \dfrac{\partial}{\partial x_1}x_1 & \dfrac{\partial}{\partial x_2}x_1 & \dots & \dfrac{\partial}{\partial x_n}x_1 \\\\
            \dfrac{\partial}{\partial x_1}x_2 & \dfrac{\partial}{\partial x_2}x_2 & \dots & \dfrac{\partial}{\partial x_n}x_2 \\\\
            \vdots & \vdots & \ddots & \vdots \\\\
            \dfrac{\partial}{\partial x_1}x_n & \dfrac{\partial}{\partial x_2}x_n & \dots & \dfrac{\partial}{\partial x_n}x_n
            \end{bmatrix} \\\\
        &= \text{ (and since } \dfrac{\partial}{\partial x_j}x_i=0\ \text{ for } j \neq i \text{)} \\\\
        &= \begin{bmatrix}
            \dfrac{\partial}{\partial x_1}x_1 & 0 & \dots & 0 \\\\
            0 & \dfrac{\partial}{\partial x_2}x_2 & \dots & 0 \\\\
            \vdots & \vdots & \ddots & \vdots \\\\
            0 & 0 & \dots & \dfrac{\partial}{\partial x_n}x_n
            \end{bmatrix} \\\\
        &= \begin{bmatrix}
            1 & 0 & \dots & 0 \\\\
            0 & 1 & \dots & 0 \\\\
            \vdots & \vdots & \ddots & \vdots \\\\
            0 & 0 & \dots & 1
            \end{bmatrix} \\\\
        &= I\ (I\ \mathrm{is\ the\ identity\ matrix\ with\ ones\ down\ the\ diagonal})

Example 1
~~~~~~~~~~

已知 :math:`\mathbf{y}=\mathbf{f}(\mathbf{w})\bigcirc\mathbf{g}(\mathbf{x})` ， :math:`|\mathbf{y}|=|\mathbf{w}|=|\mathbf{x}|=m=n` 。求 :math:`\nabla \mathbf{y}` 。

.. math::

    \begin{bmatrix}
    y_1 \\\\ y_2 \\\\ \vdots \\\\ y_n
    \end{bmatrix} = 
    \begin{bmatrix}
    f_1(\mathbf{w}) \bigcirc g_1(\mathbf{x}) \\\\
    f_1(\mathbf{w}) \bigcirc g_2(\mathbf{x}) \\\\
    \vdots \\\\
    f_1(\mathbf{w}) \bigcirc g_n(\mathbf{x})
    \end{bmatrix}

.. note:: 

    :math:`\bigcirc` 是向量的二元操作符（代表加减乘除： :math:`\oplus\ \ominus\ \otimes\ \oslash` ）。向量的四则运算与标量四则运算略有不同，它们是元素级别的操作，比如
    :math:`\begin{bmatrix} 1 \\ 2 \end{bmatrix} + \begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} 4 \\ 6 \end{bmatrix}` 。

求 :math:`\nabla \mathbf{y}` 的过程即求解 :math:`\mathit{Jacobian\ matrix}` 的过程，如下：

.. math::

    J_\mathbf{w} 
    &= \dfrac{\partial \mathbf{y}}{\partial \mathbf{w}} \\\\
    &= \begin{bmatrix} 
        \dfrac{\partial}{\partial w_1}f_1(\mathbf{w}) \bigcirc g_1(\mathbf{x}) & \dfrac{\partial}{\partial w_2}f_1(\mathbf{w}) \bigcirc g_1(\mathbf{x}) & \dots & \dfrac{\partial}{\partial w_n}f_1(\mathbf{w}) \bigcirc g_1(\mathbf{x}) \\\\
        \dfrac{\partial}{\partial w_1}f_2(\mathbf{w}) \bigcirc g_2(\mathbf{x}) & \dfrac{\partial}{\partial w_2}f_2(\mathbf{w}) \bigcirc g_2(\mathbf{x}) & \dots & \dfrac{\partial}{\partial w_n}f_2(\mathbf{w}) \bigcirc g_2(\mathbf{x}) \\\\
        \vdots & \vdots & \ddots & \vdots \\\\
        \dfrac{\partial}{\partial w_1}f_n(\mathbf{w}) \bigcirc g_n(\mathbf{x}) & \dfrac{\partial}{\partial w_2}f_n(\mathbf{w}) \bigcirc g_n(\mathbf{x}) & \dots & \dfrac{\partial}{\partial w_n}f_n(\mathbf{w}) \bigcirc g_n(\mathbf{x})
        \end{bmatrix} \\\\
    &= \text{(and since } \dfrac{\partial}{\partial w_j}\big(f_i(\mathbf{w}) \bigcirc g_i(\mathbf{x}) \big) = 0\ \text{ for } j \neq i \text{)} \\\\
    &= \begin{bmatrix}
        \dfrac{\partial}{\partial w_1}f_1(w_1) \bigcirc g_1(x_1) & 0 & \dots & 0 \\\\
        0 & \dfrac{\partial}{\partial w_2}f_2(w_2) \bigcirc g_2(x_2) & \dots & 0 \\\\
        \vdots & \vdots & \ddots & \vdots \\\\
        0 & 0 & \dots & \dfrac{\partial}{\partial w_n}f_n(w_n) \bigcirc g_n(x_n)
        \end{bmatrix} \\\\
    &= diag\big(\dfrac{\partial}{\partial w_1}f_1(w_1) \bigcirc g_1(x_1) \quad \dfrac{\partial}{\partial w_2}f_2(w_2) \bigcirc g_2(x_2) \quad \dots \quad \dfrac{\partial}{\partial w_n}f_n(w_n) \bigcirc g_n(x_n) \big) \\\\
    &= \text{(and assume } \mathbf{f}(\mathbf{w})=\mathbf{w}\text{, for most case)} \\\\
    &= \text{(and so }f_i(\mathbf{w})=\mathbf{w}\text{)} \\\\
    &= \text{(and then }f_i(w_i)=w_i\text{)} \\\\
    &= diag\big(\dfrac{\partial}{\partial w_1} w_1 \bigcirc x_1 \quad \dfrac{\partial}{\partial w_2} w_2 \bigcirc x_2 \quad \dots \quad \dfrac{\partial}{\partial w_n} w_n \bigcirc x_n \big)

同理：

.. math::

    J_\mathbf{x} 
    &= \dfrac{\partial \mathbf{y}}{\partial \mathbf{x}} \\\\
    &= \begin{bmatrix} 
        \dfrac{\partial}{\partial x_1}f_1(\mathbf{w}) \bigcirc g_1(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_1(\mathbf{w}) \bigcirc g_1(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_1(\mathbf{w}) \bigcirc g_1(\mathbf{x}) \\\\
        \dfrac{\partial}{\partial x_1}f_2(\mathbf{w}) \bigcirc g_2(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_2(\mathbf{w}) \bigcirc g_2(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_2(\mathbf{w}) \bigcirc g_2(\mathbf{x}) \\\\
        \vdots & \vdots & \ddots & \vdots \\\\
        \dfrac{\partial}{\partial x_1}f_n(\mathbf{w}) \bigcirc g_n(\mathbf{x}) & \dfrac{\partial}{\partial x_2}f_n(\mathbf{w}) \bigcirc g_n(\mathbf{x}) & \dots & \dfrac{\partial}{\partial x_n}f_n(\mathbf{w}) \bigcirc g_n(\mathbf{x})
        \end{bmatrix} \\\\
    &= \text{(and since } \dfrac{\partial}{\partial x_j}\big(f_i(\mathbf{w}) \bigcirc g_i(\mathbf{x}) \big) = 0\ \text{ for } j \neq i \text{)} \\\\
    &= \begin{bmatrix}
        \dfrac{\partial}{\partial x_1}f_1(w_1) \bigcirc g_1(x_1) & 0 & \dots & 0 \\\\
        0 & \dfrac{\partial}{\partial x_2}f_2(w_2) \bigcirc g_2(x_2) & \dots & 0 \\\\
        \vdots & \vdots & \ddots & \vdots \\\\
        0 & 0 & \dots & \dfrac{\partial}{\partial x_n}f_n(w_n) \bigcirc g_n(x_n)
        \end{bmatrix} \\\\
    &= diag\big(\dfrac{\partial}{\partial x_1}f_1(w_1) \bigcirc g_1(x_1) \quad \dfrac{\partial}{\partial x_2}f_2(w_2) \bigcirc g_2(x_2) \quad \dots \quad \dfrac{\partial}{\partial x_n}f_n(w_n) \bigcirc g_n(x_n) \big) \\\\
    &= \text{(and assume } \mathbf{g}(\mathbf{x})=\mathbf{x}\text{, for most case)} \\\\
    &= \text{(and so }g_i(\mathbf{x})=\mathbf{x}\text{)} \\\\
    &= \text{(and then }g_i(x_i)=x_i\text{)} \\\\
    &= diag\big(\dfrac{\partial}{\partial x_1} w_1 \bigcirc x_1 \quad \dfrac{\partial}{\partial x_2} w_2 \bigcirc x_2 \quad \dots \quad \dfrac{\partial}{\partial x_n} w_n \bigcirc x_n \big)

综上， 

.. math::
        
    \dfrac{\partial}{\partial \mathbf{w}}\mathbf{f}(\mathbf{w}) \oplus \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial w_1} w_1 \oplus x_1 \quad \dfrac{\partial}{\partial w_2} w_2 \oplus x_2 \quad \dots \quad \dfrac{\partial}{\partial w_n} w_n \oplus x_n \big) \\\\
    &= diag\big(1 \quad 1 \quad \dots \quad 1 \big) = I \\\\

    \dfrac{\partial}{\partial \mathbf{w}}\mathbf{f}(\mathbf{w}) \ominus \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial w_1} w_1 \ominus x_1 \quad \dfrac{\partial}{\partial w_2} w_2 \ominus x_2 \quad \dots \quad \dfrac{\partial}{\partial w_n} w_n \ominus x_n \big) \\\\
    &= diag\big(1 \quad 1 \quad \dots \quad 1 \big) = I \\\\

    \dfrac{\partial}{\partial \mathbf{w}}\mathbf{f}(\mathbf{w}) \otimes \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial w_1} w_1 \otimes x_1 \quad \dfrac{\partial}{\partial w_2} w_2 \otimes x_2 \quad \dots \quad \dfrac{\partial}{\partial w_n} w_n \otimes x_n \big) \\\\
    &= diag\big(w_1 \quad w_2 \quad \dots \quad w_n \big) = diag\big(\mathbf{w}\big) \\\\

    \dfrac{\partial}{\partial \mathbf{w}}\mathbf{f}(\mathbf{w}) \oslash \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial w_1} w_1 \oslash x_1 \quad \dfrac{\partial}{\partial w_2} w_2 \oslash x_2 \quad \dots \quad \dfrac{\partial}{\partial w_n} w_n \oslash x_n \big) \\\\
    &= diag\big(\dfrac{1}{x_1} \quad \dfrac{1}{x_2} \quad \dots \quad \dfrac{1}{x_n} \big) \\\\

    \dfrac{\partial}{\partial \mathbf{x}}\mathbf{f}(\mathbf{w}) \oplus \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial x_1} w_1 \oplus x_1 \quad \dfrac{\partial}{\partial x_2} w_2 \oplus x_2 \quad \dots \quad \dfrac{\partial}{\partial x_n} w_n \oplus x_n \big) \\\\
    &= diag\big(1 \quad 1 \quad \dots \quad 1 \big) = I \\\\

    \dfrac{\partial}{\partial \mathbf{x}}\mathbf{f}(\mathbf{w}) \ominus \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial x_1} w_1 \ominus x_1 \quad \dfrac{\partial}{\partial x_2} w_2 \ominus x_2 \quad \dots \quad \dfrac{\partial}{\partial x_n} w_n \ominus x_n \big) \\\\
    &= diag\big(-1 \quad -1 \quad \dots \quad -1 \big) = -I \\\\

    \dfrac{\partial}{\partial \mathbf{x}}\mathbf{f}(\mathbf{w}) \otimes \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial x_1} w_1 \otimes x_1 \quad \dfrac{\partial}{\partial x_2} w_2 \otimes x_2 \quad \dots \quad \dfrac{\partial}{\partial x_n} w_n \otimes x_n \big) \\\\
    &= diag\big(w_1 \quad w_2 \quad \dots \quad w_n \big) = diag\big(\mathbf{w}\big) \\\\

    \dfrac{\partial}{\partial \mathbf{x}}\mathbf{f}(\mathbf{w}) \oslash \mathbf{f}(\mathbf{x}) 
    &= diag\big(\dfrac{\partial}{\partial x_1} w_1 \oslash x_1 \quad \dfrac{\partial}{\partial x_2} w_2 \oslash x_2 \quad \dots \quad \dfrac{\partial}{\partial x_n} w_n \oslash x_n \big) \\\\
    &= diag\big(-\dfrac{w_1}{x_1^2} \quad -\dfrac{w_2}{x_2^2} \quad \dots \quad -\dfrac{w_n}{x_n^2} \big) \\\\

.. note:: 

    当含有常数项时，:math:`\mathbf{y}=\mathbf{f}(\mathbf{w})\bigcirc\mathbf{g}(\mathbf{x})` 变成了 :math:`\mathbf{y}=\mathbf{f}(\mathbf{w})\bigcirc\mathbf{g}(z)` ，其中 :math:`\mathbf{g}(z)=\vec{1}z` 。

Example 2
~~~~~~~~~~

已知 :math:`y=sum\big(\mathbf{f}(\mathbf{x})\big)=\displaystyle\sum_{i=1}^n f_i(\mathbf{x})` 求 :math:`\nabla y` 。

.. math::

    \nabla y 
    &= \dfrac{\partial y}{\partial \mathbf{x}} = \begin{bmatrix} \dfrac{\partial y}{\partial x_1} \quad \dfrac{\partial y}{\partial x_2} \quad \dots \quad \dfrac{\partial y}{\partial x_n} \end{bmatrix} \\\\
    &= \begin{bmatrix} \dfrac{\partial}{\partial x_1}\displaystyle\sum_i f_i(\mathbf{x}) \quad \dfrac{\partial}{\partial x_2}\displaystyle\sum_i f_i(\mathbf{x}) \quad \dots \quad \dfrac{\partial}{\partial x_n}\displaystyle\sum_i f_i(\mathbf{x}) \end{bmatrix} \\\\
    &= \begin{bmatrix} \displaystyle\sum_i \dfrac{\partial f_i(\mathbf{x})}{\partial x_1} \quad \displaystyle\sum_i \dfrac{\partial f_i(\mathbf{x})}{\partial x_2} \quad \dots \quad \displaystyle\sum_i \dfrac{\partial f_i(\mathbf{x})}{\partial x_n} \end{bmatrix} \\\\
    &= \text{(and assume } \mathbf{f}(\mathbf{x})=\mathbf{x} \text{, so, }f_i(\mathbf{x})=x_i \text{)} \\\\
    &= \begin{bmatrix} \displaystyle\sum_i \dfrac{\partial x_i}{\partial x_1} \quad \displaystyle\sum_i \dfrac{\partial x_i}{\partial x_2} \quad \dots \quad \displaystyle\sum_i \dfrac{\partial x_i}{\partial x_n} \end{bmatrix} \\\\
    &= \text{and since } \dfrac{\partial}{\partial x_j}x_i=0 \text{, for} j \neq i \text{)} \\\\
    &= \begin{bmatrix} \dfrac{\partial x_1}{\partial x_1} \quad \dfrac{\partial x_2}{\partial x_2} \quad \dots \quad \dfrac{\partial x_n}{\partial x_n} \end{bmatrix} \\\\
    &= \begin{bmatrix} 1 \quad 1 \quad \dots \quad 1 \end{bmatrix}
    
Example 3
~~~~~~~~~~

已知 :math:`y=sum\big(\mathbf{f}(\mathbf{x}z)\big)` 求 :math:`\nabla y` 。

.. math::

    \dfrac{\partial y}{\partial \mathbf{x}}
    &= \begin{bmatrix} \dfrac{\partial}{\partial x_1}\displaystyle\sum_i x_iz) \quad \dfrac{\partial}{\partial x_2}\displaystyle\sum_i x_iz) \quad \dots \quad \dfrac{\partial}{\partial x_n}\displaystyle\sum_i x_iz) \end{bmatrix} \\\\
    \ &= \begin{bmatrix} z \quad z \quad \dots \quad z \end{bmatrix} \\\\
    \dfrac{\partial y}{\partial z} 
    &= \dfrac{\partial}{\partial z}\displaystyle\sum_i x_iz \quad \text{(and the shape is 1} \times \text{1)}\\\\
    \ &= \displaystyle\sum_i x_i \\\\
    \ &= sum(\mathbf{x}) \\\\
    \nabla y &= \begin{bmatrix} \dfrac{\partial y}{\partial \mathbf{x}} \quad \dfrac{\partial y}{\partial z} \end{bmatrix}

链式法则
--------

到目前为止，我们无法对嵌套表达式直接进行求导，比如 :math:`sum(\mathbf{w}+\mathbf{x})` ，必须先将其转换到标量形式才能继续进行。链式法则的目标在于解决这个问题。

在求导法则中，有很多所谓的“链式法则”，我们必须仔细地区分。作者将其归纳为三种：

- single-variable chain rule 标量函数对标量变量求导
- single-variable total-derivative chain rule
- vector chain rule

Single-variable chain rule
~~~~~~~~~~~~~~~~~~~~~~~~~~~

外层函数的导数与内层函数的导数相乘即可得到结果。

函数表达式为 :math:`y = f(g(x))` 或者 :math:`(f \circ g)(x)`

其导数为 :math:`y'=f'(g(x))g'(x)` 或者更推荐记作 :math:`\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}y}{\mathrm{d}u}\dfrac{\mathrm{d}u}{\mathrm{d}x}` 。

使用 single-variable chain rule 时，可以遵循下述步骤：

1. 为嵌套表达式引入中间变量
2. 对中间变量进行求导
3. 将中间变量求导后的结果相乘
4. 将中间变量替换为原表达式

Example: :math:`y=f(g(x))=sin(x^2)`

- step 1: :math:`u = x^2, \quad y = sin(u)`
- step 2: :math:`\dfrac{\mathrm{d}u}{\mathrm{d}x}=2x, \quad \dfrac{\mathrm{d}y}{\mathrm{d}u}=cos(u)`
- step 3: :math:`\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}y}{\mathrm{d}u}\dfrac{\mathrm{d}u}{\mathrm{d}x}=cos(u)2x`
- step 3: :math:`\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}y}{\mathrm{d}u}\dfrac{\mathrm{d}u}{\mathrm{d}x}=cos(x^2)2x=2xcos(x^2)`

你可以将 :math:`\dfrac{\mathrm{d}u}{\mathrm{d}x}` 认为是当 x 发生变化时，会影响 u 。 :math:`\dfrac{\mathrm{d}y}{\mathrm{d}u}` 认为是当 u 变化时，会影响 y 。

链式法则通常情况下的书写顺序时从输出变量到输入变量 :math:`\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}y}{\mathrm{d}u}\dfrac{\mathrm{d}u}{\mathrm{d}x}` 。

如果从输入到输出到视角考虑，上面的式子就要颠倒一下顺序 :math:`\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}u}{\mathrm{d}u}\dfrac{\mathrm{d}y}{\mathrm{d}u}` 。

当从自变量到因变量只有一条数据通路时，使用 single-variable chain rule 。利用上面的表达式可以理解为只有 x 能够影响 y 的取值（虽然引入了中间变量）。

但是当从自变量到因变量不是只有一条数据通路时，情况就不一样了。考虑 :math:`y(x)=x+x^2` 可以看作 :math:`y(x, u)=x+u, for u=x^2` 。这是就需要使用 single-variable total-derivative chain rule 。

.. note:: 

    Automatic differentiation（自动求导，这是 PyTorch 中内置的求导规则）
    
    - forward differentiation（前向求导）
    - backward differentiation (back-propagation)（反向求导）

    从数据流的角度，前向求导就是从自变量影响到因变量取值的求导方向 :math:`\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}u}{\mathrm{d}x}\dfrac{\mathrm{d}y}{\mathrm{d}u}`
    ，后向求导就是考虑输出改变时，将会如何影响到输入 :math:`\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{\mathrm{d}y}{\mathrm{d}u}\dfrac{\mathrm{d}u}{\mathrm{d}x}` 。
    因为反向求导可以一次性确定所有函数变量的变化量，所以它对于计算含有大量参数的函数来讲效率更高。

single-variable total-derivative chain rule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. footbibliography::
