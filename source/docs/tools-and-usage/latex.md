(latex-basic)=
# $\LaTeX$ 入门

学习使用 $\LaTeX$ 书写文档，应该做到如下两点：

- 本文将对常用的 $\LaTeX$ 语法做简单介绍，之后就可以学习[别人精心制作的模板](https://cn.overleaf.com/latex/templates)了；
- 本文不会记录常用的符号，反复多用几次就记住了，不常用的符号记不住[上网查一下](https://www.latexlive.com/help#d11)就行了。

如果已经熟练掌握基本语法，但是有些细节记不住，[查看小抄表](https://kdocs.cn/l/ceOwwHjUhGVQ)也许会有帮助。

## 环境配置

1. 下载并安装宏包：CTeX 由于长期不更新，推荐使用 [TeXLive](https://www.tug.org/texlive/)；
2. 下载并安装编辑器：[TeXstudio](https://www.texstudio.org/)；
3. 配置编辑器：（适配中文支持）
   - `Options` > `Configure TeXstudio` > `Build` > `Default Editor` > `XeLaTeX`
   - `Options` > `Configure TeXstudio` > `Editor` > `Derault Font Encoding` > `UTF-8`

## Hello World

### 英文

```{code-block} tex
\documentclass{article}

\begin{document}
    ``Hello world!'' from \LaTeX
\end{document}
```

$\LaTeX$ 中没有双引号，因此用两个反引号和单引号输出了双引号 [^latex-syntax]。

[^latex-syntax]: [【金山文档】 一份（不太）简短的 LATEX 2ε 介绍](https://kdocs.cn/l/cvhLkILXI6Ti)

### 中文

```{code-block} tex
\documentclass{ctexart}

\begin{document}
    “你好，世界！” 来自 \LaTeX{} 的问候。
\end{document}
```

命令后面的空格默认会被忽略，因此用 `{}` 插入了一个空格，也可以用**反斜杠加空格字符**来表明有空格存在。

## 文档结构

### article 文档

```{code-block} tex
% \documentclass[<opt1, opt2, ...>]{article | book}
\documentclass[11pt, landscape]{article}

% 导言区
% \usepackage[<opt1, opt2, ...>]{<pkg1, pkg2, ...>}

\begin{document}
    
    % 正文内容
    % \chapter{Chapter title}           % 章（只有 book 才有 chapter）
    \section{Section title}             % 节
    \subsection{Subsection title} 
    \subsubsection{Subsubsection title}
    \paragraph{Paragraph title}         % 段落
    \subparagraph{Subparagraph title}
    
\end{document}

% 此后内容会被忽略
```

使用宏包和文档类前，需要事先安装到你的计算机上，否则会报错。

### book 文档

```{code-block} tex
\documentclass{book}

% 导言区，加载宏包和各项设置，包括参考文献、索引等
\usepackage{makeidx}        % 调用 makeidx 宏包，用来处理索引
\makeindex                  % 开启索引的收集
\bibliographystyle{plain}   % 指定参考文献样式为 plain

\author{name}               % 声明书籍信息
\title{title}
\date{date}

\begin{document}

    \frontmatter            % 前言部分
    \maketitle              % 生成标题页
    \include{preface}       % 前言章节 preface.tex

    \tableofcontents        % 生成目录

    \mainmatter             % 正文部分
    \include{chapter1}      % 第一章 chapter1.tex
    \include{chapter2}      % 第二章 chapter2.tex
    ...
    \appendix               % 附录
    \include{appendixA}     % 附录 A appendixA.tex
    ...

    \backmatter             % 后记部分
    \include{prologue}      % 后记 prologue.tex
    \bibliography{books}    % 利用 BibTeX 工具从数据库文件 books.bib 生成参考文献
    \printindex             % 利用 makeindex 工具生成索引

\end{document}
```

**一些重要的文件和它们的作用：**

- `.sty` 宏包文件。宏包的名称与文件名一致。
- `.cls` 文档类文件。文档类名称与文件名一致。
- `.bib` BibTeX 参考文献数据库文件。
- `.bst` BibTeX 用到的参考文献格式模板。

**导入外部文件**使用 `\include{<path/to/file>}` 或 `\input{<path/to/file>}`。

- `\include` 会另起一页
- `\input` 在当前位置插入

## 字号

```{code-block} tex
\tiny 
\scriptsize 
\footnotesize 
\small 
\normalsize
\large 
\Large 
\LARGE 
\huge 
\Huge
```

## 字体

```{code-block} tex
\textit{text}
\textbf{text}
\textsc{text}
\textnormal{text}
```

## 对齐方式

```{code-block} tex
\begin{center} 
\begin{flushleft} 
\begin{flushright}
```

## 列表

### 无序列表

```{code-block} tex
\begin{itemize} 
    \item First item 
    \item[-] Item with dash 
\end{itemize}
```

### 有序列表

```{code-block} tex
\begin{enumerate} 
    \item First item 
    \item[-] Item with dash 
\end{enumerate}
```

## 表格

```{code-block} tex
\begin{table}[htpb!] 
    \begin{tabular}{lc @{ : } r|p{6em}}  % 用 @{} 自定义竖线样式
        \hline                           % 绘制横线
        left & center & right & par box with fixed width\\
        L & C & R & P \\
        \hline
    \end{tabular}
\end{table}
```

使用 [Table Generator](https://tablesgenerator.com) 你将可以更快速地制作表格 [^latex-cheatsheet]。

[^latex-cheatsheet]: [LaTeX_Cheat_Sheet_September_2020.pdf](https://cosimameyer.rbind.io/files/LaTeX_Cheat_Sheet_September_2020.pdf)

## 图片

```{code-block} tex
\begin{figure}[htpb!] 
    \centering 
    
    \includegraphics{figurename} 
        \caption{caption} 
        \label{fig:my_label} 
\end{figure}
```

- `\caption{caption}` 给图片起标题后将自动添加编号。
- `\label{fig:my_label}` 添加交叉引用，对表格（table）、节（Section）、脚注（footnote）也有效。

## 代码

### 行内代码

```{code-block} tex
\verb<delim><code><delim>
```

`<delim>` 可以是任意非字母字符，比如 `!`、`|`、`+` 等。

### 代码块

```{code-block} tex
\begin{verbatim}
    #include <iostream>
    int main()
    {
        std::cout << "Hello, world!"
        << std::endl;
        return 0;
    }
\end{verbatim}
```

## 盒子

### 基本盒子

```{code-block} tex
|\mbox{Test some words.}|\\
|\makebox[10em]{Test some words.}|\\
|\makebox[10em][l]{Test some words.}|\\
|\makebox[10em][r]{Test some words.}|\\
|\makebox[10em][s]{Test some words.}|
```

### 水平盒子

```{code-block} tex
三字经：\parbox[t]{3em}%
{人之初 性本善 性相近 习相远}
\quad
千字文：
\begin{minipage}[b][8ex][t]{4em}
    天地玄黄 宇宙洪荒
\end{minipage}
```

### 垂直盒子

```{code-block} tex
\fbox{\begin{minipage}{15em}%
    这是一个垂直盒子的测试。
    \footnote{脚注来自 minipage。}
\end{minipage}}
```

## 定义新命令

```{code-block} tex
\newcommand{\tnss}{The not so Short Introduction to \LaTeXe}
```

引用方式：`\tnss`。比如，也可以**重新定义**标题页样式，如下：

```{code-block} tex
\renewcommand{\maketitle}{\begin{titlepage}
    ... % 用户自定义命令
\end{titlepage}}
```

## 参考文献

$\LaTeX$ 默认使用了宏包 `natbib` 来帮助我们生成参考文献自动引用，但是还需要编写少量代码。

首先，引入已经写好的 `.bib` 和 `.sty` 文件，将以下内容添加到文章末尾。

```{code-block} tex
\bibliography{your_bibfile.bib} 
\bibliographystyle{your_citation_style}
```

[CTAN: BibTeX Style](https://ctan.org/topic/bibtex-sty) 提供了很多常见的参考文献样式，需要时可以借用。

然后，在正文中引用参考文献。natlib 提供了几种引用命令，语法和示例结果如下：

```{code-block} tex
\cite{key} or \citet{key}   % 作者名 (日期)
\citep{key}                 % (作者名, 日期)
\citealt{key}               % 作者名，日期
\citeauthor{key}            % 作者名
\citeyear{key}              % 日期
\cite[4]{key}               % 作者名, (日期, 页码)
```

当然，你也可以添加脚注 `\footnote{text}`
