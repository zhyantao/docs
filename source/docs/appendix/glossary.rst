======
词汇表
======

.. hint:: 

    - `Google Developers <https://developers.google.com/machine-learning/glossary>`_
    - `ML-Glossary <https://ml-cheatsheet.readthedocs.io/en/latest/index.html>`_
    - `Glossary of artificial intelligence <https://en.wikipedia.org/wiki/Glossary_of_artificial_intelligence>`_

.. _math-glossary:

基础数学
--------

点乘（Dot product / Scalar product）
    也叫数量积或向量内积，结果是一个向量在另一个向量上的投影长度，是一个标量。点乘的记号就是一个中心圆点 :math:`\cdot` 。代数定义为
    :math:`\mathbf{a}\cdot\mathbf{b}=\displaystyle\sum_{i=1}^n a_i b_i` 。几何定义为
    :math:`\mathbf{a}\cdot\mathbf{b}=|\mathbf{a}||\mathbf{b}|cos\theta` （该定义只对二维和三维有效）。
    点乘反映了两个向量的相似度，两个向量的相似度越高，它们的点乘越大。
    当权重为非负数且和为 1 时，点乘表示加权平均。将两个向量规范化得到单位长度后，点乘表示它们的夹角余弦。

叉乘（Cross product）
    也叫向量积或向量外积，结果是一个和已有两个向量都垂直的向量。集合定义为
    :math:`\mathbf{a}\times\mathbf{b}=|\mathbf{a}||\mathbf{b}|sin\theta` 。
    :math:`\mathbf{a}\times\mathbf{b}` 有时也写作 :math:`\mathbf{a}\land\mathbf{b}` 。
    外积的方向由右手定则决定，外积的模长等于两个向量为边的平行四边形的面积。

一般矩阵乘积（Matrix multiplication）
    记作 :math:`\mathbf{A}\mathbf{B}` 有时也记作 :math:`\mathbf{A}\cdot\mathbf{B}` 。
    需要注意的是，向量之间的运算中间必须有运算符号，缺省运算符号时默认是矩阵乘法或标量乘法。
    代数定义为 :math:`(\mathbf{A}\mathbf{B})_{ij}=\displaystyle\sum_{r=1}^n a_{ir} b_{rj}` 。
    一般的矩阵乘积可以认为是行向量和列向量的内积，这是工科线性代数教材中使用的运算规则。

哈达玛乘积（Hadamard product）
    又叫分素乘积（element-wise，entrywise product）。其输入为两个相同形状的矩阵，
    输出是具有同样形状的、各个位置的元素等于两个输入矩阵相同位置元素的乘积的矩阵。
    数学定义为 :math:`(\mathbf{A}\circ\mathbf{B})_{ij}=a_{ij} b_{ij}` 。

张成
    由几个线性不相关的向量作为基，所有能够由这几个基向量表示的空间向量是总和。

张量（Tensor）
    0 维叫标量，1 维叫向量或 1 维数组，2 维叫矩阵或 2 维数组，3 维及以上叫张量或多维数组。
    numpy 最基本的数据类型是 ndarray，它是多为数组的一种表示方式，为了提升 B 格，也可以用张量称呼它。
    张量是数学理论中比向量、矩阵更为抽象、更为一般的概念。是为了方便在数学上对多维数据进行描述而提出的。
    张量中的元素不只局限于整数和浮点数，也可以是字符串。

解析解
    像线性回归这样的简单问题，可以用一个公式简单地表达出来，这类解叫做解析解。但并不是所有问题都存在解析解。
    在我们无法得到解析解的情况下，我们仍然可以有效地训练模型。

.. _machine-learning-glossary:

机器学习
--------

样本/特征向量/示例
    一行由属性值构成的组合，通常用 :math:`\mathbf{x}` 表示。

标签（Labels）
    对一个样本所作的标记，通常用 :math:`y` 表示。

样例（Samples）
    由 :math:`\mathbf{x}` 和 :math:`y` 共同组成。

属性空间/样本空间/输入空间
    由属性张成的空间，通常用 :math:`\mathbf{X}` 表示。

标记空间/输出空间
    由标签张成的空间，通常用 :math:`\mathbf{Y}` 表示。

数据集（Data Set）
    所有样例的集合。

Batch
    多个样例组成的小的数据集，通常在使用随机梯度下降方法训练神经网络时用于更新网络参数。 

归一化
    解决不同单位和比例的数据间的差异，消除量纲的影响，将数据范围缩放到 0 和 1 之间，受异常值影响比较严重。

标准化
    解决不同单位和比例的数据间的差异，消除量纲的影响，使处理后的数据符合高斯(正态)分布。常用 BN 加快收敛。

规范化
    是归一化和标准化的统称。

正则化
    解决模型的过拟合问题，常用 L1 正则和 L2 正则。 [1]_ [2]_

嵌入（Embeddings）
    通常，嵌入是指将一个高维（稀疏或稠密）向量映射到低维空间。比如，把英语句子按照单词出现的频率映射为一个特征向量。
    在 Tensorflow 中，对输入为高维向量，输出为低维向量的神经网络应用反向传播更新网络参数。

全连接层
    全连接层（Fully connected layer）也叫稠密层（Dense layer）。

迁移学习
    迁移学习强调我们有一个已学习好的源任务，然后将其直接应用于目标任务上，再通过在目标任务上的微调，达到学习目标。
    这已经被证明是一种有效的学习方式。迁移学习的过程可以表示为
    :math:`\theta^*=\arg \min\limits_{\theta} \mathcal{L}(\theta|\theta_0, \mathcal{D})`
    其中 :math:`\theta^*` 是最优参数， :math:`\theta_0` 是之前任务的超参数。这个过程也就是常用的微调（fine-tune）过程。  

基于度量学习的方法
    其目标是学习一个从图像到嵌入空间的映射，在该空间中，同一类图像彼此间的距离较近，而不同类的图像距离则较远。
    我们希望这种性质适用于那些没有见过的类。

优化器
    指的是寻找最优参数的方法，最著名的就是梯度下降法。

深度学习
    针对某一个特定的 task，从 0 开始学习，然后应用到该 task。

元学习
    目标是学会一种先验知识，学会自主学习。元学习是一种方法或过程，而小样本学习是一种场景。
    它用 task 做训练，然后应用到新 task。如何学会自主学习？用 Train Set 做训练的过程就是学习先验知识的过程。

小样本学习
    小样本学习是在有先验知识的基础上再进行学习的。
    对于小样本学习，你可以问机器这两张图片是不是同一种东西。
    比如，如果我们给神经网络一张图片（Query），问它这是什么东西时，它可能没见过，不知道如何这个照片属于哪一类。
    但是如果我们能再多提供一点信息（Support Set），它就能从 Support Set 找出 Query 属于哪个类别。
    小样本学习的模型输入是两张图片，或三张图片。输出是相似度函数。

Support Set
    很小的一个数据集，只能在预测时提供一些额外的信息。
    比如我们想要判断一个未知事物是什么东西的时候，需要与已知事物建立一种联系，这种联系很像查手册。

Train Set
    很大的一个数据集，可以用于训练一个神经网络。让神经网络学会比较异同（具备自主学习的能力，这是我们能够提供的先验），做预测时，给出 Support Set，让它分类。

One Shot Learning
    用一张卡片识别出一种动物叫 One Shot Learning。

K-way，N-shot
    The support set has k classes, every class has n samples.

相似度函数
    :math:`sim(x, x')` 理想情况下，如果 :math:`x` 和 :math:`x'` 是同一种东西，:math:`sim(x, x')=1` ，否则等于 :math:`0` 。
    通常作为标签。


参考文献
--------

.. [1] https://zhuanlan.zhihu.com/p/29957294
.. [2] https://www.zhihu.com/question/38102762
