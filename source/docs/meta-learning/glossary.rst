======
词汇表
======

.. hint:: 

    - `Google Developers <https://developers.google.com/machine-learning/glossary>`_
    - `ML-Glossary <https://ml-cheatsheet.readthedocs.io/en/latest/index.html>`_
    - `Glossary of artificial intelligence <https://en.wikipedia.org/wiki/Glossary_of_artificial_intelligence>`_

点乘（Dot product / Scalar product）
    也叫数量积或向量内积，结果是一个向量在另一个向量上的投影长度，是一个标量。点乘的记号就是一个中心圆点 :math:`\cdot` 。代数定义为
    :math:`\mathbf{a}\cdot\mathbf{b}=\displaystyle\sum_{i=1}^n a_i b_i` 。几何定义为
    :math:`\mathbf{a}\cdot\mathbf{b}=|\mathbf{a}||\mathbf{b}|cos\theta` （该定义只对二维和三维有效）。
    点乘反映了两个向量的相似度，两个向量的相似度越高，它们的点乘越大。

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

嵌入（Embeddings）
    通常，嵌入是指将一个高维（稀疏或稠密）向量映射到低维空间。比如，把英语句子按照单词出现的频率映射为一个特征向量。
    在 Tensorflow 中，对输入为高维向量，输出为低维向量的神经网络应用反向传播更新网络参数。
