======
词汇表
======

有两个网站总结的很好，一个是 `Google Developers <https://developers.google.com/machine-learning/glossary>`_
另一个是 `ML-Glossary <https://ml-cheatsheet.readthedocs.io/en/latest/index.html>`_ 。

张量
    0 维叫标量，1 维叫向量或 1 维数组，2 维叫矩阵或 2 维数组，3 维及以上叫张量或多维数组。
    numpy 最基本的数据类型是 ndarray，它是多为数组的一种表示方式，为了提升 B 格，也可以用张量称呼它。
    张量是数学理论中比向量、矩阵更为抽象、更为一般的概念。是为了方便在数学上对多维数据进行描述而提出的。
    张量中的元素不只局限于整数和浮点数，也可以是字符串。

binary
    二元的
unary
    一元的
derivatives
    导数，或称微分
total derivative
    全微分（假设变量间互相依赖）
partical derivative
    偏微分（假设除 x 外都是常量）
with respect to
    作用于
nested
    嵌套的
whereas
    但是
commute
    交换(律)

Embedding
    A categorical feature represented as a continuous-valued feature. Typically, an embedding is a translation of a high-dimensional vector into a low-dimensional space. For example, you can represent the words in an English sentence in either of the following two ways:
    
    - As a million-element (high-dimensional) sparse vector in which all elements are integers. Each cell in the vector represents a separate English word; the value in a cell represents the number of times that word appears in a sentence. Since a single English sentence is unlikely to contain more than 50 words, nearly every cell in the vector will contain a 0. The few cells that aren't 0 will contain a low integer (usually 1) representing the number of times that word appeared in the sentence.
    - As a several-hundred-element (low-dimensional) dense vector in which each element holds a floating-point value between 0 and 1. This is an embedding.
    
    In TensorFlow, embeddings are trained by backpropagating loss just like any other parameter in a neural network.



