# Tensorflow

```{code-block} python
import tensorflow as tf
```

## 数据表示

### 标量

```{code-block} python
a = tf.constant(3.0)
b = tf.constant(2.0)
a, b
```

### 向量

```{code-block} python
x = tf.range(4, dtype=tf.float32)
y = tf.ones(4)
x, y
```

### 矩阵

```{code-block} python
A = tf.reshape(tf.range(12, dtype=tf.float32), (3, 4))
B = tf.constant([[2.0, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
A, B
```

### 张量

```{code-block} python
X = tf.reshape(tf.range(36), (3, 4, -1))
X
```

## 属性和方法

### shape 和 size()

```{code-block} python
x.shape, tf.size(x), X.shape, tf.size(X)
```

### reshape()

```{code-block} python
tf.reshape(A, (2, -1))
```

### zeros()

```{code-block} python
tf.zeros((2, 3, 4))
```

### random

```{code-block} python
tf.random.normal(shape=[3, 4])  # 符合正态分布的随机数
```

### concat()

```{code-block} python
tf.concat([A, B], axis=0), tf.concat([A, B], axis=1)
```

### 求和

```{code-block} python
# 对所有元素求和（这是一种降维方法）
sum_total = tf.reduce_sum(X)
sum_total
# 指定 axis 求行和或列和，keepdims=True 保持轴数不变，可以方便后期利用广播机制
sum_X = tf.reduce_sum(X, axis=[0,1], keepdims=True)
sum_X
```

### 获取切片

值得注意的是，图像一般默认为`(H, W, C)`即 (高度, 宽度, 通道数) 但获取切片时的参数一般为`(C, H, W)`。

```{code-block} python
X, X[-1], X[1:3] # 把 X 想成是图片的三个通道，X[-1] 获取最后一个通道，X[1:3] 获取第 2 和第 3 通道。
```

## 代数运算

### 向量 $\times$ 向量

```{code-block} python
x, y, tf.tensordot(x, y, axes=1) # 点积后是一个标量，且 x 和 y 的数据类型保持一致
```

### 矩阵 $\times$ 向量

```{code-block} python
A, x, tf.linalg.matvec(A, x)
```

### 矩阵 $\times$ 矩阵

```{code-block} python
A, B, tf.matmul(tf.transpose(A), B)
```

### 范数

```{code-block} python
# 1 范数 和 2 范数
tf.reduce_sum(tf.abs(x)), tf.norm(x)
```

## 运算符

### 加减乘除

```{code-block} python
x + y, x - y, x * y, x / y, x ** y  # ** 运算符是求幂运算
```

### 广播机制

广播机制让形状不同的张量也能计算。它先将两个向量扩张成一致的形状（两个向量先变成矩阵），然后再相加（矩阵加法）。

```{code-block} python
yt = tf.reshape(y, (4, -1))
x, yt, x + yt
```

### 逻辑运算

```{code-block} python
A == B # 逻辑运算符 "按元素"
```

## 声明变量

TensorFlow 中的 `Tensors` 是不可变的，也不能被赋值。 TensorFlow 中的 `Variables` 是支持赋值的可变容器。 请记住，TensorFlow 中的梯度不会通过 `Variable` 反向传播，**这句话没说错**，记住。

```{code-block} python
X_var = tf.Variable(X) # 声明变量，预分配存储空间
X_var[0:2, 0:2, :].assign(tf.ones(X_var[0:2, 0:2, :].shape, dtype = tf.int32) * 12) # 把前两个通道的前两行都变成 12
X, X_var
```

## 节省内存

节省内存的意思就是不要重复地开辟内存，尽量原地操作。

```{code-block} python
# 默认行为
before = id(y)
y = y + x
id(y) == before

# 节省内存的做法是使用切片
z = tf.Variable(tf.zeros_like(y))
print('id(z):', id(z))
z.assign(x + y)
print('id(z):', id(z))
```

由于 TensorFlow 的 `Tensors` 是不可变的，而且梯度不会通过 `Variable` 流动， 因此 TensorFlow 没有提供一种明确的方式来原地运行单个操作。

但是，TensorFlow 提供了 `tf.function` 修饰符， 将计算封装在 TensorFlow 图中，该图在运行前经过编译和优化。 这允许 TensorFlow 删除未使用的值，并复用先前分配的且不再需要的值。 这样可以最大限度地减少 TensorFlow 计算的内存开销。

```{code-block} python
@tf.function
def computation(X, Y):
    Z = tf.zeros_like(Y)  # 这个未使用的值将被删除
    A = X + Y  # 当不再需要时，分配将被复用
    B = A + Y
    C = B + Y
    return C + Y

computation(x, y)
```

## 类型转换

Tensorflow 转换后的结果不共享内存。这个小的 **不便** 实际上是非常重要的：当你在 CPU 或 GPU 上执行操作的时候，如果 Python 的 NumPy 包也 **希望使用相同的内存块** 执行其他操作，你不希望停下计算来等它。这个不便之处，MXNet 和 Tensorflow 都没有解决，**只有** PyTorch 是解决了的。

### tensor 转 ndarray

```{code-block} python
X.numpy()
```

### ndarray 转 tensor

```{code-block} python
tf.constant(A)
```

### tensor 转 scalar

```{code-block} python
tf.constant([3.5]).numpy().item() # 仅限只含一个元素
```

## 自动求导

这可能是最重要的部分了，有了上面的基础，相信这部分很容易看懂的。

需要求导的函数：

$$
y = x^2 \\
u = y\\
z = u * x
$$

其中，变量 $x$ 的取值点为 $(0, 1, 2, 3)$

```{code-block} python
x = tf.range(4, dtype=tf.float32) # 初始化数据
x = tf.Variable(x) # 声明变量

# 把所有计算记录在磁带（GradientTape()）上，可以把磁带想象成一种资源，可能是计算图吧
with tf.GradientTape(persistent=True) as t: # 设置 persistent=True 来运行 t.gradient 多次
    y = x * x
    u = tf.stop_gradient(y) # 分离计算
    z = u * x

x_grad = t.gradient(z, x) # 求梯度

z, x_grad, x_grad == u
x = tf.range(4, dtype=tf.float32) # 初始化数据
x = tf.Variable(x) # 声明变量

# 把所有计算记录在磁带（GradientTape()）上，可以把磁带想象成一种资源，可能是计算图吧
with tf.GradientTape(persistent=True) as t: # 设置 persistent=True 来运行 t.gradient 多次
    y = x * x
    u = y # 没有分离计算
    z = u * x

x_grad = t.gradient(z, x) # 求梯度

z, x_grad, x_grad == u
```
