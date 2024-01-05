# MyST-NB

(target_header)=

## 标题（Headers）

``````{list-table}
:header-rows: 1
:widths: 20 15

* - Syntax
  - Example
* - ```md
    # Heading level 1
    ## Heading level 2
    ### Heading level 3
    #### Heading level 4
    ##### Heading level 5
    ###### Heading level 6
    ```
  - ```md
    # MyST Cheat Sheet
    ```
``````

## 引用（Quote）

``````{list-table}
:header-rows: 1
:widths: 20 10

* - Example
  - Result
* - ```md
    > this is a quote
    ```
  - > 引用文本
``````

## 超链接（Links）

``````{list-table}
:header-rows: 1
:widths: 20 10

* - Example
  - Result
* - ```md
    [Jupyter Book](https://jupyterbook.org)
    ```
  - [Jupyter Book](https://jupyterbook.org)
* - ```md
    [restructuredtext](./restructuredtext)
    ```
  - [restructuredtext](./restructuredtext)
* - ```md
    <https://jupyterbook.org>
    ```
  - <https://jupyterbook.org>
``````

## 列表（Lists）

### 有序列表（Ordered list）

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    1. First item
    2. Second item
        1. First sub-item
    ```
  - 1. First item
    2. Second item
        1. First sub-item
* - ```md
    1. First item
    2. Second item
        * First sub-item
    ```
  - 1. First item
    2. Second item
        * First subitem
``````

### 无序列表（Unordered list）

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    * First item
    * Second item
      * First subitem
    ```
  - * First item
    * Second item
      * First subitem
* - ```md
    * First item
      1. First subitem
      2. Second subitem
    ```
  - * First item
      1. First subitem
      2. Second subitem
``````

## 表格（Tables）

```{note}
通过给表格添加标题，能够让表格**自动编号**，如下{numref}`example-table` 和 表 2。
```

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    |    Training   |   Validation   |
    | :------------ | -------------: |
    |        0      |        5       |
    |     13720     |      2744      |
    ```
  - |    Training   |   Validation   |
    | :------------ | -------------: |
    |        0      |        5       |
    |     13720     |      2744      |
* - ````md
    ```{list-table} My table title
    :header-rows: 1
    :name: example-table

    * - Training
      - Validation
    * - 0
      - 5
    * - 13720
      - 2744
    ```
    ````
  - ```{list-table} My table title
    :header-rows: 1
    :name: example-table

    * - Training
      - Validation
    * - 0
      - 5
    * - 13720
      - 2744
    ```
* - ````md
    ```{list-table} This table title
    :header-rows: 1

    * - Training
      - Validation
    * - 0
      - 5
    * - 13720
      - 2744
    ```
    ````
  - ```{list-table} This table title
    :header-rows: 1

    * - Training
      - Validation
    * - 0
      - 5
    * - 13720
      - 2744
    ```
``````

## 图片（Figures and images）

```{note}
图片（Image）中**不允许**出现标题（Caption），但图像（Figure）**可以**。
```

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ````md
    ```{figure} ../../_static/images/C-3PO_droid.png
    :height: 150px
    :name: figure-example

    Here is my figure caption!
    ```
    ````
  - ```{figure} ../../_static/images/C-3PO_droid.png
    :height: 150px
    :name: figure-example

    Here is my figure caption!
    ```
* - ````md
    ```{image} ../../_static/images/C-3PO_droid.png
    :height: 150px
    :name: image-example
    ```
    ````
  - ```{image} ../../_static/images/C-3PO_droid.png
    :height: 150px
    :name: image-example
    ```
``````

## 公式（Math）

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    This is an example of an
    inline equation $z=\sqrt{x^2+y^2}$.
    ```
  - This is an example of an
    inline equation $z=\sqrt{x^2+y^2}$.
* - ```md
    This is an example of a
    math block

    $$
    z=\sqrt{x^2+y^2}
    $$
    ```
  - This is an example of a
    math block

    $$
    z=\sqrt{x^2+y^2}
    $$
* - ```md
    This is an example of a
    math block with a label

    $$
    z=\sqrt{x^2+y^2}
    $$ (mylabel)
    ```
  - This is an example of a
    math block with a label

    $$
    z=\sqrt{x^2+y^2}
    $$ (mylabel)
* - ````md
    This is an example of a
    math directive with a
    label
    ```{math}
    :label: eq-label

    z=\sqrt{x^2+y^2}
    ```
    ````
  - This is an example of a
    math directive with a
    label
    ```{math}
    :label: eq-label

    z=\sqrt{x^2+y^2}
    ```
``````

## 代码（Code）

### 行内代码（In-line code）

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    In-line code blocks: `boolean example = true;`.
    ```
  - In-line code blocks: `boolean example = true;`.
``````

### 代码高亮（Syntax highlighting）

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ````md
    ```{code-block} python
    :emphasize-lines: 2

    note = "Python syntax highlighting"
    print(node)
    ```
    ````
  - ```{code-block} python
    :emphasize-lines: 2

    note = "Python syntax highlighting"
    print(node)
    ```
``````

### HTML 代码（HTML block）

``````{list-table}
:header-rows: 1
:widths: 15 15

* - Example
  - Result
* - ```html
    <p> This is a paragraph </p>
    ```
  - <p> This is a paragraph </p>
``````

## 注解（Admonitions）

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ````md
    ```{admonition} This is a title
    An example of an admonition with a title.
    ```
    ````
  - ```{admonition} This is a title
    An example of an admonition with a title.
    ```
* - ````md
    ```{note} Notes require **no** arguments,
    so content can start here.
    ```
    ````
  - ```{note} Notes require **no** arguments,
    so content can start here.
    ```
* - ````md
    ```{warning} This is an example
    of a warning directive.
    ```
    ````
  - ```{warning} This is an example
    of a warning directive.
    ```
* - ````md
    ```{tip} This is an example
    of a tip directive.
    ```
    ````
  - ```{tip} This is an example
    of a tip directive.
    ```
* - ````md
    ```{caution} This is an example
    of a caution directive.
    ```
    ````
  - ```{caution} This is an example
    of a caution directive.
    ```
* - ````md
    ```{attention} This is an example
    of an attention directive.
    ```
    ````
  - ```{attention} This is an example
    of an attention directive.
    ```
* - ````md
    ```{danger} This is an example
    of a danger directive.
    ```
    ````
  - ```{danger} This is an example
    of a danger directive.
    ```
* - ````md
    ```{error} This is an example
    of an error directive.
    ```
    ````
  - ```{error} This is an example
    of an error directive.
    ```
* - ````md
    ```{hint} This is an example
    of a hint directive.
    ```
    ````
  - ```{hint} This is an example
    of a hint directive.
    ```
* - ````md
    ```{important} This is an example
    of an important directive.
    ```
    ````
  - ```{important} This is an example
    of an important directive.
    ```
``````

## 脚注（Footnotes）

``````{list-table}
:header-rows: 1
:widths: 20 10

* - Example
  - Result
* - ```md
    添加引用：This is a footnote reference.[^myref]
    ```
  - 添加引用：This is a footnote reference.[^myref]
* - ```md
    添加注释：[^myref]: Example for footnote definition.
    ```
  - [^myref]: Example for footnote definition.
``````

## 注释（Comment）

``````{list-table}
:header-rows: 1
:widths: 15 15

* - Example
  - Result
* - ```md
    a line
    % a comment
    another line
    ```
  - a line
    % a comment
    another line
``````

## 分隔线（Thematic break）

``````{list-table}
:header-rows: 1
:widths: 15 15

* - Example
  - Note
* - ```md
    This is the end of some text.

    ---

    ## New Header
    ```
  - 创建水平分隔线
``````

## 分隔块（Block break）

``````{list-table}
:header-rows: 1
:widths: 15 15

* - Example
  - Result
* - ```md
    This is an example of
    +++ {"meta": "data"}
    a block break
    ```
  - This is an example of
    +++ {"meta": "data"}
    a block break
``````

## 面包板（Pannels）

``````{list-table}
:header-rows: 1
:widths: 15 15

* - Example
  - Result
* - ```md
    :::{card} Card Title
    Header
    ^^^
    Card content
    +++
    Footer
    :::
    ```
  - :::{card} Card Title
    Header
    ^^^
    Card content
    +++
    Footer
    :::
* - ```md
    :::{card} Clickable Card (external)
    :link: https://example.com

    The entire card can be clicked to navigate to <https://example.com>.
    :::
    ```
  - :::{card} Clickable Card (external)
    :link: https://example.com

    The entire card can be clicked to navigate to <https://example.com>.
    :::
``````

## 交叉引用（Cross reference）

### 引用标题（Headers）

``````{list-table}
:header-rows: 1
:widths: 20 15 15

* - Syntax
  - Example
  - Note
* - ```md
    {ref}`target_header`
    ```
  - {ref}`target_header`
  - ```md
    (target_header)=
    ## 标题（Headers）
    ```
* - ```md
    {ref}`自定义显示文本 <target_header>`
    ```
  - {ref}`自定义显示文本 <target_header>`
  - ```md
    (target_header)=
    ## 标题（Headers）
    ```
* - ```md
    [Markdown 风格的引用](target_header)
    ```
  - [Markdown 风格的引用](target_header)
  - ```md
    (target_header)=
    ## 标题（Headers）
    ```
``````

### 引用表格（Tables）

```{note}
为了引用表格，你需要给表格添加 `name` 属性。
```

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    {numref}`example-table` is an example.
    ```
  - {numref}`example-table` is an example.
* - ```md
    This {ref}`table <example-table>` is an example.
    ```
  - This {ref}`table <example-table>` is an example.
* - ```md
    {numref}`Tbl %s <example-table>` is an example.
    ```
  - {numref}`Tbl %s <example-table>` is an example.
``````

### 引用图像（Figures）

```{note}
使用 `numref` 引用图像（Figures）将带有标号，使用 `ref` 则不带标号。
```

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    {numref}`figure-example`is a
    figure example.
    ```
  - {numref}`figure-example` is a
    figure example.
* - ```md
    {numref}`Figure %s <figure-example>`
    is an example.
    ```
  - {numref}`Figure %s <figure-example>`
    is an example.
* - ```md
    This {ref}`figure <figure-example>`
    is an example.
    ```
  - This {ref}`figure <figure-example>`
    is an example.
``````

### 引用图片（Images）

```{note}
图片（Images）无法使用 `numref` 引用，默认都不带标号。
```

``````{list-table}
:header-rows: 1
:widths: 20 15

* - Example
  - Result
* - ```md
    This {ref}`image <image-example>`
    is an example.
    ```
  - This {ref}`image <image-example>`
    is an example.
``````

### 引用公式（Math directives）

``````{list-table}
:header-rows: 1
:widths: 20 15

* - Example
  - Result
* - ```md
    Check out equation {eq}`eq-label`.
    ```
  - Check out equation {eq}`eq-label`.
``````

### 引用文件（Documents）

``````{list-table}
:header-rows: 1
:widths: 15 20

* - Example
  - Result
* - ```md
    See {doc}`restructuredtext`
    for more information.
    ```
  - See {doc}`restructuredtext`
    for more information.
* - ```md
    See {doc}`here <restructuredtext>`
    for more information.
    ```
  - See {doc}`here <restructuredtext>`
    for more information.
``````

## 参考文献（Citations）

```{note}
确保你已经新建了 `references.bib` 文件，点击{download}`查看文件 <../../references.bib>`撰写格式。
```

``````{list-table}
:header-rows: 1
:widths: 20 20

* - Example
  - Result
* - ```md
    Generates a citation {cite}`perez2011python`.
    ```
  - Generates a citation {cite}`perez2011python`.
``````

你可以用下面的 `bibliography` 指令添加参考文献目录。

``````md
```{bibliography}
:filter: docname in docnames
```
``````
