# PyTorch 入门

这是一段关于使用 PyTorch 编写神经网络代码的**完整片段**，或者可以称它为**标准训练流程**。
里面有一些细节需要注意，建议阅读我于 2021 年 12 月 9 日写的 [PPT](https://kdocs.cn/l/cmkgvoHbj92N)。

- 使用 PaddlePaddle 训练网络
- 钢铁缺陷检测实例
- Pandas 和 NumPy（更多工具的使用参考[Python 知识手册 v2018](https://kdocs.cn/l/ccs5HiBn4nq8)）
- 自动求导的使用方法

```Python
import torch
import random

# 生成一些假数据
def synthetic_data(w, b, num_examples):
    X = torch.normal(0, 1, (num_examples, len(w)))
    y = torch.matmul(X, w) + b
    y += torch.normal(0, 0.01, y.shape)
    return X, y.reshape((-1, 1))

# 提取小批量数据
def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
    random.shuffle(indices)
    for i in range(0, num_examples, batch_size):
        batch_indices = torch.tensor(
            indices[i: min(i + batch_size, num_examples)])
        yield features[batch_indices], labels[batch_indices]

# 定义模型
def linreg(X, w, b):
    return torch.matmul(X, w) + b

# 定义损失函数
def squared_loss(y_hat, y):
    return (y_hat - y.reshape(y_hat.shape)) ** 2 / 2

# 定义优化方法
def sgd(params, lr, batch_size):
    with torch.no_grad(): # 什么叫停止自动求导？
        for param in params:
            param -= lr * param.grad / batch_size
            param.grad.zero_() # 清除缓存

# 主函数
if __name__== "__main__":
    true_w = torch.tensor([2, -3.4])
    true_b = 4.2
    features, labels = synthetic_data(true_w, true_b, 1000)
    w = torch.normal(0, 0.01, size=(2, 1), requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    lr = 0.03
    num_epochs = 3
    batch_size = 10
    net = linreg
    loss = squared_loss
    # 开始训练
    for epoch in range(num_epochs):
        for X, y in data_iter(batch_size, features, labels):
            l = loss(net(X, w, b), y)
            l.sum().backward()          # 反向传播
            sgd([w, b], lr, batch_size) # 梯度下降
        with torch.no_grad():
            train_l = loss(net(features, w, b), labels)
            print(f'epoch {epoch + 1}, loss {float(train_l.mean()):f}')
```
