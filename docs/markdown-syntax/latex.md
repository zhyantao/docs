# LaTeX

(latex-basic)=

## 基本介绍

学习使用 $\LaTeX$ 书写文档，应该做到如下两点：

- 本文将对常用的 $\LaTeX$ 语法做简单介绍，之后就可以学习[别人精心制作的模板](https://cn.overleaf.com/latex/templates)了；
- 本文不会记录常用的符号，反复多用几次就记住了，不常用的符号记不住[上网查一下](https://www.latexlive.com/help#d11)就行了。

如果已经熟练掌握基本语法，但是有些细节记不住，[查看小抄表](https://kdocs.cn/l/ceOwwHjUhGVQ)也许会有帮助。

## 环境配置

1. 下载并安装宏包：CTeX 由于长期不更新，推荐使用 [TeXLive](https://www.tug.org/texlive/)；
2. 下载并安装编辑器：[VS Code](https://code.visualstudio.com/)；
3. 适配中文：安装插件 LaTeX Workshop，按 `F1` 搜索 `setjson` 将下面内容添加到配置中 [^cite_ref-3]。

```{code-block} javascript
"latex-workshop.latex.tools": [
    {
        // 编译工具和命令
        "name": "xelatex",
        "command": "xelatex",
        "args": [
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            "%DOCFILE%"
        ]
    },
    {
        "name": "pdflatex",
        "command": "pdflatex",
        "args": [
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            "%DOCFILE%"
        ]
    },
    {
        "name": "bibtex",
        "command": "bibtex",
        "args": [
            "%DOCFILE%"
        ]
    }
],
"latex-workshop.latex.recipes": [
    {
        "name": "xelatex",
        "tools": [
            "xelatex"
        ],
    },
    {
        "name": "pdflatex",
        "tools": [
            "pdflatex"
        ]
    },
    {
        "name": "xe->bib->xe->xe",
        "tools": [
            "xelatex",
            "bibtex",
            "xelatex",
            "xelatex"
        ]
    },
    {
        "name": "pdf->bib->pdf->pdf",
        "tools": [
            "pdflatex",
            "bibtex",
            "pdflatex",
            "pdflatex"
        ]
    }
],
```

## Hello World

### 英文

```{code-block} tex
\documentclass{article}

\begin{document}
    ``Hello world!'' from \LaTeX
\end{document}
```

$\LaTeX$ 中没有双引号，因此用两个反引号和单引号输出了双引号 [^cite_ref-1]。

### 中文

```{code-block} tex
\documentclass{ctexart}

\begin{document}
    "你好，世界！" 来自 \LaTeX{} 的问候。
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

**一些重要的文件和它们的作用：** [^cite_ref-5]

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

使用 [Table Generator](https://tablesgenerator.com) 你将可以更快速地制作表格 [^cite_ref-2]。

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

$\LaTeX$ 默认使用了宏包 `natbib` 来帮助我们生成参考文献自动引用，但是还需要编写少量代码 [^cite_ref-4]。

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

---

````{admonition} 示例代码
:class: dropdown

```{code-block} tex
\documentclass[11pt, a4paper]{book}

\usepackage{ctex} % 用于支持中文
\usepackage{verbatim} % 长注释需要用到
\usepackage{graphicx} % 插入本地图片需要用到这个宏包
\usepackage{booktabs} % 给表格划线时需要用到
\usepackage[bookmarks=true,colorlinks,linkcolor=black]{hyperref} % 超链接（包含页面内部跳转和跳转到网站）,并生成PDF书签，便于阅读。在论文中删除,colorlinks,linkcolor=black更加正规。

\pagestyle{headings} % 设置页眉页脚

\title{LaTeX入门模板}
\author{Zh~Yantao} % 一个波浪线一个空格，两个波浪线两个空格。

\begin{document}

    \maketitle % 制作封面标题和作者
    \tableofcontents % 添加目录

    \part{第一部分~文章的整体框架}
    \chapter{第一章}
    \section{第一节}
    \subsection{第一小节}
    \paragraph{第一段}

    \LaTeX 的发音为“Lay-tech”，\LaTeXe 的发音是“Lay-tech-two-e”。

    一个空格 和    几个空格的效果是一样的。结果都是没有空格。

    如果要使用空格需要使用{} 来进行隔开。例如\TeX{} 和\TeX{}nicians。

    今天是 \today。在这里插入了一个标签\label{label:example}，这里的label标签并不在正文中显示，仅供下文引用使用。

    使用 \newline 开始新的一行。或者使用 \\ 开始新的一行。

    \paragraph{第二段~全部都是注释}

    \paragraph{长注释}
    \begin{comment}
        当我们包含进包verbatim后，就可以添加长注释了。当我们包含进包verbatim后，就可以添加长注释了。当我们包含进包verbatim后，就可以添加长注释了。当我们包含进包verbatim后，就可以添加长注释了。当我们包含进包verbatim后，就可以添加长注释了。
    \end{comment}

    到这里第一章结束了。

    \part{第二部分~使用特殊格式美化文章}
    \chapter{第二章}
    \section{第一节}
    \subsection{使用列表}
    \begin{enumerate}
        \item 用小圆点或者横线来分割条目
        \begin{itemize}
            \item 显示小圆点
            \item[-] 显示横线
        \end{itemize}

        \item 用描述文字来分割条目
        \begin{description}
            \item[显示章节] 上面插入的标签所在的章节~\ref{label:example}。
            \item[显示页码] 上面插入的标签所在的页码~\pageref{label:example}。
        \end{description}
    \end{enumerate}

    \subsection{添加批注}

    添加脚注\footnote{脚注脚注脚注脚注脚注脚注脚注脚注脚注脚注}。

    添加\underline{下划线}。

    添加\emph{强调}。

    使用不同于正文字体的\textsl{文字} 。

    \subsection{居左，居中，居右}
    \begin{flushleft}
        居左显示
    \end{flushleft}
    \begin{center}
        居中显示
    \end{center}
    \begin{flushright}
        居右显示
    \end{flushright}

    \subsection{添加引用}
    我是正文。我是正文。我是正文。我是正文。我是正文。我是正文。我是正文。我是正文。
    \begin{quote}
        我是引用。我是引用。我是引用。我是引用。我是引用。我是引用。我是引用。我是引用。
    \end{quote}
    我是正文。我是正文。我是正文。我是正文。

    \subsection{正常输出空格，而不是省略}
    \begin{verbatim}
        后面一个空格 后面三个空格   结束。
    \end{verbatim}
    \begin{verbatim*}
        verbatim后面加上星号，显示三个空格   。
    \end{verbatim*}

    \subsection{使用表格}
    \paragraph{基本表格}
    \begin{tabular}{|r|c|l|} % 第二个大括号是格式控制，竖线表示有竖边框，r,c,l分表表示居右居中居左
        \hline
        居右 & 居中 & 居左 \\
        \hline
        用hline画横线 & 用\&将文字换入下一列 & 用$\backslash\backslash$换行输出。 \\
        \hline
    \end{tabular}

    \paragraph{合并单元格}
    \begin{tabular}{|c|c|c|}
        \hline
        \multicolumn{1}{|c|}{占据第1列} & \multicolumn{2}{|c|}{占据2,3列} \\
        \hline
        第1列 & 第2列 & 第3列 \\
        \hline
        \multicolumn{2}{|c|}{占据1,2列} & \multicolumn{1}{|c|}{占据第3列} \\
        \hline
        第1列 & 第2列 & 第3列 \\
        \hline
    \end{tabular}

    \paragraph{小数点对齐}
    \begin{tabular}{c r @{.} l} % @{任意字符}表示用“任意字符”作为列分隔符
        Pi的表达式 & \multicolumn{2}{c}{计算结果} \\
        \hline
        $\pi$ & 3&1416 \\
        $\pi^{\pi}$ & 36&46 \\
        $(\pi^{\pi})^{\pi}$ & 80662&7 \\
    \end{tabular}

    \paragraph{特殊的表格}
    \begin{table}
        \caption{Example table}
        \centering
        \begin{tabular}{llr}
            \toprule %\usepackage{booktabs} % 给表格划线时需要用到
            \multicolumn{2}{c}{Name} \\
            \cmidrule(r){1-2}
            First Name & Last Name & Grade \\
            \midrule
            John & Doe & $7.5$ \\
            Richard & Miles & $5$ \\
            \bottomrule
        \end{tabular}
    \end{table}

    \subsection{插入图片}

    \paragraph{浮动显示}
    Figure~\ref{figure:example} 是一个插入的图片示例.
    \begin{figure}[!hbp]
        \makebox[\textwidth]{\framebox[5cm]{\rule{0pt}{5cm}}}
        \caption{5*5厘米的大小.} \label{figure:example}
    \end{figure}

    \paragraph{插入本地图片}
    \begin{figure}
        \includegraphics[width=\linewidth]{../_static/images/bear.jpg} % Figure image \usepackage{graphicx} % 插入本地图片需要用到这个宏包
        \caption{A majestic grizzly bear} % Figure caption
        \label{bear} % Label for referencing with \ref{bear}
    \end{figure}

    \subsection{引用参考文献}
    参考文献第一次编译无法正常显示，需要进行第二次编译 \cite{knuthwebsite}。

    \part{参考文献}
    \bibliographystyle{plain}
    \bibliography{sample.bib}
\end{document}
```
````

---

[^cite_ref-1]: [一份（不太）简短的 LATEX 2ε 介绍](https://kdocs.cn/l/cvhLkILXI6Ti)
[^cite_ref-2]: [LaTeX Cheat Sheet September 2020](https://kdocs.cn/l/ccMezohdXTt2)
[^cite_ref-3]: [使用 VS Code 编写 LaTeX](https://zhuanlan.zhihu.com/p/38178015)
[^cite_ref-4]: [自然科学引文和参考文献](https://kdocs.cn/l/cjIIyloNFX6U)
[^cite_ref-5]: [LaTeX 学习小结](https://rgb-24bit.github.io/blog/2020/latex-summary.html)
