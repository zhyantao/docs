# Pandas

Pandas 是 Python 的一个第三方库，主要用于数据预处理，比如数据集中的 **缺失项** 和 **异常项**。

```{code-block} bash
pip install pandas
```

## 读取数据集

```{code-block} python
import os
import pandas as pd

# 写文件
with open('house_tiny.csv', 'w') as f:
    f.write('NumRooms,Alley,Price\n')  # 列名
    f.write('NA,Pave,127500\n')  # 每行表示一个数据样本
    f.write('2,NA,106000\n')
    f.write('4,NA,178100\n')
    f.write('NA,NA,140000\n')

data = pd.read_csv('house_tiny.csv')
print(data)
```

## 处理缺失值

Pandas 中“NaN”表示缺失项，一般用插值法或删除法处理。

```{code-block} python
inputs, outputs = data.iloc[:, 0:2], data.iloc[:, 2] # iloc 切片将数据分成两部分
inputs = inputs.fillna(inputs.mean())
print(inputs)
```

以下代码应用了插值法，对于连续值中的“NaN”项可用均值替换，对于离散值中的“NaN”项，Pandas 将自动创建一个 NaN 列，并将其值置为 1。

```{code-block} python
inputs = pd.get_dummies(inputs, dummy_na=True)
print(inputs)
type(inputs.values) # 后面可以通过类型转换，将其转换为张量，供神经网络框架使用了。
```
