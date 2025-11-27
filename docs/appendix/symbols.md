# 数学符号表

数学是符号的艺术，理解符号背后的含义是掌握数学的关键。更多 LaTeX 符号参考：

- [LaTeX 入门](#latex-basic)
- [一份不太简短的 LaTeX 2ε 介绍](https://www.kdocs.cn/p/136412211457) 4.9 小节
- [常用数学符号和公式排版](https://www.latexlive.com/help#d11)
- [在线 LaTeX 公式编辑器](https://www.latexlive.com)（支持导出为图片）

> **符号使用说明**
>
> - 函数 $f(x;\theta)$ 中的分号用于分隔自变量和参数
> - 概率 $p(\theta \mid \phi^*)$ 中的竖线用于分隔自变量和参数
> - 表达式 $\alpha = \arg \min_{\omega \in W} d(\beta, \omega), \ \forall \omega \in W$ 表示：函数取最小值时，将 $\omega$ 的值赋给 $\alpha$
> - 表达式 $\alpha = \min_{\omega \in W} d(\beta, \omega), \ \forall \omega \in W$ 表示：函数取最小值时，将该最小值赋给 $\alpha$

(symbol-definition)=

## 通用符号

| 符号            | 含义               | LaTeX 语法      | 备注                                  |
| --------------- | ------------------ | --------------- | ------------------------------------- |
| $x$             | 标量               | `x`             | 小写意大利体，LaTeX 默认字体          |
| $\tilde{x}$     | 变量的取值         | `\tilde{x}`     | 字母上方加波浪号，表示 $x$ 的特定取值 |
| $\mathbf{x}$    | 向量               | `\mathbf{x}`    | 小写粗体，高中阶段常记为 $\vec{x}$    |
| $\mathbf{X}$    | 矩阵（或多维数组） | `\mathbf{X}`    | 大写粗体                              |
| $\mathrm{d}$    | 求导数             | `\mathrm{d}`    | 直立的 $\mathrm{d}$                   |
| $\partial$      | 求偏导             | `\partial`      | 求导符号 $\mathrm{d}$ 的变体          |
| $\nabla_\theta$ | 对 $\theta$ 求梯度 | `\nabla_\theta` | 向量微分算子                          |

(probability-statistics-symbols)=

## 概率和统计

| 符号                 | 含义                     | LaTeX 语法           | 备注         |
| -------------------- | ------------------------ | -------------------- | ------------ |
| $X$                  | 观测变量（随机变量）     | `X`                  | 大写意大利体 |
| $x$                  | 观测值                   | `x`                  | 小写意大利体 |
| $p(x)$               | 观测变量取观测值时的概率 | `p(x)`               | 小写意大利体 |
| $\mathcal{X}$        | 观测变量的取值空间       | `\mathcal{X}`        | 大写花体     |
| $\mathcal{N}(\cdot)$ | 正态分布                 | `\mathcal{N}(\cdot)` | 大写花体     |
| $\mathbb{E}$         | 数学期望                 | `\mathbb{E}`         | 黑板体       |

## 矩阵分析

| 符号          | 含义     | LaTeX 语法    | 备注     |
| ------------- | -------- | ------------- | -------- |
| $\mathscr{F}$ | 函数空间 | `\mathscr{F}` | 大写花体 |
| $\mathbb{R}$  | 实数域   | `\mathbb{R}`  | 黑板体   |
| $\mathbb{C}$  | 复数域   | `\mathbb{C}`  | 黑板体   |
| $\mathbb{Q}$  | 有理数域 | `\mathbb{Q}`  | 黑板体   |

## 集合论

| 符号        | 含义             | LaTeX 语法  | 备注                                                                                             |
| ----------- | ---------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| $\subset$   | 真包含（真子集） | `\subset`   | 高中课本记作 $\subsetneqq$，也有书记作 $\subsetneq$                                              |
| $\subseteq$ | 包含（子集）     | `\subseteq` | 高中课本记作 $\subset$，存在歧义，[需注意约定](https://zh.wikipedia.org/wiki/%E5%AD%90%E9%9B%86) |
| $\in$       | 属于             | `\in`       | $a \in A$                                                                                        |
| $\notin$    | 不属于           | `\notin`    | $a \notin A$                                                                                     |

(Meta-FSL-symbols)=

## 机器学习

| 符号                       | 含义                                      | LaTeX 语法                 | 备注     |
| -------------------------- | ----------------------------------------- | -------------------------- | -------- |
| $M_{meta}$                 | 元学习模型                                | `M_{meta}`                 | 大写     |
| $M_{fine-tune}$            | 数学模型（小样本模型）                    | `M_{fine-tune}`            | 大写     |
| $\mathscr{D}_{meta-train}$ | 用于训练 $M_{meta}$ 的数据集              | `\mathscr{D}_{meta-train}` | 大写花体 |
| $\mathscr{D}_{meta-test}$  | 用于训练和测试 $M_{fine-tune}$ 的数据集   | `\mathscr{D}_{meta-test}`  | 大写花体 |
| $\mathcal{D}_{train}$      | 支持集（Support Set）                     | `\mathcal{D}_{train}`      | 大写花体 |
| $\mathcal{D}_{test}$       | 查询集（Query Set）                       | `\mathcal{D}_{test}`       | 大写花体 |
| $\mathcal{T}$（即 task）   | $\mathcal{D}$ 的一行，神经网络输入        | `\mathcal{T}`              | 大写花体 |
| $C_1 \sim C_{10}$          | $\mathcal{D}_{meta-train}$ 中的 10 个类别 | `C_1 \sim C_{10}`          | 大写     |
| $P_1 \sim P_{5}$           | $\mathcal{D}_{meta-test}$ 中的 5 个类别   | `P_1 \sim P_{5}`           | 大写     |
| $\mathcal{L}$              | 损失函数                                  | `\mathcal{L}`              | 大写花体 |

## 数据库

| 符号                                      | 含义       | LaTeX 语法                                | 备注 |
| ----------------------------------------- | ---------- | ----------------------------------------- | ---- |
| $\Pi$                                     | 投影       | `\Pi`                                     |      |
| $\sigma$                                  | 选择       | `\sigma`                                  |      |
| $\rho$                                    | 重命名     | `\rho`                                    |      |
| $\mathcal{G}$                             | 聚合函数   | `\mathcal{G}`                             |      |
| $\cap$                                    | 交         | `\cap`                                    |      |
| $\cup$                                    | 并         | `\cup`                                    |      |
| $\bowtie$                                 | 自然连接   | `\bowtie`                                 |      |
| $\mathop{\bowtie}\limits_{A \theta B}^{}$ | 内连接     | `\mathop{\bowtie}\limits_{A \theta B}^{}` |      |
| ⟕                                         | 左外连接   | --                                        |      |
| ⟖                                         | 右外连接   | --                                        |      |
| ⟗                                         | 全外连接   | --                                        |      |
| $\times$                                  | 笛卡尔积   | `\times`                                  |      |
| $\div$                                    | 除         | `\div`                                    |      |
| $\leftarrow$                              | 赋值       | `\leftarrow`                              |      |
| $\land$ 或 $\vee$                         | 条件并列   | `\land` 或 `\vee`                         |      |
| $\neg$                                    | 非         | `\neg`                                    |      |
| $\exists$                                 | 存在       | `\exists`                                 |      |
| $\forall$                                 | 对所有     | `\forall`                                 |      |
| $\gt\ \ge\ \lt\ \le\ \ne$                 | 比较运算符 | `\gt\ge\lt\le\ne`                         |      |
| $\overset{F}{\rightarrow}$                | 函数依赖   | `\overset{F}{\rightarrow}`                |      |
